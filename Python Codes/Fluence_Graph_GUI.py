import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import SPENVIS as SA
import tkinter as tk
from tkinter import filedialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#==========================================
# Title:  Fluence Graph GUI 
# Author: Justin Suys
# Date:   4/20/2024
#==========================================

def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1
def split_and_add(arr):
    # Check if the length of the array is even
    if len(arr) % 2 != 0:
        return "Error: Array length must be even."

    # Split the array into two halves
    mid = len(arr) // 2
    first_half = arr[:mid]
    second_half = arr[mid:]

    # Add the elements of each half
    sum_first_half = sum(first_half)
    sum_second_half = sum(second_half)

    return sum_first_half, sum_second_half

def reduce_fluence_array(obj):
    #Creates an array 2D arrays originating from the CSV
    
    #First index is which histogram to choose from the input file
    #Second index is which line
    #Third index is which value
    
    #for each TE fluence file there are 6 histograms(2 particles(electrons+gamma) * 3 volumes(Al+A150+Blood))
    #The order goes Al-Electron, Al-Gamma, A150-Electron, A150-Gamma, Blood-Electron, Blood-Gamma
    #for each TP fluence file there are 18 histograms(6 particles(electrons+gamma+muon+neutron+pion+proton) * 3 volumes(aluminium+A150+blood))
    #Likewise the order is Al-electron, Al-gamma, Al-muon, Al-neutron, Al-pion, Al-proton, A150-electron etc.
    counter = 0
    output=[]
    n = obj.number_of_bins
    intermediate=[]
    arr = obj.csv_to_array()
    
    for line in arr :
        if((not '*' in line) and all_numeric(line) and len(line)==6 ): #and not (line[2]==line[3])):#and (str(counter%n+1) in line)
            
            intermediate.append(line)
            counter = counter + 1
            
        if(counter == n):
            output.append(intermediate)
            intermediate=[]
            counter = 0
    #final.append(output)
    #print(len(output))
    return output
    
def all_numeric(arr):
    for element in arr:
        if isinstance(element, str):
            try:
                float(element)
            except ValueError:
                return False
        elif not isinstance(element, (int, float)):
            return False
    return True

def split_and_create(arr, n):

    first_part = arr[:n]
    second_part = arr[n:]
    return [first_part, second_part]

def get_fluence(obj,volume_name):
    arr = reduce_fluence_array(obj)
    
    if((volume_name == 'Al')or(volume_name == 'AL') or (volume_name == 'Aluminum') or (volume_name == 'Aluminium')):
        return arr[0]
    if(volume_name == 'A150'):
        return arr[1]
    if((volume_name == 'Blood')or(volume_name == 'Lymphocyte')or(volume_name == 'ICRP Blood')):
        return arr[2]
 
def get_area(obj,volume_name):
    if((volume_name == 'Al')or(volume_name == 'AL') or (volume_name == 'Aluminum') or (volume_name == 'Aluminium')):
       return SA.gdml_to_area(obj.gdml_path)[0]
    if(volume_name == 'A150'):
       return SA.gdml_to_area(obj.gdml_path)[1]
    if((volume_name == 'Blood')or(volume_name == 'Lymphocyte')or(volume_name == 'ICRP Blood')):
       return SA.gdml_to_area(obj.gdml_path)[2]
    
