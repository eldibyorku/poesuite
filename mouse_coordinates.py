import threading
import tkinter as tk
from pynput.mouse import Listener, Button
import FocusWindow as FocusWindow

# # Function to activate the application
# app_name = "PathOfExileClient"
# cmd = f'osascript -e \'activate application "{app_name}"\''
# subprocess.call(cmd, shell=True)
FocusWindow.focus_window('Path Of Exile')

# Global flag to indicate when to quit the application
should_quit = False

def on_click(x, y, button, pressed):
    global should_quit
    if pressed:
        if button == Button.left:
            print(f"Mouse clicked at position: ({x}, {y})")
        else:
            should_quit = True
            return False  # This will stop the listener

def on_move(x, y):
    popup_label.config(text=f"Mouse position: ({x}, {y})")
    popup.update_idletasks()
    popup.geometry(f"+{int(x) + 20}+{int(y) + 20}")

def start_listener():
    with Listener(on_click=on_click, on_move=on_move) as listener:
        listener.join()

def check_quit():
    if should_quit:
        popup.quit()
    else:
        popup.after(100, check_quit)

# Create and configure the popup window
popup = tk.Tk()
popup.overrideredirect(1)  # Remove window decorations
popup.attributes('-topmost', 1)  # Keep the popup on top
popup.geometry('+500+500')  # Initialize popup position

popup_label = tk.Label(popup, text="Mouse position")
popup_label.pack()

# Start the listener in a separate thread
listener_thread = threading.Thread(target=start_listener)
listener_thread.start()

# Periodically check if we should quit
popup.after(100, check_quit)

# Run the popup's main loop
popup.mainloop()
