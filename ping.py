import time
import csv
import platform
import subprocess
import slackweb
import configparser

config = configparser.ConfigParser()

try:
    config.read('config.ini')
except FileNotFoundError:
    print("Error: 'config.ini' does not exist.")

# Set up slack notifier -- Change this to match your webhook address
slack = slackweb.Slack(
    url=f"https://hooks.slack.com/services/{config['slack']['webhook']}")

downhosts = []


def ping_ip(ip):
    # ip shadows "ip" from outer scope - PEP8
    try:
        output = subprocess.check_output(
            "ping -{} 1 {}".format(
                'n' if platform.system().lower() == "windows" else 'c', ip),
            shell=True,
            universal_newlines=True)
        if 'unreachable' in output:
            return False
        else:
            return True
    except Exception:
        # Too broad clause - PEP8 Error
        return False


while 1 == 1:
    # Set to number of seconds between checks.
    time.sleep(60)
    # Make sure to set path correctly.
    with open(config['files']['hosts']) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            host = row[0]
            ip = row[1]

            if ping_ip(ip):
                if host in downhosts:
                    # Feel free to change the username and emoji on this
                    # section, and the other slack.notify section.
                    slack.notify(text=time.strftime("%m/%d/%Y - %H:%M:%S")
                                 + " [***] " + ip + " - "
                                 + host + " appears to be back up",
                                 username=config['slack']['username'],
                                 icon_emoji=config['slack']['emoji'])
                    downhosts.remove(host)
            else:
                if host in downhosts:
                    pass
                else:
                    print("host down " + host)
                    print(downhosts)
                    message = "Host offline " + host + ip
                    slack.notify(text=time.strftime("%m/%d/%Y - %H:%M:%S")
                                 + " [***] " + ip + " - "
                                 + host + " appears down",
                                 username=config['slack']['username'],
                                 icon_emoji=config['slack']['emoji'])
                    downhosts = downhosts + [host]
