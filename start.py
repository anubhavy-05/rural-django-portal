import subprocess
import sys
import time

print("🚀 Starting Smart Rural Economy System...")

try:
    # 1. Start ML Backend (FastAPI on Port 8000)
    print("-> Starting ML Backend (FastAPI)...")
    backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"])
    
    # Thoda wait karte hain taaki backend pehle aaram se start ho jaye
    time.sleep(3) 

    # 2. Start Dashboard (Django on Port 8001)
    print("-> Starting Dashboard (Django)...")
    frontend = subprocess.Popen([sys.executable, "manage.py", "runserver", "8001"])

    # Dono servers ko chalte rehne do
    backend.wait()
    frontend.wait()

except KeyboardInterrupt:
    print("\n🛑 Shutting down both servers...")
    backend.terminate()
    frontend.terminate()
    print("✅ System safely offline.")