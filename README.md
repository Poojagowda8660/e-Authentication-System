📜 Overview:

This project implements a secure e-authentication system that uses One-Time Passwords (OTP) and QR Codes to verify user identities. It enhances security, prevents phishing attacks, and provides a seamless authentication experience.

🚀 Features:

OTP-based authentication system
QR code generation and verification
Fraud-resistant identity verification
User-friendly and secure login process
Real-time authentication alerts

🛠️ Tech Stack:

Backend: Python / Node.js (depending on your implementation)
Frontend: HTML, CSS, JavaScript
Database: MySQL / SQL
Libraries:
qrcode (for QR generation)
smtplib or APIs (for sending OTP via email/SMS)
pyotp (for OTP generation, if Python)

🏗️ How It Works:

User Login: User enters their credentials.
OTP Generation: A one-time password is generated and sent to the user's registered email or phone.
QR Code Display: A QR code containing a secure token is generated.
Verification: User either enters the OTP or scans the QR code to complete authentication.
Access Granted: On successful verification, access is provided to the system.

⚡ Getting Started:
Clone the repository:
git clone https://github.com/Poojagowda8660/e-authentication-system.git

Install required libraries:
pip install qrcode pyotp flask
Set up your database and configure the connection.

Run the server:
python app.py

🤝 Contributing:

Feel free to fork the repository, open issues, and submit pull requests! Contributions are welcome to improve this project further.



