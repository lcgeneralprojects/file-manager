import tkinter as tk
from common import general_function_handler

# Master section
root = tk.Tk()
root.title('File Manager')

# Label section
method_label = tk.Label(root, text='Method: ')
base_dir_label = tk.Label(root, text='Base directory: ')
prefix_label = tk.Label(root, text='Prefix: ')
problem_name_label = tk.Label(root, text='Problem name: ')

# Entry section
# TODO: make method_entry a drop-down menu
method_entry = tk.Entry(root)
base_dir_entry = tk.Entry(root)
prefix_entry = tk.Entry(root)
problem_name_entry = tk.Entry(root)

# Button section
ok_button = tk.Button(root, text='Ok',
                      command=lambda: general_function_handler(method_entry.get(), base_dir_entry.get(),
                                                               prefix_entry.get(), problem_name_entry.get()))

if __name__ == '__main__':
    root.mainloop()