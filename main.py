# This is a project for an automated file renamer
# TODO: implement GUI
# TODO: make the empty-prefixed calls identity operations for those base directories
# TODO: edit the test files to correctly refer to their main files
# TODO: implement other file management features, like automated file creation

import os


# Rules for prefixes:
# 1. File names are obligated to start with a prefix if there is one.
# 2. Prefixes can't contain any whitespaces, underscores ('_') or digits.
# 3. Prefixes are obligated to be terminated with an underscore

def validate_prefix(prefix):
    return ''.join((char for char in prefix if char not in ' _0123456789'))  # Deleting unwanted characters


def find_end_of_prefix(file):
    for i in range(len(file)):
        if file[i].isdigit():
            return -1  # No prefix found
        elif file[i] == '_':
            return i
    return -1  # No prefix found


def find_end_of_exercise_number(file):
    prefix_end = find_end_of_prefix(file) + 1
    for i in range(prefix_end, len(file)):
        if file[i].isalpha():
            return prefix_end  # No exercise number found
        elif file[i] == '_':
            return i
    return prefix_end  # No exercise number found


def main_file_name(directory, prefix=''):
    res = os.path.basename(directory)
    pos = find_end_of_prefix(res) + 1
    res = res[:pos] + 'f_' + res[pos:]
    # for i in reversed(range(len(res))):
    #     if res[i] == '_':
    #         res = res[:i+1] + prefix + 'f_' + res[i+1:]
    return res


def renamer(base_dir, prefix):
    prefix = validate_prefix(prefix)
    for directory in os.listdir(base_dir):
        prefix_end = find_end_of_prefix(directory) + 1
        new_dir_name = base_dir + '/' + prefix + '_' + directory[prefix_end:]
        directory = base_dir + '/' + directory
        if os.path.isdir(directory):
            for file in os.listdir(directory):
                prefix_end = find_end_of_prefix(file) + 1
                new_file_name = directory + '/' + prefix + '_' + file[prefix_end:]
                os.rename(directory + '/' + file, new_file_name)  # Adding a prefix
                # TODO: probably worth it to find a good way to get rid of this 'if' block
                if file[prefix_end].isalpha():  # Adding a corresponding number to the files with solutions
                    tmp = ''
                    for char in os.path.basename(directory):
                        # TODO: introduce a flag to check if we have stumbled upon a number, and use it to stop the
                        #  loop when we stumble upon an underscore
                        if char.isdigit():
                            tmp += char
                    if tmp != '':
                        tmp += '_'
                    new_name = file[:prefix_end] + tmp + file[
                                                         prefix_end:]  # The 'cutting' point should not be at index 3, but after
                    # the prefix
                    os.rename(directory + '/' + file, directory + '/' + new_name)

            os.rename(directory, new_dir_name)


# TODO: unify this with the renamer function
def imp_adjustment(base_dir):
    for directory in os.listdir(base_dir):
        directory = base_dir + '/' + directory
        if os.path.isdir(directory):
            if 'common' in directory:
                continue
            for file in os.listdir(directory):
                # A check that makes sure that we are dealing with a test file
                if 'test' in file:
                    file_data = ''
                    with open(directory + '/' + file, 'r') as f:
                        file_data = f.read()

                    pos_1 = file_data.find('from') + 5
                    pos_2 = file_data.find('import', pos_1) - 1
                    file_data = file_data[:pos_1] + main_file_name(directory) + file_data[pos_2:]

                    with open(directory + '/' + file, 'w') as f:
                        f.write(file_data)

                else:
                    end_of_exercise_number = find_end_of_exercise_number(file)
                    # In case that we have already marked the file as a file with 'f_', we don't do that again
                    if file[end_of_exercise_number:end_of_exercise_number + 2] != 'f_':
                        new_name = file[:end_of_exercise_number] + 'f_' + file[end_of_exercise_number:]
                        os.rename(directory + '/' + file, directory + '/' + new_name)
                # else:
                #     for i in reversed(range(len(file))):
                #         if file[i] == '_':
                #             new_name = file[:i + 1] + 'f_' + file[i + 1:]
                #             os.rename(directory + '/' + file, directory + '/' + new_name)
                #             break


# The function for transforming names of problems into appropriate file names
# TODO: currently, only supports Leetcode. Need to make it more general.
def get_file_name(problem_name):
    trans_dict = str.maketrans(' ', '_', '.')
    res = problem_name.translate(trans_dict).lower()
    res = res[:res.find('_') + 1] + 'f_' + res[res.find('_') + 1:]
    return res


# TODO: implement automated file creation
def file_creation(base_dir, prefix, problem_name):
    prefix = validate_prefix(prefix)

    main_file_name = prefix + '_' + get_file_name(problem_name)
    directory_name = os.path.join(base_dir, main_file_name.replace('f_', ''))
    test_file_name = main_file_name[:find_end_of_exercise_number(main_file_name)] + '_test.py'

    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)
    try:
        with open(directory_name + '/' + main_file_name + '.py', 'x') as f:
            pass
    except FileExistsError:
        pass

    with open(directory_name + '/' + test_file_name + '.py', 'w') as new_test_file:
        try:
            with open(base_dir + f'/{prefix}_common/{prefix}_test_template.py', 'r') as template:
                for line in template:
                    new_test_file.write(line)
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    # TODO: consider generalising the handling of the method prompt using the function dictionary
    # function_dict = {'renamer': renamer, 'import_adjustment': imp_adjustment, 'file_creation': file_creation}

    while True:
        method = input("Method: ")
        if method == 'renamer':
            base_dir = input("Base directory: ")
            prefix = input("Prefix: ")
            renamer(base_dir, prefix)
        elif method == 'import_adjustment':
            base_dir = input("Base directory: ")
            imp_adjustment(base_dir)
        elif method == 'file_creation':
            base_dir = input("Base directory: ")
            prefix = input("Prefix: ")
            problem_name = input("Problem name: ")
            file_creation(base_dir, prefix, problem_name)