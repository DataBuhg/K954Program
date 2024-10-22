import os
from cx_Freeze import setup, Executable

# Set the output directory to your Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

build_exe_options = {
    "packages": ["os", "tkinter", "csv", "re"],  # Add required packages
}

# Setup cx_Freeze
setup(
    name="DogTrainingApp",
    version="1.0",
    description="Dog Training Services Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", target_name="DogTrainingApp", base=None)],  # target_name for the app
)
