import smtplib

def email(error, password):

    email = 'fentwistle12@gmail.com'

    smtp_object = smtplib.SMTP('smtp.gmail.com',587)

    smtp_object.ehlo()

    smtp_object.starttls()

    smtp_object.login(email, password)

    from_address = email
    to_address = 'fentwistle12'+'@gmail.com'
    subject = 'problem with the scrape'
    message = 'problem ' + error
    msg = 'Subject: '+subject+'\n'+message

    smtp_object.sendmail(from_address,to_address,msg)

    smtp_object.quit()