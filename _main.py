import time

from GptApiInputCommandSource import GptApiInputCommandSource
# from GptApiInputCommandSource import GptApiInputCommandSource
from KeyboardInputCommandSource import KeyboardInputCommandSource
from SpecialAgentCommandExecutor import SpecialAgentCommandExecutor
from WebSocketCommandExecutor import WebSocketCommandExecutor

commandExecutor = None
commandSource = None

# TODO
# take command line arguments for
#   - starting epoch
#   - number of epochs
#   - whether to return a plan first
#   - whether to update

if __name__ == '__main__':
    print("Running")

    # commandSource = KeyboardInputCommandSource()
    commandSource = GptApiInputCommandSource()
    webSocketCommandExecutor = WebSocketCommandExecutor()
    commandExecutor = SpecialAgentCommandExecutor(webSocketCommandExecutor)

    # Get the initial status of the world
    initial_status = webSocketCommandExecutor.execute("status")

    prompt = initial_status + "\nYour task is to put some wood on the fire."

    while True:
        generatedCommand = commandSource.generate_command(prompt)
        prompt = commandExecutor.execute(generatedCommand)