Wordpress XMLRPC System Multicall Brute Force Exploit by 1N3
Last Updated: 20170215
https://crowdshield.com

## ABOUT: 
This is an exploit for Wordpress xmlrpc.php System Multicall function affecting the most current version of Wordpress (3.5.1). The exploit works by sending 1,000+ auth attempts per request to xmlrpc.php in order to "brute force" valid Wordpress users and will iterate through whole wordlists until a valid user response is acquired. It will then selectively acquire and display the valid username and password to login.

## USAGE: 
```
./wp-xml-brute http://target.com/xmlrpc.php passwords.txt username1 [username2] [username3]...
```

## LICENSE:
This software is free to distribute, modify and use with the condition that credit is provided to the creator (1N3@CrowdShield) and is not for commercial use.

## DONATIONS:
Donations are welcome. This will help fascilitate improved features, frequent updates and better overall support.
- [x] BTC 1Fav36btfmdrYpCAR65XjKHhxuJJwFyKum
- [x] DASH XoWYdMDGb7UZmzuLviQYtUGb5MNXSkqvXG
- [x] ETH 0x20bB09273702eaBDFbEE9809473Fd04b969a794d
- [x] LTC LQ6mPewec3xeLBYMdRP4yzeta6b9urqs2f