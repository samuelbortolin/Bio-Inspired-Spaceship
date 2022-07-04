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

Project of Bio-Inspired Artificial Intelligence @ University of Trento for piloting a spaceship in the [Yellow-Spaceship](https://github.com/ph3nix-cpu/Yellow-Spaceship) game.

## Project structure

    Bio-Inspired-Spaceship
    ├── images          [folder in which are contained the images used by the game for the graphical interface]
    ├── runs            [folder in which are contained results of the runs]
    └── src
        ├── configGP                  [configuration file for the GP algorithm]
        ├── configNEAT                [configuration file for the NEAT algorithm]
        ├── gp_train                  [module that contains some classes used by the GP algorithm]
        ├── main                      [script for running the training or the best runs]
        ├── plot_utils                [module that contains utilities for plotting results]
        ├── requirements              [requirements file]
        ├── run_game                  [module that contains the game]
        └── utils                     [module that contains utils for training individuals, storing and reading best individuals]


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

* In order to launch the NEAT algorithm and find the best NN for piloting the spaceship:
```bash
    python3 main.py --neat
```

* In order to launch the GP algorithm and find the best program for piloting the spaceship:
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
