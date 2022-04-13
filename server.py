from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from model import welfare_model


def social_network(G):

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": "Blue",
            "tooltip": "id: {}<br>welfare score: {}<br>car type: {}".format(
                agents[0].unique_id, agents[0].welfare_score, agents[0].car_type
            ),
        }
        for (_, agents) in G.nodes.data("agent")
    ]

    portrayal["edges"] = [
        {
            "source": source,
            "target": target,
            "color": "gray",
            "width": 1,
        }
        for (source, target) in G.edges
    ]

    return portrayal


# Create network
grid = NetworkModule(social_network, 750, 750, library="d3")

# Define graphs
Safety_chart = ChartModule([{"Label": "Total fines collected", "Color": "#FF0000"}])

Enviroment_chart = ChartModule([{"Label": "Mean CO2", "Color": "#FF0000"}])

Welfare_chart = ChartModule([{"Label": "Mean welfare", "Color": "#FF0000"}])

Savings_chart = ChartModule([{"Label": "Mean savings", "Color": "#FF0000"}])

Car_chart = ChartModule([{"Label": "Number of autonomous vehicles", "Color": "#FF0000"}])

Early_adaptors_chart = ChartModule([{"Label": "Number of early adaptors", "Color": "#FF0000"}])

Stagnators_chart = ChartModule([{"Label": "Number of stagnators", "Color": "#FF0000"}])

Productivity_chart = ChartModule(
    [
        {"Label": "Number of accident households", "Color": "#eb9534"},
        {"Label": "Number of injured households", "Color": "#fcf92d"},
        {"Label": "Number of dead households", "Color": "#2d79fc"},
    ]
)


Healthy_households_chart = ChartModule(
    [
        {"Label": "Number of healthy households", "Color": "#FF0000"}
    ]
)

model_params = {
    "Number_households": UserSettableParameter(
        "slider", "Number of households", value=1000, min_value=500, max_value=10000, step=500
    ),
    "Social_network_size": UserSettableParameter(
        "slider", "Social network size", value=8, min_value=5, max_value=12, step=1
    ),
    "early_adaptor_prob": UserSettableParameter(
        "slider", "Early adaptor propability", value=0.001, min_value=0, max_value=0.1, step=0.001
    ),
    "stagnator_prob": UserSettableParameter(
        "slider", "Stagnator propability", value=0.1, min_value=0, max_value=1, step=0.1
    ),
    "early_adaptor_lower_threshold": UserSettableParameter(
        "slider", "Early adaptor lower treshold", value=20, min_value=0, max_value=100, step=1
    ),
    "early_adaptor_upper_threshold": UserSettableParameter(
        "slider", "Early adaptor upper treshold", value=5, min_value=0, max_value=100, step=1
    ),
    "selected_country": UserSettableParameter(
        "choice", "Select country", value="Lithuania", choices=["Germany", "Lithuania"]
    ),
}

# Run the simulation using Mesa
server = ModularServer(
    welfare_model,
    [
        grid,
        Safety_chart,
        Enviroment_chart,
        Welfare_chart,
        Savings_chart,
        Car_chart,
        Early_adaptors_chart,
        Stagnators_chart,
        Productivity_chart,
        Healthy_households_chart
    ],
    "AVs market penetration",
    model_params,
)
server.port = 8888
