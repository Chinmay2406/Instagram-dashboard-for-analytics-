import subprocess
import os

# Use raw strings or double backslashes to specify paths correctly
backend_path = r"D:\cpa\instagram_dashboard_project\server.py"
frontend_path = r"D:\cpa\instagram_dashboard_project\app.py"

# Start the Flask backend
backend_process = subprocess.Popen(["python", backend_path])

# Start the Dash frontend
frontend_process = subprocess.Popen(["python", frontend_path])

# Wait for the processes to complete (or manually stop them)
try:
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    backend_process.terminate()
    frontend_process.terminate()
