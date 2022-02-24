from mesa import Model
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
import networkx as nx

from mesa.space import NetworkGrid

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
    select_household_size,
    select_inovator_type,
    get_input_value,
    get_month,
)

from agent import Household_agent

import pandas as pd
import pickle


class welfare_model(Model):
    def __init__(
        self,
        Social_network_size,
        early_adaptor_prob,
        stagnator_prob,
        early_adaptor_lower_threshold,
        early_adaptor_upper_threshold,
        Number_households,
        selected_country,
    ):
        self.G = nx.connected_caveman_graph(l=int(Number_households / Social_network_size), k=Social_network_size)
        self.schedule = BaseScheduler(self)
        self.grid = NetworkGrid(self.G)
        self.month = 0
        self.selected_country = selected_country
        self.stagnator_prob = stagnator_prob
        self.early_adaptor_prob = early_adaptor_prob

        self.max_iters = 12 * 100

        self.input_data = pd.read_excel("Input/Input data.xlsx")
        self.TC_CO2_max = get_input_value(self.input_data, "TC_CO2_max")
        self.TC_CO2_min = get_input_value(self.input_data, "TC_CO2_min")
        self.AV_CO2_max = get_input_value(self.input_data, "AV_CO2_max")
        self.AV_CO2_min = get_input_value(self.input_data, "AV_CO2_min")
        self.AV_benefit = get_input_value(self.input_data, "AV_SI")
        self.CO2_tax_min = get_input_value(self.input_data, "CO2_tax_min")
        self.CO2_tax_max = get_input_value(self.input_data, "CO2_tax_max")
        self.car_price = get_input_value(self.input_data, "TC_price")
        self.downpayment_size = get_input_value(self.input_data, "DP") / 100
        self.loan_period = get_input_value(self.input_data, "LP")
        self.interest_rate = get_input_value(self.input_data, "IR")
        self.AV_costs = pd.read_excel("Input/AV costs.xlsx")

        if self.selected_country == "Lithuania":
            self.Accident_prob = get_input_value(self.input_data, "Acc_prob_LT")
            self.Injury_prob = get_input_value(self.input_data, "Inj_prob_LT")
            self.Fatality_prob = get_input_value(self.input_data, "Fat_prob_LT")
            self.single_person_prob = get_input_value(self.input_data, "SPH_ratio_LT")
            self.W_SH_LT = get_input_value(self.input_data, "W_SH_LT")
            self.W_CH_LT = get_input_value(self.input_data, "W_CH_LT")
            self.Trans_exp_LT = get_input_value(self.input_data, "Trans_exp_LT")

            self.fine_size = get_input_value(self.input_data, "Fine_size_LT")
            self.fine_prob = get_input_value(self.input_data, "Fine_prob_LT")

        if self.selected_country == "Germany":
            self.Accident_prob = get_input_value(self.input_data, "Acc_prob_DE")
            self.Injury_prob = get_input_value(self.input_data, "Inj_prob_DE")
            self.Fatality_prob = get_input_value(self.input_data, "Fat_prob_DE")
            self.single_person_prob = get_input_value(self.input_data, "SPH_ratio_DE")
            self.W_SH_LT = get_input_value(self.input_data, "W_SH_DE")
            self.W_CH_LT = get_input_value(self.input_data, "W_CH_DE")
            self.Trans_exp_LT = get_input_value(self.input_data, "Trans_exp_DE")

            self.fine_size = get_input_value(self.input_data, "Fine_size_DE")
            self.fine_prob = get_input_value(self.input_data, "Fine_prob_DE")

        self.datacollector = DataCollector(
            model_reporters={
                "Total fines collected": calculcate_total_fines_collected,
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
            },
            # agent_reporters={"welfare_score": "welfare_score",
            # "savings": "savings",
            # "income": "income",
            # "car_type": "car_type",
            # "health_status": "health_status",
            # "loan": "loan",
            # "monthly_payment": "monthly_payment",
            # "fine_size": "fine_size",
            # "CO2": "CO2",
            # "Month": "month"
            # }
        )

        for i, node in enumerate(self.G.nodes()):
            agents_H = Household_agent(
                unique_id=i,
                welfare_score=0,
                savings=0,
                income=select_household_size(self),
                inovator_type=select_inovator_type(self),
                loan=0,
                monthly_payment=0,
                fine_size=0,
                car_type="Traditional",
                CO2=0,
                health_status="Healthy",
                early_adaptor_lower_threshold=early_adaptor_lower_threshold,
                early_adaptor_upper_threshold=early_adaptor_upper_threshold,
                desire_to_change_car=False,
                model=self,
            )

            self.schedule.add(agents_H)
            self.grid.place_agent(agents_H, node)

        self.running = True
        self.datacollector.collect(self)

    def step(self):

        self.schedule.step()
        self.datacollector.collect(self)

        self.month += 1

        if self.month == self.max_iters:

            with open(f"Output/datacollector - {self.selected_country}.pickle", "wb") as handle:
                pickle.dump(self.datacollector, handle, protocol=pickle.HIGHEST_PROTOCOL)

        if self.month > self.max_iters:
            self.running = False
