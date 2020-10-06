__version__ = "0.1.3"

import plac 
from .app import Application

def main(): 
    plac.Interpreter.call(Application, prompt="Piggi> ")


