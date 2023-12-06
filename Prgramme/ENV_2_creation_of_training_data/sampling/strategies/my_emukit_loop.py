from typing import Callable, Union
from emukit.core.event_handler import EventHandler
from emukit.core.parameter_space import ParameterSpace
from emukit.core.optimization import GradientAcquisitionOptimizer
from emukit.core.loop import ConvergenceStoppingCondition, FixedIterationsStoppingCondition, StoppingCondition
from emukit.core.loop import FixedIntervalUpdater, OuterLoop, SequentialPointCalculator
from emukit.core.acquisition import Acquisition
from emukit.core.loop.user_function import UserFunction, UserFunctionWrapper
from emukit.core.loop import LoopState
from emukit.core.loop.loop_state import create_loop_state
from emukit.core.interfaces.models import IModel
from emukit.experimental_design.acquisitions import ModelVariance
from emukit.core.optimization import LocalSearchAcquisitionOptimizer
from my_acqusition import SmallDataContextAcquisition
import scipy.stats
import numpy as np
from emukit.test_functions import forrester_function
import matplotlib.lines as mlines
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors


class SmallDataContextLoop(OuterLoop):

    def __init__(self, space: ParameterSpace, model: IModel, acquisition: Acquisition):
        self.space = space
        self.model_updater = FixedIntervalUpdater(model, interval=1)
        self.loop_state = create_loop_state(model.X, model.Y)

        self.model = model
        self.acquisition = acquisition
        #self.acquisition = ModelVariance(model)
        self.acquisition_optimizer = GradientAcquisitionOptimizer(space)

        self.candidate_point_calculator = SequentialPointCalculator(self.acquisition, self.acquisition_optimizer)

        self.loop_start_event = EventHandler()
        self.iteration_end_event = EventHandler()

    def plot_acq_function(self, iteration: int, new_x):
        x_plot = np.linspace(self.space.parameters[0].min, self.space.parameters[0].max, 301)[:, None]
        y_values = self.acquisition.evaluate(x_plot)       
        y_values_model, _  = self.model.predict(x_plot)
        y_value_of_acq = self.acquisition.evaluate(new_x).flatten()[0]
        #bgv_factor = round(self.acquisition.get_bgv_factor()[0], 3)

        plt.axvline(new_x, color="red", label="x_nächster", linestyle="--")
        plt.plot(self.loop_state.X, self.loop_state.Y, "ro", markersize=10)
        plt.plot(x_plot, y_values_model, label="Modell")
        plt.plot(x_plot, y_values, label="Bereitstellungsfunktion b")

        
        b_acq_legend_entry = mlines.Line2D([], [], color='none', marker='None', linestyle='None', label=f'b(x_nächster) = {round(y_value_of_acq, 4)}')
        #bgv_legend_entry = mlines.Line2D([], [], color='none', marker='None', linestyle='None', label=f'|BGV Faktor x| = {bgv_factor}')
        # Combine the existing legend handles with the new bgv_legend_entry
        handles, labels = plt.gca().get_legend_handles_labels()
        handles.append(b_acq_legend_entry)
        #handles.append(bgv_legend_entry)

        # Display the legend with the combined entries
        plt.legend(handles=handles, loc=2)

        plt.savefig(f"acq_{iteration}.png")
        plt.close()

    def plot_final_model(self):
        target_function, _ = forrester_function()
        x_plot = np.linspace(self.space.parameters[0].min, self.space.parameters[0].max, 301)[:, None]

        y_values_model, _  = self.model.predict(x_plot)
        real_y = target_function(x_plot) 
        plt.plot(self.loop_state.X, self.loop_state.Y, "ro", markersize=10)
        plt.plot(x_plot, y_values_model, label="Modell")
        plt.plot(x_plot, real_y, label="Zielfunktion")

        plt.legend(loc=2)
        plt.savefig(f"final_res.png")
        plt.close()
    
    def plot_model(self, iteration: int):
        target_function, _ = forrester_function()
        x_plot = np.linspace(self.space.parameters[0].min, self.space.parameters[0].max, 301)[:, None]

        y_values_model, _  = self.model.predict(x_plot)
        real_y = target_function(x_plot) 
        plt.plot(self.loop_state.X, self.loop_state.Y, "ro", markersize=10)
        plt.plot(x_plot, y_values_model, label="Modell")
        plt.plot(x_plot, real_y, label="Zielfunktion")

        plt.legend(loc=2)
        plt.savefig(f"model_{iteration}.png")
        plt.close()


    def run(self, stopping_condition: Union[StoppingCondition, int], user_function: Callable) -> None:

        is_int = isinstance(stopping_condition, int)
        is_single_condition = isinstance(stopping_condition, StoppingCondition)

        if not (is_int or is_single_condition):
            raise ValueError(
                "Expected stopping_condition to be an int or a StoppingCondition instance,"
                "but received {}".format(type(stopping_condition))
            )

        if not isinstance(user_function, UserFunction):
            user_function = UserFunctionWrapper(user_function)

        if isinstance(stopping_condition, int):
            stopping_condition = FixedIterationsStoppingCondition(stopping_condition + self.loop_state.iteration)

        self.loop_start_event(self, self.loop_state)
        while not stopping_condition.should_stop(self.loop_state):
            
            # Update data X -> Y for model 
            self.model_updater.update(self.loop_state)

            self.plot_model(self.loop_state.iteration)
            # Aqusition function get new point
            new_x = self.candidate_point_calculator.compute_next_points(self.loop_state)
            self.plot_acq_function(self.loop_state.iteration, new_x)

            # Evaluate user function
            results = user_function.evaluate(new_x)

            # Update results and iteration
            self.loop_state.update(results)

            self.iteration_end_event(self, self.loop_state)


        self.plot_final_model()
    




















# code below this comment is outdated and currently not used!
# -------------------------------------------------------------------------
def get_BGV_response(self):
        # Which input? TODO
        factors = self.X[0]
        response = self.Y[0]

        groups = []
        number_of_samples_in_group = 10
        for factor in factors: 
            group = np.random.default_rng().normal(factor, 0.1, number_of_samples_in_group)
            groups.append(group)
        
        error_variance = sum(map(get_error_variance_of_group, groups))

        numerator = groups.count - 1
        denominator = (number_of_samples_in_group * groups.count - number_of_samples_in_group)
        adj_error_variance = error_variance / denominator
        f, p = scipy.stats.f_oneway(groups)

        F_crit = scipy.stats.f.ppf(q=1-0.05, dfn=numerator, dfd=denominator)

        BGV_res_min = (F_crit * adj_error_variance) ** 0.5
        return BGV_res_min


def get_error_variance_of_group(array) -> float:
    mean = np.mean(array)
    variance = 0
    for el in array:
        variance += (el - mean) ** 2
    return variance




