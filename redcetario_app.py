import tkinter as tk

# Create the app's main window
window = tk.Tk()
window.title("Hello, World!")

def handle_button_press():
    window.destroy()

button = tk.Button(text="My simple app.", command=handle_button_press)
button.pack()

# Start the event loop
window.mainloop()