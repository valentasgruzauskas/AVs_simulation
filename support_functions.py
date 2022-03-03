import pandas as pd
import random
import math
import numpy as np


def calculcate_total_fines_collected(welfare_model):
    fine_size = [agent.fine_size for agent in welfare_model.schedule.agents]
    total_fines = sum(fine_size)

    return total_fines


def calculcate_mean_CO2(welfare_model):
    CO2 = [agent.CO2 for agent in welfare_model.schedule.agents]
    mean_CO2 = int(np.mean(CO2))

    return mean_CO2


def calculcate_mean_welfare(welfare_model):
    welfare_score = [agent.welfare_score for agent in welfare_model.schedule.agents]
    mean_welfare_score = int(np.mean(welfare_score))

    return mean_welfare_score


def calculcate_mean_savings(welfare_model):
    welfare_score = [agent.savings for agent in welfare_model.schedule.agents]
    mean_savings = int(np.mean(welfare_score))

    return mean_savings


def calculate_productivity_healthy(welfare_model):
    health_status = [agent.health_status for agent in welfare_model.schedule.agents]
    status_no = int(health_status.count("Healthy"))

    return status_no


def calculate_productivity_accident(welfare_model):
    health_status = [agent.health_status for agent in welfare_model.schedule.agents]
    status_no = int(health_status.count("Accident"))

    return status_no


def calculate_productivity_injured(welfare_model):
    health_status = [agent.health_status for agent in welfare_model.schedule.agents]
    status_no = int(health_status.count("Injured"))

    return status_no


def calculate_productivity_dead(welfare_model):
    health_status = [agent.health_status for agent in welfare_model.schedule.agents]
    status_no = int(health_status.count("Dead"))

    return status_no


def calculate_car_type(welfare_model):
    car_type = [agent.car_type for agent in welfare_model.schedule.agents]

    autonomous_no = car_type.count("Autonomous")

    return autonomous_no


def calculate_early_adaptors_type(welfare_model):
    adaptor_type = [agent.inovator_type for agent in welfare_model.schedule.agents]

    adaptor_no = adaptor_type.count("early adaptor")

    return adaptor_no

def calculate_stagnator_type(welfare_model):
    adaptor_type = [agent.inovator_type for agent in welfare_model.schedule.agents]

    stagnator_no = adaptor_type.count("stagnator")

    return stagnator_no


def purchase_car(self):

    L5_costs = int(get_l5_costs(self))

    loan_size = int((self.model.car_price + L5_costs) * self.model.interest_rate)

    down_payment = int(loan_size * self.model.downpayment_size)

    monthly_payment = int(loan_size / self.model.loan_period)

    if self.savings > down_payment:

        self.savings = self.savings - down_payment

        self.loan = loan_size
        self.monthly_payment = monthly_payment

        self.car_type = "Autonomous"


def get_input_value(df, indicator_title):
    df = df.loc[df["Variable_sht"] == indicator_title]
    return float(df["Value"])

#TO DO - nera germany
def select_household_size(model):

    if random.uniform(0, 1) < model.single_person_prob:
        income = model.W_SH
    else:
        income = model.W_CH

    return income


def select_inovator_type(model):

    inovator_type = 'normal'

    if random.uniform(0, 1) < model.stagnator_prob:
        inovator_type = "stagnator"

    if random.uniform(0, 1) < model.early_adaptor_prob:
        inovator_type = "early adaptor"

    return inovator_type


def get_l5_costs(self):
    df = self.model.AV_costs
    current_month = self.model.month
    current_year = math.floor(current_month / 12)
    df = df.loc[df["Year"] == current_year]
    return df["L5_costs"]


def get_month(self):
    return self.month
