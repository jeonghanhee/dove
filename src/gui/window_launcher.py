import sys
import importlib

active_windows = {}

def open_gui(module_name: str):
    try:
        module_path = f"src.gui.{module_name}"

        if module_path in sys.modules:
            module = importlib.reload(sys.modules[module_path])
        else:
            module = importlib.import_module(module_path)

        class_name = "".join(word.capitalize() for word in module_name.split("_"))
        window_class = getattr(module, class_name)

        new_window = window_class()
        new_window.show()

        active_windows[module_name] = new_window
        return new_window

    except Exception as e:
        print(f"GUI load failed\n{e}")