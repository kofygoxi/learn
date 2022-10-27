import os
import dotenv
import boto3
import botocore
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_by_SDK(SUBJECT, BODY_TEXT, BODY_HTML):
    session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
    client = session.client(
        'ses',
        region_name=os.getenv("AWS_REGION")
    )
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    os.getenv('SES.RECIPIENT'),
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': SUBJECT,
                },
            },
            Source=os.getenv('SES.SENDER'),
            ConfigurationSetName=os.getenv('SES.CONFIGURATION_SET'),
        )
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        
def send_by_SMTP(SUBJECT, BODY_TEXT, BODY_HTML):
    receiver_email = os.getenv('SES.RECIPIENT')
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(os.getenv('SES.SERVER'), 465, context=context) as server:
        server.login(os.getenv('SES.USER'), os.getenv('SES.PASSWORD'))
        email_content = MIMEMultipart("alternative")
        email_content["From"] = os.getenv('SES.SENDER')
        email_content["Subject"] = SUBJECT
        email_content.attach(MIMEText(BODY_HTML, "html"))
        email_content["To"] = receiver_email
        # add header to identify the configuration set
        email_content.add_header("X-SES-CONFIGURATION-SET", os.getenv('SES.CONFIGURATION_SET'))
        server.sendmail(os.getenv('SES.SENDER'), receiver_email, email_content.as_string())

if __name__ == "__main__":
    dotenv.load_dotenv(".dotenv")
    
    SUBJECT = "Amazon SES Test (SDK for Python)"
    BODY_TEXT = "Amazon SES Test (Python)\r\nThis email was sent with Amazon SES using the AWS SDK for Python (Boto)."
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK for Python)</h1>
    <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
    """
    
    #send_by_SDK(SUBJECT, BODY_TEXT, BODY_HTML)
    send_by_SMTP(SUBJECT, BODY_TEXT, BODY_HTML)