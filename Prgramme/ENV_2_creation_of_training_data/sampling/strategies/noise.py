import numpy as np
import locale
import os
import pandas as pd

locale.setlocale(locale.LC_ALL, "de_DE.utf8")

def create_file_with_range_noise(fileName: str, percantage: int):

    new_dis_lengths = []

    with open(f"27.07-data\\{fileName}", "r") as file:
        lines = file.readlines()
        valueRange = 347.53 - 0.745
        noise_dis = valueRange * np.random.random() * float(percantage/100)

        for i in range(1, len(lines)):
            row = lines[i]
            dis_length = float(row.split(";")[-1].strip().replace(",", "."))
   
            direction=np.random.randint(0,2)
            if (direction == 0):
                new_dis_lengths.append(dis_length + noise_dis)
            else:
                new_dis_lengths.append(dis_length - noise_dis)
        
    with open(f'{fileName.split(".")[0]}-total-{percantage}%.csv', "x") as writeFile:
        with open(f"27.07-data\\{fileName}", "r") as file:
            lines = file.readlines()

            for i in range(0, len(lines)):
                if (i == 0):
                    writeFile.write(lines[i].strip() + f';res_with_ragne_noise_{percantage}\n')
                else:
                    writeFile.write(lines[i].strip() + f';{locale.format("%.4f", new_dis_lengths[i-1])}\n')

from os import listdir
from os.path import isfile, join




def add_noise(value, percantage: int):
    value = float(value.replace(',', '.'))
    valueRange = 347.53 - 0.745
    noise_dis = valueRange * np.random.random() * float(percantage/100)

    direction=np.random.randint(0,2)
    if (direction == 0):
        return str(value + noise_dis).replace('.', ',')
    else:
        return str(value - noise_dis).replace('.', ',')

def add_noise_to_all_subdirectories(noise_percentage: int):
    root_dir = f'sim_sampling_noise_{noise_percentage}'
    subdirectories = ['space-filling\\cvt', 'space-filling\\lhs\\center', 'space-filling\\lhs\\centermaximin', 
                      'space-filling\\lhs\\correlation', 'space-filling\\lhs\\maximin']

    for subdir in subdirectories:
        sub_dir_path = os.path.join(root_dir, subdir)
        
        # Loop through CSV files in the subdirectory
        for filename in os.listdir(sub_dir_path):
            if filename.endswith('.csv'):  # Check if the file is a CSV file
                file_path = os.path.join(sub_dir_path, filename)
                
                # Load the CSV file into a DataFrame
                df = pd.read_csv(file_path, sep=';')
                
                if f'dis_with_noise_{noise_percentage}' not in df.columns:  

                    print(filename)                  
                    # Apply your noise function to the last column and create a new column
                    df[f'dis_with_noise_{noise_percentage}'] = df.iloc[:, -1].apply(lambda x: add_noise(x, noise_percentage))
                    
                    # Save the modified DataFrame back to the CSV file
                    df.to_csv(file_path, sep=';', index=False)


add_noise_to_all_subdirectories(2)


















def add_noise_to_all_files(percantage: int):
    files = [f for f in listdir("27.07-data")]
    
    for file in files:
        if("noise" in file):
            continue
        create_file_with_range_noise(file, percantage)










def add_normal_distr_noise_to_all_files(percentage: int, name_of_dir: str):
    files = [f for f in listdir(name_of_dir)]
    
    for file in files:
        if("noise" in file):
            continue
        create_file_with_range_noise(f"{name_of_dir}\\{file}", percentage)


# too small deviation


def create_file_with_normal_distr_noise(file_path: str, percentage: int):
    new_dis_lengths = []

    with open(f"{file_path}", "r") as file:
        lines = file.readlines()
        
        valueRange = 347.53 - 0.745
        std_dev = percentage * valueRange

        for i in range(1, len(lines)):
            row = lines[i]
            dis_length = float(row.split(";")[-1].strip().replace(",", "."))
            res_with_noise = np.random.normal(dis_length, std_dev)
            new_dis_lengths.append(res_with_noise)

    file_name = file_path.split("\\")[1]        
    
    with open(f'{file_name.split(".")[0]}-total-{percentage}%.csv', "x") as writeFile:
        with open(f"{file_path}", "r") as file:
            lines = file.readlines()

            for i in range(0, len(lines)):
                if (i == 0):
                    writeFile.write(lines[i].strip() + f';res_with_ragne_noise_{percentage}\n')
                else:
                    writeFile.write(lines[i].strip() + f';{locale.format("%.4f", new_dis_lengths[i-1])}\n')


