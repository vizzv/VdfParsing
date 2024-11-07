import sys
from cx_Freeze import setup, Executable

# Replace 'pdf_parser.py' with your actual script name
script = "test.py"

# Build options
build_exe_options = {
    "packages": ["PIL", "pypdf"],  # Add other packages your script uses
}

# Setup configuration
setup(
    name="PDF Parser",
    version="0.1",
    description="A PDF parsing application",
    options={"build_exe": build_exe_options},
    executables=[Executable(script, base="Win32GUI" if sys.platform == "win32" else None)]
)
