import os
import shutil


label_to_folders = {
    # "tracktor": ["n04465501", "n04465501"],
    # "mower": ["n03649909"],
    # "bike": ["n03792782"],
    # "showboard": ["snowboard"],
    # "ski": ["n04228054"],
    # "truck": ["n03417042", "n04467665"],
    # "minibus": ["n03769881"],
    # "train": ["n02917067"],
    # "pickup": ["n03930630", "n04461696"],
    # "horse": ["n03538406"],
    # "unknown": ["n02980441", "n02093991", "n04409515"],
    "tank": ["n04389033"]
}
src_root = "/Users/mithrandir/avanpost_hackaton/data/resized/"
dst_root = "/Users/mithrandir/avanpost_hackaton/data/final/"


for label, folders in label_to_folders.items():
    dst_folder = os.path.join(dst_root, label) + "/"
    for folder in folders:
        src_folder = os.path.join(src_root, folder) + "/"
        shutil.copytree(src_folder, dst_folder, dirs_exist_ok=True)
