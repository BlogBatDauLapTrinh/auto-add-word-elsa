from posixpath import split, splitdrive
from ppadb.client import Client
import cv2
import matplotlib.pyplot as plt
from time import sleep
import re
import numpy as np

SHOWING_DIALOG = 150
ELSA_MAX_CHARACTER = 128

def is_showing_dialog():
    image = device.screencap()
    with open('screencap.png','wb') as f:
        f.write(image)
    image = cv2.imread('screencap.png',cv2.IMREAD_GRAYSCALE)
    sum_all_pixel = np.sum(image[0:image.shape[0],0:image.shape[1]])
    number_of_pixel = (image.shape[0]*image.shape[1])
    return sum_all_pixel / number_of_pixel < SHOWING_DIALOG

def remove_duplicates_line(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x)) and x]

def clean_script(origin_list):
    # print(origin_list)
    return "".join(origin_list).replace(". ",".").replace("“","").replace("”","").replace('\n','').replace(":",".").replace("?",".")

def join_short_sentence(origin_list):
    idx = 0
    length_list = len(origin_list)
    join_script = ""
    while idx < length_list:
        if idx < length_list - 2 and len(origin_list[idx]) + len(origin_list[idx + 1]) + len(origin_list[idx + 2]) <= ELSA_MAX_CHARACTER:
            join_script += origin_list[idx] +". "+ origin_list[idx + 1] + ". " + origin_list[idx + 2] + "\n"
            idx += 3
        elif idx < length_list - 1 and len(origin_list[idx]) + len(origin_list[idx + 1]) <= ELSA_MAX_CHARACTER:
            join_script += origin_list[idx] +". "+ origin_list[idx + 1] + "\n"
            idx += 2
        else:
            # if(len(origin_list[idx]) > ELSA_MAX_CHARACTER):
            #     print(origin_list[idx])
            #     splitted_long_setence = origin_list[idx].split(",",0)
            #     for sub_sentence in splitted_long_setence:
            #         join_script += sub_sentence + "\n"
            join_script += origin_list[idx] + "\n"
            idx += 1
    return join_script

adb = Client()
devices = adb.devices()
if(len(devices)==0):
    print('no device dettach')
device = devices[0]


with open('listword.txt', 'r') as f:
    unique_lines = remove_duplicates_line(f.readlines())
    clean_script = clean_script(unique_lines)
    splitted_script = clean_script.split(".")
    splitted_script = join_short_sentence(splitted_script)

with open("clean_list_word.txt",'w') as f:
    for single_line in splitted_script:
        f.writelines(f"{single_line}")

for w in splitted_script.split("\n"):
    device.shell('input tap 600 1000')
    device.shell('input tap 600 400')
    print(w+"endl")
    device.shell(f'input text "{w}"')
    device.shell('input keyevent 66')
    
    while(is_showing_dialog()):
        sleep(0.1)

    device.shell('input tap 920 700')
    while(is_showing_dialog()):
        sleep(0.1)
