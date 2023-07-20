## tl;dr
Pings an RTSP camera to see if it's returning images.  If it isn't, displays a macOS notification.

## About
Tested with Wyze camera with RTSP firmware.  Should work fine with other RTSP cameras as long as you
configure the ini file with your camera's username and password.

<!-- GETTING STARTED -->
## Getting Started

1. ```git clone https://github.com/ulysseskan/pingcamera.git```
2. ```cd pingcamera```
3. ```mv config.ini.sample config.ini && vi config.ini``` # enter your camera's IP, username, password
4. ```python3 pingcamera.py```

By default, it pings once per hour as long as the script is running.  You can modify the interval by
updating the schedule line near the bottom of pingcamera.py.

### Prerequisites

You need a copy of Python 3.  I only tested this with Python 3.10.  One way to install Python 3 is as follows:

1. Install [Brew](https://brew.sh).
2. ```brew install python3```
3. Ensure Brew's executable bin directory is in your PATH variable, for example:<br>
```echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile```

## Known Bugs

- [ ] None known.

## Potential Improvements

- [ ] Give instructions on how to setup to run at boot
- [ ] Allow check interval to be changed in config.ini

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<!-- CONTACT -->
## Contact

Project Link: [https://github.com/ulysseskan/pingcamera](https://github.com/ulysseskan/pingcamera)
