import os
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def confirm_account(config=None):
    time_stamp = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
    user = config['user_details']['given_name']
    system = config['system']
    email_data = ("""
Date: %s
Hello %s,

Welcome to the GAUTH %s 2 Factor Auth System

-- Step 1 :: --

Please install the google authenticator application on your smart phone, available in the following locations:.

iPhone :
The application is available here:
https://itunes.apple.com/gb/app/google-authenticator/id388497605?mt=8

Android :
The application is available here:
https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en

For Blackberry handsets and for further help in installing the application please refer to the Google Support page available here:
http://support.google.com/accounts/bin/answer.py?hl=en&answer=1066447


-- Step 2 :: --

Once the application is installed please scan the attached QR CODE into the application.
Once the QR Code is scanned in, the Google authenticator application should be displaying the verification code.

Kind Regards,

THE GAUTH TEAM""" % (time_stamp, user, system))
    return email_data


def send_mail(config=None):
    mail_from = config['email']['from']
    mail_to = config['user_details']['email']
    mail_server = config['email']['mail_server']
    list_files = os.listdir(config['user_details']['home'])

    msg = MIMEMultipart()
    msg['Subject'] = ('%s - Account Activation' % (config['system']))
    msg['From'] = mail_from
    msg['To'] = mail_to

    msg.preamble = ('%s - Account Activation' % (config['system']))
    msg = MIMEText(confirm_account(config=config))

    for file_name in list_files:
        if file_name.endswith(".png"):
            image_data = open(file_name, 'rb')
            img = MIMEImage(image_data.read())
            image_data.close()
            msg.attach(img)

    s = smtplib.SMTP(mail_server)
    s.sendmail(mail_from, mail_to, msg.as_string())
    s.quit()
