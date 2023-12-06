from typing import Dict, Callable
import pyDOE2
from freeCAD.my_API import get_displacement_magnitude, save_simulation_with_id
import base 

YOUNG_MODULUS_MID = (base.YOUNG_MODULUS_MAX + base.YOUNG_MODULUS_MIN) / 2
POISSON_RATIO_MID = (base.POISSON_RATIO_MAX + base.POISSON_RATIO_MIN) / 2
LENGTH_MID = (base.LENGTH_MAX + base.LENGTH_MIN) / 2
WIDTH_MID = (base.WIDTH_MAX + base.WIDTH_MIN) / 2
F1_MID = (base.F1_MAX + base.F1_MIN) / 2
F2_MID = (base.F2_MAX + base.F2_MIN) / 2
F3_MID = (base.F3_MAX + base.F3_MIN) / 2
F4_MID = (base.F4_MAX + base.F4_MIN) / 2

def run_box_behnken_sampling_120() -> Dict[base.Input, float]:
      results = {}
      samples = pyDOE2.bbdesign(8)

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return max
            if (val == -1):
                  return min
            return (max+min)/2

      counter = 0

      for sample in samples:
            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, base.YOUNG_MODULUS_MAX)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, base.POISSON_RATIO_MAX)
            length: float = get_real_val(sample[2], base.LENGTH_MIN, base.LENGTH_MAX)
            width: float = get_real_val(sample[3], base.WIDTH_MIN, base.WIDTH_MAX)
            f1: float = get_real_val(sample[4], base.F1_MIN, base.F1_MAX)
            f2: float = get_real_val(sample[5], base.F2_MIN, base.F2_MAX)
            f3: float = get_real_val(sample[6], base.F3_MIN, base.F3_MAX)
            f4: float = get_real_val(sample[7], base.F4_MIN, base.F4_MAX)
            input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input) is not None):
                  continue

            displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
            
            
            counter += 1
            print("Box-Behnken: " + str(counter))
      
            results.update({input: displacement})
      return results

def run_box_behnken_sampling_240():
      results = {}
      samples = pyDOE2.bbdesign(8)

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return round(max, 3)
            if (val == -1):
                  return round(min, 3)
            return round((max+min)/2)

      counter = 0

      for sample in samples:
            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, YOUNG_MODULUS_MID)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, POISSON_RATIO_MID)
            length: float = get_real_val(sample[2], base.LENGTH_MIN, LENGTH_MID)
            width: float = get_real_val(sample[3], base.WIDTH_MIN, WIDTH_MID)
            f1: float = get_real_val(sample[4], base.F1_MIN, F1_MID)
            f2: float = get_real_val(sample[5], base.F2_MIN, F2_MID)
            f3: float = get_real_val(sample[6], base.F3_MIN, F3_MID)
            f4: float = get_real_val(sample[7], base.F4_MIN, F4_MID)
            input1 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input1) is None):             
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))            
                  counter += 1
                  print("Box-Behnken: " + str(counter))
                  results.update({input1: displacement})

            young_modulus: float = get_real_val(sample[0], YOUNG_MODULUS_MID, base.YOUNG_MODULUS_MAX)
            poisson_ratio: float = get_real_val(sample[1], POISSON_RATIO_MID, base.POISSON_RATIO_MAX)
            length: float = get_real_val(sample[2], LENGTH_MID, base.LENGTH_MAX)
            width: float = get_real_val(sample[3], WIDTH_MID, base.WIDTH_MAX)
            f1: float = get_real_val(sample[4], F1_MID, base.F1_MAX)
            f2: float = get_real_val(sample[5], F2_MID, base.F2_MAX)
            f3: float = get_real_val(sample[6], F3_MID, base.F3_MAX)
            f4: float = get_real_val(sample[7], F4_MID, base.F4_MAX)
            input2 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input2) is None):             
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))            
                  counter += 1
                  print("Box-Behnken: " + str(counter))
                  results.update({input2: displacement})
             
      return results

