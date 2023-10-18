import os.path
import tkinter as tk
from tkinter import filedialog
from common import general_function_handler
from PIL import Image, ImageTk


# Master section
root = tk.Tk()
root.title('File Manager')
root.minsize(400, 250)

# TODO: consider organising things into classes

# Frame section
# TODO: make the font size bigger, and make the sizes of other elements depend on the font size
# # Main body frame
# main_body_frame = tk.Frame(root)
# main_body_frame.pack(padx=50, pady=10, fill='x')
# for r in range(2): main_body_frame.rowconfigure(index=r, weight=1)
# Label-and-entry frame
label_and_entry_frame = tk.Frame(root, relief='raised', borderwidth=5)  # TODO: remove relief and borderwidth after done testing
# label_and_entry_frame.grid(row=0, column=0, sticky='nsew')
label_and_entry_frame.pack(padx=50, pady=10, fill='x')
for c in range(4): label_and_entry_frame.columnconfigure(index=c, weight=1)
for r in range(6): label_and_entry_frame.rowconfigure(index=r, weight=1)
label_and_entry_frame.columnconfigure(index=1, weight=2)
# # Preset frame
# preset_frame = tk.Frame(main_body_frame)
# preset_frame.grid(row=1, column=0, sticky='nsew')
# for c in range(4):
# bottom frame
bottom_frame = tk.Frame(root)
bottom_frame.pack(side='bottom', fill='x')

# Label section
method_label = tk.Label(label_and_entry_frame, text='Method: ')
method_label.grid(row=0, column=0, sticky='E')
base_dir_label = tk.Label(label_and_entry_frame, text='Base directory: ')
base_dir_label.grid(row=1, column=0, sticky='E')
prefix_label = tk.Label(label_and_entry_frame, text='Prefix: ')
prefix_label.grid(row=2, column=0, sticky='E')
problem_name_label = tk.Label(label_and_entry_frame, text='Problem name: ')
problem_name_label.grid(row=3, column=0, sticky='E')
preset_name_label = tk.Label(label_and_entry_frame, text='Preset name: ')
preset_name_label.grid(row=5, column=0, sticky='E')

# Entry section
# TODO: make method_entry a drop-down menu
method_entry = tk.Entry(label_and_entry_frame)
method_entry.grid(row=0, column=1, sticky='EW')
base_dir_entry = tk.Entry(label_and_entry_frame)
base_dir_entry.grid(row=1, column=1, sticky='EW')
prefix_entry = tk.Entry(label_and_entry_frame)
prefix_entry.grid(row=2, column=1, sticky='EW')
problem_name_entry = tk.Entry(label_and_entry_frame)
problem_name_entry.grid(row=3, column=1, sticky='EW')
preset_name_entry = tk.Entry(label_and_entry_frame)
preset_name_entry.grid(row=5, column=1, sticky='EW')

ENTRY_OBJECT_DICT = {'method': method_entry, 'base dir': base_dir_entry, 'prefix': prefix_entry,
                     'problem name': problem_name_entry, 'preset name': preset_name_entry}

# Button section
ok_button = tk.Button(bottom_frame, text='Ok',
                      command=lambda: general_function_handler(method_entry.get(), base_dir_entry.get(),
                                                               prefix_entry.get(), problem_name_entry.get()))
ok_button.pack()

def set_base_dir():
    base_dir_entry.delete(0, tk.END)
    base_dir_entry.insert(0, filedialog.askdirectory())
    return

original_image = Image.open(r'assets\folder_icon.png')
directory_icon = ImageTk.PhotoImage(original_image.resize((16, 16)))
directory_button = tk.Button(label_and_entry_frame, image=directory_icon, command=lambda: set_base_dir())
directory_button.grid(row=1, column=2, sticky='W')


def save_preset():
    param_dict = {}
    for key, entry_object in ENTRY_OBJECT_DICT.items():
        param_dict[key] = entry_object.get()
    if not os.path.isdir('./preset'):
        os.makedirs('./preset')
    # TODO: consider the case where the name is empty
    with open(param_dict['Preset name'], 'w') as file:
        for key, value in param_dict.items():
            if not key == 'Preset name':
                file.write(key + ': ' + value + '\n')

save_preset_button = tk.Button(label_and_entry_frame, text='save preset', command=save_preset)
save_preset_button.grid(row=5, column=2, sticky='W')


def choose_preset():
    filename = filedialog.askopenfilename()
    param_dict = {}
    for key in ENTRY_OBJECT_DICT.keys():
        param_dict[key] = None
    with open(filename, 'r') as file:
        param_dict['Preset name'] = os.path.basename(file.name)
        for line in file:
            if line.strip() == '':
                continue
            key, value = line.split(': ', 1)
            param_dict[key] = value
    for key, value in param_dict.items():
        if value is not None:
            ENTRY_OBJECT_DICT[key].delete(0, tk.END)
            ENTRY_OBJECT_DICT[key].insert(0, value)

choose_preset_button = tk.Button(label_and_entry_frame, text='choose preset', command=choose_preset)
choose_preset_button.grid(row=5, column=3, sticky='W')


if __name__ == '__main__':
    saved_base_dir = ''
    root.mainloop()