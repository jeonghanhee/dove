import threading
from src.app import DoveApp

def main():
    app_thread = threading.Thread(target=lambda: DoveApp().run())
    app_thread.start()
    app_thread.join()

if __name__ == "__main__":
    main()