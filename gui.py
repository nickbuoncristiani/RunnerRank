import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

saves = {}

root = tk.Tk()

#GUI functions
def placeholder():
    return None

def create_rankings_window():
    rankings_window = tk.Toplevel(root)
    #Might change to grid below instead of pack
    rankings_list = tk.Text(rankings_window)
    rankings_list.grid(row=0, column=0)
    #Will be replaced with actual rankings list
    rankings = "RANKINGS HERE"
    rankings_list.insert(tk.END, rankings)
    rankings_window.mainloop()

def load_save():
    filename = askopenfilename()
    #test
    print(filename)
    return filename

#basic window setup
root.title("Runner Rank")

#athlete search bar
tk.Label(root, text="Search Athlete").grid(row=0, column=0)
athlete_search_bar = tk.Entry(root)
athlete_search_bar.insert(10, "Athlete Name")

athlete_search_bar.grid(row=0, column=1)

#new and load buttons
new_button = tk.Button(root, text="New", command=placeholder)
new_button.grid(row=1, column=0)

load_button = tk.Button(root, text="Load", command=load_save)
load_button.grid(row=1, column=1)

#show rankings button
rankings_button = tk.Button(root, text="Show Current Rankings", command=create_rankings_window)
rankings_button.grid(row=2, columnspan=2)

root.mainloop()
