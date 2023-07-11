# This is a project for an automated file renamer
# TODO: allow for the user to input the arguments using a console
# TODO: implement GUI

import os


def renamer(prefix, base_dir):
    for directory in os.listdir(base_dir):
        if os.path.isdir(directory):
            new_dir_name = prefix + '_' + directory
            os.rename(directory, new_dir_name)
            for file in os.listdir(directory):
                new_file_name = directory + '/' + prefix + '_' + file
                os.rename(directory + '/' + file, new_file_name)


if __name__ == '__main__':
    pass