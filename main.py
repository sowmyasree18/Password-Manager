from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password_entered = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password_entered
        }
    }

    if len(password_entered) == 0 or len(website) == 0 or len(email) <= 10:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            email_entry.delete(0, END)
            email_entry.insert(0, '@gmail.com')


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().title()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="ERROR", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exits.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", font=("Arial", 15))
website_label.grid(column=0, row=1)
Email_label = Label(text="Email/Username:", font=("Arial", 15))
Email_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=("Arial", 15))
password_label.grid(column=0, row=3)

# Entry
website_entry = Entry(width=21, font=("Arial", 15))
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=35, font=("Arial", 15))
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, '@gmail.com')

password_entry = Entry(width=21, font=("Arial", 15))
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(width=13, text="Search", font=("Arial", 13), command=find_password)
search_button.grid(row=1, column=2)

generate_password_button = Button(width=15, text="Generate Password", font=("Arial", 13), command=generate_password)
generate_password_button.grid(column=2, row=3, columnspan=1)

add_button = Button(text="Add", width=36, font=("Arial", 15), command=save)
add_button.grid(row=4, column=1, columnspan=4)

window.mainloop()
