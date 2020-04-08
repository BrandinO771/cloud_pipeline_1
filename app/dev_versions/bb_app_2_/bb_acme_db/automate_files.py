
import os
import glob


files_in_dir = glob.glob("data/*")
file_name_set = set()
files_bundle = []

for file in files_in_dir :

    split_raw_path = (file.split("\\"))
    print("the full path is", file)
    # print("the raw_path", raw_path)
    file_name= (split_raw_path[1])
    # print("this is file_name", file_name)
    try:
        files_bundle.append(file_name)
        # file_name_set.add( file_name)
        # print("final_name_set =", file_name_set  )      
        # print(file)
        # print(file_names)
    except IndexError :
        ConnectionRefusedError
print("the file names are", files_bundle)

# print(file_name_set)


# def createDirs():
#     for dir in extension_set:
#         try:
#             os.makedirs(dir+"_files")
#         except FileExistsError:
#             continue

# def arrange():
#     for file in files_list :
#         f_extension = file.split(sep=".")
#         try:
#             os.rename(file, f_extension[1]+"_files/"+file)
#         except (OSError, IndexError):
#             continue

# createDirs()
# arrange()