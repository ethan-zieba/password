import customtkinter as ctk
import random as rd
import json
import hashlib


def create_interface():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    global root
    root = ctk.CTk()
    root.geometry("500x280")
    root.title("Password checker")

    cond_labels_list = ["Not enough characters (min 8)", "Must contain at least 1 uppercase letter",
                        "Must contain at least 1 lowercase letter", "Must contain at least 1 number",
                        "Must contain at least 1 special character"]
    global cond_labels
    cond_labels = [ctk.CTkLabel(root, height=10, width=200, font=("Roboto", 15),
                                anchor="w", justify="left", text=cond_labels_list[i]) for i in range(5)]
    lcolumn, lrow = 0, 1
    for i in range(len(cond_labels)):
        cond_labels[i].grid(row=lrow, column=lcolumn, sticky="w", pady=3, padx=10)
        lrow += 1
    global password_entry, password_show, password_generate_button, password_save_button, checked, already_label
    password_entry = ctk.CTkEntry(root, height=60, width=350, font=("Roboto", 25), show="*")
    password_entry.grid(row=0, column=0, pady=10, padx=10)
    already_label = ctk.CTkLabel(root, height=10, width=100, pady=10, font=("Roboto", 15),
                                 text="Password already used", fg_color="#f75959")
    already_label.grid(row=6, column=0, columnspan=2)
    already_label.grid_remove()
    checked = ctk.IntVar()
    password_show = ctk.CTkCheckBox(root, height=30, width=30, text="Show password", variable=checked, onvalue=1,
                                    offvalue=0, command=display_password)
    password_show.grid(row=0, column=1)
    buttons = [("Generate", random_password), ("Save", store_password)]
    lrow = 1
    for buttonindex in range(len(buttons)):
        new_button = ctk.CTkButton(root, height=40, width=100, text=buttons[buttonindex][0], command=buttons[buttonindex][1])
        new_button.grid(row=lrow, column=1, rowspan=2, pady=5)
        lrow += 2
    password_entry.bind("<KeyRelease>", get_passentry)


def display_password():
    if checked.get() == 1:
        password_entry.configure(show="", font=("Roboto", 20))
    else:
        password_entry.configure(show="*", font=("Roboto", 25))


def get_passentry(*args):
    entry = password_entry.get()
    check_password(entry)


def check_password(entry):
    conditions = [False]*5
    if len(entry) > 7:
        conditions[0] = True
    for e in entry:
        if e in (list(map(chr, range(65, 91)))): conditions[1] = True
        if e in (list(map(chr, range(97, 123)))): conditions[2] = True
        if e in (list(map(chr, range(48, 58)))): conditions[3] = True
        if e in (list(map(chr, (33, 64, 35, 36, 94, 38, 42)))): conditions[4] = True
    for i in range(len(conditions)):
        if conditions[i]:
            cond_labels[i].grid_remove()
        else:
            cond_labels[i].grid()
    for e in conditions:
        if not e:
            return False
    return True


def random_password():
    cond_bool = False
    password = ""
    while not cond_bool:
        password = ''.join([rd.choice(list(map(chr, [33, 35, 64, 36, 94, 38, 42]
                                       + list(range(65, 91)) + list(range(97, 123))
                                       + list(range(48, 58))))) for i in range(rd.randint(13, 17))])
        if check_password(password):
            cond_bool = True
    password_entry.delete(0, ctk.END)
    password_entry.insert(0, password)


def store_password(*args):
    already_label.grid_remove()
    password = password_entry.get()
    hashed = hashlib.sha256(password.encode("utf-8"))
    hashed.digest()
    try:
        with open("passwords.json", "r") as contentfile:
            pass
    except FileNotFoundError:
        with open("passwords.json", "w") as createfile:
            content = []
            json.dump(content, createfile)
    with open("passwords.json", "r") as contentfile:
        content = json.load(contentfile)
    hexdigested = hashed.hexdigest()
    if hexdigested in content:
        already_label.grid()
    else:
        content.append(hashed.hexdigest())
    with open("passwords.json", "w") as contentfile:
        json.dump(content, contentfile, indent=4)


create_interface()
root.mainloop()

