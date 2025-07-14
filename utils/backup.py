import shutil
import os

def backup_data(src_dir, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    shutil.copytree(src_dir, backup_dir, dirs_exist_ok=True)

def restore_data(backup_dir, dst_dir):
    shutil.copytree(backup_dir, dst_dir, dirs_exist_ok=True)