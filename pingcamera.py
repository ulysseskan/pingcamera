"""ping an RTSP camera to see if it's returning images and alert if a restart is needed"""
# tested with Wyze and Wyze's RTSP firmware

import configparser
import time
import os
import signal
import datetime
import cv2
import schedule

def is_camera_streaming(url, user, passw):
    """Check if camera is streaming"""
    # Generate the RTSP URL with credentials
    rtsp_url = f"rtsp://{user}:{passw}@{url}/live"

    # Open the RTSP stream
    # pylint: disable=E1101
    cap = cv2.VideoCapture(rtsp_url)

    # Allow some time for the stream to initialize
    time.sleep(2)

    # Check if the stream is open and read the first frame
    if cap.isOpened():
        ret = cap.read()
        if ret:
            # Stream works and an image was retrieved
            return True

    # Release the stream and return False if there was an issue
    cap.release()
    return False

def check_camera_status(cam_url, c_user, c_pass):
    """Check camera status and show notification if there's an issue"""
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if is_camera_streaming(cam_url, c_user, c_pass):
        print(f"[{current_time}] Camera is streaming and returning images.")
    else:
        print(f"[{current_time}] Unable to access camera or retrieve images.")
        show_mac_notification("Camera Problem", f"{current_time}: Camera not returning images. Please check camera status and restart camera if necessary.")

def show_mac_notification(title, message):
    """Show a notification on macOS"""
    script = f'display notification "{message}" with title "{title}"'
    os.system(f"osascript -e '{script}'")

def exit_gracefully():
    """Clean up nicely if CTRL-C is pressed"""
    print("Cleaning up and exiting.")
    # Release resources
    # pylint: disable=E1101
    cv2.destroyAllWindows()
    raise SystemExit

def read_config():
    """Read and return camera configuration from config.ini"""
    config = configparser.ConfigParser()
    config.read("config.ini")
    return (
        config.get("Camera", "url"),
        config.get("Camera", "username"),
        config.get("Camera", "password"),
        int(config.get("Camera", "check_interval", fallback=1))
    )

if __name__ == "__main__":
    camera_url, username, password, check_interval = read_config()

    # Print the initial message
    print(f"Checking camera feed at {camera_url} every {check_interval} hour(s):\n")

    # Register signal handler to catch keyboard interrupts (Ctrl+C)
    signal.signal(signal.SIGINT, lambda signum, frame: exit_gracefully())

    # Check camera status on script startup
    check_camera_status(camera_url, username, password)

    # Schedule the check_camera_status function to run with the configurable interval
    schedule.every(check_interval).hours.do(check_camera_status, camera_url, username, password)

    # Run the scheduled task in an infinite loop
    while True:
        schedule.run_pending()
        time.sleep(1)
