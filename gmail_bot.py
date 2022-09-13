import pyttsx3
import speech_recognition as sr 
import smtplib
import imaplib
import email
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback 
import pyttsx3
def msg_alert():
    text_speech=pyttsx3.init()
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('naveenchikile123@gmail.com','hmzdearsbzdeybmz')
    mail.select('inbox')

    result, data = mail.search(None, 'All')
    mail_ids = data[0]

    id_list = mail_ids.split()   
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    result, data = mail.fetch(str(latest_email_id), '(RFC822)' )

    for response_part in data:
        if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                print()
                print('----Hello user ,you got a mail-----')
                print ('From : ' + email_from + '\n')
                print ('Subject : ' + email_subject + '\n')
                text_speech.say('Hello user ,you got a new mail')
                text_speech.say('From : ' + email_from + '\n')
                text_speech.say('Subject : ' + email_subject + '\n')
                text_speech.runAndWait()
def convert_special_char(text):
        temp=text
        special_chars = ['attherate','dot','underscore','dollar','hash','star','plus','minus',' ','dash']
        for character in special_chars:
            while(True):
                pos=temp.find(character)
                if pos == -1:
                    break
                else :
                    if character == 'attherate':
                        temp=temp.replace('attherate','@')
                    elif character == 'dot':
                        temp=temp.replace('dot','.')
                    elif character == 'underscore':
                        temp=temp.replace('underscore','_')
                    elif character == 'dollar':
                        temp=temp.replace('dollar','$')
                    elif character == 'hash':
                        temp=temp.replace('hash','#')
                    elif character == 'star':
                        temp=temp.replace('star','*')
                    elif character == 'plus':
                        temp=temp.replace('plus','+')
                    elif character == 'minus':
                        temp=temp.replace('minus','-')
                    elif character == ' ':
                        temp = temp.replace(' ', '')
                    elif character == 'dash':
                        temp=temp.replace('dash','-')
            return temp
def speech_text():
        r = sr.Recognizer()
        with sr.Microphone() as source:

            audio_data = r.record(source, duration=5)
            print("Recognizing...")
            n = r.recognize_google(audio_data)
            #print(n)
            return n
def compose():
    
    text_speech=pyttsx3.init()
    sender_address = 'naveenchikile123@gmail.com'
    sender_pass = 'hmzdearsbzdeybmz'
    text_speech.say("Please say your reciever mail id:")
    text_speech.runAndWait()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        reciever_data = r.record(source, duration=5)
    print("Recognizing...")
    receiver_address = r.recognize_google(reciever_data)
    #print(receiver_address+"@gmail.com")
    #receiver_address = 'naveenchikile@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = "naveenchikile123@gmail.com"
    text_speech.say("Please say Subject name:")
    text_speech.runAndWait()
    subject = r.record(source, duration=5)
    print("Recognizing...")
    subject_text = r.recognize_google(subject)
    print()
    message['Subject'] = subject_text   #The subject line
    #The body and the attachments for the mail
    text_speech.say("Please say mail_content:")
    text_speech.runAndWait()
    body = r.record(source, duration=5)
    print("Recognizing...")
    mail_content = r.recognize_google(body)
    print()
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, "naveenchikile123@gmail.com", text)
    session.quit()
    print('Mail Sent')
