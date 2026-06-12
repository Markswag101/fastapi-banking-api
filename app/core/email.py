import os
import traceback
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_NAME = os.getenv("APP_NAME", "FastAPI Banking API")


def send_email(to_email: str, subject: str, html_content: str):
    try:
        print(f"[Email] Sending to {to_email} | Subject: {subject}")
        print(f"[Email] API Key starts with: {SENDGRID_API_KEY[:20] if SENDGRID_API_KEY else 'NOT SET'}...")
        print(f"[Email] Sender: {SENDER_EMAIL}")
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"[Email] Status code: {response.status_code}")
    except Exception as e:
        print(f"[Email Error] Failed to send email to {to_email}: {e}")
        traceback.print_exc()


def email_welcome(full_name: str, email: str):
    subject = f"Welcome to {APP_NAME} 🎉"
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 30px; border: 1px solid #e0e0e0; border-radius: 8px;">
        <h2 style="color: #2c3e50;">Welcome, {full_name}! 👋</h2>
        <p>Your account has been successfully created on <strong>{APP_NAME}</strong>.</p>
        <p>You can now:</p>
        <ul>
            <li>Create bank accounts</li>
            <li>Make deposits and withdrawals</li>
            <li>Transfer funds securely</li>
            <li>View your transaction history</li>
        </ul>
        <p style="margin-top: 30px; color: #7f8c8d; font-size: 12px;">This is an automated message. Please do not reply.</p>
    </div>
    """
    send_email(email, subject, html)


def email_deposit(full_name: str, email: str, amount: float, account_number: str, balance: float, reference: str):
    subject = f"Deposit Successful — ₦{amount:,.2f} credited"
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 30px; border: 1px solid #e0e0e0; border-radius: 8px;">
        <h2 style="color: #27ae60;">Deposit Successful ✅</h2>
        <p>Hi <strong>{full_name}</strong>, a deposit has been made to your account.</p>
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <tr style="background: #f8f9fa;"><td style="padding: 10px; font-weight: bold;">Amount</td><td style="padding: 10px; color: #27ae60;">₦{amount:,.2f}</td></tr>
            <tr><td style="padding: 10px; font-weight: bold;">Account Number</td><td style="padding: 10px;">{account_number}</td></tr>
            <tr style="background: #f8f9fa;"><td style="padding: 10px; font-weight: bold;">New Balance</td><td style="padding: 10px;">₦{balance:,.2f}</td></tr>
            <tr><td style="padding: 10px; font-weight: bold;">Reference</td><td style="padding: 10px; font-family: monospace;">{reference}</td></tr>
        </table>
        <p style="margin-top: 30px; color: #7f8c8d; font-size: 12px;">If you did not initiate this transaction, please contact support immediately.</p>
    </div>
    """
    send_email(email, subject, html)


def email_withdrawal(full_name: str, email: str, amount: float, account_number: str, balance: float, reference: str):
    subject = f"Withdrawal Alert — ₦{amount:,.2f} debited"
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 30px; border: 1px solid #e0e0e0; border-radius: 8px;">
        <h2 style="color: #e74c3c;">Withdrawal Alert 🔔</h2>
        <p>Hi <strong>{full_name}</strong>, a withdrawal has been made from your account.</p>
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <tr style="background: #f8f9fa;"><td style="padding: 10px; font-weight: bold;">Amount</td><td style="padding: 10px; color: #e74c3c;">₦{amount:,.2f}</td></tr>
            <tr><td style="padding: 10px; font-weight: bold;">Account Number</td><td style="padding: 10px;">{account_number}</td></tr>
            <tr style="background: #f8f9fa;"><td style="padding: 10px; font-weight: bold;">Remaining Balance</td><td style="padding: 10px;">₦{balance:,.2f}</td></tr>
            <tr><td style="padding: 10px; font-weight: bold;">Reference</td><td style="padding: 10px; font-family: monospace;">{reference}</td></tr>
        </table>
        <p style="margin-top: 30px; color: #7f8c8d; font-size: 12px;">If you did not initiate this transaction, please contact support immediately.</p>
    </div>
    """
    send_email(email, subject, html)


def email_transfer_sender(full_name: str, email: str, amount: float, receiver_account: str, balance: float, reference: str):
    subject = f"Transfer Successful — ₦{amount:,.2f} sent"
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 30px; border: 1px solid #e0e0e0; border-radius: 8px;">
        <h2 style="color: #e67e22;">Transfer Sent 💸</h2>
        <p>Hi <strong>{full_name}</strong>, your transfer was successful.</p>
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <tr style="background: #f8f9fa;"><td style="padding: 10px; font-weight: bold;">Amount Sent</td><td style="padding: 10px; color: #e67e22;">₦{amount:,.2f}</td></tr>
            <tr><td style="padding: 10px; font-weight: bold;">To Account</td><td style="padding: 10px;">{receiver_account}</td></tr>
            <tr style="background: #f8f9fa;"><td style="padding: 10px; font-weight: bold;">Remaining Balance</td><td style="padding: 10px;">₦{balance:,.2f}</td></tr>
            <tr><td style="padding: 10px; font-weight: bold;">Reference</td><td style="padding: 10px; font-family: monospace;">{reference}</td></tr>
        </table>
        <p style="margin-top: 30px; color: #7f8c8d; font-size: 12px;">If you did not initiate this transaction, please contact support immediately.</p>
    </div>
    """
    send_email(email, subject, html)


def email_transfer_receiver(full_name: str, email: str, amount: float, sender_account: str, balance: float, reference: str):
    subject = f"Credit Alert — ₦{amount:,.2f} received"
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 30px; border: 1px solid #e0e0e0; border-radius: 8px;">
        <h2 style="color: #27ae60;">Credit Alert ✅</h2>
        <p>Hi <strong>{full_name}</strong>, you have received a transfer.</p>
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <tr style="background: #f8f9fa;"><td style="padding: 10px; font-weight: bold;">Amount Received</td><td style="padding: 10px; color: #27ae60;">₦{amount:,.2f}</td></tr>
            <tr><td style="padding: 10px; font-weight: bold;">From Account</td><td style="padding: 10px;">{sender_account}</td></tr>
            <tr style="background: #f8f9fa;"><td style="padding: 10px; font-weight: bold;">New Balance</td><td style="padding: 10px;">₦{balance:,.2f}</td></tr>
            <tr><td style="padding: 10px; font-weight: bold;">Reference</td><td style="padding: 10px; font-family: monospace;">{reference}</td></tr>
        </table>
        <p style="margin-top: 30px; color: #7f8c8d; font-size: 12px;">If you did not expect this transfer, please contact support.</p>
    </div>
    """
    send_email(email, subject, html)
