"""Show messages in two new console windows simultaneously."""

import subprocess
from sys import platform

if platform == "linux" or platform == "linux2":

	processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./Servidor.py'", shell=True)
	processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./consoleTM.py'", shell=True)
	processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./consoleTR.py'", shell=True)
	processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./consoleSP.py'", shell=True)
	processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./consoleLA.py'", shell=True)
	processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./consoleAC.py'", shell=True)


else:
	processes = subprocess.Popen('start thread.py', shell=True)
	processes = subprocess.Popen('start consoleTM.py', shell=True)
	processes = subprocess.Popen('start consoleTR.py', shell=True)
	processes = subprocess.Popen('start consoleSP.py', shell=True)
	processes = subprocess.Popen('start consoleLA.py', shell=True)
	processes = subprocess.Popen('start consoleAC.py', shell=True)


# wait for the windows to be closed