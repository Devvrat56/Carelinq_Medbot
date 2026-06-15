class ModelRouter:
    def __init__(self):
        self.models = ["Groq", "OpenAI", "LocalLLM"]
        self.current_index = 0

    def get_model(self):
        return self.models[self.current_index]

    def report_failure(self):
        self.current_index += 1
        if self.current_index >= len(self.models):
            raise Exception("All models have failed.")
        return self.get_model()
