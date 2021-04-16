# ping-slackalert

Simple script to ping a list of IP addresses and alert on slack if they are down.

You will most likely need to run `pip3 install slackweb` from the command line to get this to work. 

Create a slack webhook for the desired channel using these instructions, and paste the webhook into the `slack` variable:

https://api.slack.com/messaging/webhooks

Look for any variables that need to be changed... paths, webhook urls, etc.

Set your hostnames and IPs in `hosts.csv`.

set an @reboot crontab entry using `crontab -e` like so:

`@reboot python3 /home/pi/pathtofile/ping-slackalert/ping.py`

These instructions are geared toward raspi, but this should work on just about any *nix platform.
