import sys
import os
import imghdr
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

BASE_DIR = "{Your Directory Path}"
SUC_LOG = "success.log"
ERR_LOG = "error.log"

rename_list = []

# 指定したフォルダのフォルダリストを返す
def get_dirs(path):
    files = os.listdir(path)
    ret_dirs = [d for d in files if (os.path.isdir(os.path.join(path,d)))]
    return ret_dirs

# 指定したフォルダのファイルのフルパスリストを返す
def get_fullpath_files(path):
    files = os.listdir(path)
    ret_files = [os.path.join(path,f) for f in files if (os.path.isfile(os.path.join(path,f)))]
    return ret_files

def logoutput(filename,text):
    with open(filename,'at') as f:
        f.write(text + '\r\n')

def get_exif(lists):
    field ="DateTimeOriginal" # 入手したいExifのデータ種類
    exif_data = {}

    for list in lists:
        # 画像形式のファイルのみ処理
        if imghdr.what(list) == "jpeg":
            im = Image.open(list) # 画像の取得
            exif = im._getexif() # 画像からExifデータを抽出

            # Exifデータから特定のデータのみ抽出
            try:
                for id, value in exif.items():
                    if TAGS.get(id) == field:
                        exif_data[list] = value
            except:
                logoutput(ERR_LOG,list + " error info:" + str(sys.exc_info()))

            # exif情報から日付が取得できない場合エラーリストに追加
            if list not in exif_data:
                logoutput(ERR_LOG,list + " error info:" + "can't get date information")
            im.close()
        else:
            # JPEG形式ではないファイルをエラーリストに追加
            logoutput(ERR_LOG,list + " error info:" + "not jpeg")

    return exif_data

def rename_file(dicts):
    for key,value in dicts.items():
        try:
            os.rename(key, os.path.dirname(key) + "/" + value.replace(":","").replace(" ","") + "." + imghdr.what(key))
            logoutput(SUC_LOG,key)
        except:
            # ファイル名が重複したなどのエラー時にエラーリストに追加
            logoutput(ERR_LOG,list + " error info:" + str(sys.exc_info()))

def main():
    print("start")
    root_dir = []
    root_dir = get_dirs(BASE_DIR)
    for d in root_dir:
        rename_list.extend(get_fullpath_files(BASE_DIR + d))
        
    rename_file(get_exif(rename_list))
    print("finished")

if __name__ == "__main__":
    main()

