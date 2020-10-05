# Pig 
An illustration of reinforcement learning via the game Pig. 

## Rules
ig is a two player game played with the following rules. 

Each player maintains his or her own personal score tally. The objective of the game is to reach a score of 100. Players take turns. On each turn, a player must decide between two actions "roll" and "hold":

1. If he chooses "roll", he rolls a single 6 sided dice and adds the face value of the dice to his turn total as long as he doesn't roll 1. He can then choose to roll the dice again or "hold". 

2. If he does roll a 1, his turn ends and nothing gets added to his score. 

3. If he decides to "hold", the turn total is add to his score and his turn ends. 

## The experiment 
Can one program a computer to play Pig against a human opponent? 

One approach to programming such an AI is to use reinforcement learning. This application allows one to run a value iteration algorithm to train the policy function for the Pig AI. The algorithm is detailed in the [following paper](http://cs.gettysburg.edu/~tneller/papers/pig.zip) by Neller and Presser [1]

To run the experiment clone and build this repository from source. Then run 

```bash
# To see command options 
$ pig train -h 

$ pig train <destination file>
``` 
from the command line. The file is stored in h5py format. 

This trains the policy function the AI uses to play this game. You can then try out the AI by playing a game against it and see how you do. 

## Building the application
We use the build library `pep517` which can be installed using `pip install pep517`. 

Clone this repository and run 

```bash
$ python -m pep517.build .
``` 

from the root folder of the project directory. 

## References 
[1] The UMAP Journal 25(1) (2004), pp. 25–47