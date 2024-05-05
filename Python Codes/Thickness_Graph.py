import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import SPENVIS as SA
#==========================================
# Title:  Thickness Graph 
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
    volume_shifts = {"Blood": 1, "A150": 2}
    return volume_shifts.get(volume_name, 0)
def sum_pairs(arr):
    if len(arr) % 2 != 0:  # Check if the array length is odd
        arr = arr[:-1]  # Ignore the last element
    reshaped_arr = arr.reshape(-1, 2)  # Reshape the array into two columns
    pair_sums = reshaped_arr.sum(axis=1)  # Sum along the rows
    return pair_sums
def load_spenvis_data(al_thickness, shift):
    """Loads SPENVIS data for given aluminum thicknesses and shift."""
    spenvis_doses = []
    spenvis_errors = []
    base_folder = r"C:\Users\Justin\Desktop\SPENVIS_ANALYSIS_DATA\Box_phantom"

    for thickness in al_thickness:
        if(int(thickness)==thickness):
            folder_name = f"Cupola_{str(int(thickness))}_DEC-15-2015_JUN-18-2016"
            data_folder = os.path.join(base_folder, folder_name, "Data")
            gdml_file = f"box_embedded_geometry_{str(int(thickness))}.txt"
            gdml_path = os.path.join(base_folder, folder_name, gdml_file)
        else:
            folder_name = f"Cupola_{str(thickness)}_DEC-15-2015_JUN-18-2016"
            data_folder = os.path.join(base_folder, folder_name, "Data")
            gdml_file = f"box_embedded_geometry_{str(thickness)}.txt"
            gdml_path = os.path.join(base_folder, folder_name, gdml_file)

        print(SA.get_thickness(gdml_path))

        for file in os.listdir(data_folder):
            if file.endswith(".csv"):
                file_path = os.path.join(data_folder, file)
                obj = SA.SpenvisAnalysis(file_path, gdml_path)
                dose_index = len(obj.dose) - shift
                spenvis_doses.append(obj.dose[dose_index])
                spenvis_errors.append(obj.dose_error[dose_index])
                print(f"{file} : {obj.dose} mSv")

    return spenvis_doses, spenvis_errors

def plot_results(al_thickness, total_doserates, total_errorrates, oltaris_doserates, volume_name):
    """Plots the results of the analysis."""
    fig, ax1 = plt.subplots(figsize=(10, 8))
    ax1.set_xlabel('ISS Module Aluminium Thickness [g/cm$^2$]', fontsize=14)
    ax1.set_ylabel('Radiation Dose Rate [mSv/day]', fontsize=14)

    ax1.scatter(al_thickness, total_doserates, c='#0000FF', label='SPENVIS Dose Rate')
    ax1.errorbar(al_thickness, total_doserates, yerr=total_errorrates, capsize=3, fmt='none', ecolor="black")
    ax1.scatter(al_thickness, oltaris_doserates, c='#000000', label='OLTARIS Dose Rate')

    # Fit and plot exponential functions
    popt_spenvis, _ = curve_fit(exponential_func, al_thickness, total_doserates)
    popt_oltaris, _ = curve_fit(exponential_func, al_thickness, oltaris_doserates)
    ax1.plot(al_thickness, exponential_func(al_thickness, *popt_spenvis), 'r-', label='SPENVIS Exponential Fit')
    ax1.plot(al_thickness, exponential_func(al_thickness, *popt_oltaris), 'g-', label='OLTARIS Exponential Fit')

    ax1.legend()
    plt.title(f"Radiation Dose Rate Comparison: {volume_name}", fontsize=16)
    plt.show()

def main():
    al_thickness = np.array([0.51, 5, 10, 20.25, 30, 40, 50])
    mission_days = 186
    volume_name = "Blood"
    if(volume_name == "A150"):
        oltaris_doses = np.array([64.76,45.12,34.17,20.3,13.37,9.41,6.87]) # 1 cm of  A150, dose to A150
    if(volume_name == "Blood"):
        oltaris_doses = np.array([14.85, 12.06, 9.81, 6.64, 4.71, 3.46, 2.57]) # 1cm of A150 + 19cm of blood, dose to blood
    shift = get_shift(volume_name)

    spenvis_doses, spenvis_errors = load_spenvis_data(al_thickness, shift)
    total_doses = sum_pairs(np.array(spenvis_doses))
    total_errors = euclidean_norm(np.array(spenvis_errors))
    total_doserates = total_doses / mission_days
    total_errorrates = total_errors / mission_days
    oltaris_doserates = oltaris_doses / mission_days

    plot_results(al_thickness, total_doserates, total_errorrates, oltaris_doserates, volume_name)
if __name__ == "__main__":
    main()
