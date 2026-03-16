import app
import ctypes
import sys
import os
import platform
import subprocess
import shutil

FILEICON_GITHUB_URL = "https://github.com/mklement0/fileicon.git"
USER_BIN = os.path.expanduser("~/bin")
FILEICON_PATH = os.path.join(USER_BIN, "fileicon")

def is_admin():
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    return True

def request_admin():
    if platform.system() == "Windows":
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

def ensure_fileicon():
    if platform.system() != "Darwin":
        return

    if shutil.which("fileicon"):
        return
    
    if os.path.exists(FILEICON_PATH):
        os.environ["PATH"] += os.pathsep + USER_BIN
        return

    print("fileicon not found. Installing...")

    brew = shutil.which("brew")
    if brew:
        try:
            subprocess.run(["brew", "install", "fileicon"], check=True)
            return
        except subprocess.CalledProcessError:
            print("brew install failed. Trying manual build...")

    try:
        os.makedirs(USER_BIN, exist_ok=True)

        subprocess.run(["git", "clone", FILEICON_GITHUB_URL], check=True)
        subprocess.run(["make"], cwd="fileicon", check=True)

        shutil.move("fileicon/fileicon", FILEICON_PATH)

        os.chmod(FILEICON_PATH, 0o755)

        os.environ["PATH"] += os.pathsep + USER_BIN

        print("fileicon installed to ~/bin")

    except Exception as e:
        print("Failed to install fileicon:", e)

def main():
    if not is_admin():
        request_admin()

    ensure_fileicon()

    print("Running application!")
    app.run()

if __name__ == "__main__":
    main()