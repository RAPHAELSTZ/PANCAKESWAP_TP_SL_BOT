NAME = 'C:/Users/Ragnar_lothbroke/Desktop/Bureau/DEV/BOTS/uberbot/py2exe.py'
VERSION = '0.0.9'
DESCRIPTION = """teeest
"""
FILENAME = 'C:/Users/Ragnar_lothbroke/Desktop/Bureau/DEV/BOTS/uberbot/py2exe.py'

from cx_Freeze import setup, Executable
setup(name = NAME, version = VERSION, description = DESCRIPTION, executables = [Executable(FILENAME)])