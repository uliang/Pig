__version__ = "0.0.0"

import plac 
from .app import Application

def main(): 
    plac.Interpreter.call(Application, prompt="Piggi> ")


