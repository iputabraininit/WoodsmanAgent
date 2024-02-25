## Woodmans Agent

### Introduction
A very simple python project to demonstrate zero-shot, action-based problem solving by an LLM.

This attempts to connect to a simulator on localhost port `50102`.

Simulator code here: [Kettle Simulator](https://github.com/iputabraininit/Woodsman/Simulator.git).

_Note:_ This code is an attempt to demonstrate the concept of a problem solving agent and be simple to understand, it's not supposed to be production quality code.

### Setup
`pip install requirements.txt` to install the correct python libs.

Add your OpenAI API Key as an environment variable OPENAI_API_KEY

### Running 
If you don't want to run against OpenAI API, then uncomment the `KeyboardInputCommandSource` instead.
That class takes in input from the keyboard and sends it off to the CommandExecutors. So a little bit cheaper to experiment.

Run the Woodmans Simulator Godot project, which will start a websocket server on port `50102`.

Now run the `_main.py` main entry file.
