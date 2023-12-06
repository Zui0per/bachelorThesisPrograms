from freeCAD.my_API import get_displacement_magnitude
from freeCAD.my_API import save_simulation_with_id
import base 

#save_simulation_with_id(10, base.LENGTH_MAX, base.WIDTH_MAX, base.F1_MAX, base.F2_MAX, base.F3_MAX, base.F4_MAX, f"{base.YOUNG_MODULUS_MAX} MPa", str(base.POISSON_RATIO_MAX))
#save_simulation_with_id(11, base.LENGTH_MAX, base.WIDTH_MIN, base.F1_MAX, base.F2_MAX, base.F3_MAX, base.F4_MAX, f"{base.YOUNG_MODULUS_MAX} MPa", str(base.POISSON_RATIO_MAX))
#save_simulation_with_id(12, base.LENGTH_MIN, base.WIDTH_MAX, base.F1_MAX, base.F2_MAX, base.F3_MAX, base.F4_MAX, f"{base.YOUNG_MODULUS_MAX} MPa", str(base.POISSON_RATIO_MAX))
#save_simulation_with_id(13, base.LENGTH_MIN, base.WIDTH_MIN, base.F1_MAX, base.F2_MAX, base.F3_MAX, base.F4_MAX, f"{base.YOUNG_MODULUS_MAX} MPa", str(base.POISSON_RATIO_MAX))

def create_validation_csv():
   #save_simulation_with_id(32, base.LENGTH_MIN, base.WIDTH_MIN, base.F1_MIN, base.F2_MIN, base.F3_MAX, base.F4_MIN, f"{base.YOUNG_MODULUS_MAX} MPa", str(base.POISSON_RATIO_MAX))
   #save_simulation_with_id(33, base.LENGTH_MIN, base.WIDTH_MIN, base.F1_MIN, base.F2_MAX, base.F3_MAX, base.F4_MIN, f"{base.YOUNG_MODULUS_MAX} MPa", str(base.POISSON_RATIO_MAX))
   results = {}
   i: int = base.F2_MIN

   length = base.LENGTH_MIN
   width = base.WIDTH_MIN
   f1 = base.F1_MIN
   f3 = base.F3_MAX
   f4 = base.F4_MIN
   young_modulus = base.YOUNG_MODULUS_MAX
   poisson_ratio = base.POISSON_RATIO_MAX        

   while (i < base.F2_MAX):
    input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=i, f3=f3, f4=f4)
    res = get_displacement_magnitude(length, width, f1, i, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
    results.update({input: res})
    i += 5000
    print(f"left: {base.F2_MAX - i }")

   base.print_results_in_csv(results, "validation_firstDraft.csv")

#create_validation_csv()

def transform_csv_file(name: str):
    with open(name, "r") as file:
        content = file.read()
        new_content = content.replace(",", ";").replace(".", ",")

        with open(f"adjusted_{name}", "x") as f:
           f.write(new_content)


transform_csv_file("testdata_2500.csv")


