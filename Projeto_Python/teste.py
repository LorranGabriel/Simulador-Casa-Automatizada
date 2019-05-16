"""Show messages in two new console windows simultaneously."""
import sys
import platform
import subprocess




processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./Servidor.py'", shell=True)
processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./consoleTM.py'", shell=True)
processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./consoleTR.py'", shell=True)
processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./consoleSP.py'", shell=True)
processes= subprocess.Popen("gnome-terminal" + " --command='python3 ./consoleLA.py'", shell=True)



# wait for the windows to be closed
