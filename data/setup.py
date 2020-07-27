import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages":['pygame','time','random','datetime'],
                     "include_files":["gamerun.py",'menu.py','tutorial.py','save.py']}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Yellow Spaceship!",
        version = "1.0.0",
        description = "Yellow Spaceship! v.1.0.0",
        options = {"build_exe": build_exe_options},
        executables = [Executable(script="Yellow Spaceship!.py", base=base,icon='favicon.ico')])
