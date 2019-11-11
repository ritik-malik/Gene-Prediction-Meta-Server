# lines to be changed 10, 11, 12, 15, 16
import glob
import smtplib, os, sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from HTMLParser import HTMLParser
    
attachments = glob.glob("/home/maalik/Desktop/OUTPUT_FOLDER/*")
username = 'nakli email'
password = 'nakli_passwd'
host = 'smtp.gmail.com:587' 

fromaddr = 'nakli email' # less secure app allow karna padega
toaddr  = 'bande_ka_addr'
replyto = fromaddr

msgsubject = "Yeh humara subject hoga"

htmlmsgtext = """<h2>This is my message body in HTML...WOW!!!!!</h2>
                <p>Simple html format use karenge plain text ki jagah BC</p>
                <p><strong>Here are your attachments:</strong></p><br />"""

######### isse ne nechhe ke code se koi matlab nahi hai ############

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

########################################################################

try:
    # Make text version from HTML - First convert tags that produce a line break to carriage returns
    msgtext = htmlmsgtext.replace('</br>',"\r").replace('<br />',"\r").replace('</p>',"\r")
    # Then strip all the other tags out
    msgtext = strip_tags(msgtext)

    # necessary mimey stuff
    msg = MIMEMultipart()
    msg.preamble = 'This is a multi-part message in MIME format.\n'
    msg.epilogue = ''

    body = MIMEMultipart('alternative')
    body.attach(MIMEText(msgtext))
    body.attach(MIMEText(htmlmsgtext, 'html'))
    msg.attach(body)

    if 'attachments' in globals() and len('attachments') > 0: # are there attachments?
        for filename in attachments:
            f = filename
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(f,"rb").read() )
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

    msg.add_header('From', fromaddr)
    msg.add_header('To', toaddr)
    msg.add_header('Subject', msgsubject)
    msg.add_header('Reply-To', replyto)

    # The actual email sendy bits
    server = smtplib.SMTP(host)
    server.set_debuglevel(False) # set to True for verbose output
    try:
        # gmail expect tls
        server.starttls()
        server.login(username,password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print 'Email sent'
        server.quit() # bye bye
    except:
        # if tls is set for non-tls servers you would have raised an exception, so....
        server.login(username,password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print('Email sent')
        server.quit() # sbye bye        
except:
    print ('Email NOT sent to %s successfully. %s ERR: %s %s %s ', str(toaddr), 'tete', str(sys.exc_info()[0]), str(sys.exc_info()[1]), str(sys.exc_info()[2]) )
    #just in case