def search_person_mail():
    text_speech=pyttsx3.init()
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('naveenchikile123@gmail.com','hmzdearsbzdeybmz')
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox") # connect to inbox.
    print("Enter the person address of mail you want to read.")
    text_speech.say("Enter the person address of mail you want to read.")
    text_speech.runAndWait()
    mail_address=speech_text()
    mail_address1=convert_special_char(mail_address).lower()
    #print('"'+(mail_address1)+'"')
    mail_address2='"'+(mail_address1)+'"'
    result, data = mail.search(None, '(FROM "onlinecourses@nptel.iitm.ac.in")' )

    ids = data[0] # data is a list.
    id_list = ids.split() # ids is a space separated string
    #print(len(id_list))
    msg_list=[]
    for item in id_list[0:7]:
        result, data = mail.fetch(item, "(RFC822)") # fetch the email body (RFC822)             for the given ID

        #raw_email = data[0][0] # here's the body,
        for response_part in data:
                    if isinstance(response_part, tuple):
                            # from_bytes, not from_string
                        msg = email.message_from_bytes(response_part[1])
                        email_subject = msg['subject']
                        email_from = msg['from']
                        #print('Subject:'+email_subject)
                        msg_list.append(msg['Message-ID'])
    print(len(msg_list))
                #texttospeech("Enter the email number of mail you want to read.",file + i)
    text_speech.say("You have got "+str(len(msg_list))+"mails")
    text_speech.runAndWait()

    #msg_list.reverse()
                #texttospeech("Enter the email number of mail you want to read.",file + i)
    text_speech.say("Enter the email number of mail you want to read.")
    text_speech.runAndWait()



    n = int(speech_text())
    print(n)
    msgid = msg_list[n - 1]
    print("message id is =", msgid)
    typ, data = mail.search(None, '(HEADER Message-ID "%s")' % msgid)
    data = data[0]
    result, email_data = mail.fetch(data, '(RFC822)')
    raw_email = email_data[0][1].decode()
    raw=email_data[0][1]
    message = email.message_from_string(raw_email)
    To = message['To']
    From = message['From']
    Subject = message['Subject']
    Msg_id = message['Message-ID']
    print('From :', From)
    print('To :', To)
    print('Subject :', Subject)
    #mail_content = raw.decode('utf-8')
    print('Body :'+str(message.get_payload()[0].get_payload()))
    text_speech.say('From :', From)
    text_speech.say('Subject :', Subject)
    text_speech.say('Body :'+str(message.get_payload()[0].get_payload()))
    text_speech.runAndWait()
ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "naveenchikile123" + ORG_EMAIL 
FROM_PWD = "hmzdearsbzdeybmz" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993

def delete_email_from_gmail():
    ORG_EMAIL = "@gmail.com" 
    FROM_EMAIL = "naveenchikile123" + ORG_EMAIL 
    FROM_PWD = "hmzdearsbzdeybmz" 
    SMTP_SERVER = "imap.gmail.com" 
    SMTP_PORT = 993
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        text_speech=pyttsx3.init()
        text_speech.say("Enter the person address of mail you want to delete the mail")
        text_speech.runAndWait()
        data = mail.search(None, '(FROM "nse_alerts@nse.co.in")')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        #text_speech.say('Following are the first ten mails in your inbox')
        for i in id_list:
            data = mail.fetch(i, '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    #print('From : ' + email_from + '\n')
                    #print('Subject : ' + email_subject + '\n')
                    
            mail.store(i,"+FLAGS","\\DELETED")
        text_speech.say("mail deleted Succesfully")
        text_speech.runAndWait()
    except Exception as e:
        traceback.print_exc() 
        print(str(e))

def read_email_from_gmail():
    text_speech=pyttsx3.init()
    print("=====Welcome to Inbox======")
    text_speech.say("Welcome to Inbox Page")
    text_speech.runAndWait()
    print("please choose the option:")
    text_speech.say("please choose the option:")
    text_speech.runAndWait()
    print("Compose"+"Inbox"+"Search"+"\n"+"Delete")
    text_speech.say("If you choose Inbox ,please say Inbox:")
    text_speech.say("If you choose Search ,please say search:")
    text_speech.say("If you choose delete ,please say Delete:")
    text_speech.runAndWait()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        text = r.recognize_google(audio_data)
    if text=='inbox':
        try:
            mail = imaplib.IMAP4_SSL(SMTP_SERVER)
            mail.login(FROM_EMAIL,FROM_PWD)
            mail.select('inbox')
    
            data = mail.search(None, 'ALL')
            mail_ids = data[1]
            id_list = mail_ids[0].split()   
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])
            text_speech.say('Following are the first ten mails in your inbox')
            for (index,i) in enumerate(range(latest_email_id,first_email_id, -1)):
                data = mail.fetch(str(i), '(RFC822)' )
                for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        msg = email.message_from_string(str(arr[1],'utf-8',errors='ignore'))
                        email_subject = msg['subject']
                        email_from = msg['from']
                        print('From : ' + email_from + '\n')
                        print('Subject : ' + email_subject + '\n')
                        text_speech.say(email_from )
                        text_speech.runAndWait()
                if index>8:
                    break
            search_person_mail()
        except Exception as e:
            traceback.print_exc() 
            print(str(e))
    elif text=='search':
        search_person_mail()
    elif text=='Delete':
        delete_email_from_gmail()

