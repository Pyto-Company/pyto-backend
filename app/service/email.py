from fastapi_mail import FastMail, MessageSchema
import uuid
from sqlmodel import Session, select

class EmailService():

    def SendValidationEmailToUser(email: str, token: str) -> None:
        message = MessageSchema(
            subject="Email Validation",
            recipients=[email],
            body=f"Please validate your email by clicking on the following link: "
                f"http://example.com/validate-email?token={token}",
            subtype="html"
        )
        
        # Send the email (assumes FastMail is configured properly)
        fm = FastMail()
        fm.send_message(message)