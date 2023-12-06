import re
import math
import matplotlib
import matplotlib.pyplot as plt

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

def create_plot_from_res_csv(file_name: str, my_name):

    group_1 = ['#FF5733', '#33FF57', '#5733FF', '#33FFFF', '#FF33FF']

    group_2 = [
    "#00CC66", 
    "#009933", 
    "#007722",  
    "#005511",  
    "#003300"   
    ]

    group_3_colors = [
    "#FF3333",  
    "#CC0000"   
    ]
    
    optimal_colors = ['#FF0000', '#FFCCE8', '#8108EC', '#F500FC', '#470B2C'] # box-behnken, CCD-C, CCD-F, CCD-I, 2-Stufen FFD
    space_filling_colors = ['FF8F00', 'FFF700', 'BEE239', '5FA163', '053908'] # CVT, LHS-center, LHS-centermaximin, LHS-correlation, LHS-maximin
    adaptive_colors = ['#1A079E', '#0d85ec'] # model-varianz, IVR
    mixed_colors = ['#1A079E', '053908'] #'#0C73AA', '#3E8A36', '#0074AA', '#425C43'
    matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=space_filling_colors)

    with open(file_name, "r") as file:
        lines = file.readlines()
        column_names = [item.strip() for item in lines[0].split(";")[1:]]
        data_lines = lines[1:]

        column_count = 0
        column_data = {}

        for column in column_names:
            for line in data_lines:
                cells = line.split(";")
                name_with_number = cells[0]
                data_cells = cells[1:]

                name = get_custom_name(name_with_number)
                x_val = int(re.search(r"(?:-|_)(\d+)", name_with_number).group(1))

                y_val = float(data_cells[column_count])

                if 'MSE' in column:
                    y_val = math.sqrt(y_val)
                
                if (name in column_data):
                    column_data[name]["x"].append(x_val)
                    column_data[name]["y"].append(y_val)
                else:
                    column_data[name] = {}
                    column_data[name]["x"] = []
                    column_data[name]["y"] = []
                    column_data[name]["x"].append(x_val)
                    column_data[name]["y"].append(y_val)

            for sample_strat in column_data:
                if ("adjusted_testdata" in sample_strat):
                    continue
                line = '-'
                opc = 1
                color = None
                if ("2%" in sample_strat):
                    opc = 0.5
                if ("5%" in sample_strat):
                    if ("Emukit" in sample_strat):
                        line = (0, (1, 2))
                    else:
                        opc = 0.2
                    #line = (0, (1, 3))
                if ("10%" in sample_strat):
                    if ("Emukit" in sample_strat):
                        color="magenta"
                    else:
                        color = "lawngreen"
                #opc = 0.66 if "2%" in sample_strat else 1
                plt.plot(column_data[sample_strat]["x"], column_data[sample_strat]["y"], label=sample_strat, alpha=opc, linestyle=line, color=color)
            
            plt.xlabel("Anzahl an Stichproben")
            plt.ylabel(column)
            plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
            fig = plt.gcf()
            fig.set_size_inches(9.5, 4.8)
            plt.tight_layout()
            #plt.title("Model Varianz und LHS")
            plt.grid(True)

            column = column.replace("MSE", "RMSE")
            plt.savefig(f"{column}-{my_name}.png", bbox_inches="tight")
            plt.close()

            column_count = column_count + 1
            column_data.clear()

def create_plot_from_res_csv_for_relevant_results(file_name: str):
    with open(file_name, "r") as file:
        lines = file.readlines()
        column_names = [item.strip() for item in lines[0].split(";")[1:]]
        data_lines = lines[1:]

        column_count = 0
        column_data = {}

        for column in column_names:
            for line in data_lines:
                cells = line.split(";")
                name_with_number = cells[0]
                data_cells = cells[1:]

                name = re.sub(r"(-|_)(\d+)", "", name_with_number)
                x_val = int(re.search(r"\d+", name_with_number).group())
                y_val = float(data_cells[column_count])

                if (name in column_data):
                    column_data[name]["x"].append(x_val)
                    column_data[name]["y"].append(y_val)
                else:
                    column_data[name] = {}
                    column_data[name]["x"] = []
                    column_data[name]["y"] = []
                    column_data[name]["x"].append(x_val)
                    column_data[name]["y"].append(y_val)

            for sample_strat in column_data:
                if ("adjusted_testdata" in sample_strat):
                    continue
                plt.plot(column_data[sample_strat]["x"], column_data[sample_strat]["y"], label=sample_strat)
            
            if ("r2" in column):
                plt.ylim(0, 1)
            
            if ("mse" in column):
                plt.ylim(0, 2000)

            plt.xlabel("sample count")
            plt.ylabel(column)
            plt.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0)
            fig = plt.gcf()
            fig.set_size_inches(9, 4.8)
            plt.tight_layout()
            plt.title("sample strategies results")
            plt.grid(True)

            plt.savefig(f"{column}-relevant.png", bbox_inches="tight")
            plt.close()

            column_count = column_count + 1
            column_data.clear()

