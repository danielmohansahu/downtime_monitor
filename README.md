# downtime_monitor

Python script to log the downtime of a given website.

### Usage

This could be run manually (and probably should be for debugging) but is ultimately intended to run as a background process (e.g. upstart job). To test locally (after cloning) you can run:

```bash
python3 ping.py https://SPOTTY_WEBSITE.com
```

This default execution should start adding logs to the `logs` folder every few seconds. Verify that it does this and that there are no (or few) errors printed to the console. If this operation succeeds then you can go ahead and add it as an upstart job.

Instructions for Ubuntu 18.04:

First, create a new file `downtime-monitor.service` in `/etc/systemd/system/` and populate it with the following. Be sure to fill out fields marked with dummy values.

```
[Unit]
Description=Ping website and measure resulting error codes.

[Service]
ExecStart={PATH TO CLONED REPOSITORY)/ping.py start

[Install]
WantedBy=multi-user.target
``` 

After that's done you can start the service via:

```bash
# run, but don't start up on boot
sudo systemctl start downtime-monitor.service

# set to start up on boot
sudo systemctl enable downtime-monitor.service

# check status
sudo systemctl status downtime-monitor.service

# more detailed status
sudo journalctl -u downtime-monitor.service
```
