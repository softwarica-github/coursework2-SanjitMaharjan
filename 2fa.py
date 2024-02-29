import mysql.connector
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox, PhotoImage, font
import subprocess

# Function to generate a random username
def generate_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

# Function to generate a random password
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=12))

SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
DB_HOST = "37.187.149.30"
DB_PORT = "3306"
DB_USER = "u5266_hxP3EYoA3j"
DB_PASSWORD = "62csHC6Qk^yA=5BFtSz^9bf@"
DB_NAME = "s5266_Checker"

# Function to get sender email and password from database
def get_sender_info():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()
        select_query = "SELECT email, password FROM sender_info LIMIT 1"
        cursor.execute(select_query)
        result = cursor.fetchone()
        return result  # Return email and password as a tuple (email, password)
    except mysql.connector.Error as e:
        print(f"Error fetching sender info from database: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to insert user data into the database
import mysql.connector

def insert_or_update_user_in_db(email, username, password):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()

        # Check if email already exists
        select_query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(select_query, (email,))
        result = cursor.fetchall() 
        if len(result) > 0:
            # Email exists, update user info
            update_query = "UPDATE users SET username = %s, password = %s WHERE email = %s"
            cursor.execute(update_query, (username, password, email))
        else:
            # Email does not exist, insert new user
            insert_query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (email, username, password))
        
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Error updating user in database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def send_email(root, receiver_email, username, password, sender_email, sender_password):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Generated Username and Password"
        body = f"Username: {username}\nPassword: {password}"
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        subprocess.Popen(["python", "main.py"], shell=True)
       
    except Exception as e:
        # Show popup message indicating failure
        messagebox.showerror("Error", "Failed to send email.", parent=root)
        print(e)


# GUI setup
def generate_and_send_email():
    receiver_email = email_entry.get()
    sender_info = get_sender_info()
    if sender_info:
        sender_email, sender_password = sender_info
        username = generate_username()
        password = generate_password()
        
        # Save the generated username, password, and email to the database
        insert_or_update_user_in_db(receiver_email, username, password)
        
        # Send email with the generated username and password and show success popup
        send_email(root, receiver_email, username, password, sender_email, sender_password)
    else:
        messagebox.showerror("Error", "Failed to fetch sender information from database.", parent=root)


root = tk.Tk()
root.geometry("500x300+500+100")
root.title("Generate username and password ")
bold_font = font.Font(family="Helvetica", size=20, weight="bold")

email_label = tk.Label(root, text="Enter your Gmail address:", font=bold_font, pady=30)
email_label.pack()

email_entry = tk.Entry(root,font=bold_font )
email_entry.pack()

generate_button = tk.Button(root, text="Generate and Send Email", command=generate_and_send_email, font=bold_font)
generate_button.pack()

root.mainloop()
