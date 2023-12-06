import pickle
import base 
import os
import autosklearn.regression

#save_simulation_with_id(10, base.LENGTH_MAX, base.WIDTH_MAX, base.F1_MAX, base.F2_MAX, base.F3_MAX, base.F4_MAX, f"{base.YOUNG_MODULUS_MAX} MPa", str(base.POISSON_RATIO_MAX))
#save_simulation_with_id(11, base.LENGTH_MAX, base.WIDTH_MIN, base.F1_MAX, base.F2_MAX, base.F3_MAX, base.F4_MAX, f"{base.YOUNG_MODULUS_MAX} MPa", str(base.POISSON_RATIO_MAX))
#save_simulation_with_id(12, base.LENGTH_MIN, base.WIDTH_MAX, base.F1_MAX, base.F2_MAX, base.F3_MAX, base.F4_MAX, f"{base.YOUNG_MODULUS_MAX} MPa", str(base.POISSON_RATIO_MAX))
#save_simulation_with_id(13, base.LENGTH_MIN, base.WIDTH_MIN, base.F1_MAX, base.F2_MAX, base.F3_MAX, base.F4_MAX, f"{base.YOUNG_MODULUS_MAX} MPa", str(base.POISSON_RATIO_MAX))

def transform_csv_file(name: str):
    with open(name, "r") as file:
        content = file.read()
        new_content = content.replace(",", ";").replace(".", ",")

        with open(f"adjusted_{name}", "x") as f:
           f.write(new_content)

def get_model_from_file(name_of_file: str) -> autosklearn.regression.AutoSklearnRegressor:
    with open(name_of_file, "rb") as file:
        model = pickle.load(file)
    return model 

def create_validation_excel_2500(): 
   packet_file_names = list(filter(lambda file_name: "_2500.pickle" in file_name, os.listdir()))

   i: int = base.F2_MIN
   length = base.LENGTH_MIN
   width = base.WIDTH_MIN
   f1 = base.F1_MIN
   f3 = base.F3_MAX
   f4 = base.F4_MIN
   young_modulus = base.YOUNG_MODULUS_MAX
   poisson_ratio = base.POISSON_RATIO_MAX

   for name in packet_file_names: 
      model = get_model_from_file(name)
      results = {}
      name_without_ending = name.split(".")[0]

      while i <= base.F2_MAX:
         input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=i, f3=f3, f4=f4)
         input_model = [[young_modulus, poisson_ratio, length, width, f1, i, f3, f4]]
         res = model.predict(input_model)
         results.update({input: res})
         i += 80000
         print(f"left: {base.F2_MAX - i }")

      base.print_results_in_csv(results, f"{name_without_ending}_validation.csv")
      i = base.F2_MIN
      print("----------------------------------------------")

def create_validation_excel(name: str): 

   i: int = base.F2_MIN
   length = base.LENGTH_MIN
   width = base.WIDTH_MIN
   f1 = base.F1_MIN
   f3 = base.F3_MAX
   f4 = base.F4_MIN
   young_modulus = base.YOUNG_MODULUS_MAX
   poisson_ratio = base.POISSON_RATIO_MAX

   model = get_model_from_file(name)
   results = {}
   name_without_ending = name.split(".")[0]

   while i <= base.F2_MAX:
      input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=i, f3=f3, f4=f4)
      input_model = [[young_modulus, poisson_ratio, length, width, f1, i, f3, f4]]
      res = model.predict(input_model)
      results.update({input: res})
      i += 80000
      print(f"left: {base.F2_MAX - i }")

   base.print_results_in_csv(results, f"{name_without_ending}_validation.csv")



create_validation_excel("lhs-center-10_all_10k.pickle")


   

