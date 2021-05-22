# Pacman programming project

Below are the explanations given in the Introduction to Artificial Intelligence course taught by Professor Gilles Louppe during the 2020-2021 year (https://github.com/glouppe/info8006-introduction-to-ai).

---

The goal of this programming project is to implement intelligent agents for the game of Pacman. The project is divided into three parts:
- [**Project I**]: you have to implement a Search agent for eating all the food dots as quickly as possible.
- [**Project II**]: you have to implement a Minimax agent for eating all the food dots as quickly as possible, while avoiding the ghost enemies that are chasing you.
- [**Project III**]: you have to implement a Bayes filter for tracking all the non-visible ghosts' positions.

## Table of contents

- [Installation](#installation)
    * [Setup](#setup)
    * [Usage](#usage)
- [Instructions](#instructions)
- [FAQ](#faq)
    * [Game score](#score)
    * [API](#api)
    * [Illegal moves](#illegal-moves)
	* [Questions about the projects](#questions-about-the-projects)
- [Credits](#credits)

---

## Installation

> The instructions below have been tested under Windows, Linux and MacOS.

We recommend to install a Python (3) environment using the `conda` package manager. The easiest way is to install [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

You will also need a code editor that supports Python. If you don't already have one, here are a few you might consider : [Sublime Text](https://www.sublimetext.com/), [VS Code](https://code.visualstudio.com/), [Atom](https://atom.io/), [Vim](https://www.vim.org/), ...

Once Miniconda is installed, open the Anaconda prompt (Windows) or a terminal (Linux/MacOS).

### Setup

(Linux) Create a `pacman` environment and activate it:
```bash
conda create --name pacman python=3.6
conda activate pacman
```

(MacOS) Create a `pacman` environment and activate it:
```bash
conda create --name pacman python=3.6.6
conda activate pacman
```

(Windows) Create a `pacman` environment and activate it:
```bash
conda create --name pacman python=3.6
conda activate pacman
```

From now, it is assumed that `pacman` is activated.

Dependencies should be installed through `conda`:
```bash
conda install numpy
```

### Usage

Start the game with a Pacman agent controlled by the keyboard (keys `j`, `l`, `i`, `k` or arrow keys):
```bash
python run.py
```

**Options**:

`--agentfile`: Start the game with a Pacman agent following a user-defined control policy:
```bash
python run.py  --agentfile randomagent.py
```

`--ghostagent`: Start the game with a ghost agent (either `dumbyd`, `greedy` or `smarty`):
```bash
python run.py  --ghostagent=greedy
```

`--silentdisplay`: Disable the graphical user interface:
```bash
python run.py --silentdisplay
```

`--layout`: Start the game with a user-specifed layout for the maze (see the `/pacman_module/layouts/` folder):
```bash
python run.py --layout medium
```

`--ghostagent`: Start the game with a user-specifed ghost agent (see [**project II**](https://github.com/glouppe/info8006-introduction-to-ai/tree/master/projects/project2)):
```bash
python run.py --ghostagent greedy
```

`-h`: For further details, check the command-line help section:
```bash
python run.py -h
```

---

## Instructions

For each part of the project, you must provide the following deliverables:

- The source code of your Pacman agent(s).
- A report in PDF format. A template will be provided for each part of the project in order to set the structure and page layout of the report. This template must be completed without any modification.

The three parts of the project must be carried out in groups of maximum 2 students (with the same group across all parts).

Your deliverables must be submitted as a *tar.gz* archive on the [Montefiore submission platform](https://submit.montefiore.ulg.ac.be/teacher/courseDetails/INFO8006/).

We tolerate only **one delay of maximum 24 hours**. For example, if you submit your first part late, no more delay will be allowed for the two other parts. In case of *more than one delay*, the concerned parts will receive a *0/20* grade.


---

## FAQ

### Game score

The score function of the game is computed as follows:

`score = -#time steps + 10*#number of eaten food dots - 5*#number of eaten capsules + 200*#number of eaten ghost + (-500 if #losing end) + (500 if #winning end)`.

We ask you to implement an agent that wins the game while maximizing its score.

Note that you should ask yourself if this score function satisfies all the properties of the search algorithms you will implement. If not, you are free to modify it as long as the optimal solutions remain the same.

### API

You must implement your agent as a `PacmanAgent` class, following the template of `pacmanagent.py`.
The core of your algorithm should be implemented or called within the `get_action` method. This method  receives the current state `s` of the game and should return the action to take.

Useful methods of the state are specified below:

 - ```s.generatePacmanSuccessors()``` : Returns a list of pairs of successor states and moves given the current state ```s``` for the pacman agent.
    * This method **must** be called for any node expansion for pacman agent.
 - ```s.generateGhostSuccessors(agentIndex)``` : Returns a list of pairs of successor states and moves given the current state ```s``` for the ghost agent indexed by ```agentIndex>0```.
    * This method **must** be called for any node expansion for ghost agent.
 - ```s.getLegalActions(agentIndex)``` : Returns a list of legal moves given the state ```s``` and the agent indexed by ```agentIndex```. 0 is always the Pacman agent.
 - ```s.getPacmanPosition()``` : Returns the Pacman position in a ```(x,y)``` pair.
 - ```s.getScore()``` : Returns the total score of a state (as defined above).
 - ```s.getFood()``` : Returns a boolean matrix which gives the position of all food dots.
 - ```s.getWalls()``` : Returns a boolean matrix which gives the position of all walls.
 - ```s.getGhostPosition(agentIndex)``` : Returns the position of the ghost agent indexed by ```agentIndex>0```.
 - ```s.getGhostDirection(agentIndex)``` : Returns the direction of the ghost agent indexed by ```agentIndex>0```.
 - ```s.getCapsules()``` : Returns a list of positions of the remaining capsules in the maze.
 - ```s.isWin()``` : Returns True if the state is in a *winning end*.
 - ```s.isLose()``` : Returns True if the state is in a *losing end*.

Implementation examples are provided in `humanagent.py` and `randomagent.py`.

### Illegal moves

You need to ensure that your agent always returns a legal move. If it is not the case, the previous move is repeated if it is still legal. Otherwise, it remains in the same location.

### Questions about the projects

You may send your questions at **info8006@montefiore.ulg.ac.be**. 

---

## Credits

The programming projects are adapted from [CS188 (UC Berkeley)](http://ai.berkeley.edu/project_overview.html).
