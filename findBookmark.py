from pyautogui import *
import pyautogui
import time
from pynput import keyboard
import random
import mouse
import tkinter as tk
import threading

# Total about of rolls (num * 3 = skystones used)
total = 500

#Config settings if you dont use standard monitor size
config_values = {
    "confirmX": 1360,
    "confirmY": 940,
    "offsetX": 900,
    "offsetY": 100,
    "resetX": 650,
    "resetY": 1175,
    "resetX2": 1440,
    "resetY2": 850,
}

#Destructuring
confirmX = config_values["confirmX"]
confirmY = config_values["confirmY"]
offsetX = config_values["offsetX"]
offsetY = config_values["offsetY"]
resetX = config_values["resetX"]
resetY = config_values["resetY"]
resetX2 = config_values["resetX2"]
resetY2 = config_values["resetY2"]

#Ignore these
mysticCount = 0
bookmarkCount = 0

#Quit key (press q)
def on_press(key):
    print(key)
    try:
        if key.char == 'q':
          print('terminating')
          os._exit(0)
    except:
        k = key.name

#Listes for key
listener = keyboard.Listener(
    on_press=on_press)
listener.start()

#Main function - Reads for mystic medal and covenant bookmarks
def check_bookmarks():
    print("Checking bookmarks")
    time.sleep((random.random() * 0.2) + 1)
    mysticLocation = pyautogui.locateOnScreen('Bookmarks/mystic.png', confidence = .6)
    covLocation = pyautogui.locateOnScreen('Bookmarks/bookmark.png', confidence = .7)
    #Found mystic
    if mysticLocation != None:
        print("You have a mystic bookmark on screen")
        global mysticCount
        mysticCount += 1
        print("Total mystic medals found: %d" %(mysticCount))
        click(mysticLocation[0]+offsetX,mysticLocation[1]+offsetY)
        time.sleep(random.random() + 1)
        click(confirmX,confirmY)
        time.sleep(random.random() + 1)
    #Found covenant
    if covLocation != None:
        print("You have a covenant bookmark on screen")
        global bookmarkCount
        bookmarkCount += 1
        print("Total mystic medals found: %d" %(bookmarkCount))
        click(covLocation[0]+offsetX,covLocation[1]+offsetY)
        time.sleep(random.random() + 1)
        click(confirmX,confirmY)
        time.sleep(random.random() + 1)
    print("Finished Checking bookmarks")

#Scrolls the shop down
def scroll():
    print("Scrolling")
    mouse.drag(confirmX + (random.random()*100), confirmY + (random.random()*50), confirmX + (random.random()*100), confirmY-500 + (random.random()*100), absolute=True, duration=0.3)
    time.sleep((random.random() * 0.5) + 0.5)
    print("Done Scrolling")

#Clicks on the refresh shop
def reset():
    print("Resetting Shop")
    click(resetX + ((random.random() - 0.5) * 300),resetY + ((random.random() - 0.5) * 10))
    time.sleep((random.random() * 0.5) + 0.5)
    click(resetX2 + ((random.random() - 0.5) * 200),resetY2 + ((random.random() - 0.5) * 10))
    time.sleep((random.random() * 0.5) + 0.5)
    print("Done Resetting Shop")

#Clicks at a location (twice)
def click(x,y):
    mouse.move(x,y,absolute=True,duration=0)
    mouse.click('left')
    time.sleep((random.random() * 0.5) + 0.5)
    mouse.click('left')

def update_settings():
    for entry, var in config_vars.items():
        config_values[entry] = int(var.get())

    text_widget.delete(1.0, tk.END)

    text_widget.insert(tk.END, "Updated Settings:\n")

    for entry, value in config_values.items():
        text_widget.insert(tk.END, f"{entry}: {value}\n")

def update_total(event=None):
    try:
        new_total = int(total_var.get())
        global total
        total = new_total
    except ValueError:
        pass

def start_click():
    global thread
    if not thread or not thread.is_alive():
        thread = threading.Thread(target=run_script)
        thread.daemon = True
        thread.start()

def run_script():
    update_total()
    pulls = 0
    scrolled = False
    global active
    if not active:
        active = True
        active_text.config(text="Running...")
        while pulls < total*2:
            print("Loop: %d/%d Mystic: %d Covenant: %d" %(pulls/2,total,mysticCount,bookmarkCount))
            pulls += 1
            check_bookmarks()
            #time.sleep((random.random() * 0.5) + 0.5)
            if scrolled == False:
                scroll()
                scrolled = True
            else:
                reset()
                scrolled = False
            #time.sleep((random.random() * 0.5) + 0.5)
        root.after(1000, stop_script)

def stop_script():
    global active
    active = False
    active_text.config(text="")

active = False
thread = None

root = tk.Tk()
root.title("Secret Shop Refresh")
root.attributes("-topmost", True)
root.geometry("560x320+0+0")
root.resizable(False, False)

pad_x = 5
pad_y = 5

config_vars = {}

for row, (config, default_value) in enumerate(config_values.items()):
    label = tk.Label(root, text=f"{config}:")
    label.grid(row=row, column=0, padx=pad_x, pady=pad_y)

    var = tk.StringVar()
    var.set(str(default_value))
    config_vars[config] = var

    config_widget = tk.Entry(root, textvariable=var)
    config_widget.grid(row=row, column=1, padx=pad_x, pady=pad_y)

update_button = tk.Button(root, text="Update Settings", command=update_settings)
update_button.grid(row=8, column=0, columnspan=2)

text_widget = tk.Text(root, width=40, height=10)
text_widget.insert(tk.END, "Current Settings:\n")
for entry, value in config_values.items():
    text_widget.insert(tk.END, f"{entry}: {value}\n")
text_widget.grid(row=0, column=2, rowspan=8, padx=pad_x, pady=pad_y)

total_label = tk.Label(root, text="Refreshes:")
total_label.grid(row=7, column=2, padx=pad_x, pady=pad_y, sticky="w")
total_var = tk.StringVar()
total_var.set(str(total))
total_widget = tk.Entry(root, textvariable=total_var)
total_widget.grid(row=7, column=2, padx=pad_x, pady=pad_y, sticky="ns")

active_text = tk.Label(root, width=20, height=2)
active_text.grid(row=9, column=2, padx=pad_x, pady=pad_y, sticky="w")

button = tk.Button(root, text="Start", command=start_click, height=2, width=40)
button.grid(row=8, column=2)

root.mainloop()