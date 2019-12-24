#!/usr/bin/env python3

import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.scrolledtext import ScrolledText
import time
import threading as th
import subprocess as sp
import re
import youtube_dl as ytdl
from urllib.parse import *

class DLThread(th.Thread):
    def __init__(self, ui):
        th.Thread.__init__(self)
        self.ui = ui
     
    def run(self):
        class MyLogger:
            def __init__(self, ui):
                self.ui = ui
                self.step = 0
                self.steps = ['-', '\\', '|', '/']
                self.list_dl = {}

            def debug(self, msg):
                print("DBG %s" % len(msg))
                print("LOG %d" % id(self.ui.log))
                print("%s" % type(self.ui.log))
                if self.ui.log is not None and ord(msg[0]) != 13:
                    self.ui.log.insert(tk.INSERT, "%s\n" % msg)
                    self.ui.log.see(tk.INSERT)
                elif re.search(r'has already been downloaded and merged', msg):
                    print("Match")
                    self.ui.finish()
                else:
                    print("DBG [%s]" % msg)

            def warning(self, msg):
                print(msg)

            def error(self, msg):
                print(msg)

            def prog_hook(self, d):
                print(repr(d))
                fn = d['filename']
                if d['filename'] not in self.list_dl:
                    self.list_dl[fn] = False
                if d['status'] == 'downloading' and self.ui.progress is None:
                    self.ui.extract_ui()
                    for fn in self.list_dl.keys():
                        txt = "Télécharger: %s" % fn
                        if self.list_dl[fn]:
                            txt += " OK!"
                        txt += "\n"
                        self.ui.log.insert(tk.INSERT, txt)
                        self.ui.log.see(tk.INSERT)
                if d['status'] == 'downloading' and self.ui.progress is not None:
                    print(repr(d))
                    m = re.search(r'(\d+(\.\d+))%', d['_percent_str'])
                    perc = float(m.groups()[0])
                    print("PERCENT %s" % perc)
                    self.ui.progress['value'] = perc
                    self.ui.btn.configure(text="Extraction en cours %s" % self.steps[self.step])
                    self.step = (self.step + 1) % len(self.steps)
                elif d['status'] == 'finished':
                    self.list_dl[fn] = True    
                    self.ui.finish()

        log = MyLogger(self.ui)
        # TODO: urllib.urlparse
        opts = {'logger': log, 'progress_hooks': [log.prog_hook], 'nooverwrites': True}
        url = self.ui.link_txt.get()
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        if 
        with ytdl.YoutubeDL(opts) as dl:
            dl.download([url])

class UI:
    def __init__(self):
        self.top = tk.Tk()
        self.top.title("Youtube DL UI")
        self.lbl = tk.Label(self.top, text="Copier/coller le lien dans le tampon puis clicker sur le boutton")
        self.lbl.grid(column=0, row=0, columnspan=2)
        self.link_txt = tk.StringVar()
        self.txt = tk.Entry(self.top, width=105, state=tk.DISABLED, textvariable=self.link_txt)
        self.txt.grid(column=0, row=1, columnspan=3)
        self.btnextract = tk.Button(self.top, text="Récuperer du tampon", command=self.get_from_clipboard)
        self.btnextract.grid(column=0, row=2)
        self.btn = tk.Button(self.top, text="Extraire!", command=self.extract, state=tk.DISABLED)
        self.btn.grid(column=1, row=2)
        self.chk_state = tk.BooleanVar()
        self.chk_state.set(False)
        self.chk = tk.Checkbutton(self.top, text="Audio seulement", var=self.chk_state)
        self.chk.grid(column=2, row=2)

    def get_from_clipboard(self):
        txt = self.top.clipboard_get()
        if txt != "":
            self.link_txt.set(txt)
            self.btn.configure(state=tk.NORMAL)
        else:
            self.btn.configure(state=tk.DISABLED)

    def extract(self):
        self.extract_ui()
        self.bg_task = DLThread(self)
        self.bg_task.start()

    def extract_ui(self):
        self.top.configure(cursor='watch')
        self.txt.configure(cursor='watch')
        self.lbl.configure(text="Extraire %s" % self.link_txt.get())
        self.btn.configure(text="Extraction en cours .", state=tk.DISABLED)
        self.log = ScrolledText(self.top, cursor='watch')
        self.log.grid(column=1, row=3)
        self.progress = Progressbar(self.top, orient="horizontal", length=600, mode="determinate")
        self.progress["value"] = 0.0
        self.progress["maximum"] = 100.0
        self.progress.grid(column=1, row=4)

    def finish(self):
        self.top.configure(cursor='arrow')
        self.txt.configure(cursor='arrow')
        self.lbl.configure(text="Copier/coller le lien dans le tampon puis clicker sur le boutton")
        # finish
        self.link_txt.set("")
        if self.log is not None:
            self.log.vbar.destroy()
            self.log.frame.destroy()
            self.log.destroy()
            self.log = None
        if self.progress is not None:
            self.progress.destroy()
            self.progress = None

    def mainloop(self):
        self.top.mainloop()

if __name__ == "__main__":
    ui = UI()
    ui.mainloop()