def run_box_behnken_sampling_360():
      results = {}
      samples = pyDOE2.bbdesign(8)

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return round(max, 3)
            if (val == -1):
                  return round(min, 3)
            return round((max+min)/2)

      counter = 0

      YOUNG_MODULUS_SPAN = (base.YOUNG_MODULUS_MAX - base.YOUNG_MODULUS_MIN) / 3
      POISSON_RATIO_SPAN = (base.POISSON_RATIO_MAX - base.POISSON_RATIO_MIN) / 3
      LENGTH_SPAN = (base.LENGTH_MAX - base.LENGTH_MIN) / 3
      WIDTH_SPAN = (base.WIDTH_MAX - base.WIDTH_MIN) / 3
      F1_SPAN = (base.F1_MAX - base.F1_MIN) / 3
      F2_SPAN = (base.F2_MAX - base.F2_MIN) / 3
      F3_SPAN = (base.F3_MAX - base.F3_MIN) / 3
      F4_SPAN = (base.F4_MAX - base.F4_MIN) / 3

      for sample in samples:
            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, base.YOUNG_MODULUS_MIN + YOUNG_MODULUS_SPAN)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, base.POISSON_RATIO_MIN + POISSON_RATIO_SPAN)
            length: float = get_real_val(sample[2], base.LENGTH_MIN, base.LENGTH_MIN + LENGTH_SPAN)
            width: float = get_real_val(sample[3], base.WIDTH_MIN, base.WIDTH_MIN + WIDTH_SPAN)
            f1: float = get_real_val(sample[4], base.F1_MIN, base.F1_MIN + F1_SPAN)
            f2: float = get_real_val(sample[5], base.F2_MIN, base.F2_MIN + F2_SPAN)
            f3: float = get_real_val(sample[6], base.F3_MIN, base.F3_MIN + F3_SPAN)
            f4: float = get_real_val(sample[7], base.F4_MIN, base.F4_MIN + F4_SPAN)
            input1 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input1) is None):
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
                  counter += 1
                  print("Box-Behnken: " + str(counter))
                  results.update({input1: displacement})

            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN + YOUNG_MODULUS_SPAN, base.YOUNG_MODULUS_MIN + 2 * YOUNG_MODULUS_SPAN)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN + POISSON_RATIO_SPAN, base.POISSON_RATIO_MIN + 2 * POISSON_RATIO_SPAN)
            length: float = get_real_val(sample[2], base.LENGTH_MIN + LENGTH_SPAN, base.LENGTH_MIN + 2 * LENGTH_SPAN)
            width: float = get_real_val(sample[3], base.WIDTH_MIN + WIDTH_SPAN, base.WIDTH_MIN + 2 * WIDTH_SPAN)
            f1: float = get_real_val(sample[4], base.F1_MIN + F1_SPAN, base.F1_MIN + 2 * F1_SPAN)
            f2: float = get_real_val(sample[5], base.F2_MIN + F2_SPAN, base.F2_MIN + 2 * F2_SPAN)
            f3: float = get_real_val(sample[6], base.F3_MIN + F3_SPAN, base.F3_MIN + 2 * F3_SPAN)
            f4: float = get_real_val(sample[7], base.F4_MIN + F4_SPAN, base.F4_MIN + 2 * F4_SPAN)
            input2 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input2) is None):
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
                  counter += 1
                  print("Box-Behnken: " + str(counter))
                  results.update({input2: displacement})
            
            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN + 2 * YOUNG_MODULUS_SPAN, base.YOUNG_MODULUS_MAX)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN + 2 * POISSON_RATIO_SPAN, base.POISSON_RATIO_MAX)
            length: float = get_real_val(sample[2], base.LENGTH_MIN + 2 * LENGTH_SPAN,  base.LENGTH_MAX)
            width: float = get_real_val(sample[3], base.WIDTH_MIN + 2 * WIDTH_SPAN, base.WIDTH_MAX)
            f1: float = get_real_val(sample[4], base.F1_MIN + 2 * F1_SPAN, base.F1_MAX)
            f2: float = get_real_val(sample[5], base.F2_MIN + 2 * F2_SPAN, base.F2_MAX)
            f3: float = get_real_val(sample[6], base.F3_MIN + 2 * F3_SPAN, base.F3_MAX)
            f4: float = get_real_val(sample[7], base.F4_MIN + 2 * F4_SPAN, base.F4_MAX)
            input3 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input3) is None):
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
                  counter += 1
                  print("Box-Behnken: " + str(counter))
                  results.update({input3: displacement})

      return results
      
def run_ccd_sampling_c():
      results = {}
      samples = pyDOE2.ccdesign(8)

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return max
            if (val == -1):
                  return min
            return (max+min)/2
      
      counter = 0

      for sample in samples:
            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, base.YOUNG_MODULUS_MAX)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, base.POISSON_RATIO_MAX)
            length: float = get_real_val(sample[2], base.LENGTH_MIN, base.LENGTH_MAX)
            width: float = get_real_val(sample[3], base.WIDTH_MIN, base.WIDTH_MAX)
            f1: float = get_real_val(sample[4], base.F1_MIN, base.F1_MAX)
            f2: float = get_real_val(sample[5], base.F2_MIN, base.F2_MAX)
            f3: float = get_real_val(sample[6], base.F3_MIN, base.F3_MAX)
            f4: float = get_real_val(sample[7], base.F4_MIN, base.F4_MAX)
            input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input) is not None):
                  continue
            
            #save_simulation_with_id(1, length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
            displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
      
            counter += 1
            print("CCD: " + str(counter))

            results.update({input: displacement})

      return results

