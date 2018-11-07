import tkinter as tk
from tkinter import ttk

root = tk.Tk()
saves = []

#gui functions
def placeholder():
    return None

def create_rankings_window():
    rankings_window = tk.Toplevel(root)

#basic window setup
root.title("Runner Rank")

#athlete search bar
tk.Label(root, text="Search Athlete").grid(row=0, column=0)
athlete_search_bar = tk.Entry(root)
athlete_search_bar.grid(row=0, column=1)

#new and load buttons
tk.Button(root, text="New", command=placeholder).grid(row=1, column=0)
tk.Button(root, text="Load", command=placeholder).grid(row=1, column=1)

#show rankings button
tk.Button(root, text="Show Current Rankings", command=create_rankings_window).grid(row=2, column=0, columnspan=2)

root.mainloop()
