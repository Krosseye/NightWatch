"""Script to build the NightWatch application."""

import os
import platform

import PyInstaller.__main__

PROJECT_DIR = os.getcwd()
SRC_DIR = os.path.join(PROJECT_DIR, "src")
ICON_FILE = os.path.join(SRC_DIR, "resources", "icon.ico")
BIN_DIR = os.path.join(PROJECT_DIR, "bin")
DIST_DIR = os.path.join(BIN_DIR, "dist")
BUILD_DIR = os.path.join(BIN_DIR, "build")
VENV_LIB_SITE_PACKAGES = os.path.join(PROJECT_DIR, ".venv", "Lib", "site-packages")
THEME_DIR = os.path.join(VENV_LIB_SITE_PACKAGES, "sv_ttk")
EXECUTABLE_NAME = f"NightWatch-{platform.system().lower()}-{platform.machine().lower()}"


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
            BIN_DIR,
            "--add-data",
            f"{ICON_FILE};.",
            "--add-data",
            f"{THEME_DIR};sv_ttk",
            "--onefile",
            "--clean",
            "--noconfirm",
            "--windowed",
        ]
    )


if __name__ == "__main__":
    main()
