from mesa import Agent

from support_functions import purchase_car

import random


class Household_agent(Agent):
    def __init__(
        self,
        unique_id,
        welfare_score,
        savings,
        income,
        inovator_type,
        loan,
        monthly_payment,
        fine_size,
        car_type,
        CO2,
        health_status,
        early_adaptor_lower_threshold,
        early_adaptor_upper_threshold,
        desire_to_change_car,
        model,
    ):
        self.unique_id = unique_id
        self.welfare_score = welfare_score
        self.savings = savings
        self.income = income
        self.inovator_type = inovator_type
        self.car_type = car_type
        self.health_status = health_status
        self.loan = loan
        self.monthly_payment = monthly_payment
        self.fine_size = fine_size
        self.CO2 = CO2
        self.early_adaptor_lower_threshold = early_adaptor_lower_threshold
        self.early_adaptor_upper_threshold = early_adaptor_upper_threshold
        self.desire_to_change_car = desire_to_change_car
        self.model = model
        self.month = self.model.month

    def check_health_status(self):
        self.health_status = "Healthy"

    def check_inovator_status(self):

        if random.uniform(0, 1) < self.model.stagnator_prob:
            self.inovator_type = "stagnator"
        elif random.uniform(0, 1) < self.model.early_adaptor_prob:
            self.inovator_type = "early adaptor"
        else:
            self.inovator_type = "normal"

    # Based on car type generate CO2 emmision
    def generate_CO2(self):

        if self.car_type == "Traditional":

            self.CO2 = random.uniform(self.model.TC_CO2_min, self.model.TC_CO2_max)

        # If autonomous decrease level of CO2 generated
        if self.car_type == "Autonomous":

            self.CO2 = random.uniform(self.model.AV_CO2_min, self.model.AV_CO2_max)

    def generate_accident(self):

        if self.car_type == "Traditional":
            benefit = 1

        if self.car_type == "Autonomous":
            benefit = (1 - self.model.AV_benefit)

        Accident_prob = self.model.Accident_prob * benefit
        Injury_prob = self.model.Injury_prob * benefit
        Fatality_prob = self.model.Fatality_prob * benefit

        if random.uniform(0, 1) < Accident_prob:
            self.health_status = "Accident"

        if random.uniform(0, 1) < Injury_prob:
            self.health_status = "Injured"

        if random.uniform(0, 1) < Fatality_prob:
            self.health_status = "Dead"

    def generate_offense(self):

        self.fine_size = 0

        if self.car_type == "Traditional":
            benefit = 1

        if self.car_type == "Autonomous":
            benefit = 1 - self.model.AV_benefit

        offense_prob = self.model.fine_prob * benefit

        if random.uniform(0, 1) < offense_prob:

            self.fine_size = self.model.fine_size

    def update_savings(self):

        # Reduce income based on health status
        if self.health_status == "Accident":
            income = self.income * 0.75

        if self.health_status == "Injured":
            income = self.income * 0.55

        if self.health_status == "Dead":
            income = 0

        if self.health_status == "Healthy":
            income = self.income

        # update savings with income
        self.savings = self.savings + income

        # Pay fines
        self.savings = self.savings - self.fine_size

        # Pay loan
        if self.loan != 0:

            if self.savings > self.monthly_payment:
                self.loan = self.loan - self.monthly_payment
                self.savings = self.savings - self.monthly_payment

        # Pay other expenditures
        other_expenses = self.income * (0.85 - self.model.Trans_exp) #basad on average saving ratio
        self.savings = self.savings - other_expenses

        return income

    def calculate_welfare(self, income):

        tax_per_CO2 = random.uniform(self.model.CO2_tax_min, self.model.CO2_tax_max)

        lost_income = self.income - income
        costs_CO2 = self.CO2 * tax_per_CO2

        total_loss = lost_income + costs_CO2 + self.fine_size

        AV_CO2_benefit = random.uniform(self.model.AV_CO2_min, self.model.AV_CO2_max) / 100

        possible_gain_co2 = costs_CO2 - (costs_CO2 * AV_CO2_benefit)

        possible_gain = possible_gain_co2 + lost_income + 0 # Theoretically no fine, thus +0

        welfare_score = int(total_loss - possible_gain)

        self.welfare_score = int(self.welfare_score + welfare_score)

    def change_car(self):

        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)

        compare_welfare_score = 0
        for agent in self.model.grid.get_cell_list_contents(neighbors_nodes):
            compare_welfare_score = compare_welfare_score + agent.welfare_score
        compare_welfare_score = int(compare_welfare_score / len(neighbors_nodes))

        if self.car_type == "Traditional":

            if self.inovator_type == "early adaptor":
                if self.welfare_score * (1 + self.early_adaptor_upper_threshold) > compare_welfare_score:
                    purchase_car(self)

            if self.inovator_type == "stagnator":
                if (compare_welfare_score / self.welfare_score) > self.early_adaptor_lower_threshold:
                    purchase_car(self)

            if self.inovator_type == "normal":
                if self.welfare_score > compare_welfare_score:
                    purchase_car(self)

    def get_agent_month(self):
        self.month = self.model.month

    def step(self):
        self.get_agent_month()
        self.check_health_status()
        self.check_inovator_status()
        self.generate_accident()
        self.generate_offense()
        self.generate_CO2()
        income = self.update_savings()
        self.calculate_welfare(income)
        self.change_car()
