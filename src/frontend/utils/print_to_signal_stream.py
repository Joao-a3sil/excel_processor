class PrintToSignalStream:
    def __init__(self, signal):
        self.signal = signal

    def write(self, message):
        if message.strip():
            self.signal.emit(message.strip())

    def flush(self):
        pass