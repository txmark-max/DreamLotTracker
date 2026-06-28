from dreamlottracker.database.init_db import init_database
from dreamlottracker.app import DreamLotApplication


init_database()
DreamLotApplication().run()
