__version__ = "0.1.2"

import plac 
from .app import Application

def main(): 
    plac.Interpreter.call(Application, prompt="Piggi> ")


