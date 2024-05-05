import tkinter as tk
from tkinter import ttk, filedialog
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import SPENVIS as SA
#==========================================
# Title:  Thickness Graph GUI 
# Author: Justin Suys
# Date:   4/20/2024
#==========================================
def exponential_func(x, a, b, c):
    """Exponential function used for curve fitting."""
    return a * np.exp(-b * x) + c
def euclidean_norm(arr):
    if len(arr) % 2 != 0:  # Check if the array length is odd
        arr = arr[:-1]  # Ignore the last element if the count is odd
    reshaped_arr = arr.reshape(-1, 2)  # Reshape the array into two columns
    # Calculate the square root of the sum of squares of each pair
    euc_norm = np.sqrt(np.sum(np.square(reshaped_arr), axis=1))
    return euc_norm
def get_shift(volume_name):
    """Determines the shift based on the volume name."""
    volume_shifts = {"Blood": 1, "A150": 2, "Aluminium": 3}
    return volume_shifts.get(volume_name, 0)
def sum_pairs(arr):
    if len(arr) % 2 != 0:  # Check if the array length is odd
        arr = arr[:-1]  # Ignore the last element
    reshaped_arr = arr.reshape(-1, 2)  # Reshape the array into two columns
    pair_sums = reshaped_arr.sum(axis=1)  # Sum along the rows
    return pair_sums
