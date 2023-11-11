# file-manager
Personal automated mass directory and file management project developed for faster workflow when dealing with problemsets from various sites.

Currently allows the user to perform the following actions:
- Rename directories and files - renames files and directories in an encompassing directory to be of the format encompassing_directory/prefix+problem_number+problem_name/prefix+problem_number+'f_'+problem_name+extension, also adjusts the names of the relevant test files if such are present to the format prefix+problem_number+test+extension
- Create directories and files - creates a directory and a file in an encompassing directory with names of the format encompassing_directory/prefix+problem_number+problem_name/prefix+problem_number+'f_'+problem_name+extension, as well as a test file with the name prefix+problem_number+'test'+extension, and writes into that file the context of a test template in encompassing_directory/prefix+'common'/prefix+'test_template'
- Adjust import sections in files - changes the files from which the importation happens, to be rolled into the 'rename' action.