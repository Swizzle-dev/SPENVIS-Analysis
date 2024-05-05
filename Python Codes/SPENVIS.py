import numpy as np
import csv
import math
from matplotlib import pyplot as plt
import os
#==========================================
# Title:  SPENVIS Class
# Author: Justin Suys
# Date:   4/20/2024
#==========================================
class SpenvisAnalysis:
    def __init__(self, csv_path, gdml_path):
        self.csv_path = csv_path
        self.gdml_path = gdml_path
        self.csv_array = self.csv_to_array()
        self.filtered_array = self.filter_array()
        self.dose, self.dose_error = self.array_to_dose()
        self.module_name = self.gdml_to_module_name()
        self.particle_type, self.particle_number, self.cut_length, self.module_thickness, self.analysis_type = self.split_csv()
        self.number_of_bins = self.get_number_of_bins()

    def get_number_of_bins(self):
        for line in self.csv_array:
            if 'X_AXIS_NBINS' in line:
                return int(line[2])
        return None

    def csv_to_array(self):
        with open(self.csv_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            output_csv = [self.clean_row(row) for row in csv_reader]
        return output_csv

    @staticmethod
    def clean_row(row):
        return [element.replace("\"", "").replace("\'", "").replace(" ", "") for element in row]

    def filter_array(self):
        filtered_array = []
        required_table = False
        for row in self.csv_array:
            if 'DOSESPECTRUM' in row:
                required_table = True
            elif 'TOTALDOSE' in row:
                required_table = False
            elif required_table and len(row) == 6:
                filtered_array.append(row)
        return filtered_array

    def array_to_dose(self):
        dose = []
        dose_error = []
        for volume in range(3):
            volume_data = self.filtered_array[volume * 100:(volume + 1) * 100]
            volume_dose = sum(float(row[2]) * float(row[3]) for row in volume_data)
            volume_error = sum(float(row[2]) * float(row[4]) for row in volume_data)
            dose.append(volume_dose)
            dose_error.append(volume_error)
        return dose, dose_error

    def gdml_to_module_name(self):
        module_names = []
        with open(self.gdml_path, mode='r') as gdml_file:
            for line in gdml_file:
                if "materialref" in line and "Vacuum" not in line:
                    cleaned_line = line.replace("<materialref ref=\"", "").replace("\"/>\n", "")
                    module_names.append(cleaned_line)
        return module_names

    def print_dose(self):
        print("########################################################################")
        print(f"Particle type: {self.particle_type}")
        print(f"Number of Simulated Particles: {self.particle_number}")
        print(f"Cut length: {self.cut_length} µm\n")
        for volume, name in enumerate(self.module_name):
            print(f"Volume: {name}")
            print(f"Dose: {self.dose[volume]}±{self.dose_error[volume]} mSv\n")

    def split_csv(self):
        base_name = os.path.basename(self.csv_path).replace(".csv", "")
        parts = base_name.split("_")
        return parts[0], parts[1], parts[2], parts[3], parts[4]

# Utility functions
def convert_strings_to_floats(input_array):
    return [float(element) for element in input_array]

def m_to_cm(x):
    return 100 * x

def mm_to_cm(x):
    return x / 10

def get_area_cylinder(R, h):
    return 2 * math.pi * (m_to_cm(R))**2 + 2 * math.pi * m_to_cm(R) * m_to_cm(h)

def get_area_box(x, y, z):
    return 2 * (m_to_cm(x) * m_to_cm(y) + m_to_cm(x) * m_to_cm(z) + m_to_cm(y) * m_to_cm(z))

def convert_to_scientific_notation(array):
    return [format(num, '.0e') for num in array]

def next_n_characters_after_substring(string, substring, n):
    index = string.find(substring)
    if index != -1:
        return string[index + len(substring):index + len(substring) + n]
    else:
        return "Substring not found"

def get_thickness(path):
    flag1 = flag2 = False
    max_radius = min_radius = 0
    with open(path, mode='r') as file:
        for line in file:
            if 'tube name="s01_out"' in line:
                max_radius = mm_to_cm(float(next_n_characters_after_substring(line, "rmax=\"", 9).replace('E', 'e')))
                flag1 = True
            elif 'tube name="s01_in"' in line:
                min_radius = mm_to_cm(float(next_n_characters_after_substring(line, "rmax=\"", 9).replace('E', 'e')))
                flag2 = True
            if flag1 and flag2:
                return (max_radius - min_radius) * 2.7  # Assuming density for calculation

def gdml_to_area(path):
    area = []
    with open(path, mode='r') as file:
        for line in file:
            if "World" not in line:
                if "box name" in line:
                    if "_out" in line:
                        x_max, y_max, z_max = [mm_to_cm(float(next_n_characters_after_substring(line, dim, 9).replace('E', 'e'))) for dim in ["x=\"", "y=\"", "z=\""]]
                    elif "_in" in line:
                        x_min, y_min, z_min = [mm_to_cm(float(next_n_characters_after_substring(line, dim, 9).replace('E', 'e'))) for dim in ["x=\"", "y=\"", "z=\""]]
                        area.append(2 * (x_max * y_max + y_max * z_max + x_max * z_max))
                    else:
                        x, y, z = [mm_to_cm(float(next_n_characters_after_substring(line, dim, 9).replace('E', 'e'))) for dim in ["x=\"", "y=\"", "z=\""]]
                        area.append(2 * x * y + 2 * x * z + 2 * y * z)
                elif "tube name" in line:
                    if "_out" in line:
                        z_max = mm_to_cm(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E', 'e')))
                        r_max = mm_to_cm(float(next_n_characters_after_substring(line, "rmax=\"", 9).replace('E', 'e')))
                    elif "_in" in line:
                        z_min = mm_to_cm(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E', 'e')))
                        r_min = mm_to_cm(float(next_n_characters_after_substring(line, "rmax=\"", 9).replace('E', 'e')))
                        area.append(2 * math.pi * r_max * (z_max + r_max))
                    else:
                        z = mm_to_cm(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E', 'e')))
                        r = mm_to_cm(float(next_n_characters_after_substring(line, "rmax=\"", 9).replace('E', 'e')))
                        area.append(2 * math.pi * r * (z + r))
    return area