def create_plot_from_res_csv_for_most_relevant_results(file_name: str):
    with open(file_name, "r") as file:
        lines = file.readlines()
        column_names = [item.strip() for item in lines[0].split(";")[1:]]
        data_lines = lines[1:]

        column_count = 0
        column_data = {}

        for column in column_names:
            for line in data_lines:
                cells = line.split(";")
                name_with_number = cells[0]
                data_cells = cells[1:]

                name = re.sub(r"(-|_)(\d+)", "", name_with_number)
                x_val = int(re.search(r"\d+", name_with_number).group())
                y_val = float(data_cells[column_count])

                if (name in column_data):
                    column_data[name]["x"].append(x_val)
                    column_data[name]["y"].append(y_val)
                else:
                    column_data[name] = {}
                    column_data[name]["x"] = []
                    column_data[name]["y"] = []
                    column_data[name]["x"].append(x_val)
                    column_data[name]["y"].append(y_val)

            diagram_lines = []

            if ("r2" in column):
                plt.ylim(0.85, 1)
            
            if ("mse" in column):
                plt.ylim(0, 1000)

            for sample_strat in column_data:
                if ("adjusted_testdata" in sample_strat):
                    continue
                line_y_min = min(column_data[sample_strat]["y"])
                if (plt.ylim()[0] <= line_y_min <= plt.ylim()[1]):
                    plt.plot(column_data[sample_strat]["x"], column_data[sample_strat]["y"], label=sample_strat)

            plt.xlabel("sample count")
            plt.ylabel(column)
            plt.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0)
            fig = plt.gcf()
            fig.set_size_inches(9, 4.8)
            plt.tight_layout()
            plt.title("sample strategies results")
            plt.grid(True)

            plt.savefig(f"{column}-most-relevant-custom.png", bbox_inches="tight")
            plt.close()

            column_count = column_count + 1
            column_data.clear()

def create_plot_from_classic_res_csv(file_name: str):

    classis_colors = ['#FF0000', '#FFCCE8', '#8108EC', '#470B2C'] # box-behnken, CCD-C, CCD-F, CCD-I, 2-Stufen FFD


    matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=classis_colors)

    with open(file_name, "r") as file:
        lines = file.readlines()
        column_names = [item.strip() for item in lines[0].split(";")[1:]]
        data_lines = lines[1:]

        column_count = 0
        column_data = {}

        for column in column_names:
            fig, ax = plt.subplots()
            for line in data_lines:
                cells = line.split(";")
                name_with_number = cells[0]
                data_cells = cells[1:]

                name = get_custom_name(name_with_number)
                x_val = 0

                if (name == 'Box-Behnken Design'):
                    x_val = 113
                elif (name == '2-Stufen FFD'):
                    x_val = 256
                elif (name == 'CCD-C'):
                    x_val = 257
                elif (name == 'CCD-F'):
                    x_val = 273  
                else:
                    continue

                y_val = float(data_cells[column_count])

                if 'RMSE' in column:
                    y_val = math.sqrt(y_val)
                
                ax.scatter(x_val, y_val, marker='*')

            plt.xlabel("Anzahl an Stichproben")
            plt.ylabel(column)
            plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
            fig = plt.gcf()
            fig.set_size_inches(9.5, 4.8)
            plt.tight_layout()
            plt.title("Klassische Methoden")
            plt.grid(True)

            plt.savefig(f"{column}-classic-plain.png", bbox_inches="tight")
            plt.close()

            column_count = column_count + 1
            column_data.clear()




#create_plot_from_res_csv('res_adaptive_avg_lhs_10k.csv', "adaptive")
#create_plot_from_res_csv('res_adaptive_2_avg_lhs_10k.csv', "adaptive_2")
#create_plot_from_res_csv('res_adaptive_5_avg_lhs_10k.csv', "adaptive_5")
#create_plot_from_res_csv('res_adaptive_10_avg_lhs_10k.csv', "adaptive_10")

#create_plot_from_res_csv('res_optimal_avg_lhs_10k.csv', "optimal")

#create_plot_from_res_csv('res_space-filling_avg_lhs_10k.csv', "space_filling")

#create_plot_from_res_csv('res_space-filling_2_avg_lhs_10k.csv', "space_filling_2")
#create_plot_from_res_csv('res_space-filling_5_avg_lhs_10k.csv', "space_filling_5")
create_plot_from_res_csv('res_space-filling_10_avg_lhs_10k.csv', "space_filling_10")
