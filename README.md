# sms_superbomber
Send 1000s of text messages
Heavily based on the tool in the iPwn repository for iOS

# Requirements:
 - Python
 - mechanize
 - BeautifulSoup
 - A throwaway gmail account

To install requirements:
 - easy_install mechanize BeautifulSoup

# Run:
 - git clone https://github.com/falconscript/sms_superbomber.git
 - chmod 777 sms_superbomber/super_bomb.py
 - sms_superbomber/super_bomb.py -h
 - Open sms_superbomber/super_bomb.py in an editor. Put your gmail username/pass into the hash at the start of the script. 
 - sms_superbomber/super_bomb.py -n 4151234567 -q 100 -s "" -m "Hello is your refrigerator running?"

# Tips:
Determining the phone number's carrier can be the hardest part. This can be done by typing in the target phone number into http://www.freecarrierlookup.com

Use responsibly! Don't abuse or destroy people! It can be known to freeze older phones and dramatically slow down even modern smartphones...

# Limits:
 - These texts are being sent through Gmail's system. You can only send a maximum of 200 messages per hour per Gmail.
 - I probably DO NOT recommend using your primary Gmail to send mass textspam.
 - This script will alternate through the email addresses within that hash table.