def plot_spenvis_data(folder_path, gdml_path, input_particle, output_particle, volume_name,ax=None):
    if ax is None:
        fig, ax = plt.subplots()
        ax.set_title(f'Fluence Spectrum for {output_particle}')
    mission_days = 186
    area = []
    fluence_spectrum = []
    x = []
    y = []
    error = []

    if input_particle == 'TP':
        if output_particle in ["Gamma", "Electron"]:
            x_tick = [0.1, 1, 10]
        else:
            x_tick = [0.01, 0.1, 1, 10, 100]
    else:
        x_tick = [0.01, 0.1, 0.5]

    file_list = os.listdir(folder_path)
    for file in file_list:
        if ".csv" in file and input_particle in file and output_particle in file:
            obj = SA.SpenvisAnalysis(os.path.join(folder_path, file), gdml_path)
            area_value = get_area(obj, volume_name)
            area.append(area_value)
            fluence_data = get_fluence(obj, volume_name)
            fluence_spectrum.append(fluence_data)

    for fluence in fluence_spectrum:
        x_temporary = [float(i[2]) for i in fluence if not i[3] == i[4]]
        y_temporary = [float(i[3]) / (mission_days * area[0]) for i in fluence if not i[3] == i[4]]
        error_temporary = [float(i[4]) / (mission_days * area[0]) for i in fluence if not i[3] == i[4]]
        x.extend(x_temporary)
        y.extend(y_temporary)
        error.extend(error_temporary)

    x = np.array(x)
    y = np.array(y)
    error = np.array(error)

    # Plotting
    
    ax.plot(x, y, label=f"SPENVIS - {output_particle}")
    ax.errorbar(x, y, yerr=error, capsize=2, fmt='none', ecolor="black")
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.set_xlabel('Energy [MeV]', fontsize="24")
    ax.set_ylabel(r'$\dot{\phi}$ [particles/AMeV·day·cm$^{2}$]', fontsize="24")
    
    ax.legend(fontsize="16")
    plt.grid(True, which="both", ls="-")
    
def plot_oltaris_data(oltaris_fluence_path,output_particle,ax=None):
    if ax is None:
        fig, ax = plt.subplots()
        ax.set_title(f'Fluence Spectrum for {output_particle}')
    results=[]
    oltaris_fluence=[]
    oltaris_energy=[]
    
    with open(oltaris_fluence_path, mode='r') as oltaris_file:
        csv_reader = csv.reader(oltaris_file)
            
        for row in csv_reader:
            results.append(row)
        if(output_particle == "Gamma"):
            index = index_containing_substring(results[0],"photon")
        else:
            index = index_containing_substring(results[0],output_particle.lower())
        for i in range(1,len(results[index])):
            oltaris_energy.append(float(results[i][0]))
            oltaris_fluence.append(float(results[i][index]))
            #print(oltaris_energy)
            #print(oltaris_fluence)
        line2, = ax.plot(oltaris_energy,oltaris_fluence)
        line2.set_label("OLTARIS - "+output_particle)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.tick_params(axis='both', which='major', labelsize=20)
        ax.set_xlabel('Energy [MeV]', fontsize="24")
        ax.set_ylabel(r'$\dot{\phi}$ [particles/AMeV·day·cm$^{2}$]', fontsize="24")
        
        ax.legend(fontsize="16")
    plt.grid(True, which="both", ls="-")    

def incident_fluence_graph(folder_path,gdml_path,oltaris_fluence_path,volume_name):   
    fig, ax = plt.subplots()
    #To generate separate subplots do not include ax, it will automatically make a plot
    plot_spenvis_data(folder_path, gdml_path, 'TP', 'Proton', volume_name,ax)
    plot_oltaris_data(oltaris_fluence_path,'Proton',ax)
    plot_spenvis_data(folder_path, gdml_path, 'TP', 'Neutron', volume_name,ax)
    plot_oltaris_data(oltaris_fluence_path,'Neutron',ax)
    plot_spenvis_data(folder_path, gdml_path, 'TP', 'Electron', volume_name,ax)
    plot_oltaris_data(oltaris_fluence_path,'Electron',ax)
    plot_spenvis_data(folder_path, gdml_path, 'TP', 'Gamma', volume_name,ax)
    plot_oltaris_data(oltaris_fluence_path,'Gamma',ax)

    fig.suptitle("SPENVIS and OLTARIS AP-8 flux spectrum comparison \n for a 6 month mission incident on " + volume_name, fontsize="30")
    plt.show()
def oltaris_incident_fluence_graph(oltaris_fluence_path,volume_name):   
    fig, ax = plt.subplots()
    #To generate separate subplots do not include ax, it will automatically make a plot
    
    plot_oltaris_data(oltaris_fluence_path,'Proton',ax)
    
    plot_oltaris_data(oltaris_fluence_path,'Neutron',ax)
    
    plot_oltaris_data(oltaris_fluence_path,'Electron',ax)
    
    plot_oltaris_data(oltaris_fluence_path,'Gamma',ax)

    fig.suptitle("OLTARIS AP-8 flux spectrum \n for a 6 month mission incident on " + volume_name, fontsize="30")
    plt.show()
