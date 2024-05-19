import pygetwindow as gw

def focus_window(title):
    try:
        # Attempt to get the window by title
        window = gw.getWindowsWithTitle(title)[0]  # This gets the first window that matches the title
        if window:
            window.activate()
            window.activate()
            print("done")
            # If the window is minimized, maximize it
            if window.isMinimized:
                window.maximize()
                print("min to")
            # Additional check to ensure the window comes to the foreground
            # pyautogui.click(window.left + 10, window.top + 10)
    except IndexError:
        # No window with the specified title was found
        print(f"No window with the title '{title}' was found.")

# # Example usage
# focus_window("Path of Exile")
        

# import win32gui
# import win32con

# def focus_window_win32(title):
#     def enum_windows_proc(hwnd, lParam):
#         if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == title:
#             win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Unminimize if minimized
#             win32gui.SetForegroundWindow(hwnd)  # Bring to front
#             return False  # Stop enumeration
#         return True

#     win32gui.EnumWindows(enum_windows_proc, None)
