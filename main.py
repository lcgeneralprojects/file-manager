import os.path
import tkinter as tk
from tkinter import filedialog, ttk

import common
from common import general_function_handler
from PIL import Image, ImageTk
import pyperclip


# Master section
root = tk.Tk()
root.title('File Manager')
root.minsize(600, 250)

# TODO: Introduce a label to indicate whether the chosen 'action' finished successfully or not
# TODO: consider organising things into classes

# Frame section
# TODO: make the font size bigger, and make the sizes of other elements depend on the font size
# Label-and-entry frame
label_and_entry_frame = tk.Frame(root, relief='raised', borderwidth=5)  # TODO: remove relief and borderwidth after done testing
# label_and_entry_frame.grid(row=0, column=0, sticky='nsew')
label_and_entry_frame.pack(padx=20, pady=10, fill='x')
for c in range(4): label_and_entry_frame.columnconfigure(index=c, weight=1)
for r in range(7): label_and_entry_frame.rowconfigure(index=r, weight=1)
label_and_entry_frame.columnconfigure(index=1, weight=2, minsize=200)
label_and_entry_frame.rowconfigure(index=5, minsize=16)
# bottom frame
bottom_frame = tk.Frame(root)
bottom_frame.pack(side='bottom', fill='x')

# Label section
action_label = tk.Label(label_and_entry_frame, text='Action: ')
action_label.grid(row=0, column=0, sticky='E')
base_dir_label = tk.Label(label_and_entry_frame, text='Base directory: ')
base_dir_label.grid(row=1, column=0, sticky='E')
prefix_label = tk.Label(label_and_entry_frame, text='Prefix: ')
prefix_label.grid(row=2, column=0, sticky='E')
problem_name_label = tk.Label(label_and_entry_frame, text='Problem name: ')
problem_name_label.grid(row=3, column=0, sticky='E')
extension_label = tk.Label(label_and_entry_frame, text='Extension: ')
extension_label.grid(row=4, column=0, sticky='E')
preset_name_label = tk.Label(label_and_entry_frame, text='Preset name: ')
preset_name_label.grid(row=6, column=0, sticky='E')

# Entry section
OPTION_LIST = list(common.ACTIONS_DICT.keys())
action_text_var = tk.StringVar(label_and_entry_frame)
# TODO: implement auto-completion
action_combobox = ttk.Combobox(label_and_entry_frame, textvariable=action_text_var, values=OPTION_LIST)
action_combobox.grid(row=0, column=1, sticky='EW')
# method_dropbox = tk.OptionMenu(label_and_entry_frame, action_text_var, *OPTION_LIST)    # Including this in the 'entry' section, at least for now
# method_dropbox.grid(row=0, column=1, sticky='EW')
# method_entry = tk.Entry(label_and_entry_frame)
# method_entry.grid(row=0, column=1, sticky='EW')
base_dir_entry = tk.Entry(label_and_entry_frame)
base_dir_entry.grid(row=1, column=1, sticky='EW')
prefix_entry = tk.Entry(label_and_entry_frame)
prefix_entry.grid(row=2, column=1, sticky='EW')
problem_name_entry = tk.Entry(label_and_entry_frame)
problem_name_entry.grid(row=3, column=1, sticky='EW')
extension_entry = tk.Entry(label_and_entry_frame)
extension_entry.grid(row=4, column=1, sticky='EW')
preset_name_entry = tk.Entry(label_and_entry_frame)
preset_name_entry.grid(row=6, column=1, sticky='EW')

ENTRY_OBJECT_DICT = {'action': action_text_var, 'base dir': base_dir_entry, 'prefix': prefix_entry,
                     'problem name': problem_name_entry, 'extension': extension_entry, 'preset name': preset_name_entry}

# Button section
# TODO: pass {key: ENTRY_OBJECT_DICT[key].get() for key in ENTRY_OBJECT_DICT.keys() if key != 'preset name'}
ok_button = tk.Button(bottom_frame, text='Ok',
                      command=lambda: general_function_handler(action=action_text_var.get(), base_dir=base_dir_entry.get(),
                                                               prefix=prefix_entry.get(), problem_name=problem_name_entry.get(),
                                                               extension=extension_entry.get()))
ok_button.pack()

def set_base_dir():
    base_dir_entry.delete(0, tk.END)
    # TODO: might be preferable to first ask for directory and save the result in a variable, then delete-insert
    base_dir_entry.insert(0, filedialog.askdirectory())
    return

original_image = Image.open(r'assets\folder_icon.png')
directory_icon = ImageTk.PhotoImage(original_image.resize((16, 16)))
directory_button = tk.Button(label_and_entry_frame, image=directory_icon, command=lambda: set_base_dir())
directory_button.grid(row=1, column=2, sticky='W')


def paste_problem_name():
    problem_name = pyperclip.paste().strip(' \n\r')
    problem_name_entry.delete(0, tk.END)
    problem_name_entry.insert(0, problem_name)

paste_problem_name_button = tk.Button(label_and_entry_frame, text='paste name', command=paste_problem_name)
paste_problem_name_button.grid(row=3, column=2, sticky='EW')


def clear_problem_name():
    problem_name_entry.delete(0, tk.END)

clear_problem_name_button = tk.Button(label_and_entry_frame, text='clear name', command=clear_problem_name)
clear_problem_name_button.grid(row=3, column=3, sticky='EW')


def save_preset():
    param_dict = {}
    for key, entry_object in ENTRY_OBJECT_DICT.items():
        param_dict[key] = entry_object.get()
    if not os.path.isdir('./preset'):
        os.makedirs('./preset')
    # TODO: consider the case where the name is empty
    with open('./preset/' + param_dict['preset name'] + '.txt', 'w') as file:
        for key, value in param_dict.items():
            if not key == 'preset name':
                file.write(key + ': ' + value + '\n')

save_preset_button = tk.Button(label_and_entry_frame, text='save preset', command=save_preset)
save_preset_button.grid(row=6, column=2, sticky='EW')

# TODO: handle the FileNotFoundError when the directory request gets cancelled more gracefully
# TODO: add default preset directory
def choose_preset():
    filename = filedialog.askopenfilename()
    param_dict = {}
    for key in ENTRY_OBJECT_DICT.keys():
        param_dict[key] = None
    with open(filename, 'r') as file:
        param_dict['preset name'] = os.path.basename(file.name)
        for line in file:
            if line.strip() == '':
                continue
            # TODO: use ternary operator for when there are fewer than 2 elements in line.split(': ')
            key, value = line.split(': ', 1)
            param_dict[key] = value.replace('\n', '')
    for key, value in param_dict.items():
        if value is not None:
            if isinstance(ENTRY_OBJECT_DICT[key], tk.StringVar):
                ENTRY_OBJECT_DICT[key].set(value)
            else:
                ENTRY_OBJECT_DICT[key].delete(0, tk.END)
                ENTRY_OBJECT_DICT[key].insert(0, value)

choose_preset_button = tk.Button(label_and_entry_frame, text='choose preset', command=choose_preset)
choose_preset_button.grid(row=6, column=3, sticky='EW')


if __name__ == '__main__':
    saved_base_dir = ''
    root.mainloop()