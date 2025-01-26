import json
import os
import shutil
import sqlite3
from specialcharts import aprilfool, speedup, official

debug_mode = False  # 设为False减少cli输出内容
copy = False


def plstcheck(plst):
    packs = set()
    for pack in plst["packs"]:
        packs.add(pack["id"])

    return packs


def slst_remake(slst):
    # 定义初始变量
    normal_list = []
    speedup_list = []
    aprilfool_list = []
    practice_list = []

    num = 0
    spnum = 800
    apnum = 1000
    packs = set()

    # 各版本时间戳
    ver047 = 1692835200
    ver048 = 1695513600
    ver050 = 1700784000
    ver060 = 1707523200
    ver070 = 1711929600
    ver080 = 1719792000
    ver100 = 1722816000
    ver110 = 1727654400
    ver120 = 1728864000
    ver130 = 1732291200
    ver140 = 1736596800

    for song in slst["songs"]:
        # idx分类并排序
        if song.get("idx") is not None:  # 检测有没有idx字段
            if song["id"] not in aprilfool and song["id"] not in speedup:
                song["idx"] = num
                num += 1
                normal_list.append(song)
                if debug_mode:
                    print(song["idx"], song["id"])
        else:  # 特殊标级处理
            for diff in song["difficulties"]:
                if diff["ratingClass"] in range(2, 4):
                    diff["rating"] = -2  # 练
            practice_list.append(song)

        if song["id"] in speedup:
            song["difficulties"][2]["rating"] = -3  # 倍
            song["idx"] = spnum
            spnum += 1
            speedup_list.append(song)

        if song["id"] in aprilfool:
            song["difficulties"][2]["rating"] = -4  # 愚
            song["idx"] = apnum
            apnum += 1
            aprilfool_list.append(song)

        # 根据服务器数据库中的定数规范常规谱面标级
        # db = sqlite3.connect('arcaea_database.db')
        # cursor = db.cursor()
        # cursor.execute("SELECT * FROM chart WHERE song_id = ?", (song["id"],))
        # ratings = list(cursor.fetchone()[2:7])
        # rtcls = 0
        # for rating in ratings:
        #     if rating == -1:
        #         if rtcls > 2:
        #             if len(song["difficulties"]) < 3:
        #                 print(f"{song["id"]}的{rtcls}难度不存在，请修正")
        #         rtcls += 1
        #         continue
        #     elif rating == 0:
        #         rtcls += 1
        #         continue
        #     else:
        #         try:
        #             if rtcls == 4:
        #                 song["difficulties"][rtcls - 1]["rating"] = int(rating / 10)
        #                 print(song["id"], rtcls, song["difficulties"][rtcls - 1]["rating"])
        #                 if rating % 10 > 4:
        #                     song["difficulties"][rtcls - 1]["ratingPlus"] = True
        #                 else:
        #                     song["difficulties"][rtcls - 1]["ratingPlus"] = False
        #             else:
        #                 song["difficulties"][rtcls]["rating"] = int(rating / 10)
        #                 print(song["id"],rtcls,song["difficulties"][rtcls]["rating"])
        #                 if rating % 10 > 4:
        #                     song["difficulties"][rtcls]["ratingPlus"] = True
        #                 else:
        #                     song["difficulties"][rtcls]["ratingPlus"] = False
        #         except IndexError:
        #             pass
        #         rtcls += 1


        # pst prs标x
        for diff in song["difficulties"]:
            if diff["ratingClass"] in range(0, 2):
                diff["rating"] = -1  # ×

        #设定特殊字段version
        if song["set"] == "base":
            song["version"] = "Arcaea Official"
        if song["set"] == "single":
            song["version"] = "慢速练习"
        if song["set"] == "parts" and song["version"] != "赛博字帖":
            song["version"] = "切片练习"

        # 时间戳排序
        try:
            if song["version"] == "1.4":
                song["date"] = ver140
                ver140 += 1
            elif song["version"] == "1.3":
                song["date"] = ver130
                ver130 += 1
            elif song["version"] == "1.2":
                song["date"] = ver120
                ver120 += 1
            elif song["version"] == "1.1":
                song["date"] = ver110
                ver110 += 1
            elif song["version"] == "1.0":
                song["date"] = ver100
                ver100 += 1
            elif song["version"] == "0.8":
                song["date"] = ver080
                ver080 += 1
            elif song["version"] == "0.7":
                song["date"] = ver070
                ver070 += 1
            elif song["version"] == "0.6":
                song["date"] = ver060
                ver060 += 1
            elif song["version"] == "0.5":
                song["date"] = ver050
                ver050 += 1
            elif song["version"] == "0.4.8":
                song["date"] = ver048
                ver048 += 1
            elif song["version"] == "0.4.7":
                song["date"] = ver047
                ver047 += 1
            else:
                song["date"] = ver070
                ver070 += 1
        except Exception:
            print(song["id"])

        # 光侧自动加换侧
        if song["side"] == 0 and not song.get("bg_inverse"):
            if song["bg"] == 'zettai':
                song["bg_inverse"] = song["bg"] + 'light'
            elif song["bg"] in ['testify', 'epilogue']:
                song["bg_inverse"] = 'finale_conflict'
            elif song["bg"][-5:] == 'light':
                song["bg_inverse"] = song["bg"][:-5] + 'conflict'
            else:
                song["bg_inverse"] = 'byd_2_conflict'


        # 记录曲包名称
        packs.add(song["set"])

    # 倍速愚人节统一放最后
    for sp in speedup_list:
        sp["idx"] = num
        num += 1
        if debug_mode:
            print(sp["idx"], sp["id"])

    for ap in aprilfool_list:
        ap["idx"] = num
        num += 1
        if debug_mode:
            print(ap["idx"], ap["id"])

    # 按顺序写入新slst
    new_slst = {"songs": []}

    new_slst["songs"].extend(normal_list)
    new_slst["songs"].extend(speedup_list)
    new_slst["songs"].extend(aprilfool_list)
    new_slst["songs"].extend(practice_list)

    new_slst_json = json.dumps(new_slst, ensure_ascii=False)
    file2 = open("songlist.json", "w", encoding="utf-8")
    file2.write(new_slst_json)
    file2.flush()
    file2.close()

    return num - 1, packs, practice_list


