import os.path as osp
import glob
from fastreid.data.datasets import DATASET_REGISTRY
from fastreid.data.datasets.bases import ImageDataset
import re
import csv
import os    
import xml.etree.ElementTree as ET
import chardet
@DATASET_REGISTRY.register()
class AIC19(ImageDataset):
    dataset_name = "AIC19"  # Name the dataset as "AIC19"

    def __init__(self, root="datasets", **kwargs):
        self.root = root
        self.dataset_dir = osp.join(self.root, self.dataset_name)
        self.train_dir = osp.join(self.dataset_dir, "new_sets", "train")  # Directory for the train set
        self.query_dir = osp.join(self.dataset_dir, "new_sets", "query")  # Directory for the query set
        self.gallery_dir = osp.join(self.dataset_dir, "new_sets", "test")  # Directory for the gallery set

        required_files = [self.train_dir, self.query_dir, self.gallery_dir]
        self.check_before_run(required_files)

        train = self.process_dir(self.train_dir, is_train=True)
        query = self.process_dir(self.query_dir, is_train=False)
        gallery = self.process_dir(self.gallery_dir, is_train=False)

        super().__init__(train, query, gallery, **kwargs)











    def detect_encoding(self, file_path):
        with open(file_path, "rb") as file:
            raw_data = file.read()

        result = chardet.detect(raw_data)
        return result["encoding"]

    def process_dir(self, dir_path,is_train):
        img_paths = glob.glob(os.path.join(dir_path, "*.jpg"))
        data = []

        label_file_path = "datasets/AIC19/train_label.xml"

        # Detect the encoding of the file
        encoding = self.detect_encoding(label_file_path)

        # Parse the XML file with the detected encoding
        tree = ET.parse(label_file_path, parser=ET.XMLParser(encoding=encoding))
        root = tree.getroot()

        label_dict = {}
        for item in root.findall(".//Item"):
            img_name = item.get("imageName")
            vehicle_id = item.get("vehicleID")
            camera_id = item.get("cameraID")
            label_dict[img_name] = (int(vehicle_id), camera_id)

        for img_name in img_paths:
            if img_name.endswith(".jpg"):
                img_name = os.path.basename(img_name)
                img_path = os.path.join(dir_path, img_name)

                pid, camera_id = label_dict.get(img_name, (None, None))
                camid = int(camera_id[1:]) if camera_id is not None else -1
                pid = int(pid) if pid is not None else -1

                # Required form for train set
                if is_train:
                    pid = self.dataset_name + "_" + str(pid)
                    camid = self.dataset_name + "_" + str(camid)
                data.append((img_path, pid, camid))

        return data








