import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def calculate_gst(bill_amount, gst_rate=0.18):
    return bill_amount * gst_rate

def send_email(to_email, subject, body):
    from_email = "emailcom"  
    from_password = "password"  

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Setup the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)

        # Send the email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

        print(f"Email sent successfully to {to_email}!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to send email: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.quit()

def main():
    name = input("Enter your name: ")
    email = input("Enter your email ID: ")

    products = []
    total_amount = 0

    while True:
        product_name = input("Enter product name (or 'done' to finish): ")
        if product_name.lower() == 'done':
            break
        product_price = float(input(f"Enter price for {product_name}: "))
        products.append((product_name, product_price))
        total_amount += product_price

    
    gst_amount = calculate_gst(total_amount)
    total_bill = total_amount + gst_amount

    
    current_datetime = datetime.datetime.now()
    date_str = current_datetime.strftime("%Y-%m-%d")
    time_str = current_datetime.strftime("%H:%M:%S")

    
    bill_details = f"--- Bill Details ---\n"
    bill_details += f"Name: {name}\n"
    bill_details += f"Email ID: {email}\n"
    bill_details += f"Date: {date_str}\n"
    bill_details += f"Time: {time_str}\n"
    bill_details += f"Products Purchased:\n"

    for product, price in products:
        bill_details += f"- {product}: {price:.2f}\n"

    bill_details += f"\nTotal Amount: {total_amount:.2f}\n"
    bill_details += f"GST (18%): {gst_amount:.2f}\n"
    bill_details += f"Total Bill: {total_bill:.2f}\n"
    bill_details += "---------------------"

    print(bill_details)

    send_email(email, "Your Supermarket Bill", bill_details)
    print("Bill processing completed!")


main()
