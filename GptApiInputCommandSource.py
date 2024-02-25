import json
import os

from openai import OpenAI
from colorama import Fore
from colorama import Style

GPT_VERSION = "gpt-4-0125-preview"

class GptApiInputCommandSource:

    messageList = [{"role": "system", "content": "You are a problem solving agent in a simulation of a woodland clearning. "
                                                 "Each tool call is being executed in series by the environment, and the results supplied back. "
                                                 "Therefore you must only ever call one function at a time, no parallel function calling."}]
    tools = [
        {
            "type" : "function",
            "function" : {
                "name" : "moveto",
                "description" : "move to a particular location so it can be picked up or interacted with, you will be told when you have arrived.",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "destination" : {
                            "type" : "string",
                            "description" : "the named destination in the simulation to move to"
                        }
                    },
                    "required" : ["destination"]
                }
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "pickup",
                "description" : "pick up a named target object to carry or use",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "target" : {
                            "type" : "string",
                            "description" : "the name of the target object to pick up"
                        }
                    },
                    "required" : ["target"]
                }
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "status",
                "description" : "get the status of the world, what objects are around, what you are holding"
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "drop",
                "description" : "drop a target object that's being carried",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "target" : {
                            "type" : "string",
                            "description" : "the name of a target object that's being carried"
                        }
                    },
                    "required" : ["target"]
                }
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "use",
                "description" : "use a held object on a target object",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "held_object" : {
                            "type" : "string",
                            "description" : "the name of a held object to use"
                        },
                        "target_object" : {
                            "type" : "string",
                            "description" : "the name of target object to use the held object on"
                        }
                    },
                    "required" : ["held_object", "target_object"]
                }
            }
        },

        {
            "type" : "function",
            "function" : {
                "name" : "quit",
                "description": "request the agent be shut down when all tasks have been completed"
            }
        }
    ]

    def __init__(self):
        # NOTE - you'll have to have set up an OPENAI_API_KEY first, for the next line to pick it up
        self.client = OpenAI()

    def generate_command(self, promptOrFunctionResponse: str):
        # NOTE - hacky setup - we need to check if the previous call was a function, and create a tool call
        #  response with the id

        if len(self.messageList) <= 1:
            print("\n\nCalling GPT API with initial prompt '", promptOrFunctionResponse, "'")
            self.messageList.append({"role": "user", "content": promptOrFunctionResponse})
        else:
            print("\n\nCalling GPT API with response from simulation '", promptOrFunctionResponse, "'", sep="")
            previous_function_call = self.messageList[-1].tool_calls[0]
            self.messageList.append({"role" : "tool",
                                     "tool_call_id": previous_function_call.id,
                                     "name" : previous_function_call.function.name,
                                     "content": promptOrFunctionResponse})

        chat_completion = self.client.chat.completions.create(messages=self.messageList, model=GPT_VERSION, tools=self.tools)

        print("Response from GPT:")
        print(chat_completion.choices[0].message)

        generated_message = chat_completion.choices[0].message
        # XXX - if this has multiple tools, then this fails as we only deal with the 0th one
        self.messageList.append(generated_message)

        if generated_message.tool_calls is not None:
            if len(generated_message.tool_calls) > 1:
                print(f"{Fore.RED} WARNING: more than one tool call detected, slicing {Style.RESET_ALL}")
                generated_message.tool_calls = generated_message.tool_calls[:1]

            function = generated_message.tool_calls[0].function
            function_name = function.name
            print("Response from GPT API (tool call):", function_name)

            command_string = function_name
            if function.arguments:
                argument_json = json.loads(function.arguments)
                for key, value in argument_json.items():
                    command_string += " "
                    command_string += value

            return command_string
        else:
            print("Response from GPT API (text message) ", generated_message.content)
            return generated_message.content

    def reset(self):
        self.messageList.clear()
