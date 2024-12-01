# enigma2-debugger-plugin
This extension allows you to launch [debugpy](https://github.com/microsoft/debugpy) on demand from your Enigma2 user interface, or automatically on startup.

3 commands are added to the extensions menu:
- Python Debugger Setup
- Python Debugger: Start
- Python Debugger: Stop

You can also set the environment variable `ENIGMA_DEBUGPY_START_MODE` to override the config setting from the command line
- `0` don't start the debug server (default)
- `1` starts the debug server during Enigma2's startup
- `2` also pauses for a debug client to attach

This is handy if you want to ensure running enigma2 from bash always has a debug server available. e.g define an alias
```
alias e2debug="export ENIGMA_DEBUGPY_START_MODE=1;enigma2;unset ENIGMA_DEBUGPY_START_MODE"
```

### Pre-requisites
debugpy must be installed on your enigma2 machine
```
opkg install gdb python3-compile python3-xmlrpc python3-plistlib python3-ensurepip
python -m ensurepip
pip3 install debugpy
```

### On a dev machine
- In Visual Studio Code, create a _launch.json_
```
{
	"version": "0.2.0",
	"configurations": [
		{
			"name": "Attach to Enigma2",
			"type": "python",
			"request": "attach",
			"pathMappings": [
				{
					"localRoot": "${workspaceRoot}\\lib\\python",
					"remoteRoot": "/usr/lib/enigma2/python",
				}
			],
			"port": 9998,
			"host": "192.168.1.85",
			"justMyCode": false, // Need this because our code is under /usr/lib
		}
	]
}
```
- Press F5 to attach

# Known issues
The stop command removes all the hookpoints that debugpy has in the Python stack, but debugpy doesn't have a command to shut down the socket that it opens. This means subsequent starts will fail until you restart Enigma2.

Running with the debugger attached can be a little slower and less stable. Always restart Enigma2 when returning your device to normal usage.
