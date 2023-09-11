import tkinter as tk
from tkinter import filedialog
from common import general_function_handler


# Master section
root = tk.Tk()
root.title('File Manager')
root.minsize(400, 250)

# Frame section
# TODO: unify the frames into a single one and use a grid to align the labels and the entries
# TODO: set the frame sizes
method_frame = tk.Frame(root)
method_frame.pack(padx=50, pady=10)
for c in range(3): method_frame.columnconfigure(index=c, weight=1)
for r in range(1): method_frame.rowconfigure(index=r, weight=1)
base_dir_frame = tk.Frame(root)
base_dir_frame.pack(padx=50, pady=10)
for c in range(3): base_dir_frame.columnconfigure(index=c, weight=1)    # Leaving one column for a button for file browsing
for r in range(1): base_dir_frame.rowconfigure(index=r, weight=1)
prefix_frame = tk.Frame(root)
prefix_frame.pack(padx=50, pady=10)
for c in range(3): prefix_frame.columnconfigure(index=c, weight=1)
for r in range(1): prefix_frame.rowconfigure(index=r, weight=1)
problem_name_frame = tk.Frame(root)
problem_name_frame.pack(padx=50, pady=10)
for c in range(3): problem_name_frame.columnconfigure(index=c, weight=1)
for r in range(1): problem_name_frame.rowconfigure(index=r, weight=1)
bottom_frame = tk.Frame(root)
bottom_frame.pack(side='bottom', fill='x')

# Label section
method_label = tk.Label(method_frame, text='Method: ')
method_label.grid(row=0, column=0)
base_dir_label = tk.Label(base_dir_frame, text='Base directory: ')
base_dir_label.grid(row=0, column=0)
prefix_label = tk.Label(prefix_frame, text='Prefix: ')
prefix_label.grid(row=0, column=0)
problem_name_label = tk.Label(problem_name_frame, text='Problem name: ')
problem_name_label.grid(row=0, column=0)

# Entry section
# TODO: make method_entry a drop-down menu
method_entry = tk.Entry(method_frame)
method_entry.grid(row=0, column=1)
base_dir_entry = tk.Entry(base_dir_frame)
base_dir_entry.grid(row=0, column=1)
prefix_entry = tk.Entry(prefix_frame)
prefix_entry.grid(row=0, column=1)
problem_name_entry = tk.Entry(problem_name_frame)
problem_name_entry.grid(row=0, column=1)

# Button section
# TODO: introduce a file explorer button for easier base_dir selection
ok_button = tk.Button(bottom_frame, text='Ok',
                      command=lambda: general_function_handler(method_entry.get(), base_dir_entry.get(),
                                                               prefix_entry.get(), problem_name_entry.get()))
ok_button.pack()

def set_base_dir():
    base_dir_entry.delete(0,tk.END)
    base_dir_entry.insert(0, filedialog.askdirectory())
    return

directory_icon = tk.PhotoImage(file=r'assets\folder_icon.png')
directory_button = tk.Button(base_dir_frame, image=directory_icon, command=lambda: set_base_dir())
directory_button.grid(row=0, column=2)

if __name__ == '__main__':
    saved_base_dir = ''
    root.mainloop()