def spenvis_incident_fluence_graph(folder_path,gdml_path,volume_name):
    fig, ax = plt.subplots()
    #To generate separate subplots do not include ax, it will automatically make a plot
    plot_spenvis_data(folder_path, gdml_path, 'TP', 'Proton', volume_name,ax)
    
    plot_spenvis_data(folder_path, gdml_path, 'TP', 'Neutron', volume_name,ax)
    
    plot_spenvis_data(folder_path, gdml_path, 'TP', 'Electron', volume_name,ax)
    
    plot_spenvis_data(folder_path, gdml_path, 'TP', 'Gamma', volume_name,ax)
    

    fig.suptitle("SPENVIS AP-8 flux spectrum \n for a 6 month mission incident on " + volume_name, fontsize="30")
    plt.show()
class ParticlePlotterApp:
    def __init__(self, root):
        
        self.root = root
        self.root.title("Fluence Rate Grapher")

        # Existing setup code for folder path, GDML path, etc.

        # Volume Name Dropdown
        ttk.Label(root, text="Volume Name:").grid(column=0, row=3)
        self.volume_name_var = tk.StringVar()
        self.volume_name_dropdown = ttk.Combobox(root, textvariable=self.volume_name_var, width=97)
        # Example volume names - replace with your actual data
        self.volume_name_dropdown['values'] = ('Aluminium', 'A150', 'Blood')
        self.volume_name_dropdown.grid(column=1, row=3)

        # Particle Type Dropdown
        ttk.Label(root, text="Particle Type:").grid(column=0, row=4)
        self.particle_type_var = tk.StringVar()
        self.particle_type_dropdown = ttk.Combobox(root, textvariable=self.particle_type_var, width=97)
        # Example particle types - replace with your actual data
        self.particle_type_dropdown['values'] = ('Proton', 'Neutron', 'Electron', 'Gamma','All','OLTARIS','SPENVIS')
        self.particle_type_dropdown.grid(column=1, row=4)

 

        # Placeholder for the matplotlib figure
     
        # Folder Path
        ttk.Label(root, text="Folder Path:").grid(column=0, row=0)
        self.folder_path_entry = ttk.Entry(root, width=140)
        self.folder_path_entry.grid(column=1, row=0)
        self.folder_path_button = ttk.Button(root, text="Browse...", command=self.browse_folder_path)
        self.folder_path_button.grid(column=2, row=0)

        # GDML Path
        ttk.Label(root, text="GDML Path:").grid(column=0, row=1)
        self.gdml_path_entry = ttk.Entry(root, width=140)
        self.gdml_path_entry.grid(column=1, row=1)
        self.gdml_path_button = ttk.Button(root, text="Browse...", command=self.browse_gdml_path)
        self.gdml_path_button.grid(column=2, row=1)

        # OLTARIS Fluence Path
        ttk.Label(root, text="OLTARIS Fluence Path:").grid(column=0, row=2)
        self.oltaris_path_entry = ttk.Entry(root, width=140)
        self.oltaris_path_entry.grid(column=1, row=2)
        self.oltaris_path_button = ttk.Button(root, text="Browse...", command=self.browse_oltaris_path)
        self.oltaris_path_button.grid(column=2, row=2)



        # Button to plot data
        self.plot_button = ttk.Button(root, text="Plot Data", command=self.plot_data)
        self.plot_button.grid(column=2, row=3)

        # Placeholder for the matplotlib figure
        self.figure = plt.Figure(figsize=(12, 8), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().grid(column=0, row=5, columnspan=3)

        self.save_button = ttk.Button(root, text="Save as PNG", command=self.save_plot_as_png)
        self.save_button.grid(column=2, row=4)
    def save_plot_as_png(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.figure.savefig(file_path)
    def browse_folder_path(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry.delete(0, tk.END)
        self.folder_path_entry.insert(0, folder_path)

    def browse_gdml_path(self):
        file_path = filedialog.askopenfilename()
        self.gdml_path_entry.delete(0, tk.END)
        self.gdml_path_entry.insert(0, file_path)

    def browse_oltaris_path(self):
        file_path = filedialog.askopenfilename()
        self.oltaris_path_entry.delete(0, tk.END)
        self.oltaris_path_entry.insert(0, file_path)
    def plot_data(self):
        # Clear the current plot
        self.ax.clear()
        self.ax.grid(True, which="both", ls="-")
        # Get the input values
        folder_path = self.folder_path_entry.get()
        gdml_path = self.gdml_path_entry.get()
        oltaris_path = self.oltaris_path_entry.get()
        volume_name = self.volume_name_var.get()
        particle_type = self.particle_type_var.get()

        # Your plotting logic here
        if(not(particle_type=='All')and not(particle_type=='OLTARIS')and not (particle_type=='SPENVIS')):

            plot_spenvis_data(folder_path, gdml_path, 'TP', particle_type, volume_name, ax=self.ax)
            plot_oltaris_data(oltaris_path, particle_type, ax=self.ax)
        elif(particle_type=='All'):
            
            plot_spenvis_data(folder_path, gdml_path, 'TP', 'Proton', volume_name, ax=self.ax)
            plot_oltaris_data(oltaris_path, 'Proton', ax=self.ax)
            plot_spenvis_data(folder_path, gdml_path, 'TP', 'Neutron', volume_name, ax=self.ax)
            plot_oltaris_data(oltaris_path, 'Neutron', ax=self.ax)
            plot_spenvis_data(folder_path, gdml_path, 'TP', 'Gamma', volume_name, ax=self.ax)
            plot_oltaris_data(oltaris_path, 'Gamma', ax=self.ax)
            plot_spenvis_data(folder_path, gdml_path, 'TP', 'Electron', volume_name, ax=self.ax)
            plot_oltaris_data(oltaris_path, 'Electron', ax=self.ax)
        elif(particle_type=='OLTARIS'):
           
            plot_oltaris_data(oltaris_path, 'Proton', ax=self.ax)
            plot_oltaris_data(oltaris_path, 'Neutron', ax=self.ax)
            plot_oltaris_data(oltaris_path, 'Gamma', ax=self.ax)
            plot_oltaris_data(oltaris_path, 'Electron', ax=self.ax)
        elif(particle_type=='SPENVIS'):
      
            plot_spenvis_data(folder_path, gdml_path, 'TP', 'Proton', volume_name, ax=self.ax)
            plot_spenvis_data(folder_path, gdml_path, 'TP', 'Neutron', volume_name, ax=self.ax)
            plot_spenvis_data(folder_path, gdml_path, 'TP', 'Gamma', volume_name, ax=self.ax)
            plot_spenvis_data(folder_path, gdml_path, 'TP', 'Electron', volume_name, ax=self.ax)
            
        # Draw the plot
        self.canvas.draw()
"""
    def plot_data(self):
        # Clear the current plot
        self.ax.clear()

        # Get the input values
        folder_path = self.folder_path_entry.get()
        gdml_path = self.gdml_path_entry.get()
        oltaris_path = self.oltaris_path_entry.get()
        volume_name = self.volume_name_entry.get()

        # Example plotting call - replace with actual function calls
        plot_spenvis_data(folder_path, gdml_path, 'TP', 'Proton', volume_name, ax=self.ax)
        plot_oltaris_data(oltaris_path, 'Proton', ax=self.ax)

        # Example plot to show functionality - remove this and use actual data
        #self.ax.plot([1, 2, 3], [4, 5, 6], label="Example Data")
        self.ax.legend()

        # Draw the plot
        self.canvas.draw()
"""


folder_path = "C:/Users/Justin/Desktop/SPENVIS_ANALYSIS_DATA/Box_phantom/Cupola_20.25_DEC-15-2015_JUN-18-2016/Fluence/"
gdml_path = "C:/Users/Justin/Desktop/SPENVIS_ANALYSIS_DATA/Box_phantom/Cupola_20.25_DEC-15-2015_JUN-18-2016/box_embedded_geometry_20.25.txt"
oltaris_fluence_path = 'C:/Users/Justin/Desktop/Aluminum_Fluence.csv'
volume_name = 'Aluminium'
"""
incident_fluence_graph(folder_path,gdml_path,oltaris_fluence_path,volume_name)
spenvis_incident_fluence_graph(folder_path,gdml_path,volume_name)
oltaris_incident_fluence_graph(oltaris_fluence_path,volume_name)
"""



if __name__ == "__main__":
    root = tk.Tk()
    app = ParticlePlotterApp(root)
    root.mainloop()