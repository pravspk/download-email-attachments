import datetime
import email
import imaplib
import mailbox
import json
import os

print('Enter your e-mail id:')
EMAIL_ACCOUNT = input()
print('Enter your password:')
PASSWORD = input()
print('Enter the e-mail subject you are looking for:')
exp_subject = input()
print('Enter a name to create new folder:')
folder_name = input() + '/'
folderPath = os.path.join('/Users/yuvaraj/Desktop/', folder_name)
if not os.path.isfile(folderPath) :
    os.mkdir(folderPath, 0o666)


mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.list()
mail.select('inbox')
result, data = mail.uid('search', None, "ALL") # (ALL/UNSEEN)
i = len(data[0].split())

for x in range(i):
    latest_email_uid = data[0].split()[x]
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    # result, email_data = conn.store(num,'-FLAGS','\\Seen') 
    # this might work to set flag to seen, if it doesn't already
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    subject = email_message['subject']
    

    if(subject == exp_subject):
        for part in email_message.walk():
            if part.get_content_maintype() == 'multiemail_message':
                continue
            # if email_message.get('Content-Disposition') is None:
            #    continue

            fileName = part.get_filename()
            print(fileName)
            if bool(fileName):
                filePath = os.path.join(folderPath, fileName)
                if not os.path.isfile(filePath) :
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject, uid=latest_email_uid.decode('utf-8')))