def run_ccd_sampling_c_2box():
      results = {}
      samples = pyDOE2.ccdesign(8)

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return round(max, 3)
            if (val == -1):
                  return round(min, 3)
            return round((max+min)/2)
      
      counter = 0

      for sample in samples:
            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, YOUNG_MODULUS_MID)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, POISSON_RATIO_MID)
            length: float = get_real_val(sample[2], base.LENGTH_MIN, LENGTH_MID)
            width: float = get_real_val(sample[3], base.WIDTH_MIN, WIDTH_MID)
            f1: float = get_real_val(sample[4], base.F1_MIN, F1_MID)
            f2: float = get_real_val(sample[5], base.F2_MIN, F2_MID)
            f3: float = get_real_val(sample[6], base.F3_MIN, F3_MID)
            f4: float = get_real_val(sample[7], base.F4_MIN, F4_MID)
            input1 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input1) is None):             
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))            
                  counter += 1
                  print("CCD: " + str(counter))
                  results.update({input1: displacement})

            young_modulus: float = get_real_val(sample[0], YOUNG_MODULUS_MID, base.YOUNG_MODULUS_MAX)
            poisson_ratio: float = get_real_val(sample[1], POISSON_RATIO_MID, base.POISSON_RATIO_MAX)
            length: float = get_real_val(sample[2], LENGTH_MID, base.LENGTH_MAX)
            width: float = get_real_val(sample[3], WIDTH_MID, base.WIDTH_MAX)
            f1: float = get_real_val(sample[4], F1_MID, base.F1_MAX)
            f2: float = get_real_val(sample[5], F2_MID, base.F2_MAX)
            f3: float = get_real_val(sample[6], F3_MID, base.F3_MAX)
            f4: float = get_real_val(sample[7], F4_MID, base.F4_MAX)
            input2 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input2) is None):             
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))            
                  counter += 1
                  print("CCD: " + str(counter))
                  results.update({input2: displacement})

      return results

def run_ccd_sampling_i():
      results = {}
      samples = pyDOE2.ccdesign(8, face="inscribed")

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return max
            if (val == -1):
                  return min
            return (max+min)/2
      
      counter = 0

      for sample in samples:
            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, base.YOUNG_MODULUS_MAX)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, base.POISSON_RATIO_MAX)
            length: float = get_real_val(sample[2], base.LENGTH_MIN, base.LENGTH_MAX)
            width: float = get_real_val(sample[3], base.WIDTH_MIN, base.WIDTH_MAX)
            f1: float = get_real_val(sample[4], base.F1_MIN, base.F1_MAX)
            f2: float = get_real_val(sample[5], base.F2_MIN, base.F2_MAX)
            f3: float = get_real_val(sample[6], base.F3_MIN, base.F3_MAX)
            f4: float = get_real_val(sample[7], base.F4_MIN, base.F4_MAX)
            input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input) is not None):
                  continue
            
            #save_simulation_with_id(1, length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
            displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))

            
            counter += 1
            print("CCD: " + str(counter))

            results.update({input: displacement})

      return results

