from installer import activate_virtual_environment, install_required_libraries, check_virtual_environment
import sys


def main(argument):
    from show_similar_weather import show_similar
    show_similar(argument, "application")


if __name__ == "__main__":
    check_virtual_environment()

    # Activate the virtual environment before installing libraries or running the main function
    activate_virtual_environment()

    # Install required libraries
    install_required_libraries()

    # Get the argument passed to the script
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        main(arg)
    else:
        print("No argument provided.")
