import autosklearn.regression
import pickle
import os
import re
import matplotlib.pyplot as plt
import csv
import numpy as np
from matplotlib.colors import ListedColormap

def get_model_from_file(name_of_file: str) -> autosklearn.regression.AutoSklearnRegressor:
    with open(name_of_file, "rb") as file:
        model = pickle.load(file)
    return model 

def get_all_pickle_file_paths(file_path: str):
    pickle_files = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith('.pickle'):
                pickle_files.append(os.path.join(root, file))
    return pickle_files

def transform_res_to_my_format(results):
    # TODO: transfrom to custom name
    dict = {}
    for weight, model in results:
        model_name = model.config['regressor:__choice__']
        
        if model_name in dict:
            dict[model_name] += weight
        else:
            dict[model_name] = weight

    return dict

def add_dicts_together(dict1, dict2):
    result = {}

    for key in set(dict1) & set(dict2):
        result[key] = dict1[key] + dict2[key]

    # Add keys and values from dict1 and dict2 that are unique to each dictionary
    for key in set(dict1) - set(dict2):
        result[key] = dict1[key]

    for key in set(dict2) - set(dict1):
        result[key] = dict2[key]

    return result

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

def get_groups_from_all_sorted_keys(sorted_keys):
    groups = []
    group = []
    for index in range(len(sorted_keys)):        
        
        group.append(sorted_keys[index])

        if index + 1 < len(sorted_keys) and get_custom_name(sorted_keys[index + 1]) is not get_custom_name(sorted_keys[index]):
            groups.append(group)
            group = []

    groups.append(group)
    return groups
  

def create_model_type_plot(path: str):
    pickle_paths = get_all_pickle_file_paths(path)
    dict = {}

    for pickle_path in pickle_paths:
        pickle_name = os.path.basename(pickle_path)
        key = re.sub(r'_seed_\d\.pickle$', '', pickle_name)
        
        model = get_model_from_file(pickle_path)
        res = transform_res_to_my_format(model.get_models_with_weights())

        if key in dict:
            dict[key] = add_dicts_together(dict[key], res)
        else:
            dict[key] = res

    for key in dict:
        for inner_key in dict[key]:
            dict[key][inner_key] /= 5

    sorted_keys = sorted(dict.keys(), key=custom_sort_key)
    for key in sorted_keys: 
        print("------------------")
        print(key)
        for inner_key in dict[key]:
            print(f"{inner_key}: {dict[key][inner_key]}")

    # dict: Key: long name -> (inner_dict: Key: ML-type -> weight)

    # group long names for graph 
    groups = get_groups_from_all_sorted_keys(sorted_keys)
    print(f"GROUPS: {groups}")
    count = 0
    for group in groups:

        distinct_model_types = set()

        # Iterate over the selected keys
        for key in group:
            # Get the inner dictionary for the current key
            inner_dict = dict.get(key, {})
            
            # Add the model types from the inner dictionary to the distinct_model_types set
            distinct_model_types.update(inner_dict.keys())

        distinct_model_types_list = list(distinct_model_types)
        distinct_labels = ["adaboost", "ard_regression", "decision_tree", "extra_trees", "gaussian_process", "gradient_boosting", "k_nearest_neighbors", "liblinear_svr", "libsvm_svr", "mlp", "random_forest", "sgd"]

        distinct_colors = [
            '#1f77b4',  # Blue
            '#ff7f0e',  # Orange
            '#2ca02c',  # Green
            '#d62728',  # Red
            '#9467bd',  # Purple
            '#8c564b',  # Brown
            '#e377c2',  # Pink
            '#7f7f7f',  # Gray
            '#bcbd22',  # Olive
            '#17becf',  # Cyan
            '#ff33cc',  # Pink
            '#33ff99',  # Light Green
        ]
        
        cmap = ListedColormap(distinct_colors)

        res = {key: np.zeros(len(group), dtype=float) for key in distinct_model_types_list}

        i = 0
        for key in group: 
            inner_dict = dict[key]
            for inner_key in inner_dict:
                res_list = res[inner_key]
                res_list[i] = inner_dict[inner_key]
            i+=1

        
        numbers = list(map(lambda x: (re.search(r"(?:-|_)(\d+)", x).group(1)), group))

        width = 0.5
        fig, ax = plt.subplots(figsize=(9.5, 4.8))
        #fig.set_size_inches(9.5, 4.8)
        bottom = np.zeros(len(group))

        for model_type, values in res.items():
            label_index = distinct_labels.index(model_type) 
            color = cmap(label_index)
            p = ax.bar(numbers, values, width, label=model_type, bottom=bottom, color=color)
            bottom += values

        ax.set_title(f"Aufteilung des Ensembles - {get_custom_name(group[0])} - 10% Unsicherheit")
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        plt.xlabel("Anzahl an Stichproben/Größe des Trainingsdatensatzes")
        plt.ylabel("Gewichtung der Modelltypen")
        plt.tight_layout()
        plt.savefig(f"{get_custom_name(group[0])}.png")
        plt.close()
        count += 1


