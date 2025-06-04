import os
import sys
from modules.gui import TextEditor

if __name__ == "__main__":
    # Find the folder where this script lives:
    base_dir = os.path.dirname(os.path.abspath(__file__))    # …/PwndaApps/PwndaTxt
    modules_dir = os.path.join(base_dir, "modules")          # …/PwndaApps/PwndaTxt/modules

    # Ensure “modules” is on sys.path before importing anything under modules/
    if modules_dir not in sys.path:
        sys.path.insert(0, modules_dir)

    app = TextEditor()
    app.run()