class ParticlePlotterApp:
    def __init__(self, root):
        self.root = root
        self.base_folder = ""
        self.volume_type = tk.StringVar(value="Aluminium")
        self.setup_gui()

    def setup_gui(self):
        self.folder_button = ttk.Button(self.root, text="Browse...", command=self.choose_base_folder)
        self.folder_button.grid(column=2, row=0, pady=10)
        self.plot_button = ttk.Button(self.root, text="Plot Graph", command=self.plot_graph)
        self.plot_button.grid(column=2, row=1, pady=10)
        self.save_button = ttk.Button(self.root, text="Save Graph", command=self.save_graph)
        self.save_button.grid(column=2, row=2, pady=10)   
        ttk.Label(root, text="Base Folder Path:").grid(column=0, row=0)
        self.folder_path_entry = ttk.Entry(root, width=100)
        self.folder_path_entry.grid(column=1, row=0)

        ttk.Label(root, text="Number of Mission Days").grid(column=0, row=1)
        self.number_of_days = ttk.Entry(root, width=10)
        self.number_of_days.grid(column=1, row=1)
        
        ttk.Label(root, text="Volume Name : ").grid(column=0, row=2)

     
        volume_options = ["Aluminium", "A150", "Blood"]
        self.volume_dropdown = ttk.Combobox(self.root, textvariable=self.volume_type, values=volume_options)
        self.volume_dropdown.grid(row=2, column=1, pady=10)

        self.figure = plt.Figure(figsize=(12, 8), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=3,padx=10, pady=10)
    def save_graph(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.figure.savefig(file_path)
    def plot_graph(self):
        if self.base_folder:
            print(f"Selected Base Folder: {self.base_folder}")
            al_thickness = np.array([0.51, 5, 10, 20.25, 30, 40, 50])
            mission_days = int(self.number_of_days.get())#186
            volume_name = self.volume_type.get()
            print(volume_name)
            if(volume_name == "Aluminium"):
                oltaris_doses = np.array([0,0,0,0,0,0,0]) # 1 cm of  A150, dose to A150
            if(volume_name == "A150"):
                oltaris_doses = np.array([64.76,45.12,34.17,20.3,13.37,9.41,6.87]) # 1 cm of  A150, dose to A150
            if(volume_name == "Blood"):
                oltaris_doses = np.array([14.85, 12.06, 9.81, 6.64, 4.71, 3.46, 2.57]) # 1cm of A150 + 19cm of blood, dose to blood
            shift = get_shift(volume_name)
            self.load_spenvis_data(al_thickness, shift)
            
            total_doses = sum_pairs(np.array(self.spenvis_doses))
            total_errors = euclidean_norm(np.array(self.spenvis_errors))
            total_doserates = total_doses / mission_days
            total_errorrates = total_errors / mission_days
            oltaris_doserates = oltaris_doses / mission_days
            self.plot_results(al_thickness, total_doserates, total_errorrates, oltaris_doserates, volume_name)
    def choose_base_folder(self):
        self.base_folder = filedialog.askdirectory()
        self.folder_path_entry.delete(0, tk.END)
        self.folder_path_entry.insert(0, self.base_folder)
        

    def load_spenvis_data(self,al_thickness, shift):
        # Update the function to use self.base_folder for loading data
        print("Loading SPENVIS data from base folder:", self.base_folder)
        """Loads SPENVIS data for given aluminum thicknesses and shift."""
        self.spenvis_doses = []
        self.spenvis_errors = []
    

        for thickness in al_thickness:
            if(int(thickness)==thickness):
                folder_name = f"Cupola_{str(int(thickness))}_DEC-15-2015_JUN-18-2016"
                data_folder = os.path.join(self.base_folder, folder_name, "Data")
                gdml_file = f"box_embedded_geometry_{str(int(thickness))}.txt"
                gdml_path = os.path.join(self.base_folder, folder_name, gdml_file)
            else:
                folder_name = f"Cupola_{str(thickness)}_DEC-15-2015_JUN-18-2016"
                data_folder = os.path.join(self.base_folder, folder_name, "Data")
                gdml_file = f"box_embedded_geometry_{str(thickness)}.txt"
                gdml_path = os.path.join(self.base_folder, folder_name, gdml_file)

            print(SA.get_thickness(gdml_path))

            for file in os.listdir(data_folder):
                if file.endswith(".csv"):
                    file_path = os.path.join(data_folder, file)
                    obj = SA.SpenvisAnalysis(file_path, gdml_path)
                    dose_index = len(obj.dose) - shift
                    self.spenvis_doses.append(obj.dose[dose_index])
                    self.spenvis_errors.append(obj.dose_error[dose_index])
                    print(f"{file} : {obj.dose} mSv")

        

    def plot_results(self,al_thickness, total_doserates, total_errorrates, oltaris_doserates, volume_name):
        # Example plot for demonstration
        self.ax.clear()
        self.ax.grid(True, which="both", ls="-")
        self.ax.set_xlabel('ISS Module Aluminium Thickness [g/cm$^2$]', fontsize=14)
        self.ax.set_ylabel('Radiation Dose Rate [mSv/day]', fontsize=14)

        self.ax.scatter(al_thickness, total_doserates, c='#0000FF', label='SPENVIS Dose Rate')
        self.ax.errorbar(al_thickness, total_doserates, yerr=total_errorrates, capsize=3, fmt='none', ecolor="black")
        self.ax.scatter(al_thickness, oltaris_doserates, c='#000000', label='OLTARIS Dose Rate')

    # Fit and plot exponential functions
        popt_spenvis, _ = curve_fit(exponential_func, al_thickness, total_doserates)
        popt_oltaris, _ = curve_fit(exponential_func, al_thickness, oltaris_doserates)
        self.ax.plot(al_thickness, exponential_func(al_thickness, *popt_spenvis), 'r-', label='SPENVIS Exponential Fit')
        self.ax.plot(al_thickness, exponential_func(al_thickness, *popt_oltaris), 'g-', label='OLTARIS Exponential Fit')

        self.ax.legend()
        #ax1.title(f"Radiation Dose Rate Comparison: {volume_name}", fontsize=16)
        #canvas = FigureCanvasTkAgg(self.figure, master=self.canvas)
        self.canvas.draw()
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Doserate Grapher")
    app = ParticlePlotterApp(root)
    root.mainloop()