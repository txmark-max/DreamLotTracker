from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent
SRC = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC))

from dreamlottracker.app import DreamLotApplication

DreamLotApplication().run()
