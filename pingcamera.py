"""ping an RTSP camera to see if it's returning images and alert if a restart is needed"""
# tested with Wyze and Wyze's RTSP firmware

import configparser
import time
import os
import signal
import cv2
import schedule

def is_camera_streaming(url, username, password):
    """Check if camera is streaming"""
    # Generate the RTSP URL with credentials
    rtsp_url = f"rtsp://{username}:{password}@{url}/live"

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

def check_camera_status():
    """Read configuration file and check camera status"""
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Extract RTSP credentials from the config file
    camera_url = config.get("Camera", "url")
    username = config.get("Camera", "username")
    password = config.get("Camera", "password")

    if is_camera_streaming(camera_url, username, password):
        print("Camera is streaming and returning images.")
    else:
        print("Unable to access the camera or retrieve images.")
        show_mac_notification("Camera Problem", "The camera is not returning images. \
                              Please check camera status and restart camera if necessary.")

def show_mac_notification(title, message):
    """Show a notification every 1 hour on macOS"""
    script = f'display notification "{message}" with title "{title}"'
    os.system(f"osascript -e '{script}'")

def exit_gracefully():
    """Clean up nicely if CTRL-C is pressed"""
    print("Cleaning up and exiting.")
    # Release any resources or perform cleanup here, if needed.
    # For example, you can close open file handles or release the camera stream.
    # pylint: disable=E1101
    cv2.destroyAllWindows()
    raise SystemExit

if __name__ == "__main__":
    # Register a signal handler to catch keyboard interrupts (Ctrl+C)
    signal.signal(signal.SIGINT, lambda signum, frame: exit_gracefully())

    # Check the camera status immediately on script startup
    check_camera_status()

    # Schedule the check_camera_status function to run every 1 hour
    schedule.every(1).hour.do(check_camera_status)

    # Run the scheduled tasks in an infinite loop
    while True:
        schedule.run_pending()
        time.sleep(1)
