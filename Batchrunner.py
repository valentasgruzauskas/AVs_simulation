from mesa.batchrunner import BatchRunnerMP
from mesa.datacollection import DataCollector
from multiprocessing import freeze_support
from model import welfare_model

import pandas as pd
import numpy as np

from support_functions import (
    calculcate_total_fines_collected,
    calculate_car_type,
    calculate_early_adaptors_type,
    calculate_stagnator_type,
    calculcate_total_CO2,
    calculcate_total_welfare,
    calculcate_total_savings,
    calculate_productivity_healthy,
    calculate_productivity_accident,
    calculate_productivity_injured,
    calculate_productivity_dead,
    get_month,
)

# #### Single run, many iterations
# Number_households = 1000
#
# fixed_params = {"Number_households": Number_households,
#                 "early_adaptor_prob": 0.001,
#                 "stagnator_prob": 0.3,
#                 "early_adaptor_lower_threshold": 9,
#                 "early_adaptor_upper_threshold": 3,
#                 "selected_country": "Germany"
#                 }
#
# variable_parameters = {
#     "Social_network_size": range(8, 12, 1)}

#### parameter analysis, large space

Number_households = 1000

fixed_params = {"Number_households": Number_households}

variable_parameters = {
    "Social_network_size": range(8, 12, 1),
    "early_adaptor_prob": np.arange(0.001, 0.01, 0.002),
    "stagnator_prob": np.arange(0.1, 1, 0.2),
    "early_adaptor_lower_threshold": np.arange(0, 10, 1),
    "early_adaptor_upper_threshold": np.arange(0, 10, 1),
    "selected_country": ["Lithuania", "Germany"],
}

#set iteration number
iterations = 30

if __name__ == "__main__":
    freeze_support()

    batch_run = BatchRunnerMP(
        welfare_model,
        variable_parameters=variable_parameters,
        fixed_parameters=fixed_params,
        iterations=iterations,
        max_steps=12 * 50,
        nr_processes=23,
        model_reporters={
            "Total offenses": calculcate_total_fines_collected,
            "Total CO2": calculcate_total_CO2,
            "Total welfare": calculcate_total_welfare,
            "Total savings": calculcate_total_savings,
            "Number of autonomous vehicles": calculate_car_type,
            "Number of early adaptors": calculate_early_adaptors_type,
            "Number of stagnators": calculate_stagnator_type,
            "Number of healthy households": calculate_productivity_healthy,
            "Number of accident households": calculate_productivity_accident,
            "Number of injured households": calculate_productivity_injured,
            "Number of dead households": calculate_productivity_dead,
            "Month": get_month,
            "Data Collector": lambda m: m.datacollector,
        },
        display_progress=True,
    )

    batch_run.run_all()

    # Save model output
    df = batch_run.get_model_vars_dataframe()
    df_step_data = pd.DataFrame()

    j = 1
    for i in range(len(df["Data Collector"])):
        if isinstance(df["Data Collector"][i], DataCollector):
            i_run_data = df["Data Collector"][i].get_model_vars_dataframe()
            i_run_data["scenario_id"] = i
            i_run_data["early_adaptor_prob"] = df["early_adaptor_prob"][i]
            i_run_data["stagnator_prob"] = df["stagnator_prob"][i]
            i_run_data["early_adaptor_lower_threshold"] = df["early_adaptor_lower_threshold"][i]
            i_run_data["early_adaptor_upper_threshold"] = df["early_adaptor_upper_threshold"][i]
            i_run_data["Social_network_size"] = df["Social_network_size"][i]
            i_run_data["Number_households"] = df["Number_households"][i]
            i_run_data["selected_country"] = df["selected_country"][i]
            i_run_data["Iteration"] = j
            i_run_data = i_run_data.iloc[1:, :]
            df_step_data = df_step_data.append(i_run_data, ignore_index=True)

            j = j + 1

            if j == iterations + 1:
                j = 1

    df_step_data.sort_values(by=["Social_network_size", "Iteration", "Month"])
    df_step_data.to_csv(f"Output/batchrunner model output.csv")
