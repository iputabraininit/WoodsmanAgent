import argparse
import time
import csv
from datetime import datetime

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from GptApiInputCommandSource import GptApiInputCommandSource
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
    parser = argparse.ArgumentParser(description="System to run a problem solving agent")
    parser.add_argument('-e', '--epochs', type=int, dest='epochs', default=1,
                        help='The number of runs to execute the simulation')
    parser.add_argument('-s', '--start', type=int, dest='start', default=0,
                        help='The starting epoch, in case of wanting to rerun from a different epoch')

    args = parser.parse_args()

    colorama_init()

    epochs = args.epochs
    print(f"{Fore.GREEN} Running for {epochs} epochs {Style.RESET_ALL}")

    # commandSource = KeyboardInputCommandSource()
    commandSource = GptApiInputCommandSource()
    webSocketCommandExecutor = WebSocketCommandExecutor()
    commandExecutor = SpecialAgentCommandExecutor(webSocketCommandExecutor)

    global_start_time = time.time()
    now = datetime.now().isoformat().replace(":", "_")


    with open('woodman-%s.csv' % now, 'w', newline='') as csvfile:
        fieldnames = ['epoch', 'start', 'commands', 'errors']
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()

        improved_prompt = ""

        for i in range(args.start, args.start + epochs):
            epoch_start_time = time.time()
            print(f"{Fore.MAGENTA} Epoch: {i} {Style.RESET_ALL}")
            commandSource.reset()
            initial_status = webSocketCommandExecutor.execute("status")

            commands = 0
            errors = 0

            prompt = initial_status + ("\nYour task is to put some wood on the fire.\n"
                                       + improved_prompt
                                       + "First output your full plan, then call a function. After that, only call functions, do not return text other than the full plan.")
            # prompt = initial_status + ("\nYour task is to put some wood on the fire.")

            webSocketCommandExecutor.execute(f"reset {i}")

            while prompt != 'quit':
                generatedCommand = commandSource.generate_command(prompt)
                prompt = commandExecutor.execute(generatedCommand)

                commands += 1
                if prompt.startswith("[Error]"):
                    errors += 1

            improved_prompt = commandSource.generate_command("Please provide an update to the prompt instructions to make you better at solving the problem in future iterations. "
                                                             "Don't provide a plan, just provide a better prompt in how to deal with the simulation logic. "
                                                             "Provide only the improved prompt, not the rationale.")
            print("Improved prompt:\n" + improved_prompt)
            print(f"\n\nEpoch {i} - completed in {commands} commands, with {errors} errors\n\n")
            writer.writerow({'epoch' : i, 'start': epoch_start_time, 'commands' : commands, 'errors' : errors})