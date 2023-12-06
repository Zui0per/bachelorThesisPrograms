import subprocess
import re
import os
import signal
import time

def save_simulation_with_id(id: int, length: float, width: float, force1: float, force2: float, force3: float, force4: float, young_modulus: str, poisson_ratio: str):
    cli_command = f"start FreeCAD simulation.py {id} {length} {width} {force1} {force2} {force3} {force4} {young_modulus} {poisson_ratio}"
    subprocess.run(cli_command, encoding="utf8", cwd=r'C:\\Users\\oskar\\Desktop\\bachelor-sampling\\sampling\\strategies\\freeCAD', capture_output=True, shell=True, check=True)
    a = 34


    

def get_displacement_magnitude(length: float, width: float, force1: float, force2: float, force3: float, force4: float, young_modulus: str, poisson_ratio: str):
    try:
        cli_command = f"FreeCADcmd simulation_cmd.py {length} {width} {force1} {force2} {force3} {force4} {young_modulus} {poisson_ratio}"
        popen = subprocess.Popen(cli_command, encoding="utf8", cwd=r'C:\\Users\\oskar\\Desktop\\bachelor-sampling\\sampling\\strategies\\freeCAD', shell=True, stdout=subprocess.PIPE)
        out, err = popen.communicate()

        if err is not None:
            print("ERROR: " + str(err))

        #time.sleep(0.5)
        popen.kill()

        #console_output = subprocess.run(cli_command, encoding="utf8", cwd=r'C:\\Users\\oskar \\Desktop\\freecadPython-2\\sampling\\strategies\\freeCAD',capture_output=True, shell=True, check=True).stdout
        res = re.search(r'(?<=(Value  : ))\d+.\d+', out).group(0)
        return float(res)
    
    except subprocess.CalledProcessError as e:
        print(f"CalledProcessError - {e}")
        popen.kill()
        time.sleep(100)
        return float(get_displacement_magnitude(length, width, force1, force2, force3, force4, young_modulus, poisson_ratio))
    except AttributeError as e:
        print(f"AttributeError - {e}")
        popen.kill()
        time.sleep(100)
        return float(get_displacement_magnitude(length, width, force1, force2, force3, force4, young_modulus, poisson_ratio))     
   