#! /usr/bin/python3.8

"""
# File        : sendemail.py
# Author      : Jon Evans
# Last Updated: July 9, 2020
# GitHub      : https://github.com/SoundsLikeJonny
#
# This document is a part of the j_pyutils module.
#
# SendEmail encapsulates the popular email.mime and smtplib functions into a single class for easy emailing
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pathlib
import getpass


class SendEmail():  
    """This class provides a simplified approach to sending emails from Python.

    Sending an email can be as simple as:

        message = "Hey, there!"
        new_email = SendEmail(  from_email='me@myemail.com', \
                                password=****, \
                                to_email='you@youemail.com', \
                                subject='Let's Chat!', \
                                message_body=message)
        new_email.send()

    /*---------If not sending from a gmail account, then specify the smtp host and port---------*/

    **kwargs: 
    ==========
    from_email   (str): the senders email (must be from the same SMTP server)
    password     (str): your password, as a getpass call (bypassing 2-factor authentication 
                        for Google accounts requires an app password)
    to_email     (str): the addressees email
    subject      (str): subject of the email
    message_body (str): body of the email
    attachment   (str): the file name of the desired attachment. Currently only works if in same path as the client file
    
    smtp_host (str): the email server host
    smtp_port (int): the server port
    """

    
    def __init__(self, **kwargs):

        self.from_email   = kwargs.get('from_email', '')

        # If a password is not entered on object instantiation, prompt user to enter password without saving in CLI history
        self.password     = kwargs.get('password', getpass.getpass(prompt='Enter your email password and press enter: '))
        
        self.to_email     = kwargs.get('to_email', self.from_email)
        self.subject      = kwargs.get('subject', '')
        self.message_body = kwargs.get('message_body', '')
        self.attachment   = kwargs.get('attachment', None)
        
        # Default to the Google SMTP server. Use an app passord instead to bypass 2-factor authentication
        self.smtp_host = kwargs.get('smtp_host', 'smtp.gmail.com')
        self.smtp_port = kwargs.get('smtp_port', 587)
        
        self.mime_message = self.create_mime()
        self.attach_doc(self.attachment)
    

    def __repr__(self):
        return repr(self.__dict__)


    def create_mime(self) -> MIMEMultipart:
        """Creates the MIMEMultipart object and initializes the fields for a basic email
        """

        message = MIMEMultipart()
        message['From'] = self.from_email
        message['To'] = self.to_email
        message['Subject'] = self.subject
        message.attach(MIMEText(self.message_body))

        return message


    def send(self) -> None:
        """Creates the SMTP session, attempts to login and send the message
        """
        
        smtp = smtplib.SMTP(host=self.smtp_host, port=self.smtp_port)

        try:    
            smtp.starttls()
            smtp.login(self.from_email, self.password)
            smtp.send_message(self.mime_message)
            print(f'\n\nMessage "{str(self.subject)}" sent to {str(self.to_email)}\n\n')
        finally:
            del smtp
    
    
    def attach_doc(self, file_path: str) -> None:
        """Optional attachment of a single document

        Args:
            file_path (str): File path of the document to be attached

        Returns:
            None
        """
        
        if file_path is not None:
            
            try:
                file = open(f'{str(pathlib.Path(__file__).parent.absolute())}/{file_path}', 'rb')
            except:
                print(f'Error with file: {file_path}\nTry moving the file to the same directory as the Python file')
                return None

            mime_base_obj = MIMEBase('application', 'octet-stream')
            mime_base_obj.set_payload((file).read())
            
            encoders.encode_base64(mime_base_obj)

            mime_base_obj.add_header('Content-Disposition', f'attachment; filename={file_path}')
            self.mime_message.attach(mime_base_obj)
        else:
            return None