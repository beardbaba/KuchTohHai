import shutil
import os
import glob

# dictionary mapping with each extensions with its corresponding folders

extensions = {
    "jpg": "image",
    "png": "image",
    "gif": "image",
    "mp3": "audio",
    "wav": "audio",
    "mp4": "video",
    "mov": "video",
    "txt": "text",
    "docx": "word",
    "pdf": "pdf",
    "xlsx": "excel",
    "csv": "excel",
    "pptx": "presentation",
    "ppt": "presentation",
    "zip": "archive",
    "rar": "archive",
    "gz": "archive",
    "tar": "archive",
    "exe": "programs",
    "py": "python",
    "ipynb": "python",
}


path = r"C:\Users\Virendra Pratap\Downloads"  # here r is used to specify raw since py assumes \ as special characters. therefore by mentioning \ it takes as raw

# setting verbose to 1(or True) will show all file moves
# setting verbose to 0(or False) will show all basic necessary info

verbose = 0

for extension, folder_name in extensions.items():
    # get all the files matching the extension
    files = glob.glob(os.path.join(path, f"*.{extension}"))
    print(f"[*] Found {len(files)} files with {extension} extension")
    if not os.path.isdir(os.path.join(path, folder_name)) and files:
        # create the folder if it doesn't exist
        print(f"[+] Making {folder_name} folder")
        os.makedirs(os.path.join(path, folder_name))
    for file in files:
        # for each file in that extension, move it to the corresponding folder
        basename = os.path.basename(file)
        new_path = os.path.join(path, folder_name, basename)
        if verbose:
            print(f"[*] Moving {file} to {new_path}")
        shutil.move(file, new_path)
