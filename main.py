from funcs import slst_remake, plstcheck, check, check_folders
from create_server_database import db_items, db_charts
from update_database import update_db
import json

"""
请提前修改路径！！！
并将服务端的arcaea_database.db拷贝至项目文件夹
"""
# assets文件路径
directory_path = "C:\\Users\\Arcti\\Desktop\\server\\assets\\songs"
destination_dir = "C:\\Users\\Arcti\\Desktop\\server\\assets"

# 文件处理
try:
    file = open(directory_path + '\\songlist', "r", encoding="utf-8")
    file2 = open(directory_path + '\\packlist', "r", encoding="utf-8")
except Exception as e:
    print("slst或plst不存在，请检测目录中是否存在该文件")
    print(e)
else:
    songlist = json.loads(file.read())
    packlist = json.loads(file2.read())
    file.close()
    file2.close()

    # 重新生成slst并检查文件
    num, packs, practice_list = slst_remake(songlist)
    plst = plstcheck(packlist)

    print("slst生成完毕，在本级目录，新文件名为songlist.json")
    print(f"共检测到{num}首可联机曲目，{len(practice_list)}首慢速练习曲目与切片，共{num + len(practice_list)}首")
    print(f"slst中共检测到{len(packs)}个曲包")
    print(f"plst中共检测到{len(plst)}个曲包\n")

    if packs == plst:
        print("plst无需更改")
    else:
        set1 = plst.difference(packs)
        set2 = packs.difference(plst)
        set2.remove("single")
        if set1:
            print(f"请移除packlist中的以上曲包{set1}")
        if set2:
            print(f"请在packlist中添加以上曲包{set2}")

    # 检查文件夹中内容
    for song in songlist["songs"]:
        required_files = ["base_256.jpg", "base.jpg"]

        try:
            if song["remote_dl"]:
                target_string = "dl_" + song["id"]
                required_files.append("preview.ogg")
            else:
                target_string = song["id"]
                required_files.append("base.ogg")
        except Exception:
            target_string = song["id"]

        count = 0
        for diff in song["difficulties"]:
            count += 1
            if count == 4:
                for key in diff.keys():
                    if key == "audioOverride":
                        required_files.append("3_preview.ogg")
                    if key == "jacketOverride":
                        required_files.append("3.jpg")
                        required_files.append("3_256.jpg")


        # try:
        #     if song["difficulties"][3]["audioOverride"]:
        #         required_files.append("3_preview.ogg")
        #     if song["difficulties"][3]["jacketOverride"]:
        #         required_files.append("3.jpg")
        # except Exception:
        #     pass

        check_folders(directory_path, target_string, required_files)

    check(songlist, destination_dir)


    print("\n记得把songlist.json扔编辑器里格式化一下去掉后缀再丢进去")

    if input("若检查无误，请输入 Y 以开始服务器数据库生成") == ('Y' or 'y'):
        file3 = open("songlist.json", "r", encoding="utf-8")
        new_slst = json.loads(file3.read())
        file3.close()

        db_charts(new_slst)
        db_items(new_slst, packlist)
        update_db('new_database.db', 'arcaea_database.db', 'charts', 'chart', 'song_id')

        print("\n新数据库已导出至new_database.db，请手动更新新曲目至服务器")

print("Made by caqtzesthesium")
