from typing import Tuple
from emukit.core.acquisition import Acquisition
from sklearn.linear_model import LinearRegression
from typing import List
from emukit.core.interfaces import IModel
import numpy as np

class SmallDataContextAcquisition(Acquisition):

    def __init__(self, acquisition: Acquisition, model: IModel, bgv_res: List[float]) -> None:
        self.acquisition = acquisition
        self.model = model
        self.bgv_res = bgv_res
        self.count = 0

        self.linear_reg_model = LinearRegression()
        self.linear_reg_model.fit(self.model.X, self.model.Y)


    def evaluate(self, x: np.ndarray) -> np.ndarray:
        coefficients = self.linear_reg_model.coef_.flatten()
        bgv_factor = [a / b for a, b in zip(self.bgv_res, abs(coefficients))]

        acquisition_values = np.zeros((x.shape[0], 1))

        for i, candidate_point in enumerate(x):
            # Check if the candidate point is within the exclusion radius of any existing point
            within_exclusion_zone = any(np.all(np.abs(candidate_point - existing_point) < bgv_factor) for existing_point in self.model.X)
            
            if within_exclusion_zone:
                acquisition_values[i, 0] = 0
            else:
                # Calculate acquisition value using your acquisition function logic
                acquisition_values[i, 0] = self.acquisition.evaluate(np.array([candidate_point]))

        return acquisition_values
    
    def evaluate_with_gradients(self, x: np.ndarray) -> Tuple:
        return self.acquisition.evaluate_with_gradients(x)

    def update_parameters(self) -> None:
        self.linear_reg_model = LinearRegression()
        self.linear_reg_model.fit(self.model.X, self.model.Y)

    def get_bgv_factor(self) -> float:
        coefficients = self.linear_reg_model.coef_.flatten()
        bgv_factor = [a / b for a, b in zip(self.bgv_res, abs(coefficients))]
        return bgv_factor
    
    def has_gradients(self) -> bool:
        pass
    