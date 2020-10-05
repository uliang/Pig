"""
Pig Application 

This is a cli interface allowing one to experience reinforcement learning
using the Pig dice rolling game. 

Available commands: "train", "play", "q"
"""
import plac 
import h5py
from time import time
from pathlib import Path

from wasabi import msg

from .game import game_loop
from .train import training_loop
from .game.player import Player
from .game.dice import Dice


class Application: 
    "Welcome to the Pig Application"

    commands = "train", "play", "q" 

    def __init__(self): 
        self.__doc__ += ('\nUse help to see available commands\n')

    def __missing__(self, cmd):
        "Missing command handler"
        yield "Unknown command {}. Please enter one of {}".format(
            cmd, 
            ', '.join(self.commands)
        )

    def train(self, 
        destination: (
            "Name of file to save training results." +
            " File will be saved as .hdf5 format so file extension" +
            " need not be provided.", 
            "positional", 
            None, 
            str 
        ),
        max_iter: (
            "Maximum number of iterations.", 
            "option", 
            "m", 
            int)=3, 
        tolerence: (
            "Convergence threshold.", 
            "option", 
            "t", 
            float)=0.001, 
        dry_run: (
            "Perform training but do not save data.", 
            "flag", 
            "d")=False
        ):
        "Train Pig AI using value iteration"
        msg.info("Train Pig AI")

        policy_matrix = training_loop(max_iter, tolerence)
        
        if not dry_run: 
            try: 
                filename = destination+'.hdf5' 
                with h5py.File(filename, 'w') as h5f: 
                    h5f.create_dataset('policy', data=policy_matrix)
                    msg.good(f"Policy function written to {filename}.")
            except AttributeError as e: 
                    msg.fail(f"Failed to save policy." + e)

    def play(self, 
        num_players: (
            "Numer of players. Valid values are 1 or 2", 
            "option", 
            "p", 
            int, 
            ["1", "2"])=2
    ):
        "Play Pig" 
        msg.info( "playing Pig. Press X to exit.")
        player_gen = Player.from_input()

        p1 = next(player_gen)
        msg.text( f"Player 1 {p1} created" )
        
        p2 = next(player_gen)
        msg.text( f"Player 2 {p2} created" )
        
        coin = Dice(1, 2, None)
        if coin() == 1: 
            players = [p1, p2]
            msg.text(f"{p1} goes first.")
        else:
            players = [p2, p1]
            msg.text(f"{p2} goes first.")
        
        exit_code = game_loop(*players)
        
        # if not exit_code: 
        #     raise plac.Interpreter.Exit

    def q(self): 
        "Quit application" 
        raise plac.Interpreter.Exit