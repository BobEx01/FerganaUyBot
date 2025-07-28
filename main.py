from handlers.start import start_handler
from handlers.elon_berish import elon_handler

def run_bot():
    start_handler()
    elon_handler()

if __name__ == "__main__":
    run_bot()
