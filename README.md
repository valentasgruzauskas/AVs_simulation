# Autonomous vehicle market simulation

```
Purpose

The purpose of the model is to identify the penetration of AVs to the market and show their influence on sustainability from
the perspective of environmental side, road safety and economical aspects.
```

```
State variables and scale

The simulation mainly consists of 1 type of agents. Households, which decides when to change cars.
The household has in ownership a car, which can be either traditional either autonomous.
Traditional cars generates a particular amount of CO2 emission level and are responsible for traffic offenses and accidents.
AVs, who also generates CO2 emission and traffic offenses and accidents, but on different assumptions.
The decision of car change depends on the social network and welfare score of households.
The score of households are set based on total amount of CO2 emission level generated, traffic accidents and offenses.
The welfare score is expressed in cash, which is calculated as difference between losses (taxes for CO2 emission,
fines for offenses and lost income from work due to inability to work (e.g. jail, injury or death)
and ideal income. Households decide to change car from traditional to autonomous
when the households in their common social network reach a certain welfare score.
The timestep of the simulation is set for 1 month and is simulated for a long period of time - 50 years.
```

## Install docker

```
Docker installation - https://www.docker.com/
Windows Subsystem for Linux installation - https://docs.microsoft.com/en-us/windows/wsl/install
Docker plugin for pycharm (community version) installation - https://plugins.jetbrains.com/plugin/7724-docker
Instruction for docker-compose configuration - https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#configuring-docker
```

## Installation

```bash
docker-compose build
```

## Run interface

```bash
docker-compose run --rm auto_market_sim python /home/run.py
```

## Run batch

```bash
docker-compose run --rm auto_market_sim python /home/Batchrunner.py
```

## Run result analysis

```bash
docker-compose up
```

## Port issue

```
Mesa server and jupyter notebook are running on the same port
make sure to restart docker container before running that the port would be opened
```

## Alternatively you can create virtual env and install requirements.txt

```
Create enviroment
Activate enviroment
Install packages: pip install -r requirements.txt
```

# License
```
CC BY-NC 3.0
```

# Publication access & citation
```
Saulius Baskutis, Valentas Gružauskas, Peter Leibl, Linas Obcarskas, Agent-based modelling approach for autonomous vehicle influence on countries’ welfare, Journal of Cleaner Production, 2022, 134008, ISSN 0959-6526, https://doi.org/10.1016/j.jclepro.2022.134008.

https://www.sciencedirect.com/science/article/pii/S0959652622035806
```
