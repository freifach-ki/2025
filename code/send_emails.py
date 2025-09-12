import pandas as pd
import smtplib
import ssl
import getpass  # For securely asking for the password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION: Please check these values ---
EXCEL_FILE = "data.xlsx"  # The name of your Excel file
EMAIL_COLUMN = "email"      # The header of the email column in your Excel file
CODE_COLUMN = "code"        # The header of the code column in your Excel file

SMTP_SERVER = "mail.bbw.ch"
SMTP_PORT = 465  # Port for SSL
SENDER_EMAIL = "pietro.rossi@bbw.ch"
# ---------------------------------------------

def send_personalized_emails():
    """
    Reads an Excel file and sends personalized emails using the data.
    """
    try:
        # Prompt for password securely in the terminal
        sender_password = getpass.getpass(f"Please enter the password for {SENDER_EMAIL}: ")
    except Exception as e:
        print(f"Could not read password: {e}")
        return

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Read data from the Excel file
        df = pd.read_excel(EXCEL_FILE)
        print(f"Successfully loaded {len(df)} rows from {EXCEL_FILE}.")
    except FileNotFoundError:
        print(f"ERROR: The file '{EXCEL_FILE}' was not found. Please make sure it is in the same directory as the script.")
        return
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return

    # Connect to the server and send emails
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            print("Connecting to the mail server...")
            server.login(SENDER_EMAIL, sender_password)
            print("Login successful. Starting to send emails...")

            # Iterate over each row in the DataFrame
            for index, row in df.iterrows():
                recipient_email = str(row[EMAIL_COLUMN])
                user_code = str(row[CODE_COLUMN])

                # --- Create the email message using MIME for correct headers and encoding ---
                # This fixes the encoding (umlauts) and "Unknown recipient" issues.
                message = MIMEMultipart()
                message["From"] = SENDER_EMAIL
                message["To"] = recipient_email
                message["Subject"] = "Ihr persönlicher Code"

                body = (
                    f"Guten Tag,\n\n"
                    f"Ihr persönlicher Code lautet: {user_code}\n\n"
                    f"Freundliche Grüsse\n\n"
                    f"Pietro Rossi"
                )
                
                # Attach the body to the email, specifying the charset is utf-8
                message.attach(MIMEText(body, "plain", "utf-8"))
                # -----------------------------------------------------------------------------

                try:
                    print(f"  -> Sending email to {recipient_email}...")
                    # Convert the message object to a string and send
                    server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
                    print(f"     Email sent successfully.")
                except Exception as e:
                    print(f"     ERROR: Failed to send email to {recipient_email}. Reason: {e}")

            print("\nProcess complete!")

    except smtplib.SMTPAuthenticationError:
        print("\nERROR: Login failed. Please check your email and password.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please remember you might need to be connected to the BBW network or VPN.")

# Run the main function
if __name__ == "__main__":
    send_personalized_emails()

