import json
import os
import shutil

"""
该脚本用于将slst中的曲目移出assets文件夹，请注意该脚本对应的slst是需要移走的文件
"""


def extract_values_by_key(data, key):
    return [item[key] for item in data if key in item]


def move_folders_by_name(source_directory, destination_directory, folder_name):
    # 检查目标目录是否存在，不存在则创建
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    for folder in os.listdir(source_directory):
        source_path = os.path.join(source_directory, folder)
        if os.path.isdir(source_path) and folder == folder_name:
            destination_path = os.path.join(destination_directory, folder)
            try:
                shutil.move(source_path, destination_path)
                print(f"Moved folder: {source_path} to {destination_path}")
            except Exception as e:
                print(f"Failed to move {source_path}: {e}")


file = open("slst.json","r",encoding="utf-8")
data_list = json.loads(file.read())
names = extract_values_by_key(data_list["songs"], 'id')

source_directory = 'C:/Users/Arcti/Desktop/server/assets/songs'
destination_directory = 'C:/Users/Arcti/Desktop/server/assets_official/songs'

for song in names:
    song = "dl_" + song
    move_folders_by_name(source_directory, destination_directory, song)
