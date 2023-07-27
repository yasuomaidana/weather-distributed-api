import os
import subprocess
import sys


def create_virtual_environment():
    # Create a virtual environment using venv
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

def check_virtual_environment():
    if not os.path.exists("venv"):
        print(f"Creating virtual environment:")
        create_virtual_environment()

def activate_virtual_environment():
    # Replace "venv" with the name of your virtual environment directory
    venv_path = "venv"

    if os.name == "nt":
        activate_cmd = f"{venv_path}\\Scripts\\activate"
    else:
        activate_cmd = f"source {venv_path}/bin/activate"

    subprocess.run(activate_cmd, shell=True, check=True)


def install_required_libraries():
    # Check if all required libraries are installed from "requirements.txt"

    with open("requirements.txt") as file:
        required_libraries = file.read().splitlines()

    for lib in required_libraries:
        try:
            if lib == "pymongo[srv]":
                lib = "pymongo"
            if lib == "PyYAML":
                lib = "yaml"
            if lib == "scikit-learn":
                lib = "sklearn"
            __import__(lib)
        except ImportError:
            print(f"Installing {lib}...")
            subprocess.run([sys.executable, "-m", "pip", "install", lib], check=True)
    file.close()