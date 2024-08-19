import os
import random
import smtplib
from email.message import EmailMessage
from flask import request, jsonify

class OtpValidation:
    def generate_otp(self, length=6):
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    def send_otp(self, to_mail, otp):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        from_mail = "edward.koikai@student.moringaschool.com"
        server.login(from_mail, 'rcfv zriz pcmr yrsd')

        msg = EmailMessage()
        msg["Subject"] = "OTP Verification"
        msg["From"] = from_mail
        msg["To"] = to_mail
        msg.set_content("Your OTP is: " + otp)

        server.send_message(msg)
        server.quit()

    def validate_otp(self):
        data = request.get_json()
        to_mail = data.get('email')
        input_otp = data.get('otp')

        otp = self.generate_otp()
        self.send_otp(to_mail, otp)

        if input_otp == otp:
            return jsonify({"message": "OTP verified"})
        else:
            return jsonify({"message": "Invalid OTP"})