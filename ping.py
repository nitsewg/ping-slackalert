import time
import csv
import platform
import subprocess
import slackweb

# Set up slack notifier -- Change this to match your webhook address
slack = slackweb.Slack(url="https://hooks.slack.com/services/<slackwebhookaddress>")



downhosts = []


def ping_ip(ip):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
        ) == "windows" else 'c', ip), shell=True, universal_newlines=True)
        if 'unreachable' in output:
            return False
        else:
            return True
    except Exception:
        return False


while 1 == 1:
    # Set to number of seconds between checks.
    time.sleep(60)
    # Make sure to set path correctly.
    with open('/home/pi/python/monitoring/hosts.csv') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            host = row[0]
            ip = row[1]

            if ping_ip(ip):
                if host in downhosts:
                    slack.notify(text=time.strftime("%m/%d/%Y - %H:%M:%S") + " [***] " + ip + " - " + host + " appears to be back up", username="Arthur-Dent", icon_emoji=":rocket:")
                    downhosts.remove(host)
            else:
                if host in downhosts:
                    pass
                else:
                    print("host down " + host)
                    print(downhosts)
                    message = "Host offline " + host + ip
                    slack.notify(text=time.strftime("%m/%d/%Y - %H:%M:%S") + " [***] " + ip + " - " + host + " appears down", username="Arthur-Dent", icon_emoji=":rocket:")
                    downhosts = downhosts + [host]

