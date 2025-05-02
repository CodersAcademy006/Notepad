import tkinter as tk
from tkinter import ttk, font, colorchooser, messagebox, filedialog
import os
from datetime import datetime

class AdvancedNotepad:
    """
    An advanced text editor application with enhanced features and a modern UI.
    """
    def __init__(self, root):
        """
        Initializes the main application window and its components.

        Args:
            root (tk.Tk): The main application window.
        """
        self.root = root
        self.root.title("Pinnacle Text Editor")
        self.set_icon()
        self.width, self.height = 800, 600
        self.center_window()

        # --- Enhanced Styling ---
        self.style = ttk.Style()
        self.configure_styles()

        # --- Main Content Area ---
        self.text_area = tk.Text(self.root, wrap=tk.WORD, undo=True)  # Initialize text_area FIRST
        self.create_text_area()
        self.scroll_bar = ttk.Scrollbar(self.root, command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scroll_bar.set)
        self.status_bar = ttk.Label(self.root, text="Ready", anchor=tk.W)

        # --- Main Menu ---
        self.menu_bar = tk.Menu(self.root)
        self.create_menu()  # Then create the menu, which uses text_area

        self.create_layout()

        # --- Initial Setup ---
        self.file_path = None
        self.text_area.focus_set()
        self.update_status()
        self.root.bind("<Key>", self.update_status)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def set_icon(self):
        """Sets the application icon.  Handles potential errors."""
        try:
            # The icon file should be in the same directory as the script or in a location where the script can access it.
            # If you still have issues, replace 'icon.ico' with the full path to your icon file.
            icon_path = "icon.ico"  # <--- Make sure this path is correct!
            if not os.path.exists(icon_path):
                print(f"Error: Icon file not found at {icon_path}")
                return  # Don't try to set the icon if the file doesn't exist.
            self.root.wm_iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting icon: {e}")

    def center_window(self):
        """Centers the application window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) - (self.height / 2)
        self.root.geometry(f"{self.width}x{self.height}+{int(x)}+{int(y)}")

    def configure_styles(self):
        """Configures ttk styles for a modern look.  Uses 'clam' if available."""
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            self.style.theme_use('default')

        self.style.configure("TextArea",
                             font=("Calibri", 12),
                             background="#f0f0f0",
                             foreground="#333333",
                             insertcolor="#000000")
        self.style.configure("StatusBar.TLabel",
                             font=("Calibri", 10),
                             background="#e0e0e0",
                             foreground="#555555")

    def create_menu(self):
        """Creates the main menu bar with File, Edit, View, and Help menus."""
        self.root.config(menu=self.menu_bar)

        # --- File Menu ---
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As...", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_close)

        # --- Edit Menu ---
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.text_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.select_all_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find...", accelerator="Ctrl+F", command=self.show_find_dialog)
        self.edit_menu.add_command(label="Replace...", accelerator="Ctrl+H", command=self.show_replace_dialog)

        # --- View Menu ---
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Toggle Status Bar", command=self.toggle_status_bar)
        self.view_menu.add_command(label="Font...", command=self.show_font_dialog)

        # --- Help Menu ---
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about_dialog)

        # --- Bind Accelerators ---
        self.root.bind("<Control-n>", self.new_file)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-a>", self.select_all_text)
        self.root.bind("<Control-f>", self.show_find_dialog)
        self.root.bind("<Control-h>", self.show_replace_dialog)

    def create_text_area(self):
        """Creates the text area widget and configures its appearance."""
        self.text_area.config(
            wrap=tk.WORD,
            undo=True,
            font=("Calibri", 12),
            relief=tk.FLAT,
            bg="#f0f0f0",
            fg="#333333",
            insertbackground="#000000",
            selectbackground="#b0e0e6",
            selectforeground="#000000"
        )
        self.text_area.focus_set()

    def create_layout(self):
        """Arranges the main widgets using grid layout."""
        self.text_area.grid(row=0, column=0, sticky=tk.NSEW)
        self.scroll_bar.grid(row=0, column=1, sticky=tk.NS)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky=tk.EW)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    # --- File Menu Functions ---
    def new_file(self, event=None):
        """Creates a new file.  Checks for unsaved changes."""
        if self.confirm_save():
            self.text_area.delete(1.0, tk.END)
            self.file_path = None
            self.root.title("Untitled - Pinnacle Text Editor")
            self.update_status()

    def open_file(self, event=None):
        """Opens an existing file.  Checks for unsaved changes."""
        if self.confirm_save():
            file_path = filedialog.askopenfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(1.0, file.read())
                        self.file_path = file_path
                        self.root.title(os.path.basename(file_path) + " - Pinnacle Text Editor")
                        self.update_status()
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open file:\n{e}")

    def save_file(self, event=None):
        """Saves the current file.  If no path, calls save_as_file."""
        if not self.file_path:
            self.save_as_file()
        else:
            try:
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                    self.update_status()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")

    def save_as_file(self):
        """Saves the current file to a new path."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="Untitled.txt"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.file_path = file_path
                self.root.title(os.path.basename(file_path) + " - Pinnacle Text Editor")
                self.update_status()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")

    def confirm_save(self):
        """
        Checks for unsaved changes and prompts the user to save.

        Returns:
            bool: True if the user saves or discards changes, False if canceled.
        """
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel(
                "Pinnacle Text Editor",
                "Do you want to save changes?"
            )
            if response == True:
                self.save_file()
                return True
            elif response == False:
                return True
            else:
                return False
        return True

    def on_close(self):
        """Handles the window close event.  Checks for unsaved changes."""
        if self.confirm_save():
            self.root.destroy()

    # --- Edit Menu Functions ---
    def cut_text(self, event=None):
        """Cuts selected text to the clipboard."""
        self.text_area.event_generate("<<Cut>>")
        self.update_status()

    def copy_text(self, event=None):
        """Copies selected text to the clipboard."""
        self.text_area.event_generate("<<Copy>>")
        self.update_status()

    def paste_text(self, event=None):
        """Pastes text from the clipboard."""
        self.text_area.event_generate("<<Paste>>")
        self.update_status()

    def select_all_text(self, event=None):
        """Selects all text in the text area."""
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        self.update_status()

    # --- View Menu Functions ---
    def toggle_status_bar(self):
        """Toggles the visibility of the status bar."""
        if self.status_bar.winfo_ismapped():
            self.status_bar.grid_remove()
        else:
            self.status_bar.grid(row=1, column=0, columnspan=2, sticky=tk.EW)
        self.update_status()

    def show_font_dialog(self):
        """Displays a font dialog and applies the selected font to the text area."""
        font_family = self.text_area.cget("font")[0]
        font_size = self.text_area.cget("font")[1]
        font_color = self.text_area.cget("foreground")

        font_options = {'family': font_family, 'size': font_size}

        font_tuple = tk.font. families()
        font_family = tk.StringVar()
        font_family.set(font_options['family'])
        font_size = tk.IntVar()
        font_size.set(font_options['size'])
        font_color = tk.StringVar()
        font_color.set(font_color)

        top = tk.Toplevel()
        top.title("Select Font")
        top.geometry("350x300")

        top.resizable(False, False)

        label_family = ttk.Label(top, text="Font Family:")
        label_family.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        family_box = ttk.Combobox(top, textvariable=font_family, values=font_tuple, width=20)
        family_box.grid(row=0, column=1, padx=10, pady=5)

        label_size = ttk.Label(top, text="Size:")
        label_size.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        size_box = ttk.Spinbox(top, textvariable=font_size, from_=8, to=72, increment=1, width=5)
        size_box.grid(row=1, column=1, padx=10, pady=5)

        label_color = ttk.Label(top, text="Color:")
        label_color.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        color_button = ttk.Button(top, text="Choose Color", command=lambda: self.choose_color(font_color))
        color_button.grid(row=2, column=1, padx=10, pady=5)
        color_label = ttk.Label(top, textvariable=font_color, width=8)
        color_label.grid(row=2, column=2, padx=2, pady=5)

        ok_button = ttk.Button(top, text="OK", command=lambda: self.apply_font(top, font_family.get(), font_size.get(), font_color.get()))
        ok_button.grid(row=3, column=0, columnspan=2, pady=10)

        top.wait_window()

    def choose_color(self, font_color):
        color = colorchooser.askcolor()[1]
        if color:
            font_color.set(color)

    def apply_font(self, top, family, size, color):
        """Applies the selected font to the text area."""
        try:
            new_font = font.Font(family=family, size=size)
            self.text_area.config(font=new_font, foreground=color)
            top.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply font:\n{e}")

    # --- Help Menu Functions ---
    def show_about_dialog(self):
        """Displays an about dialog box."""
        messagebox.showinfo(
            "About Pinnacle Text Editor",
            "Pinnacle Text Editor\n"
            "Version 1.0\n"
            "Developed by Swara Sawane and Srijan Upadhyay\n"
            "First Year Data Science Project\n"
            "Pune University"
        )

    # --- Status Bar Functions ---
    def update_status(self, event=None):
        """Updates the status bar with the current file path, line, and column."""
        if self.file_path:
            filename = os.path.basename(self.file_path)
        else:
            filename = "Untitled"
        line, column = self.text_area.index(tk.INSERT).split(".")
        modified = " *" if self.text_area.edit_modified() else ""
        self.status_bar.config(text=f"File: {filename}{modified} | Line: {line}, Column: {column}")

    # --- Find and Replace Functionality ---
    def show_find_dialog(self, event=None):
        """Displays a find dialog box."""
        self.find_dialog = tk.Toplevel(self.root)
        self.find_dialog.title("Find")
        self.find_dialog.geometry("300x100")
        self.find_dialog.transient(self.root)
        self.find_dialog.resizable(False, False)

        ttk.Label(self.find_dialog, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.find_entry = ttk.Entry(self.find_dialog, width=25)
        self.find_entry.grid(row=0, column=1, padx=5, pady=5)
        self.find_next_button = ttk.Button(self.find_dialog, text="Find Next", command=self.find_next)
        self.find_next_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
        self.find_entry.focus_set()

        self.find_dialog.bind('<Return>', self.find_next)

    def find_next(self, event=None):
        """Finds the next occurrence of the search string."""
        search_term = self.find_entry.get()
        if not search_term:
            messagebox.showwarning("Find", "Please enter text to find.")
            return

        start_pos = self.text_area.index(tk.INSERT)
        end_pos = self.text_area.index(tk.END)
        self.text_area.tag_remove("found", "1.0", tk.END)

        count = tk.IntVar()
        pos = self.text_area.search(search_term, start_pos, stopindex=end_pos, nocase=1, count=count)

        if pos:
            self.text_area.tag_add("found", pos, f"{pos}+{count.get()}c")
            self.text_area.tag_config("found", background="yellow", foreground="black")
            self.text_area.mark_set(tk.INSERT, f"{pos}+{count.get()}c")
            self.text_area.see(tk.INSERT)
        else:
            messagebox.showinfo("Find", "No more occurrences found.")

    def show_replace_dialog(self, event=None):
        """Displays a replace dialog box."""
        self.replace_dialog = tk.Toplevel(self.root)
        self.replace_dialog.title("Replace")
        self.replace_dialog.geometry("350x130")
        self.replace_dialog.transient(self.root)
        self.replace_dialog.resizable(False, False)

        ttk.Label(self.replace_dialog, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.replace_entry = ttk.Entry(self.replace_dialog, width=25)
        self.replace_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.replace_dialog, text="Replace With:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.replace_with_entry = ttk.Entry(self.replace_dialog, width=25)
        self.replace_with_entry.grid(row=1, column=1, padx=5, pady=5)

        replace_button = ttk.Button(self.replace_dialog, text="Replace", command=self.replace_text)
        replace_button.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        replace_all_button = ttk.Button(self.replace_dialog, text="Replace All", command=self.replace_all_text)
        replace_all_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.replace_entry.focus_set()
        self.replace_dialog.bind('<Return>', self.replace_text)

    def replace_text(self, event=None):
        """Replaces the next occurrence of the search string."""
        search_term = self.replace_entry.get()
        replace_term = self.replace_with_entry.get()
        if not search_term:
            messagebox.showwarning("Replace", "Please enter text to find.")
            return

        start_pos = self.text_area.index(tk.INSERT)
        end_pos = self.text_area.index(tk.END)
        self.text_area.tag_remove("found", "1.0", tk.END)

        count = tk.IntVar()
        pos = self.text_area.search(search_term, start_pos, stopindex=end_pos, nocase=1, count=count)

        if pos:
            self.text_area.delete(pos, f"{pos}+{count.get()}c")
            self.text_area.insert(pos, replace_term)
            self.text_area.mark_set(tk.INSERT, pos)
            self.text_area.see(tk.INSERT)
        else:
            messagebox.showinfo("Replace", "No more occurrences found.")

    def replace_all_text(self):
        """Replaces all occurrences of the search string."""
        search_term = self.replace_entry.get()
        replace_term = self.replace_with_entry.get()
        if not search_term:
            messagebox.showwarning("Replace All", "Please enter text to find.")
            return

        start_pos = "1.0"
        end_pos = tk.END
        self.text_area.tag_remove("found", "1.0", tk.END)

        count = tk.IntVar()
        while True:
            pos = self.text_area.search(search_term, start_pos, stopindex=end_pos, nocase=1, count=count)
            if not pos:
                break
            self.text_area.delete(pos, f"{pos}+{count.get()}c")
            self.text_area.insert(pos, replace_term)
            start_pos = pos
        self.update_status()
        messagebox.showinfo("Replace All", "All occurrences replaced.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedNotepad(root)
    root.mainloop()