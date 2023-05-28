import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import os


class AcronymDictionary:
    def __init__(self):
        self.dictionary = {}

    def load_from_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                self.dictionary = {row[0]: row[1] for row in reader}
        else:
            self.dictionary = {}

    def save_to_file(self, file_path):
        with open(file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Acronym", "Definition"])
            for acronym, definition in self.dictionary.items():
                writer.writerow([acronym, definition])

    def add_entry(self, acronym, definition):
        if acronym in self.dictionary:
            self.dictionary[acronym] += '; ' + definition
        else:
            self.dictionary[acronym] = definition

    def remove_entry(self, acronym, definition):
        if acronym in self.dictionary:
            definitions = self.dictionary[acronym].split('; ')
            definitions.remove(definition)
            if definitions:
                self.dictionary[acronym] = '; '.join(definitions)
            else:
                del self.dictionary[acronym]


class AcronymApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Acronym Dictionary')
        self.acronym_dict = AcronymDictionary()

        # Load the default dictionary file on startup
        self.file_path = "acrodict.csv"
        self.acronym_dict.load_from_file(self.file_path)

        # Menu Bar
        self.menubar = tk.Menu(root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open Dictionary", command=self.open_dictionary)
        self.filemenu.add_command(label="Save Dictionary", command=self.save_dictionary)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.root.config(menu=self.menubar)

        # Search Bar
        self.search_frame = ttk.Frame(root)
        self.search_frame.pack(fill='x')

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side='left')

        self.search_button = ttk.Button(self.search_frame, text='Search', command=self.search)
        self.search_button.pack(side='left')

        # Add Entry Button
        self.add_button = ttk.Button(root, text='Add Entry', command=self.add_entry)
        self.add_button.pack()

        # Remove Entry Button
        self.remove_button = ttk.Button(root, text='Remove Entry', command=self.remove_entry)
        self.remove_button.pack()

        # Result Panel
        self.result_frame = ttk.LabelFrame(root, text='Results')
        self.result_frame.pack(fill='x')

        self.result_listbox = tk.Listbox(self.result_frame)
        self.result_listbox.pack()

    def open_dictionary(self):
        self.file_path = filedialog.askopenfilename(filetypes=(("CSV Files", "*.csv"),))
        if self.file_path:
            self.acronym_dict.load_from_file(self.file_path)

    def save_dictionary(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if self.file_path:
            self.acronym_dict.save_to_file(self.file_path)

    def search(self):
        search_term = self.search_entry.get()
        if search_term in self.acronym_dict.dictionary:
            self.result_listbox.delete(0, tk.END)
            definitions = self.acronym_dict.dictionary[search_term].split('; ')
            for definition in definitions:
                self.result_listbox.insert(tk.END, f'{search_term}: {definition}')
        else:
            self.result_listbox.delete(0, tk.END)

    def add_entry(self):
        def save_entry():
            acronym = new_acronym_entry.get()
            definition = new_definition_entry.get()
            self.acronym_dict.add_entry(acronym, definition)
            self.acronym_dict.save_to_file(self.file_path)
            self.search_entry.focus_set()  # Transfer the focus back to the search bar
            new_entry_top.destroy()

        new_entry_top = tk.Toplevel(self.root)

        new_acronym_entry = ttk.Entry(new_entry_top)
        new_acronym_entry.pack()
        new_definition_entry = ttk.Entry(new_entry_top)
        new_definition_entry.pack()
        save_button = ttk.Button(new_entry_top, text='Save Entry', command=save_entry)
        save_button.pack()


    def remove_entry(self):
        selected = self.result_listbox.get(tk.ANCHOR)
        if selected:
            acronym, definition = selected.split(': ', 1)
            self.acronym_dict.remove_entry(acronym, definition)
            self.acronym_dict.save_to_file(self.file_path)
            self.result_listbox.delete(tk.ANCHOR)



if __name__ == "__main__":
    root = tk.Tk()
    app = AcronymApp(root)
    root.mainloop()
