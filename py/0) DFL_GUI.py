import os
import subprocess
import tkinter as tk

# Constants for background colors
DATA_SRC_COLOR = "blue"
DATA_DST_COLOR = "red"
MISC_COLOR = "green"

def run_script(script_name):
    subprocess.run([script_name])

def get_bg_color(column):
    if column == "Data SRC":
        return DATA_SRC_COLOR
    elif column == "Data DST":
        return DATA_DST_COLOR
    else:
        return MISC_COLOR

def create_frame(root, column, idx):
    frame = tk.Frame(root)
    frame.configure(bg=get_bg_color(column))
    frame.grid(row=1, column=idx, sticky="n")
    return frame

def create_buttons(frame, column):
    for i, script in enumerate(sorted(columns[column]), 1):
        label = script.split(")")[1].split(".bat")[0]
        button = tk.Button(frame, text=label, command=lambda s=script: run_script(s))
        button.configure(wraplength=200, width=30, bg='black', fg='white')
        button.grid(row=i, column=0, pady=2, padx=2)

root = tk.Tk()
root.title("DFL GUI - " + os.path.basename(os.getcwd()))

columns = {"Data SRC": [], "Data DST": [], "Processing": []}

for file in os.listdir("."):
    if file.endswith(".bat") and not file.startswith(("_", "10.misc")):
        if "data_dst" in file:
            columns["Data DST"].append(file)
        elif "data_src" in file:
            columns["Data SRC"].append(file)
        else:
            columns["Processing"].append(file)

for idx, column in enumerate(columns):
    tk.Label(root, text=column).grid(row=0, column=idx, sticky="nsew")
    frame = create_frame(root, column, idx)
    create_buttons(frame, column)

root.mainloop()
