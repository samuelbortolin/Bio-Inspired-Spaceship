# Bio Inspired Spaceship

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Project structure](#project-structure)
- [Setup](#setup)
  - [Installation](#installation)
  - [Required Python Packages](#required-python-packages)
- [Usage](#usage)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Project of Bio-Inspired Artificial Intelligence @ University of Trento.

The goal is the project is to pilot a spaceship in the [Yellow-Spaceship](https://github.com/ph3nix-cpu/Yellow-Spaceship) game using Bio-Inspired techniques.

We focused on two main algorithms, NEAT and GP, and we adapted the game in order to allow the algorithms to control the spaceship.

## Project structure

    Bio-Inspired-Spaceship
    ├── images          [folder in which are contained the images used by the game for the graphical interface]
    ├── runs            [folder in which are contained results of the runs]
    ├── videos          [folder in which are contained videos of the best individuals]
    ├── configGP        [configuration file for the GP algorithm]
    ├── configNEAT      [configuration file for the NEAT algorithm]
    ├── configRandom    [configuration file for the randomly piloted spaceship]
    ├── gp_train        [module that contains some classes used by the GP algorithm]
    ├── main            [script for running the training or the best runs]
    ├── plot_utils      [module that contains utilities for plotting results]
    ├── report          [report explaining the methodologies used and the results obtained]
    ├── requirements    [requirements file]
    ├── run_game        [module that contains the game]
    └── utils           [module that contains utils for training individuals, storing and reading best individuals]


## Setup

### Installation

This repository can be cloned using the command:

```bash
    git clone https://github.com/samuelbortolin/Bio-Inspired-Spaceship.git
```


### Required Python Packages

Required Python packages can be installed using the command:

```bash
    pip install -r requirements.txt
```


## Usage

The script can be run using the following commands:

* In order to launch the NEAT algorithm and find the best NN for piloting the spaceship based on `configGP.txt`:
```bash
    python3 main.py --neat
```

* In order to launch the GP algorithm and find the best program for piloting the spaceship based on `configNEAT.txt`:
```bash
    python3 main.py --gp
```

* In order to load the best results obtained using the NEAT algorithm:
```bash
    python3 main.py --run_best_neat
```

* In order to load the best results obtained using the GP algorithm:
```bash
    python3 main.py --run_best_gp
```

* The default without any arguments or with the argument `--human` will execute a game instance that should be piloted.

* With the argument `--random` will execute a randomly piloted spaceship based on `configRandom.txt`.
