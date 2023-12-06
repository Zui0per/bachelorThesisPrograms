from auto_sklearn import get_model_from_file
from sklearn.metrics import r2_score
from auto_sklearn import get_model_from_file
import os
import re
import base
import pickle
import matplotlib.pyplot as plt
import numpy as np

testdata = base.get_results_form_csv("lhs-center-10.000.csv")
X_test = testdata[0]
Y_test = testdata[1]

def get_dict_from_file(name_of_file: str) -> dict:
    with open(name_of_file, "rb") as file:
        dict = pickle.load(file)
    return dict 


def get_all_pickle_file_paths(file_path: str):
    pickle_files = []
    for root, dirs, files in os.walk(file_path):
        print(dirs)
        if "classic" in dirs:
            dirs.remove("classic")
        for file in files:
            if file.endswith('.pickle'):
                pickle_files.append(os.path.join(root, file))
    return pickle_files


def create_json_files_for_files(file_path, noise):
    pickle_paths = get_all_pickle_file_paths(file_path)
    print(pickle_paths)
    res = {}
    i = 0
    for pickle_path in pickle_paths:
        automl = get_model_from_file(pickle_path)

        pickle_name = os.path.basename(pickle_path)
        name_without_seed_count = re.sub(r'_seed_\d\.pickle$', '', pickle_name)

        if name_without_seed_count not in res:
            res[name_without_seed_count] = []


        predict_test = automl.predict(X_test)
        test_r2 = r2_score(Y_test, predict_test)
        res[name_without_seed_count].append(test_r2)
        i += 1
        print(f"{i}/{len(pickle_paths)}")
    

    pickle.dump(res, open(f'variance_dict_noise_{noise}.pickle', 'wb'))
    

def custom_sort_key(key):
    alphabetic_part = ''
    numeric_part = '0'

    pattern = r'(.*?)[-_]([0-9]+)'
    match = re.search(pattern, key)
    if match:
        alphabetic_part = match.group(1)
        numeric_part = match.group(2)

    return (alphabetic_part, int(numeric_part))

def get_custom_name(name: str):
    if ("10emukit-with-model-variance" in name):
        return "Emukit Model-Varianz 10%"
    if ("10lhs-center" in name):
        return "LHS-center 10%"
    if ("10lhs-maximin" in name):
        return "LHS-maximin 10%"
    if ("5emukit-with-model-variance" in name):
        return "Emukit Model-Varianz 5%"
    if ("5lhs-center" in name):
        return "LHS-center 5%"
    if ("5lhs-maximin" in name):
        return "LHS-maximin 5%"
    if ("2emukit-with-model-variance" in name):
        return "Emukit Model-Varianz 2%"
    if ("2lhs-center" in name):
        return "LHS-center 2%"
    if ("2lhs-maximin" in name):
        return "LHS-maximin 2%"
    if ("emukit-with-model-variance" in name or "emukit-Model-Varianz" in name):
        return "Emukit Model-Varianz"
    if ("emukit_with_ivr" in name or "emukit-IVR" in name):
        return "Emukit IVR"
    if ("2-level-full" in name or "two-level-full-factorial" in name):
        return "2-Stufen FFD"
    if ("box-behnken" in name):
        return "Box-Behnken Design"
    if ("central-composite_c" in name):
        return "CCD-C"
    if ("central-composite_f" in name):
        return "CCD-F"
    if ("central-composite_i" in name):
        return "CCD-I"
    if ("placket-burman" in name):
        return "Plackett Burman Design"
    if ("CVT" in name):
        return "CVT"
    if ("lhs-centermaximin" in name):
        return "LHS-centermaximin"
    if ("lhs-center" in name):
        return "LHS-center"
    if ("lhs-correlation" in name):
        return "LHS-correlation"
    if ("lhs-maximin" in name):
        return "LHS-maximin"
    
    return name

def get_groups_from_all_sorted_keys(sorted_keys, exclude):
    groups = []
    group = []
    for index in range(len(sorted_keys)):        
        
        if(get_custom_name(sorted_keys[index]) in exclude):
            continue

        group.append(sorted_keys[index])
        if index + 1 < len(sorted_keys) and get_custom_name(sorted_keys[index + 1]) is not get_custom_name(sorted_keys[index]):
            groups.append(group)
            group = []

    if len(group) != 0:
        groups.append(group)
    return groups

def create_var_plots(pickle_file):
    dict = get_dict_from_file(pickle_file)

    sorted_keys = sorted(dict.keys(), key=custom_sort_key)
    groups = get_groups_from_all_sorted_keys(sorted_keys, exclude=['Box-Behnken Design', 'CCD-C', 'CCD-F', 'CCD-I', 'Emukit IVR', '2-Stufen FFD'])
    numbers = list(map(lambda x: (re.search(r"(?:-|_)(\d+)", x).group(1)), groups[0]))
    names = [get_custom_name(group[0]) for group in groups]

    res = {key: np.zeros(len(numbers), dtype=float) for key in names}

    for group in groups:
        cur_name = get_custom_name(group[0])

        i = 0
        for key in group:
            print(key)
            res[cur_name][i] = np.std(dict[key])
            i += 1
            #res[cur_name] = max(dict[key]) - min(dict[key])

    print("---------")
    for key, val in res.items():
        print(f"{key}: {val}")

    x = np.arange(len(numbers))  # the label locations
    width = 0.12  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(figsize=(12, 4.8))

    for name, variances in res.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, variances, width, label=name)
        #ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title('R2 Standardabweichung für Modelle mit adaptiven und space-filling Trainingsdatensätzen')
    ax.set_xticks(x + 2*width, numbers)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 0.27)

    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.xlabel("Anzahl an Stichproben/Größe des Trainingsdatensatzes")
    plt.ylabel("R2 Standardabweichung")
    plt.tight_layout()
    
    plt.savefig("std_with_cor.png")

    
#create_var_plots("variance_dict.pickle")

dict = get_dict_from_file("variance_dict_noise_10.pickle")

for key, val in dict.items():
    if ("emukit" in key):
        print(f"{key}: {val}")
