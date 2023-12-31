# This is a project for an automated file renamer
# TODO: make the empty-prefixed calls identity operations for those base directories
# TODO: make choice of extension available
# TODO: consider file name + extension limitations

import os
# from exceptions import EmptyArgsException
from exceptions import EmptyArgsException

# Rules for prefixes:
# 1. File names are obligated to start with a prefix if there is one.
# 2. Prefixes can't contain any whitespaces, underscores ('_') or digits.
# 3. Prefixes are obligated to be terminated with an underscore


def validate_prefix(prefix):
    return ''.join((char for char in prefix if char not in ' _0123456789'))  # Deleting unwanted characters


DEFAULT_EXTENSION = '.py'


def validate_extension(extension):
    if extension == '':
        return DEFAULT_EXTENSION
    else:
        extension = ''.join((char for char in extension if char not in ' _0123456789'))  # Deleting unwanted characters
        if extension[0] != '.':
            extension = '.' + extension
        return extension


def validate_args(**kwargs):
    empty_args = []
    for key, value in kwargs.items():
        if value == '' or value is None:
            empty_args.append(key)
    if empty_args:
        raise EmptyArgsException(empty_args)


def find_end_of_prefix(file):
    for i in range(len(file)):
        if file[i].isdigit():
            return -1  # No prefix found
        elif file[i] == '_':
            return i
    return -1  # No prefix found


def find_end_of_exercise_number_from_file(file):
    prefix_end = find_end_of_prefix(file) + 1
    for i in range(prefix_end, len(file)):
        if file[i].isalpha():
            return prefix_end  # No exercise number found
        elif file[i] == '_':
            return i
    return prefix_end  # No exercise number found


def find_end_of_exercise_number_from_directory(directory):
    return os.path.basename(directory).split('_')[1]


def main_file_name(**kwargs):   # directory, prefix=''
    directory, prefix = kwargs['directory'], kwargs['prefix']
    res = os.path.basename(directory)
    pos = find_end_of_prefix(res) + 1
    res = res[:pos] + 'f_' + res[pos:]
    # for i in reversed(range(len(res))):
    #     if res[i] == '_':
    #         res = res[:i+1] + prefix + 'f_' + res[i+1:]
    return res


def renamer(**kwargs):   # base_dir, prefix
    base_dir, prefix = kwargs['base_dir'], kwargs['prefix']
    prefix = validate_prefix(prefix)
    for directory in os.listdir(base_dir):
        prefix_end = find_end_of_prefix(directory) + 1
        new_dir_name = base_dir + '/' + prefix + '_' + directory[prefix_end:]
        directory = base_dir + '/' + directory
        if os.path.isdir(directory):
            if 'common' not in os.path.basename(directory):
                # TODO: consider a more elegant solution using the split() method
                for file in os.listdir(directory):
                    prefix_end = find_end_of_prefix(file) + 1
                    new_file_name = directory + '/' + prefix + '_' + file[prefix_end:]
                    os.rename(directory + '/' + file, new_file_name)  # Adding a prefix
                    # TODO: probably worth it to find a good way to get rid of this 'if' block
                    # Checking for if the character at the prefix_end is a letter prevents us from adding a
                    # problem number for no good reason
                    if file[prefix_end].isalpha():  # Adding a corresponding number to the files with solutions
                        # tmp = ''
                        # for char in os.path.basename(directory):
                        #     # TODO: introduce a flag to check if we have stumbled upon a number, and use it to stop the
                        #     #  loop when we stumble upon an underscore
                        #     if char.isdigit():
                        #         tmp += char
                        # if tmp != '':
                        #     tmp += '_'
                        problem_number = find_end_of_exercise_number_from_directory(directory)

                        # new_name = file[:prefix_end] + problem_number + file[
                        #                                                 prefix_end:]    # The 'cutting' point should not be at index 3, but after
                        #                                                                 # the prefix

                        if 'test' in os.path.basename(file):
                            file_data = ''
                            with open(directory + '/' + file, 'r') as f:
                                file_data = f.read()

                            pos_1 = file_data.find('from') + 5
                            pos_2 = file_data.find('import', pos_1) - 1
                            file_data = file_data[:pos_1] + main_file_name(directory=directory) + file_data[pos_2:]

                            with open(directory + '/' + file, 'w') as f:
                                f.write(file_data)

                            new_name = file[:prefix_end] + problem_number + file[
                                                                            prefix_end:]    # The 'cutting' point should not be at index 3, but after
                                                                                            # the prefix
                        else:
                            new_name = file[:prefix_end] + problem_number + 'f_' + file[
                                                                                   prefix_end:]     # The 'cutting' point should not be at index 3, but after
                                                                                                    # the prefix
                        os.rename(directory + '/' + file, directory + '/' + new_name)

            os.rename(directory, new_dir_name)


