#Installation and Run Guide

##Installing Python
MCNN-Hex was originally written to run on Python 3.7.9 so this is the recommended version to install

##Installing Packages
This program uses 2 main libraries for running the base game: Tensorflow, and numpy

They can both be installed with the command `pip install tensorflow` (at the time of writing this, the version of tensorflow is 2.3.1)

##Running the Game
The game can be viewed in two ways:
1. **<ins>The GUI:</ins>** To run the GUI, run the `hexgui.jar` file. The GUI attaches itself to the underlying CLI, but provides a better interface for users. To setup the GUI, see the setup section below. NOTE: It is recommended that the CLI be set up and run first as the GUI does not display any setup errors

2. **<ins>The CLI interface:</ins>** Running the main function in main.py (`python main.py`). This brings up a CLI version of the game. On startup, the game will not display any text.
 This is normal and required for the gui to work. Commands can be seen using the command `list_commands` <br/>
 Moves are made with the letter first, number second in a single argument: ex. `play w e6`. Note that move order is not enforced. A detailed description of the game can be found in the CLI commands section below 

## Setting up the GUI
To set up the GUI, follow these steps:
1. Go to Program -> New Program. The name can be whatever you want, but the command must be the command to run the main (`python main.py`). Working Directory should be left blank
2. Hit `Ok` to save, then load the program by going to Program -> Connect Local Program and selecting the name given in the previous step
3. If you get a blank error message, that means the CLI that powers the GUI is not correctly set up
4. Now, if it loads, you can start to play against the AI. The game plays in a standard, turn-based form, with the user going first. The AI will think for 30 seconds by default

## CLI commands
CLI commands are in the form of [command] [arguments] (for example, `play w e6`, `showboard`, and `genmove`)

play - Play a stone of a given colour in a given cell. 1st arg = color (white = w or black = b). 2nd arg = cell to play (ex. `play b a1`). Note that turn order is not enforced, and out of order turns resets the game tree for the agent

genmove - Asks the AI to generate a move given the current board, and plays it. Defaults the color to the next player, however a single argument for the color can be set. Note that turn order is not enforced, and out of order turns resets the game tree for the agent

showboard - Prints the board to console. same as print

print - same as showboard, prints board to console

name - Displays the name of the program

version - Displays the version of the program

protocol_version - Displays the version of GTP used

known_command - Displays a boolean if the command is a known command. Takes in a single argument: the command to check (ex. `known_command play`)

list_commands - Lists all the valid commands

quit - Quits the game

boardsize - sets the boardsize to a given value. **NOTE:** This operation is provided for the gtp interface to function and will not have any effect

size - Same as boardsize

clear_board - Clears the board, starting a new game

set_time - Sets the time the AI is given to run rollouts for. Takes a single argument, which is the time in seconds. (ex. `set_time 120`)

winner - Displays the winner of the board, if there is one

hexgui-analyze_commands - unknown **NOTE:** This operation is provided for the gtp interface to function and will not have any effect

##Additional Notes - Training
For training the network, more libraries are required. These include sklearn (scikit-learn 0.23.2) for splitting testing and training data, and matplotlib (matplotlib 3.3.3) for visualizing data.
Accelerating training by using tensorflow-gpu is also helpful (version 2.3.1 was used). This requires setup of a CUDA environment, including setting up CUDA and cuDNN on a computer with NVIDIA CUDA-compatible hardware. Both the 10.1 and 11.0 setups of CUDA were done to maximize compatibility
