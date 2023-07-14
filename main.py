# This is a project for an automated file renamer
# TODO: implement GUI
# TODO: make the empty-prefixed calls identity operations for those base directories
# TODO: edit the test files to correctly refer to their main files
# TODO: implement other file management features

import os


# Rules for prefixes:
# 1. File names are obligated to start with a prefix if there is one.
# 2. Prefixes can't contain any underscores ('_') or digits.
# 3. Prefixes are obligated to be terminated with an underscore

def validate_prefix(prefix):
    return ''.join((char for char in prefix if char not in '_0123456789'))


def main_file_name(directory, prefix=None):
    res = os.path.basename(directory)
    for i in reversed(range(len(res))):
        if res[i] == '_':
            res = res[:i+1] + prefix + 'f_' + res[i+1:]
    return res


def find_end_of_prefix(file):
    for i in range(len(file)):
        if file[i].isdigit():
            return -1           # No prefix found
        elif file[i] == '_':
            return i
    return -1                   # No prefix found


def find_end_of_exercise_number(file):
    prefix_end = find_end_of_prefix(file) + 1
    for i in range(prefix_end, len(file)):
        if file[i].isalpha():
            return prefix_end
        elif file[i] == '_':
            return i
    return prefix_end


def renamer(prefix, base_dir):
    prefix = validate_prefix(prefix)
    for directory in os.listdir(base_dir):
        new_dir_name = base_dir + '/' + prefix + '_' + directory
        directory = base_dir + '/' + directory
        if os.path.isdir(directory):
            for file in os.listdir(directory):
                # TODO: find current prefix end and edit that
                prefix_end = find_end_of_prefix(file) + 1
                if prefix != '':
                    new_file_name = directory + '/' + prefix + '_' + file[prefix_end:]
                    os.rename(directory + '/' + file, new_file_name)   # Adding a prefix
                # TODO: probably worth it to find a good way to get rid of this 'if' block
                if file[prefix_end].isalpha():   # Adding a corresponding number to the files with solutions
                    tmp = ''
                    for char in directory:
                        if char.isdigit():
                            tmp += char
                    if tmp != '':
                        tmp += '_'
                    new_name = file[:prefix_end] + tmp + file[prefix_end:]      # The 'cutting' point should not be at index 3, but after
                                                                                # the prefix
                    os.rename(directory + '/' + file, directory + '/' + new_name)

            os.rename(directory, new_dir_name)

# TODO: unify this with the renamer function
def imp_adjustment(base_dir):
    for directory in os.listdir(base_dir):
        directory = base_dir + '/' + directory
        if os.path.isdir(directory):
            for file in os.listdir(directory):
                # A check that makes sure that we are dealing with a test file
                if 'test' in file:
                    file_data = ''
                    with open(directory + '/' + file, 'r') as f:
                        file_data = f.read()

                    pos_1 = file_data.find('from') + 5
                    pos_2 = file_data.find('import') - 1
                    file_data = file_data[:pos_1] + main_file_name(directory) + file_data[pos_2:]

                    with open(directory + '/' + file, 'w') as f:
                        f.write(file_data)
                else:
                    for i in reversed(range(len(file))):
                        if file[i] == '_':
                            new_name = file[:i + 1] + 'f_' + file[i + 1:]
                            os.rename(directory + '/' + file, directory + '/' + new_name)
                            break


if __name__ == '__main__':
    while True:
        method = input("Method: ")
        if method == 'renamer':
            prefix = input("Prefix: ")
            base_dir = input("Base directory: ")
            renamer(prefix, base_dir)
        elif method == 'import_adjustment':
            base_dir = input("Base directory: ")
            imp_adjustment(base_dir)
