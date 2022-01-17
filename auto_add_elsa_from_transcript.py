from distutils.command.clean import clean
from ppadb.client import Client
import cv2
import matplotlib.pyplot as plt
from time import sleep
import numpy as np

SHOWING_DIALOG = 150
ELSA_MAX_CHARACTER = 128

def is_showing_dialog():
    sleep(0.05)
    image = device.screencap()
    with open('images/screencap.png', 'wb') as f:
        f.write(image)
    image = cv2.imread('images/screencap.png', cv2.IMREAD_GRAYSCALE)
    sum_all_pixel = np.sum(image[0:image.shape[0], 0:image.shape[1]])
    number_of_pixel = (image.shape[0]*image.shape[1])
    return sum_all_pixel / number_of_pixel < SHOWING_DIALOG

def take_screenshot():
    image = device.screencap()
    with open('images/screencap.png', 'wb') as f:
        f.write(image)

def get_add_phrase_position():
    image = cv2.imread('images/screencap.png', 0)
    template = cv2.imread('images/add_phrase.png', 0)
    w, h = template.shape[::-1]
    method = eval("cv2.TM_CCORR_NORMED")
    res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc[0] + w//2, max_loc[1] + h//2

def get_plus_icon_position():
    image = cv2.imread('images/screencap.png', 0)
    template = cv2.imread('images/plus_icon.png', 0)
    w, h = template.shape[::-1]
    method = eval("cv2.TM_CCORR_NORMED")
    res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val, max_val, min_loc, max_loc)
    return max_loc[0] + w//2, max_loc[1] + h//2

def get_search_bar_position():    
    image = cv2.imread('images/screencap.png', 0)
    template = cv2.imread('images/search_bar.png', 0)
    w, h = template.shape[::-1]
    method = eval("cv2.TM_CCORR_NORMED")
    res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc[0] + w//2, max_loc[1] + h//2



def get_click_postition():
    take_screenshot()
    x_add_phrase,y_add_phrase = get_add_phrase_position()
    device.shell(f'input tap {x_add_phrase} {y_add_phrase}')
    take_screenshot()
    x_search_bar,y_search_bar = get_search_bar_position()
    device.shell(f'input tap {x_search_bar} {y_search_bar}')
    device.shell(f'input text "BatDauLapTrinh.com"')
    device.shell('input keyevent 66')
    while(is_showing_dialog()):
        sleep(0.1)
    take_screenshot()
    x_plus_icon,y_plus_icon = get_plus_icon_position()
    device.shell('input keyevent 4')
    return x_add_phrase,y_add_phrase,x_search_bar,y_search_bar,x_plus_icon,y_plus_icon


def remove_duplicates_line(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x)) and x]


def clean_script(origin_list):
    return "".join(origin_list).replace("“", "").replace("”", "").replace(":", ".").replace(". ", ".").replace("?", ".").replace("’","'").replace("\n\n","\n").replace("\n ","\n")


def join_short_sentence(origin_list):
    origin_list = origin_list[::-1]
    idx = 0
    length_list = len(origin_list)
    join_script = ""
    while idx < length_list:
        if(len(origin_list[idx].split(" ")) <= 3): idx += 1
        elif idx < length_list - 2 and len(origin_list[idx]) + len(origin_list[idx + 1]) + len(origin_list[idx + 2]) <= ELSA_MAX_CHARACTER:
            join_script += origin_list[idx+2] + ". " + \
                origin_list[idx + 1] + ". " + origin_list[idx] + "\n"
            idx += 3
        elif idx < length_list - 1 and len(origin_list[idx]) + len(origin_list[idx + 1]) <= ELSA_MAX_CHARACTER:
            join_script += origin_list[idx+1] + \
                ". " + origin_list[idx] + "\n"
            idx += 2
        else:
            join_script += origin_list[idx] + "\n"
            idx += 1
    return join_script

adb = Client()
devices = adb.devices()
if(len(devices) == 0):
    print('no device dettach')
device = devices[0]

with open('transcript/transcript.txt', 'r') as f:
    unique_lines = remove_duplicates_line(f.readlines())
    clean_script = clean_script(unique_lines)
    print(clean_script)
    if "." in clean_script:
        splitted_script = clean_script.split(".")
    else:
        splitted_script = clean_script.split("\n")

    splitted_script = join_short_sentence(splitted_script)

with open("transcript/clean_transcript.txt", 'w') as f:
    for single_line in splitted_script:
        f.writelines(f"{single_line}")

x_add_phrase,y_add_phrase,x_search_bar,y_search_bar,x_plus_icon,y_plus_icon = get_click_postition()

for w in splitted_script.split("\n"):

    if len(w.split(" ")) <= 3: continue
    device.shell(f'input tap {x_add_phrase} {y_add_phrase}')
    device.shell(f'input tap {x_search_bar} {y_search_bar}')
    sleep(0.1)
    # print(w+"endl")   
    device.shell(f'input text "{w}"')
    device.shell('input keyevent 66')

    while(is_showing_dialog()):
        sleep(0.1)
    # x_plus_icon,y_plus_icon = get_plus_icon_position()
    device.shell(f'input tap {x_plus_icon} {y_plus_icon}')
    while(is_showing_dialog()):
        sleep(0.1)