# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
#fp = open(textfile, 'rb')
# Create a text/plain message
msg = MIMEText("test")#fp.read())
#fp.close()

# me == the sender's email address
# you == the recipient's email address
you="pierre-louis.guhur@laposte.net"
me="pierre-louis.guhur@randomsets.net"
msg['Subject'] = 'Simulation finie'
msg['From'] = me
msg['To'] =  you 

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail(me, [you], msg.as_string())
s.quit()
