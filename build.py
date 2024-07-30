"""Script to build the NightWatch application."""

import os
import platform

import PyInstaller.__main__

PROJECT_DIR = os.getcwd()
PLATORM = platform.system().lower()
ARCHITECTURE = platform.machine().lower()
SRC_DIR = os.path.join(PROJECT_DIR, "src")
RESOURCE_DIR = os.path.join(SRC_DIR, "resources")
THEME_DIR = os.path.join(RESOURCE_DIR, "sv_ttk")
if PLATORM == "windows":
    ICON_FILE = os.path.join(RESOURCE_DIR, "icon.ico")
else:
    ICON_FILE = os.path.join(RESOURCE_DIR, "icon.png")
BIN_DIR = os.path.join(PROJECT_DIR, "bin")
DIST_DIR = os.path.join(BIN_DIR, f"{PLATORM}-{ARCHITECTURE}")
BUILD_DIR = os.path.join(BIN_DIR, f"{PLATORM}-{ARCHITECTURE}", "build")
SPEC_DIR = DIST_DIR
EXECUTABLE_NAME = f"NightWatch-{PLATORM}-{ARCHITECTURE}"


def main():
    """Main function to build the NightWatch application."""
    script_path = os.path.join(SRC_DIR, "main.py")

    PyInstaller.__main__.run(
        [
            script_path,
            "--name",
            EXECUTABLE_NAME,
            "--icon",
            ICON_FILE,
            "--distpath",
            DIST_DIR,
            "--workpath",
            BUILD_DIR,
            "--specpath",
            SPEC_DIR,
            "--add-data",
            f"{RESOURCE_DIR}:resources",
            "--add-data",
            f"{THEME_DIR}:sv_ttk",
            "--onefile",
            "--clean",
            "--noconfirm",
            "--windowed",
            "--uac-admin",
        ]
    )


if __name__ == "__main__":
    main()
