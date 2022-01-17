import math
from ppadb.client import Client
import cv2
import matplotlib.pyplot as plt
from time import sleep
import numpy as np

WORD_PER_SET = 50
SHOWING_DIALOG = 150
ELSA_MAX_CHARACTER = 128
WATTING_TIME = 0.1

def is_showing_dialog():
    sleep(0.03)
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
    # image = cv2.imread("images/screencap.png",cv2.IMREAD_GRAYSCALE)
    # plt.imshow(image)
    # plt.show()

def get_icon_position(icon_name):
    image = cv2.imread('images/screencap.png', 0)
    template = cv2.imread(f'images/{icon_name}', 0)
    w, h = template.shape[::-1]
    method = eval("cv2.TM_CCORR_NORMED")
    res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc[0] + w//2, max_loc[1] + h//2

def get_create_set_position(set_name):
    take_screenshot()
    x_create_study_set,y_create_study_set = get_icon_position("create_study_set.png")
    device.shell(f'input tap {x_create_study_set} {y_create_study_set}')
    take_screenshot()
    x_study_set_name,y_study_set_name = get_icon_position('study_set_name.png')
    device.shell(f'input tap {x_study_set_name} {y_study_set_name}')
    device.shell(f'input text "{set_name}"')
    take_screenshot()
    x_category,y_category = get_icon_position('category.png')
    device.shell(f'input tap {x_category} {y_category}')
    while not is_showing_dialog():
        print("not is_showing_dialog() -> OK")
        sleep(2*WATTING_TIME)
        take_screenshot()
    x_ok,y_ok = get_icon_position('ok.png')
    device.shell(f'input tap {x_ok} {y_ok}')
    take_screenshot()
    #take screenshot
    x_ok,y_ok = get_icon_position('ok.png')
    device.shell(f'input tap {x_ok} {y_ok}')
    take_screenshot()
    x_add_phrases_in_create_new_set,y_add_phrases_in_create_new_set = get_icon_position('add_phrases_in_create_new_set.png')
    device.shell(f'input tap {x_add_phrases_in_create_new_set} {y_add_phrases_in_create_new_set}')
    take_screenshot()
    x_search_bar,y_search_bar = get_icon_position('search_bar.png')
    device.shell(f'input tap {x_search_bar} {y_search_bar}')
    device.shell(f'input text "get this show on the road"')
    device.shell('input keyevent 66')
    while(is_showing_dialog()):
        sleep(WATTING_TIME)
    take_screenshot()
    x_plus_icon,y_plus_icon = get_icon_position('plus_icon.png')
    device.shell(f'input tap {x_plus_icon} {y_plus_icon}')
    take_screenshot()
    x_finish,y_finish = get_icon_position('finish.png')
    device.shell(f'input tap {x_finish} {y_finish}')
    while(is_showing_dialog()):
        sleep(WATTING_TIME)
    take_screenshot()
    x_add_phrase,y_add_phrase = get_icon_position("add_phrase.png")
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

def split_set_word():
    idx = 0
    while idx < number_of_set:
        with open(f'set_word/set_word_number_{idx+1}','a') as f:
            for i in range(idx*WORD_PER_SET,idx*WORD_PER_SET+WORD_PER_SET):
                try:
                    f.writelines(f"{list_word[i]}")
                except:
                    print('finished')
        idx += 1

adb = Client()
devices = adb.devices()
if(len(devices) == 0):
    print('no device dettach')
device = devices[0]

with open("set_word/origin_word_list.txt", 'r') as f:
    list_word = f.readlines()
number_of_set = math.ceil(len(list_word)/WORD_PER_SET)

for x in range(45,number_of_set):
    set_name = f"5000 OXFORD WORDS - SET {x}"
    x_add_phrase,y_add_phrase,x_search_bar,y_search_bar,x_plus_icon,y_plus_icon = get_create_set_position(set_name)
    print(x_add_phrase,y_add_phrase,x_search_bar,y_search_bar,x_plus_icon,y_plus_icon)
    with open(f'set_word/set_word_number_{x+1}','r') as f:
        list_word = f.readlines()
    
    sleep(2*WATTING_TIME)
    for idx in range(WORD_PER_SET):
        take_screenshot()
        device.shell(f'input tap {x_add_phrase} {y_add_phrase}')
        device.shell(f'input tap {x_search_bar} {y_search_bar}')
        print(idx,len(list_word))
        device.shell(f'input text "{list_word[idx]}"')
        device.shell('input keyevent 66')
        while(is_showing_dialog()):
            sleep(WATTING_TIME)
        device.shell(f'input tap {x_plus_icon} {y_plus_icon}')
        while(is_showing_dialog()):
            sleep(WATTING_TIME)
    device.shell(f'input keyevent 4')
    sleep(2*WATTING_TIME)