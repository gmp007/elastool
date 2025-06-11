import tkinter as tk
from tkinter import messagebox

class InputFileViewer:
    def __init__(self, filename):
        self.filename = filename
       
        self.open_input_file()

    def update_line_numbers(self, event=None):
        line_numbers = ""
        row, _ = self.text_widget.index("end").split(".")
        for i in range(1, int(row)):
            line_numbers += f"{i}\n"
        self.line_number_widget.config(state="normal")
        self.line_number_widget.delete("1.0", "end")
        self.line_number_widget.insert("1.0", line_numbers)
        self.line_number_widget.config(state="disabled")

    def open_input_file(self):
        try:
            with open(self.filename, "r") as f:
                file_content = f.read()
                # Create a top-level window with specified width and height
                self.view_window = tk.Toplevel()
                self.view_window.title(f"File Content: {self.filename}")
                self.view_window.geometry("600x400")  # Set the width and height of the window
                # Create a frame to hold both the line numbers and text widget
                frame = tk.Frame(self.view_window)
                frame.pack(fill="both", expand=True)

                # Create a text widget for line numbers
                self.line_number_widget = tk.Text(frame, width=3, padx=3, state="disabled", bg="lightgrey")
                self.line_number_widget.pack(side="left", fill="y")

                # Display the file content in a text widget
                self.text_widget = tk.Text(frame, wrap="word", bg="white", padx=10)
                self.text_widget.pack(side="left", fill="both", expand=True)
                self.text_widget.insert("1.0", file_content)
                 

                # Link scrolling of both widgets
                scrollbar = tk.Scrollbar(frame, command=self.on_scrollbar)
                scrollbar.pack(side="right", fill="y")
                self.text_widget.config(yscrollcommand=scrollbar.set)
                self.line_number_widget.config(yscrollcommand=scrollbar.set)

                # Bind events to update line numbers
                self.text_widget.bind("<KeyRelease>", self.update_line_numbers)
                self.text_widget.bind("<MouseWheel>", self.update_line_numbers)
                self.text_widget.bind("<Button-1>", self.update_line_numbers)
                self.text_widget.bind("<Configure>", self.update_line_numbers)
                self.text_widget.bind("<FocusIn>", self.update_line_numbers)
                self.update_line_numbers()
                    # Enable editing
                def enable_editing():
                    self.text_widget.configure(state="normal")
                    edit_button.config(state="disabled")  # Disable the Edit button after enabling editing

                # Save changes
                def save_changes():
                    try:
                        with open(self.filename, "w") as f:
                            content = self.text_widget.get("1.0", tk.END)
                            f.write(content)
                        messagebox.showinfo("Success", "Changes saved successfully!")
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while saving changes: {e}")

                # Create a menu bar
                menubar = tk.Menu(self.view_window)
                self.view_window.config(menu=menubar)

                # Add a File menu
                file_menu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label="File", menu=file_menu)
                file_menu.add_command(label="Save", command=save_changes)

                # Add a Edit menu
                edit_menu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label="Edit", menu=edit_menu)
                edit_menu.add_command(label="Enable Editing", command=enable_editing)

                # Button to enable editing
                edit_button = tk.Button(self.view_window, text="Edit", command=enable_editing)
                edit_button.pack(side=tk.LEFT, padx=5, pady=5)

                # Make the text widget read-only by default
                self.text_widget.configure(state="normal")
                   

        except FileNotFoundError:
            messagebox.showerror("Error", f"The file '{self.filename}' does not exist.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_changes(self):
        try:
            with open(self.filename, "w") as f:
                content = self.text_widget.get("1.0", tk.END)
                f.write(content)
            messagebox.showinfo("Success", "Changes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving changes: {e}")

    def on_scrollbar(self, *args):
        self.text_widget.yview(*args)
        self.line_number_widget.yview(*args)