# TODO: unify this with the renamer function
def imp_adjustment(**kwargs):   # base_dir
    base_dir = kwargs['base_dir']
    for directory in os.listdir(base_dir):
        directory = base_dir + '/' + directory
        if os.path.isdir(directory):
            if 'common' in os.path.basename(directory):
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
                    end_of_exercise_number = find_end_of_exercise_number_from_file(file)
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
def get_file_name(problem_name):    # problem_name
    trans_dict = str.maketrans(' ', '_', '.')
    res = problem_name.translate(trans_dict).lower()
    res = res[:res.find('_') + 1] + 'f_' + res[res.find('_') + 1:]
    return res


# TODO: check for errors using a decorator?
# TODO: allow for configurable file extensions
def file_creation(**kwargs):        # base_dir, prefix, problem_name
    base_dir, prefix, problem_name, extension = kwargs['base_dir'], kwargs['prefix'], kwargs['problem_name'], kwargs['extension']
    try:
        validate_args(base_dir=base_dir, prefix=prefix, problem_name=problem_name)
    except EmptyArgsException:
        return

    prefix = validate_prefix(prefix)
    extension = validate_extension(extension)

    main_file_name = prefix + '_' + get_file_name(problem_name)
    directory_name = os.path.join(base_dir, main_file_name.replace('f_', ''))
    test_file_name = main_file_name[:find_end_of_exercise_number_from_file(main_file_name)] + '_test'

    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)

    try:
        with open(directory_name + '/' + main_file_name + extension, 'x') as f:
            pass
    except FileExistsError:
        pass

    with open(directory_name + '/' + test_file_name + extension, 'w') as new_test_file:
        try:
            with open(base_dir + f'/{prefix}_common/{prefix}_test_template' + extension, 'r') as template:
                for line in template:
                    new_test_file.write(line)
        except FileNotFoundError:
            pass


METHODS_DICT = {'renamer': renamer, 'import_adjustment': imp_adjustment, 'file_creation': file_creation}


def general_function_handler(**kwargs): # method, base_dir, prefix, problem_name
    method = kwargs['method']
    del kwargs['method']
    METHODS_DICT[method](**kwargs)


if __name__ == '__main__':
    # TODO: consider generalising the handling of the method prompt using the function dictionary
    # function_dict = {'renamer': renamer, 'import_adjustment': imp_adjustment, 'file_creation': file_creation}

    # TODO: consider allowing users to save some parameters during execution
    while True:

        method = str(input("Method: "))
        if method == 'renamer':
            base_dir = str(input("Base directory: "))
            prefix = str(input("Prefix: "))
            renamer(base_dir=base_dir, prefix=prefix)
        elif method == 'import_adjustment':
            base_dir = str(input("Base directory: "))
            imp_adjustment(base_dir=base_dir)
        elif method == 'file_creation':
            base_dir = str(input("Base directory: "))
            prefix = str(input("Prefix: "))
            problem_name = str(input("Problem name: "))
            file_creation(base_dir=base_dir, prefix=prefix, problem_name=problem_name)