def check(slst, destination_dir):
    packs = set()
    global copy

    # 获取源目录下的所有文件夹
    path = "C:\\Users\\Arcti\\Desktop\\server\\assets\\songs"

    all_folders = [folder for folder in os.listdir(path) if
                   os.path.isdir(os.path.join(path, folder))]

    for song in slst["songs"]:
        song_id = song["id"]
        if song.get("remote_dl"):
            match_string = "dl_" + song_id
        else:
            match_string = song_id

        # 筛选与输入字符串匹配的文件夹
        matching_folders = [folder for folder in all_folders if match_string in folder]

        # 创建目标目录，如果不存在的话
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # 复制匹配的文件夹到目标目录

        if matching_folders:
            if copy:
                source_path = os.path.join(path, matching_folders[0])
                destination_path = os.path.join(destination_dir, matching_folders[0])
                try:
                    shutil.copytree(source_path, destination_path)
                except Exception:
                    pass
            else:
                continue
        else:
            print(f"{song_id}文件夹不匹配，请修改")
        # 检测曲包变动
        packs.add(song["set"])


def check_folders(directory, target_str, required):
    """
    检查目录下所有与传入字符串匹配的文件夹是否都包含指定的文件。

    参数：
    - directory: 目标目录的路径
    - target_string: 要匹配的字符串
    - required_files: 必须存在的文件列表

    返回值：
    如果所有匹配的文件夹都包含指定的文件，则返回 True，否则返回 False，并输出不符合要求的文件夹名称。
    """
    matching_folders = [folder for folder in os.listdir(directory) if target_str in folder]

    if not matching_folders:
        print(f"No folders found matching the string '{target_str}'.")
        return False

    non_compliant_folders = []

    for folder in matching_folders:
        missing_files = [file for file in required if not os.path.exists(os.path.join(directory, folder, file))]
        if missing_files:
            # 如果缺失的文件中包含"base.jpg"或"base_256.jpg"，再次扫描文件夹内容
            if "base.jpg" in missing_files or "base_256.jpg" in missing_files:
                additional_files = ["1080_base.jpg", "1080_base_256.jpg"]
                for file in additional_files:
                    if os.path.exists(os.path.join(directory, folder, file)):
                        missing_files.remove("base.jpg")
                        missing_files.remove("base_256.jpg")
                        break

            # 如果缺失的文件中包含"3.jpg"或"3_256.jpg"，再次扫描文件夹内容
            if "3.jpg" in missing_files or "3_256.jpg" in missing_files:
                additional_files = ["1080_3.jpg", "1080_3_256.jpg"]
                for file in additional_files:
                    if os.path.exists(os.path.join(directory, folder, file)):
                        missing_files.remove("3.jpg")
                        missing_files.remove("3_256.jpg")
                        break

            if missing_files:
                non_compliant_folders.append((folder, missing_files))

    if not non_compliant_folders:
        return True
    else:
        for folder, missing_files in non_compliant_folders:
            print(f"- {folder}:\t 缺失文件: {', '.join(missing_files)}")
        return False
