from email.message import EmailMessage
import ssl
import smtplib

reciever = "coding-challenges@sprinterhealth.com"


def send_alert(clinician_id, email, password):

    print("Sent")
    global reciever
    
    subject = "Alert for Clinician Id: "+clinician_id
    body = "Clinician ID: " +clinician_id+ " is missing."

    em = EmailMessage()
    em['From'] = email
    em['To'] = reciever
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email, password)
        smtp.sendmail(email, reciever, em.as_string())
        
    return(True)
        