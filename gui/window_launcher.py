import subprocess
import sys
from pathlib import Path

def open_gui(module_name: str):
    project_root = Path(__file__).parent.parent.resolve()
    file_path = project_root / "gui" / f"{module_name}.py"

    if not file_path.exists():
        return

    try:
        subprocess.Popen([sys.executable, str(file_path)], cwd=str(project_root))
    except Exception as e:
        print(e)