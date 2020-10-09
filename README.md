# Pig 
An illustration of reinforcement learning via the game Pig. 

## Rules
Pig is a two player game played with the following rules. 

Each player maintains his or her own personal score tally. The objective of the game is to reach a score of 100. Players take turns. On each turn, a player must decide between two actions "roll" and "hold":

1. If he chooses "roll", he rolls a single 6 sided dice and adds the face value of the dice to his turn total as long as he doesn't roll 1. He can then choose to roll the dice again or "hold". 

2. If he does roll a 1, his turn ends and nothing gets added to his score. 

3. If he decides to "hold", the turn total is add to his score and his turn ends. 

## Playing Pig 
```
usage: pig play [-h] [-p 2] [-ai None]

Play Pig

optional arguments:
  -h, --help            show this help message and exit
  -p 2, --num-players 2
                        Numer of players. Valid values are 1 or 2
  -ai None, --ai-file None
                        File path to hdf5 file containing the policy matrix.
```

This game can be played in single player or two player mode. 

To play in two player mode (the default) type 

```bash
pig play 
```

For single player mode type 
```bash
pig play -p 1 
``` 
In single player mode, you play against the computer who has been trained with value iteration. This program comes 
preinstalled with an optimal AI Pig player. Test yourself against this AI player and see how well you do. 

If you have a policy matrix file in hdf5 format. You can pass the path to this file to the `-ai` option. The policy matrix
needs to be stored at the `'policy'` key of the hdf5 dataset as a `100 x 100 x 100` numpy matrix where at each cell, the
entry `i,j,k` is the probability of winning the game if your current score is `i`, opponent's current score is `j` 
and your turn score is `k`. 

In this way, you can customize your own AI by specifying the chances of winning from a given game state. The 
AI calculates whether to 'hold' or 'roll' by selecting the maximum of the two computations:
$$ P^{hold}_{i,j,k}= 1-P_{j,i+k,0}$$
and $$ P^{roll}_{i,j,k}=\frac 16 (1-P_{j,i,0} + P_{i,j,k+2}+\ldots+P_{i,j,k+6}) $$

It does seem difficult then to design a good policy matrix from scratch. The `pig train` command assists us by training the
policy matrix using value iteration.

## The experiment 
Can one program a computer to play Pig against a human opponent? 

One approach to programming such an AI is to use reinforcement learning. This application allows one to run a value iteration algorithm to train the policy function for the Pig AI. The algorithm is detailed in the [following paper](http://cs.gettysburg.edu/~tneller/papers/pig.zip) by Neller and Presser [1]

To run the experiment, we have provided the `pig train` command to train such policy matrix using value iteration.  
```
usage: pig train [-h] [-m 10] [-t 0.001] [-d] destination

Train Pig AI using value iteration

positional arguments:
  destination           Name of file to save training results. File will be
                        saved as .hdf5 format so file extension need not be
                        provided.

optional arguments:
  -h, --help            show this help message and exit
  -m 10, --max-iter 10  Maximum number of iterations.
  -t 0.001, --tolerence 0.001
                        Convergence threshold.
  -d, --dry-run         Perform training but do not save data.
```

So to use the command line to start the training, type 
```bash
$ pig train <destination file>
``` 
from the command line. The file is stored in h5py format. 

This trains the policy function the AI uses to play this game. To use this freshly trained policy matrix
for your games instead of the in build one, pass the path to `<destination file>` to the `-ai` option of 
the `pig play` command. 

## Building the application
We use the build library `pep517` which can be installed using `pip install pep517`. 

Clone this repository and run 

```bash
$ python -m pep517.build .
``` 

from the root folder of the project directory. 

## References 
[1] The UMAP Journal 25(1) (2004), pp. 25–47
