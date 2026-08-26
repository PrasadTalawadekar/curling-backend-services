import subprocess
import time
import os
import sys

def install_requirements():
    print("[+] Checking requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"])

def main():
    install_requirements()
    
    # Import pyngrok AFTER ensuring it's installed
    from pyngrok import ngrok, conf

    # 1. Start Uvicorn backend in the background
    print("\n[+] Starting FastAPI (Uvicorn) on port 8090...")
    uvicorn_process = subprocess.Popen("start cmd /c \"python -m uvicorn main:app --host 0.0.0.0 --port 8090 --reload\"", shell=True)
    time.sleep(3) # Wait for it to boot

    # 2. Configure Ngrok
    print("[+] Configuring Ngrok with Static Domain...")
    NGROK_AUTH_TOKEN = "3Fw0q4Dl2559rJsRB5Nz7kraUT5_653unKLvxp8dwkKvukbVm"
    STATIC_DOMAIN = "puzzling-wafer-posing.ngrok-free.dev"
    
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    
    try:
        # 3. Start Ngrok tunnel
        public_url = ngrok.connect(8090, domain=STATIC_DOMAIN).public_url
        print("\n=======================================================")
        print(f" SUCCESS! Your Permanent Backend is Live at: {public_url}")
        print(" The Unity Editor and Mobile builds are permanently hardcoded.")
        print(" You can now press PLAY or BUILD without worrying about URLs!")
        print(" (Keep this window open until you are done playing)")
        print("=======================================================\n")
        
        # Keep process alive until user cancels
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[+] Shutting down...")
            ngrok.kill()
    except Exception as e:
        print(f"\n[-] Failed to start Ngrok tunnel: {e}")
        print("Did you claim the static domain in your Ngrok dashboard?")

if __name__ == "__main__":
    main()
