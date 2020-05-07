import sys
import signal

def listen_signals():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def signal_handler(signum, frame):
    if signum == signal.SIGINT or signum == signal.SIGTERM:
        sys.exit('\nexit')