#read_email_from_gmail()



#delete_email_from_gmail()


def trash_mails():
    text_speech=pyttsx3.init()
    ORG_EMAIL = "@gmail.com" 
    FROM_EMAIL = "naveenchikile123" + ORG_EMAIL 
    FROM_PWD = "hmzdearsbzdeybmz" 
    SMTP_SERVER = "imap.gmail.com" 
    SMTP_PORT = 993
    print("==========Welcome to Mail Trash Page=========")
    text_speech.say("Welcome to Mail Trash Page")
    text_speech.runAndWait()
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('"[Gmail]/Trash"')
        ext_speech=pyttsx3.init()
        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()  
        print("You have "+str(len(id_list))+ "mails in your Trash" )
        text_speech.say("You have "+str(len(id_list))+ "mails in your Trash" )
        text_speech.runAndWait()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        #text_speech.say('Following are the first ten mails in your inbox')
        for i in id_list:
            data = mail.fetch(i, '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                    text_speech.say("From : " + email_from )
                    text_speech.say("Subject : " + email_subject  )
                    text_speech.runAndWait()
            #mail.store(i,"+FLAGS","\TRASH")
    
        
    except Exception as e:
        traceback.print_exc() 
        print(str(e))

#trash_mails()
def main_page():
    text_speech=pyttsx3.init()
    print("=====Welcome to Main Page======")
    text_speech.say("Welcome to Gmail Bot")
    text_speech.runAndWait()
    print("please choose the option:")
    text_speech.say("please choose the option:")
    text_speech.runAndWait()
    print("Compose"+"\n"+"Inbox"+"\n"+"Trash"+"\n"+"Logout")
    text_speech.say("If you choose Compose ,please say compose:")
    text_speech.say("If you choose Inbox ,please say Inbox:")
    text_speech.say("If you choose trash ,please say Trash:")
    text_speech.say("If you choose logout ,please say Logout:")
    text_speech.runAndWait()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        text = r.recognize_google(audio_data)
        if text=="inbox":
            read_email_from_gmail()
        
#main_page() 
def login():
    text_speech=pyttsx3.init()
    text_speech.say("Welcome to Gmail Bot")
    text_speech.say("Enter the your mail id")
    text_speech.runAndWait()
    n=speech_text()
    m_id=convert_special_char(n).lower()
    
    text_speech=pyttsx3.init()
    text_speech.say("Enter the your password")
    text_speech.runAndWait()
    p=speech_text()
    p_id=convert_special_char(p).lower()
    
    ORG_EMAIL = "@gmail.com" 
    FROM_EMAIL = "naveenchikile123" + ORG_EMAIL 
    FROM_PWD = "hmzdearsbzdeybmz" 
    SMTP_SERVER = "imap.gmail.com" 
    SMTP_PORT = 993
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        data=mail.search(None,'ALL')
        if data[0]=='OK':
            text_speech=pyttsx3.init()
            text_speech.say("you succesfully Login,you redirected to main page")
            text_speech.runAndWait()
            main_page()
    except Exception as e:
        traceback.print_exc() 
        print(str(e))         
login()