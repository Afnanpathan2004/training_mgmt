import subprocess
import webbrowser
import os
import sys
import time

# Path to your Django project directory
project_dir = r"C:\Users\shg187514\OneDrive - TATA MOTORS LTD\Python Projects\TrainingMgmt\skilledge-main\skilledge-main\training_mgmt"

# Activate virtual environment if needed
venv_activate = os.path.join(project_dir, "venv", "Scripts", "activate_this.py")
if os.path.exists(venv_activate):
    exec(open(venv_activate).read(), dict(__file__=venv_activate))

# Change working directory to project
os.chdir(project_dir)

# Start Django server in a subprocess
# Use 0.0.0.0:8000 if you want to access from other devices
server = subprocess.Popen([sys.executable, "manage.py", "runserver"], shell=False)

# Wait a moment to let the server start
time.sleep(2)

# Open the browser
webbrowser.open("http://127.0.0.1:8000/")

# Wait for the server process to finish
try:
    server.wait()
except KeyboardInterrupt:
    server.terminate()