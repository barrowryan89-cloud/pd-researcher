#!/usr/bin/env python3
"""
Gmail SMTP/IMAP Client - Uses app password, no OAuth needed
"""
import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_USER = "barrowryan89@gmail.com"
GMAIL_APP_PASSWORD = "xjmqpmlofamnkkcq"  # App password provided by user

def send_email(to, subject, body, html_body=None):
    """Send email via SMTP"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = to
    
    msg.attach(MIMEText(body, 'plain'))
    if html_body:
        msg.attach(MIMEText(html_body, 'html'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to, msg.as_string())
    
    return True

def search_emails(query="ALL", limit=10):
    """Search emails via IMAP"""
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    mail.select('inbox')
    
    _, data = mail.search(None, query)
    email_ids = data[0].split()[-limit:]
    
    results = []
    for eid in email_ids:
        _, msg_data = mail.fetch(eid, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        results.append({
            'id': eid.decode(),
            'from': msg['From'],
            'subject': msg['Subject'],
            'date': msg['Date']
        })
    
    mail.close()
    mail.logout()
    return results

def get_unread_count():
    """Get count of unread emails"""
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    mail.select('inbox')
    
    _, data = mail.search(None, 'UNSEEN')
    count = len(data[0].split())
    
    mail.close()
    mail.logout()
    return count

if __name__ == "__main__":
    # Test
    print(f"Unread emails: {get_unread_count()}")
    print("\nRecent emails:")
    for email in search_emails('ALL', 3):
        print(f"  - {email['subject']} (from: {email['from']})")
