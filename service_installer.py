import win32serviceutil
import sys
import os

def install_service():
    try:
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Install the service
        win32serviceutil.InstallService(
            pythonClassString='main.LEDMonitorService',
            serviceName='LEDMonitorService',
            displayName='LED Monitor Service',
            description='Monitors CPU/GPU temperature and displays on LED device',
            exeName=sys.executable,
            startType='auto'
        )
        print("Service installed successfully")
    except Exception as e:
        print(f"Failed to install service: {e}")

def remove_service():
    try:
        win32serviceutil.RemoveService('LEDMonitorService')
        print("Service removed successfully")
    except Exception as e:
        print(f"Failed to remove service: {e}")

def start_service():
    try:
        win32serviceutil.StartService('LEDMonitorService')
        print("Service started successfully")
    except Exception as e:
        print(f"Failed to start service: {e}")

def stop_service():
    try:
        win32serviceutil.StopService('LEDMonitorService')
        print("Service stopped successfully")
    except Exception as e:
        print(f"Failed to stop service: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python service_installer.py [install|remove|start|stop]")
        sys.exit(1)
        
    action = sys.argv[1].lower()
    
    if action == "install":
        install_service()
    elif action == "remove":
        remove_service()
    elif action == "start":
        start_service()
    elif action == "stop":
        stop_service()
    else:
        print("Invalid action. Use: install, remove, start, or stop")