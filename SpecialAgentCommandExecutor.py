import sys
import time

#
# A class that handles commands that the agent itself should be handling and not forwarding to the kettle.
# Commands handled:
#   quit - the agent has finished its jobs and should be shut down
#   sleep - the agent should sleep for a given amount of seconds, after which, control should be ceded back to the LLM
#
#   any other commands should be forwarded to the environment (kettle) for execution
class SpecialAgentCommandExecutor:

    def __init__(self, delegated_executor):
        self.delegatedExecutor = delegated_executor
        self.initialisationTime = time.time()

    output = None

    def execute(self, command: str):
        if command == 'quit':
            print("Quitting agent")
            sys.exit()
        else:
            print("Delegating command to woodsman: '", command, "'", sep='')
            output = self.delegatedExecutor.execute(command)

        return output
