class KeyboardInputCommandSource:
    def generate_command(self, prompt: str):
        print("Current prompt: " + prompt)
        keyboard_inputs = input()
        return keyboard_inputs