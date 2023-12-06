import tkinter as tk
import customtkinter as ctk
import random as rd
import json
import _sha256


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.title("Password checker")


def check_password(entry):
    conditions = [False]*5
    if len(entry) > 7:
        conditions[0] = True
    for e in entry:
        if e in (list(map(chr, range(65, 91)))): conditions[1] = True
        if e in (list(map(chr, range(97, 123)))): conditions[2] = True
        if e in (list(map(chr, range(48, 57)))): conditions[3] = True
        if e in (list(map(chr, (33, 64, 35, 36, 94, 38, 42)))): conditions[4] = True
    return conditions


root.mainloop()