#create_model_type_plot("sim_sampling_done/optimal")

    #create_model_type_plot("sim_sampling_done/classic")

#create_model_type_plot("sim_sampling_done/adaptive")
#create_model_type_plot("sim_sampling_done/optimal")
#create_model_type_plot("sim_sampling_done/space-filling/cvt")
#create_model_type_plot("sim_sampling_done/space-filling/lhs/center")
#create_model_type_plot("sim_sampling_done/space-filling/lhs/centermaximin")
#create_model_type_plot("sim_sampling_done/space-filling/lhs/maximin")
#create_model_type_plot("sim_sampling_done/space-filling/lhs/correlation")

create_model_type_plot("sim_sampling_noise_10/emukit_model_variance_noise_10")
create_model_type_plot("sim_sampling_noise_10/space-filling/cvt")
create_model_type_plot("sim_sampling_noise_10/space-filling/lhs/center")
create_model_type_plot("sim_sampling_noise_10/space-filling/lhs/centermaximin")
create_model_type_plot("sim_sampling_noise_10/space-filling/lhs/maximin")
create_model_type_plot("sim_sampling_noise_10/space-filling/lhs/correlation")

exit()

create_model_type_plot("sim_sampling_noise_2/emukit_model_variance_noise_2")
create_model_type_plot("sim_sampling_noise_2/space-filling/cvt")
create_model_type_plot("sim_sampling_noise_2/space-filling/lhs/center")
create_model_type_plot("sim_sampling_noise_2/space-filling/lhs/centermaximin")
create_model_type_plot("sim_sampling_noise_2/space-filling/lhs/maximin")
create_model_type_plot("sim_sampling_noise_2/space-filling/lhs/correlation")

create_model_type_plot("sim_sampling_noise_5/emukit_model_variance_noise_5")
create_model_type_plot("sim_sampling_noise_5/space-filling/cvt")
create_model_type_plot("sim_sampling_noise_5/space-filling/lhs/center")
create_model_type_plot("sim_sampling_noise_5/space-filling/lhs/centermaximin")
create_model_type_plot("sim_sampling_noise_5/space-filling/lhs/maximin")
create_model_type_plot("sim_sampling_noise_5/space-filling/lhs/correlation")

create_model_type_plot("sim_sampling_noise_10/emukit_model_variance_noise_10")
create_model_type_plot("sim_sampling_noise_10/space-filling/cvt")
create_model_type_plot("sim_sampling_noise_10/space-filling/lhs/center")
create_model_type_plot("sim_sampling_noise_10/space-filling/lhs/centermaximin")
create_model_type_plot("sim_sampling_noise_10/space-filling/lhs/maximin")
create_model_type_plot("sim_sampling_noise_10/space-filling/lhs/correlation")
