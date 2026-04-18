import os
import zipfile
import tarfile
import requests
import gdown
import subprocess
import shutil
from pathlib import Path
from tqdm import tqdm

class DatasetManager:
    def __init__(self):
        self.data_dir = Path(__file__).parent.resolve()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def _check_space(self, total_size_bytes: int, filename: str | None = None):
        if total_size_bytes > 0:
            required_bytes = total_size_bytes * 2.5
            total, used, free = shutil.disk_usage(self.data_dir)
            
            if free < required_bytes:
                req_gb = required_bytes / (1024**3)
                free_gb = free / (1024**3)
                print(f"[Error] No Space for {self.data_dir if filename is None else filename}! Needed ~{req_gb:.1f}GB, available {free_gb:.1f}GB.")
                return True
        return False

    def download_file(self, url: str, filename: str):
        filepath = self.data_dir / filename
        try:
            response = requests.get(url, stream=True)
            total_size_bytes = int(response.headers.get('content-length', 0))

            if filepath.exists():
                local_size = filepath.stat().st_size
                
                if total_size_bytes > 0 and local_size == total_size_bytes:
                    print(f"[Exist] {filename}")
                    return filepath
                else:
                    print(f"[Warning] {filename} sizes is not equal (Local: {local_size} B, Server: {total_size_bytes} B).")
                    # os.remove(filepath)

            print(f"[Download] {filename}...")

            if self._check_space(total_size_bytes, filename):
                return None

            print(f"[Download] {filename} ({(total_size_bytes / 1024**3):.1f} GB)...")
            
            if shutil.which("axel") is None:
                print("[Error] 'axel' is not installed! Write: sudo apt install axel")
                return None

            result = subprocess.run(
                ["axel", "-n", "16", "-a", "-o", str(filepath), url],
                check=True
            )

            # with open(filepath, "wb") as f, tqdm(
            #     total=total_size_bytes, unit='B', unit_scale=True, desc=filename
            # ) as pbar:
            #     for data in response.iter_content(chunk_size=8192):
            #         f.write(data)
            #         pbar.update(len(data))
                    
            print(f"[Download Done] {filename}")
            return filepath
            
        except Exception as e:
            print(f"[Error] Cannot install {filename}: {e}")
            return None

    def download_from_drive(self, drive_id: str, filename: str):
        filepath = self.data_dir / filename
        
        if filepath.exists():
            print(f"[EXIST] {filename}")
            return filepath

        print(f"[DOWNLOAD] Fetching {filename} from Google Drive...")
        try:
            output_path = str(filepath)
            gdown.download(id=drive_id, output=output_path, quiet=False)
            
            if filepath.exists() and filepath.stat().st_size > 1000:
                print(f"[DONE] {filename}")
                return filepath
            else:
                print(f"[ERROR] Failed to download {filename} or file is corrupted.")
                if filepath.exists(): 
                    filepath.unlink()
                return None
                
        except Exception as e:
            print(f"[ERROR] gdown exception for {filename}: {e}")
            return None

    def unpack(self, filepath: Path | None, dirname: str | None = None):
        if not filepath or not filepath.exists(): return
        
        folder_name = dirname if dirname else filepath.stem
        extract_to = self.data_dir / folder_name

        print(f"[Unpack] {filepath.name}...")
        if filepath.suffix == '.zip':
            with zipfile.ZipFile(filepath, 'r') as ref:
                ref.extractall(extract_to)
        elif filepath.suffix in ['.gz', '.tgz', '.tar']:
            with tarfile.open(filepath, 'r:gz') as ref:
                ref.extractall(extract_to)
        
        print(f"[Unpack Done] {filepath.name} to {extract_to}")
        print(f"[Delete by yourself if not needed] {filepath}")

if __name__ == "__main__":
    manager = DatasetManager()

    coco_train_url = "http://images.cocodataset.org/zips/train2017.zip"
    coco_zip = manager.download_file(coco_train_url, "train2017.zip")
    manager.unpack(coco_zip, "coco_train_2017")

    ncd_zip = manager.download_from_drive("1nUOw-lQ6EN5ZWTZT8opZ1dSKn6h56Bkf", "NCD_Dataset.zip")
    manager.unpack(ncd_zip, "NCD")

    coco_val_url = "http://images.cocodataset.org/zips/val2017.zip"
    coco_val_zip = manager.download_file(coco_val_url, "val2017.zip")
    manager.unpack(coco_val_zip, "coco_val_2017")

    flowers_url = "https://www.robots.ox.ac.uk/~vgg/data/flowers/102/102flowers.tgz"
    flowers_tgz = manager.download_file(flowers_url, "flowers.tgz")
    manager.unpack(flowers_tgz, "flowers")

    print("\n[Done]")