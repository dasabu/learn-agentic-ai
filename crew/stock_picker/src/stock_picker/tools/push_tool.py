from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import sendgrid
from sendgrid.helpers.mail import Mail, To, Content, Email

class PushNotificationInput(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user")
    

class PushNotificationTool(BaseTool):
    name: str = "Push Notification Tool"
    description: str = "Send an email using SendGrid to the user"
    args_schema: Type[BaseModel] = PushNotificationInput
 
    def _run(self, message: str) -> str:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email('anh.leduy04@hcmut.edu.vn') # Verified sender
        to_email = To('duyanhlucas302@gmail.com') # To recipient
        subject = 'Stock Picker Decision'
        content = Content('text/plain', message)
        mail = Mail(from_email, to_email, subject, content).get()
        response = sg.client.mail.send.post(request_body=mail)
        return '{"notification": "ok"}'
    
    