import Save, pickle
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd

def load(save, filename = 'my_save.bin'):
    with open(filename, 'rb') as file:
        s = pickle.load(file)
    return s

def save(save, filename = 'my_save.bin'):
    with open(filename, 'wb') as file:
        pickle.dump(save, file)


root = tk.Tk()

rankings = "Please load a save!"
current = None

#GUI functions
def placeholder():
    return None

def create_rankings_window():
    rankings_window = tk.Toplevel(root)
    #Might change to grid below instead of pack
    rankings_list = tk.Text(rankings_window)
    rankings_list.grid(row=0, column=0)
    #Will be replaced with actual rankings list
    rankings_list.insert(tk.END, rankings)
    rankings_window.mainloop()

def load_save():
    filename = fd.askopenfilename()
    current = load(str(filename))
    rankings = str(current)

def new_save():
    #not sure how much of this functionality is covered elsewhere. In the meanwhile - opens a save dialogue
    #might have to work more with this functionality... consider this a placeholder
    filename = fd.asksaveasfilename()
    s = Save.Save()
    s.import_data(1, 12421023)
    save(s, str(filename))

def generate_rankings():
    return

if __name__ == "__main__":
        #basic window setup
        root.title("Runner Rank")

        #athlete search bar
        tk.Label(root, text="Search Athlete").grid(row=0, column=0)
        athlete_search_bar = tk.Entry(root)
        athlete_search_bar.insert(10, "Athlete Name")
        athlete_search_bar.grid(row=0, column=1)

        #new and load buttons
        new_button = tk.Button(root, text="New", command=new_save)
        new_button.grid(row=1, column=0)

        load_button = tk.Button(root, text="Load", command=load_save)
        load_button.grid(row=1, column=1)

        #show rankings button
        rankings_button = tk.Button(root, text="Show Current Rankings", command=create_rankings_window)
        rankings_button.grid(row=2, columnspan=2)

        root.mainloop()
