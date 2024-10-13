import signal

class SignalHandler:
    def __init__(self):
        self._reset()

    def _reset(self):
        self._signaled = False
        self._orig_SIGINT_handler = None
        self._orig_SIGKILL_handler = None
        self._orig_SIGQUIT_handler = None
        self._orig_SIGTERM_handler = None
        self._initialized = False

    def __enter__(self):
        if self._initialized:
            return
        self._orig_SIGINT_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.signal)

        self._orig_SIGTERM_handler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, self.signal)

        if hasattr(signal, 'SIGKILL'):
            self._orig_SIGKILL_handler = signal.getsignal(signal.SIGKILL)
            signal.signal(signal.SIGKILL, self.signal)
        if hasattr(signal, 'SIGQUIT'):
            self._orig_SIGQUIT_handler = signal.getsignal(signal.SIGQUIT)
            signal.signal(signal.SIGQUIT, self.signal)

        self._initialized = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._initialized:
            return
        signal.signal(signal.SIGINT, self._orig_SIGINT_handler)
        signal.signal(signal.SIGTERM, self._orig_SIGTERM_handler)
        if hasattr(signal, 'SIGKILL'):
            signal.signal(signal.SIGKILL, self._orig_SIGKILL_handler)
        if hasattr(signal, 'SIGQUIT'):
            signal.signal(signal.SIGQUIT, self._orig_SIGQUIT_handler)
        self._reset()

    def signal(self, signum, frame):
        if not self._initialized:
            return
        print("Termination signaled!")
        self._signaled = True
    
    def is_signaled(self):
        return self._signaled