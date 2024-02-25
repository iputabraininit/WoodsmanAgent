import websocket

import CommandPayload

class WebSocketCommandExecutor:
    def __init__(self):
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://127.0.0.1:50102")

    def execute(self, command: str):
        # print("WebSocket executor, calling woodsman:", command)

        self.ws.send(command)
        executionResult = self.ws.recv()
        # print("WebSocket executor, response:", executionResult)

        return executionResult
