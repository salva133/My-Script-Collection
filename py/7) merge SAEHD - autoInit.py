"""
Script Name: 7) merge SAEHD - autoInit.py
Description: This script automates the initialization and running of the merging process for SAEHD models using a graphical user interface (GUI). It leverages PyAutoGUI to simulate user inputs, thereby automating the merge process based on predefined settings.

Functions:
    debug_print(msg) - Prints debug messages if DEBUG mode is on.
    send_values(values) - Sends a series of values (commands or inputs) to a subprocess using PyAutoGUI.
    start_merge() - Initializes and starts the merging process with settings obtained from the GUI.

Variables:
    DEBUG - Flag to turn on/off debugging messages.
    INTERACTIVE_MERGER, mode, mask_mode, etc. - Variables associated with merge settings, controlled through the GUI.

Note:
    This script assumes that the GUI for the merging tool is already open and in its default state when executed.
"""



import tkinter as tk
from tkinter import ttk
import pyautogui
import time
import subprocess

DEBUG = True


def debug_print(msg):
    if DEBUG:
        print(f"DEBUG: {msg}")


def send_values(values):
    debug_print("Sending values to subprocess...")
    for value in values:
        pyautogui.write(str(value))
        pyautogui.press("enter")


def start_merge():
    debug_print("Starting merge...")
    INTERACTIVE_MERGER = interactive_merger_var.get()
    mode = mode_var.get()
    mask_mode = mask_mode_var.get()
    erode_mask = erode_mask_var.get()
    blur_mask = blur_mask_var.get()
    motion_blur = motion_blur_var.get()
    output_face_scale = output_face_scale_var.get()
    ct_mode = ct_mode_var.get()
    sharpen_mode = sharpen_mode_var.get()
    super_resolution = super_resolution_var.get()
    denoise = denoise_var.get()
    bicubic_rescale = bicubic_rescale_var.get()
    degrade_color = degrade_color_var.get()
    workers = workers_var.get()

    values = [
        INTERACTIVE_MERGER,
        mode,
        mask_mode,
        erode_mask,
        blur_mask,
        motion_blur,
        output_face_scale,
        ct_mode,
        sharpen_mode,
        super_resolution,
        denoise,
        bicubic_rescale,
        degrade_color,
        workers,
    ]

    debug_print("Calling batch file...")
    subprocess.Popen(file_to_call, shell=True)

    time.sleep(1)  # Warte 1 Sekunde

    debug_print("Switching focus to CMD window...")
    pyautogui.hotkey("alt", "tab")

    debug_print("Sending preliminary values...")
    for _ in range(2):
        pyautogui.write("0")
        pyautogui.press("enter")

    debug_print("Waiting for subprocess to initialize...")

    time.sleep(15)
    send_values(values)


debug_print("Initializing GUI...")
root = tk.Tk()
root.title("Merge SAEHD Einstellungen")

file_to_call = "7) merge SAEHD.bat"
interactive_merger_var = tk.StringVar(value="n")
mode_var = tk.IntVar(value=1)
mask_mode_var = tk.IntVar(value=8)
erode_mask_var = tk.IntVar(value=30)
blur_mask_var = tk.IntVar(value=150)
motion_blur_var = tk.IntVar(value=0)
output_face_scale_var = tk.IntVar(value=0)
ct_mode_var = tk.StringVar(value="rct")
sharpen_mode_var = tk.IntVar(value=0)
super_resolution_var = tk.IntVar(value=0)
denoise_var = tk.IntVar(value=0)
bicubic_rescale_var = tk.IntVar(value=0)
degrade_color_var = tk.IntVar(value=0)
workers_var = tk.IntVar(value=20)

debug_print("Setting up input fields and labels...")
labels_and_vars = [
    ("Mode", mode_var),
    ("Mask Mode", mask_mode_var),
    ("Erode Mask", erode_mask_var),
    ("Blur Mask", blur_mask_var),
    ("Motion Blur", motion_blur_var),
    ("Output Face Scale", output_face_scale_var),
    ("CT Mode", ct_mode_var),
    ("Sharpen Mode", sharpen_mode_var),
    ("Super Resolution", super_resolution_var),
    ("Denoise", denoise_var),
    ("Bicubic Rescale", bicubic_rescale_var),
    ("Degrade Color", degrade_color_var),
    ("Workers", workers_var),
]

for label, var in labels_and_vars:
    row = tk.Frame(root)  # Setzen Sie den Hintergrund des Frames auf schwarz
    row.pack(fill=tk.X, padx=5, pady=5)

    # Setzen Sie den Hintergrund des Labels auf schwarz und den Text auf weiß
    tk.Label(row, text=label).pack(side=tk.LEFT)

    # Erstellen Sie das Eingabefeld mit einem rechtsbündigen Text und einer festgelegten Breite
    entry = tk.Entry(row, textvariable=var, justify="right", width=5)
    entry.pack(side=tk.RIGHT, fill=tk.X)

debug_print("Setting up Execute button...")
ttk.Button(root, text="Execute", command=start_merge).pack(pady=20)

debug_print("Entering main loop...")
root.mainloop()
