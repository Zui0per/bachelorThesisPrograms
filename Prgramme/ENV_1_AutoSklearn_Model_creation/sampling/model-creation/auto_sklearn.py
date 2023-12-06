import base
from typing import List
import autosklearn.regression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
import pickle
import os

#testdata = base.get_results_form_csv("adjusted_testdata_2500.csv")
#X_test = testdata[0]
#Y_test = testdata[1]

def save_model(model: autosklearn.regression.AutoSklearnRegressor, name_of_file: str):
    pickle.dump(model, open(f'{name_of_file}.pickle', 'wb'))
    
def get_model_from_file(name_of_file: str) -> autosklearn.regression.AutoSklearnRegressor:
    with open(name_of_file, "rb") as file:
        model = pickle.load(file)
    return model 

def createSkLearnModel_with_split(csv_name: str):
    res = base.get_results_form_csv(csv_name)
    name = csv_name.split(".")[0]

    X = res[0]
    Y = res[1]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    automl = autosklearn.regression.AutoSklearnRegressor(
        time_left_for_this_task = 600,# 200  # 150? # spike up time and compare with results, play around --> which inputs give the best results, run multiple times to validate
        per_run_time_limit = 60, # 20
        initial_configurations_via_metalearning=25,
        memory_limit=3072, # half the ram  
        resampling_strategy='cv',
        resampling_strategy_arguments={'folds':5},
        tmp_folder=f"/tmp/{name}",
        n_jobs=1 # use half the number of cores
    )

    automl.fit(X_train, Y_train) 
    print(automl.leaderboard())

    save_model(automl, name)
    train_predictions = automl.predict(X_train)
    print("Train R2 score:", r2_score(Y_train, train_predictions))

    test_predictions = automl.predict(X_test)
    print("Test R2 score:", r2_score(Y_test, test_predictions))
    print("--------------------------------------------------------------")
    print("--------------------------------------------------------------")

def getSkLearnModel(csv_name: str, seed: int):

    res = base.get_results_form_csv(csv_name)

    X = res[0]
    Y = res[1]

    automl = autosklearn.regression.AutoSklearnRegressor(
        seed=seed,
        time_left_for_this_task = 600,# 200  # 150?
        per_run_time_limit = 60, # 20
        initial_configurations_via_metalearning=25,
        memory_limit=3072,
        resampling_strategy='cv',
        resampling_strategy_arguments={'folds':5},
        n_jobs=4
    )

    automl.fit(X, Y) 
    print("--------------------------------------------------------------")
    print("--------------------------------------------------------------")
    return automl
    #print(automl.leaderboard())

    #save_model(automl, name)
    #train_predictions = automl.predict(X)
    #print("Train R2 score:", r2_score(Y, train_predictions))

    #test_predictions = automl.predict(X_test)
    #print("Test R2 score:", r2_score(Y_test, test_predictions))

def process_and_save_files(folder_path, seeds: List[int]):
    for seed in seeds:
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith('.csv'):
                    file_path = os.path.join(root, filename)
                    new_file_path = os.path.splitext(file_path)[0] + f'_seed_{seed}.pickle'

                    if (os.path.exists(new_file_path)):
                        continue
                    
                    print(f"-------- Working on: {new_file_path} --------")
                    # Perform your operation on the file here
                    automl = getSkLearnModel(file_path, seed)
                        
                    with open(new_file_path, 'wb') as pickle_file:
                        # Serialize and save the processed data using pickle
                        pickle.dump(automl, pickle_file)   
                    print(f"Processed and saved: {new_file_path}")


if __name__ == '__main__':
    process_and_save_files('sim_sampling_noise_2', [1, 2, 3, 4, 5])



     