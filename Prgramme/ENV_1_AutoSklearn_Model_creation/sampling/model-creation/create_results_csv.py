import os
import re
import base
from auto_sklearn import get_model_from_file
from sklearn.metrics import r2_score, mean_squared_error
import csv

testdata = base.get_results_form_csv("lhs-center-10.000.csv")
X_test = testdata[0]
Y_test = testdata[1]

def get_all_pickle_file_paths(file_path: str):
    pickle_files = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith('.pickle'):
                pickle_files.append(os.path.join(root, file))
    return pickle_files

def custom_sort_key(key):
    alphabetic_part = ''
    numeric_part = '0'

    pattern = r'(.*?)[-_]([0-9]+)'
    match = re.search(pattern, key)
    if match:
        alphabetic_part = match.group(1)
        numeric_part = match.group(2)

    return (alphabetic_part, int(numeric_part))

def create_res_excel(file_path: str, name):
    pickle_paths = get_all_pickle_file_paths(file_path)

    dict = {}
    i = 0
    count = len(pickle_paths)

    for pickle_path in pickle_paths:

        print(f"left: {count - i}")
        automl = get_model_from_file(pickle_path)

        # r2 train
        csv_path = re.sub(r'_seed_\d\.pickle$', '.csv', pickle_path)
        X_train, Y_train = base.get_results_form_csv(csv_path)
        predict_train = automl.predict(X_train)
        train_r2 = r2_score(Y_train, predict_train)

        # r2 test
        predict_test = automl.predict(X_test)
        test_r2 = r2_score(Y_test, predict_test)

        # mse train
        mse_train = mean_squared_error(Y_train, predict_train)

        # mse test
        mse_test = mean_squared_error(Y_test, predict_test)

        pickle_name = os.path.basename(pickle_path)
        key = re.sub(r'_seed_\d\.pickle$', '', pickle_name)

        if key in dict:
            dict[key] = [a + b for a, b in zip(dict[key], [train_r2, test_r2, mse_train, mse_test])]
        else:
            dict[key] = [train_r2, test_r2, mse_train, mse_test]

        i += 1

    for key, value in dict.items():
        dict[key] = [x / 5 for x in value]

    sorted_keys = sorted(dict.keys(), key=custom_sort_key)

    with open(f'res_{name}_avg_lhs_10k.csv', mode='w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file, delimiter=';')  # Use comma as the delimiter
        
        # Write the header row with a single column header
        csv_writer.writerow(['name', 'R2 (Trainingsdaten)', 'R2 (Testdaten)', 'MSE (Trainingsdaten)', 'MSE (Testdaten)'])
        
        # Write the data rows with dictionary keys in the "Method" column and values in the rest of the row
        for key in sorted_keys:
            csv_writer.writerow([key] + dict[key])
    
    print(f"saved res_{name}_avg_lhs_10k.csv")

    



if __name__ == '__main__':
    print("entered")

    #create_res_excel("sim_sampling_done/space-filling", "space-filling")
    create_res_excel("sim_sampling_done/adaptive", "adaptive")
    create_res_excel("sim_sampling_done/optimal", "optimal")

    create_res_excel("sim_sampling_noise_2/emukit_model_variance_noise_2", "adaptive_2")
    create_res_excel("sim_sampling_noise_2/space-filling", "space-filling_2")

    create_res_excel("sim_sampling_noise_5/emukit_model_variance_noise_5", "adaptive_5")
    create_res_excel("sim_sampling_noise_5/space-filling", "space-filling_5")

    create_res_excel("sim_sampling_noise_10/emukit_model_variance_noise_10", "adaptive_10")
    create_res_excel("sim_sampling_noise_10/space-filling", "space-filling_10")