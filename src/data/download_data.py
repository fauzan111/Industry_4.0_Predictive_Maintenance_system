import shutil
import subprocess
from pathlib import Path

REPO_URL = "https://github.com/murtazadroid/Predictive-Maintenance---Remaining-useful-life-prediction-using-CMAPSS-Dataset.git"
RAW_DATA_DIR = Path("data/raw")

import os
import stat
import zipfile

def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    try:
        func(path)
    except Exception:
        pass

def download_data():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if data already exists
    if (RAW_DATA_DIR / "train_FD001.txt").exists():
        print("Data already exists.")
        return

    print(f"Cloning data from {REPO_URL}...")
    temp_dir = RAW_DATA_DIR / "temp_repo"
    
    if temp_dir.exists():
        shutil.rmtree(temp_dir, onerror=on_rm_error)
        
    try:
        subprocess.run(["git", "clone", REPO_URL, str(temp_dir)], check=True)
        
        # Extract zip file
        zip_path = temp_dir / "CMAPSSData.zip"
        if zip_path.exists():
            print("Extracting zip file...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(RAW_DATA_DIR)
            print("Data extracted.")
        else:
            print("Zip file not found in repo.")
        
    except subprocess.CalledProcessError as e:
        print(f"Git clone failed: {e}")
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, onerror=on_rm_error)

if __name__ == "__main__":
    download_data()
