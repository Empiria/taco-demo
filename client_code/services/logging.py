class Logger:
    def __init__(self):
        self.content = []

    def log(self, msg):
        self.content.append(msg)

    def flush(self):
        return "\n".join(self.content)