def run_ccd_sampling_i_2box():
      results = {}
      samples = pyDOE2.ccdesign(8, face="inscribed")

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return round(max, 3)
            if (val == -1):
                  return round(min, 3)
            return round((max+min)/2)
      
      counter = 0

      for sample in samples:
            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, YOUNG_MODULUS_MID)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, POISSON_RATIO_MID)
            length: float = get_real_val(sample[2], base.LENGTH_MIN, LENGTH_MID)
            width: float = get_real_val(sample[3], base.WIDTH_MIN, WIDTH_MID)
            f1: float = get_real_val(sample[4], base.F1_MIN, F1_MID)
            f2: float = get_real_val(sample[5], base.F2_MIN, F2_MID)
            f3: float = get_real_val(sample[6], base.F3_MIN, F3_MID)
            f4: float = get_real_val(sample[7], base.F4_MIN, F4_MID)
            input1 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input1) is None):             
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))            
                  counter += 1
                  print("CCD: " + str(counter))
                  results.update({input1: displacement})

            young_modulus: float = get_real_val(sample[0], YOUNG_MODULUS_MID, base.YOUNG_MODULUS_MAX)
            poisson_ratio: float = get_real_val(sample[1], POISSON_RATIO_MID, base.POISSON_RATIO_MAX)
            length: float = get_real_val(sample[2], LENGTH_MID, base.LENGTH_MAX)
            width: float = get_real_val(sample[3], WIDTH_MID, base.WIDTH_MAX)
            f1: float = get_real_val(sample[4], F1_MID, base.F1_MAX)
            f2: float = get_real_val(sample[5], F2_MID, base.F2_MAX)
            f3: float = get_real_val(sample[6], F3_MID, base.F3_MAX)
            f4: float = get_real_val(sample[7], F4_MID, base.F4_MAX)
            input2 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input2) is None):             
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))            
                  counter += 1
                  print("CCD: " + str(counter))
                  results.update({input2: displacement})

      return results

def run_ccd_sampling_f():
      results = {}
      samples = pyDOE2.ccdesign(8, face="faced")

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return max
            if (val == -1):
                  return min
            return (max+min)/2
      
      counter = 0

      for sample in samples:
            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, base.YOUNG_MODULUS_MAX)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, base.POISSON_RATIO_MAX)
            length: float = get_real_val(sample[2], base.LENGTH_MIN, base.LENGTH_MAX)
            width: float = get_real_val(sample[3], base.WIDTH_MIN, base.WIDTH_MAX)
            f1: float = get_real_val(sample[4], base.F1_MIN, base.F1_MAX)
            f2: float = get_real_val(sample[5], base.F2_MIN, base.F2_MAX)
            f3: float = get_real_val(sample[6], base.F3_MIN, base.F3_MAX)
            f4: float = get_real_val(sample[7], base.F4_MIN, base.F4_MAX)
            input = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input) is not None):
                  continue
            
            #save_simulation_with_id(1, length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))
            displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))

            
            counter += 1
            print("CCD: " + str(counter))

            results.update({input: displacement})

      return results

def run_ccd_sampling_f_2box():
      results = {}
      samples = pyDOE2.ccdesign(8, face="faced")

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return round(max, 3)
            if (val == -1):
                  return round(min, 3)
            return round((max+min)/2)
      
      counter = 0

      for sample in samples:
            young_modulus: float = get_real_val(sample[0], base.YOUNG_MODULUS_MIN, YOUNG_MODULUS_MID)
            poisson_ratio: float = get_real_val(sample[1], base.POISSON_RATIO_MIN, POISSON_RATIO_MID)
            length: float = get_real_val(sample[2], base.LENGTH_MIN, LENGTH_MID)
            width: float = get_real_val(sample[3], base.WIDTH_MIN, WIDTH_MID)
            f1: float = get_real_val(sample[4], base.F1_MIN, F1_MID)
            f2: float = get_real_val(sample[5], base.F2_MIN, F2_MID)
            f3: float = get_real_val(sample[6], base.F3_MIN, F3_MID)
            f4: float = get_real_val(sample[7], base.F4_MIN, F4_MID)
            input1 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input1) is None):             
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))            
                  counter += 1
                  print("CCD: " + str(counter))
                  results.update({input1: displacement})

            young_modulus: float = get_real_val(sample[0], YOUNG_MODULUS_MID, base.YOUNG_MODULUS_MAX)
            poisson_ratio: float = get_real_val(sample[1], POISSON_RATIO_MID, base.POISSON_RATIO_MAX)
            length: float = get_real_val(sample[2], LENGTH_MID, base.LENGTH_MAX)
            width: float = get_real_val(sample[3], WIDTH_MID, base.WIDTH_MAX)
            f1: float = get_real_val(sample[4], F1_MID, base.F1_MAX)
            f2: float = get_real_val(sample[5], F2_MID, base.F2_MAX)
            f3: float = get_real_val(sample[6], F3_MID, base.F3_MAX)
            f4: float = get_real_val(sample[7], F4_MID, base.F4_MAX)
            input2 = base.Input(young_modulus=young_modulus, poisson_ratio=poisson_ratio, length=length, width=width, f1=f1, f2=f2, f3=f3, f4=f4)
            
            if (results.get(input2) is None):             
                  displacement = get_displacement_magnitude(length, width, f1, f2, f3, f4, f"{young_modulus} MPa", str(poisson_ratio))            
                  counter += 1
                  print("CCD: " + str(counter))
                  results.update({input2: displacement})

      return results

