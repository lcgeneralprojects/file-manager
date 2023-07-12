# This is a project for an automated file renamer
# TODO: implement GUI
# TODO: make the empty-prefixed calls identity operations for those base directories

import os


def renamer(prefix, base_dir):
    for directory in os.listdir(base_dir):
        if os.path.isdir(base_dir + '/' + directory):
            for file in os.listdir(base_dir + '/' + directory):
                if prefix != '':
                    new_file_name = base_dir + '/' + directory + '/' + prefix + '_' + file
                    os.rename(base_dir + '/' + directory + '/' + file, new_file_name)   # Adding a prefix
                # TODO: probably worth it to find a good way to get rid of this 'if' block
                if file[3].isalpha():   # Adding a corresponding number to the files with solutions
                    tmp = ''
                    for char in directory:
                        if char.isdigit():
                            tmp += char
                    if tmp != '':
                        tmp += '_'
                    new_name = file[:3] + tmp + file[3:]    # The 'cutting' point should not be at index 3, but after
                                                            # the prefix
                    os.rename(base_dir + '/' + directory + '/' + file, base_dir + '/' + directory + '/' + new_name)
            new_dir_name = base_dir + '/' + prefix + '_' + directory
            os.rename(base_dir + '/' + directory, new_dir_name)


if __name__ == '__main__':
    prefix = input("Prefix: ")
    base_dir = input("Base directory: ")
    renamer(prefix, base_dir)
