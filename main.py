import app
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if not is_admin():
        print("Requesting administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW( None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit()

    print("Running as administrator!")
    app.run()

if __name__ == "__main__":
    main()