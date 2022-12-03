import os
from pathlib import Path
from PIL import Image
from tqdm import tqdm


src_root = "/Users/mithrandir/avanpost_hackaton/data/imagenet/ILSVRC/Data/CLS-LOC/train/"
# src_root = "/Users/mithrandir/avanpost_hackaton/data/snowboard/"
dst_root = "/Users/mithrandir/avanpost_hackaton/data/resized/"

for dirpath, dirnames, filenames in tqdm(os.walk(src_root)):
    if dirpath.split("/")[-1] not in ["n04389033"]:
        continue
    for filename in tqdm(filenames):
        src_path = os.path.join(dirpath, filename)
        dst_path = Path(os.path.join(dst_root, src_path[len(src_root):])).with_suffix(".jpg")
        # dst_path = Path(os.path.join(dst_root, src_path.lstrip(src_root))).with_suffix(".jpg")
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src_path) as img:
            img: Image.Image
            img = img.resize((224, 224))
            img.save(dst_path, "jpeg")
