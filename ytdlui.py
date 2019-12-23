#!/usr/bin/env python3

import tkinter as tk
from tkinter.ttk import Progressbar
import time
import threading as th
import subprocess as sp

class UI:
    def __init__(self):
        self.top = tk.Tk()
        self.top.title("Youtube DL UI")
        self.lbl = tk.Label(self.top, text="Copier/coller le lien dans le tampon puis clicker sur le boutton")
        self.lbl.grid(column=1, row=0, columnspan=2)
        self.link_txt = tk.StringVar()
        self.txt = tk.Entry(self.top, width=105, state=tk.DISABLED, textvariable=self.link_txt)
        self.txt.grid(column=0, row=1, columnspan=3)
        self.btn = tk.Button(self.top, text="Récuperer du tampon", command=self.get_from_clipboard)
        self.btn.grid(column=1, row=2)
        self.chk_state = tk.BooleanVar()
        self.chk_state.set(False)
        self.chk = tk.Checkbutton(self.top, text="Audio seulement", var=self.chk_state)
        self.chk.grid(column=2, row=2)

    def get_from_clipboard(self):
        self.link_txt.set(self.top.clipboard_get())
        self.btn.configure(text="Extraire!", command=self.extract)

    def dl_task(self):
        self.finish()

    def finish(self):
        # finish
        self.lbl.configure(text="Copier/coller le lien dans le tampon puis clicker sur le boutton")
        self.link_txt.set("")
        self.btn.configure(text="Récuperer du tampon", command=self.get_from_clipboard, state=tk.NORMAL)
        lschild = self.top.grid_slaves()
        for ch in lschild:
            if ch is self.log:
                ch.destroy()
            if ch is self.scroll:
                ch.destroy()
        self.log = None
        self.scroll = None

    def extract(self):
        self.lbl.configure(text="Extraire %s" % self.link_txt.get())
        self.btn.configure(text="Extraction en cours", state=tk.DISABLED)
        self.scroll = tk.Scrollbar(self.top)
        self.log = tk.Text(self.top, yscrollcommand=self.scroll.set)
        self.log.grid(column=1, row=3)
        self.scroll.grid(column=2, row=3)
        self.scroll.configure(command=self.log)
        self.bck_task = th.Thread(self.dl_task)
        self.bck_task.start()

    def mainloop(self):
        self.top.mainloop()

if __name__ == "__main__":
    ui = UI()
    ui.mainloop()
