## tl;dr
Pings an RTSP camera to see if it's returning images.  If it isn't, displays a macOS notification.

## About
Tested with Wyze camera with RTSP firmware.  Other cameras untested, but they probably work fine?  Let me know if it works for you.

<!-- GETTING STARTED -->
## Getting Started

1. ```git clone https://github.com/ulysseskan/pingcamera.git```
2. ```cd pingcamera```
3. ```pip3 install -r requirements.txt```
4. ```mv config.ini.sample config.ini && vi config.ini``` # enter your camera's IP, username, password
5. ```python3 pingcamera.py```

By default, it pings once per hour as long as the script is running.  You can modify the interval by
updating check_interval in config.ini.

### Prerequisites

You need a copy of Python 3.  I only tested this with Python 3.10.  One way to install Python 3 is as follows:

1. Install [Brew](https://brew.sh).
2. ```brew install python3```
3. Ensure Brew's executable bin directory is in your PATH variable, for example:<br>
```echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile```

## Running at Startup on macOS

You can either go the launchd route (or use Lingon/LaunchControl), or you can do what I did and do
it via Automator:

1. Open Automator.  Create a new App with the action Run AppleScript.
2. Paste in code similar to the following, then drag the new App to your Login Items.

```
on run
	tell application "Terminal"
		do script "cd /Users/username/pingcamera; /usr/local/bin/python3 /Users/username/pingcamera/pingcamera.py; exit"
		activate
	end tell
end run
```

This opens a Terminal with the script running.  If you want it running silently in the
background instead, use Run Shell Script instead and make it a background process (`&`` at the end
of the command).

## Known Bugs

- [ ] None known.

## Potential Improvements

- [x] Allow check interval to be changed in config.ini
- [x] Include time of check in output (and in notification?)
- [x] Give instructions on how to setup to run at boot

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<!-- CONTACT -->
## Contact

Project Link: [https://github.com/ulysseskan/pingcamera](https://github.com/ulysseskan/pingcamera)