def save_ccd_sampling():
      res = run_ccd_sampling_c()
      base.print_results_in_csv(res, "central-composite_c.csv")
      res2 = run_ccd_sampling_i()
      base.print_results_in_csv(res2, "central-composite_i.csv")
      res3 = run_ccd_sampling_f()
      base.print_results_in_csv(res3, "central-composite_f.csv")

def save_bb_sampling():
      res = run_box_behnken_sampling_120()
      base.print_results_in_csv(res, "box-behnken.csv")

def save_bb_boxed_sampling():
      res = run_box_behnken_sampling_240()
      base.print_results_in_csv(res, "box-behnken-2box.csv")
      res2 = run_box_behnken_sampling_360()
      base.print_results_in_csv(res2, "box-behnken-3box.csv")

def save_ccd_boxed_sampling():
      res = run_ccd_sampling_c_2box()
      base.print_results_in_csv(res, "central-composite_c_2box.csv")
      res2 = run_ccd_sampling_i_2box()
      base.print_results_in_csv(res2, "central-composite_i_2box.csv")
      res3 = run_ccd_sampling_f_2box()
      base.print_results_in_csv(res3, "central-composite_f_2box.csv")



def save_bb_sampling():
      res = run_box_behnken_sampling_120()
      base.print_results_in_csv(res, "box-behnken.csv")






res = run_ccd_sampling_i()
base.print_results_in_csv(res, "central-composite_i.csv")































def run_ccd_c_with_func(function: Callable[[float, float, float, float, float, float], float], min, max):
      samples = pyDOE2.ccdesign(6)
      results = {}

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return max
            if (val == -1):
                  return min
            return (max+min)/2
      
      for sample in samples:
            A: float = get_real_val(sample[0], min[0], max[0])
            B: float = get_real_val(sample[1], min[1], max[1])
            C: float = get_real_val(sample[2], min[2], max[2])
            D: float = get_real_val(sample[3], min[3], max[3])
            E: float = get_real_val(sample[4], min[4], max[4])
            F: float = get_real_val(sample[5], min[5], max[5])

            res = function(A, B, C, D, E, F)   
            results.update({(A, B, C, D, E, F): res})
      return results

def run_ccd_i_with_func(function: Callable[[float, float, float, float, float, float], float], min, max):
      samples = pyDOE2.ccdesign(6, face='inscribed')
      results = {}
      
      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return max
            if (val == -1):
                  return min
            return (max+min)/2
      
      for sample in samples:
            A: float = get_real_val(sample[0], min[0], max[0])
            B: float = get_real_val(sample[1], min[1], max[1])
            C: float = get_real_val(sample[2], min[2], max[2])
            D: float = get_real_val(sample[3], min[3], max[3])
            E: float = get_real_val(sample[4], min[4], max[4])
            F: float = get_real_val(sample[5], min[5], max[5])

            res = function(A, B, C, D, E, F)   
            results.update({(A, B, C, D, E, F): res})
      return results

def run_ccd_f_with_func(function: Callable[[float, float, float, float, float, float], float], min, max):
      samples = pyDOE2.ccdesign(6, face="faced")
      results = {}

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return max
            if (val == -1):
                  return min
            return (max+min)/2

      for sample in samples:
            A: float = get_real_val(sample[0], min[0], max[0])
            B: float = get_real_val(sample[1], min[1], max[1])
            C: float = get_real_val(sample[2], min[2], max[2])
            D: float = get_real_val(sample[3], min[3], max[3])
            E: float = get_real_val(sample[4], min[4], max[4])
            F: float = get_real_val(sample[5], min[5], max[5])

            res = function(A, B, C, D, E, F)   
            results.update({(A, B, C, D, E, F): res})
      return results

def run_box_behnken_with_func(function: Callable[[float, float, float, float, float, float], float], min, max):
      results = {}
      samples = pyDOE2.bbdesign(6)

      def get_real_val(val: float, min: float, max: float):
            if (val == 1):
                  return max
            if (val == -1):
                  return min
            return (max+min)/2
      
      for sample in samples:
            A: float = get_real_val(sample[0], min[0], max[0])
            B: float = get_real_val(sample[1], min[1], max[1])
            C: float = get_real_val(sample[2], min[2], max[2])
            D: float = get_real_val(sample[3], min[3], max[3])
            E: float = get_real_val(sample[4], min[4], max[4])
            F: float = get_real_val(sample[5], min[5], max[5])

            res = function(A, B, C, D, E, F)   
            results.update({(A, B, C, D, E, F): res})
      return results