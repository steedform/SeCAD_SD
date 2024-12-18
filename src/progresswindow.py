'''
Copyright (c) 2024, Steedform All rights reserved.
Redistribution and use in source and binary forms, with or without   
modification, are not permitted provided that the code retains the 
above copyright notice.
'''

import tkinter as tk
from tkinter import ttk

# Initialize Tkinter Window
class ProgressWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Progress")
        self.root.geometry("500x300")
        self.messages = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, bg="white")
        self.messages.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(root, command=self.messages.yview)
        self.messages.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_message(self, message):
        self.messages.config(state=tk.NORMAL)
        self.messages.insert(tk.END, f"{message}\n")
        self.messages.see(tk.END)
        self.messages.config(state=tk.DISABLED)
        self.root.update()