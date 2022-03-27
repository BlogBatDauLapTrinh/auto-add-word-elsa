import math
from multiprocessing.connection import wait
from ppadb.client import Client
import cv2
import matplotlib.pyplot as plt
from time import sleep
import numpy as np
import os
import json
import glob

#! 1000 Common phrase index set 12
START_INDEX = 0
WORD_PER_SET = 30
WATTING_TIME = 0.1
BASE_SET_NAME = "TEST OOP"  
SHOWING_DIALOG = 210
ELSA_MAX_CHARACTER = 128

class AutoAddELSA():

    def __init__(self):
        adb = Client()
        devices = adb.devices()
        if(len(devices) == 0):
            print('no self.device dettach')
        else:
            self.device = devices[0]
        self.x_create_study_set,self.y_create_study_set,self.x_study_set_name,self.y_study_set_name,self.x_category,self.y_category,self.x_ok,self.y_ok,self.x_add_phrases,self.y_add_phrases,self.x_search_bar,self.y_search_bar,self.x_plus,self.y_plus,self.x_finish,self.y_finish,self.x_additionally_add_phrases,self.y_additionally_add_phrases = self.get_icon_position()

    def remove_duplicates_line(self,seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x)) and x]

    def clean_script(self,origin_list):
        return "".join(origin_list).replace("“", "").replace("”", "").replace(":", ".").replace(". ", ".").replace("?", ".").replace("’","'").replace("\n\n","\n").replace("\n ","\n")

    def join_short_sentence(self,origin_list):
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

    def split_set_word_files(self):
        with open("set_word/origin_word_list.txt", 'r') as f:
            list_word = f.readlines()
        self.number_of_set = math.ceil(len(list_word)/WORD_PER_SET)
        idx = 0
        while idx < self.number_of_set:
            with open(f'set_word/set_word_number_{idx+1}','a') as f:
                for i in range(idx*WORD_PER_SET,idx*WORD_PER_SET+WORD_PER_SET):
                    try:
                        f.writelines(f"{list_word[i]}")
                    except:
                        print('error')
            idx += 1

    def is_showing_dialog(self):
        # sleep(0.03)
        self.take_screenshot()
        image = cv2.imread('images/screencap.png', cv2.IMREAD_GRAYSCALE)
        sum_all_pixel = np.sum(image[0:image.shape[0], 0:image.shape[1]])
        number_of_pixel = (image.shape[0]*image.shape[1])
        return sum_all_pixel / number_of_pixel < SHOWING_DIALOG

    def take_screenshot(self):
        os.system('adb exec-out screencap -p > images/screencap.png')
        
    def get_icon_position(self):
        with open('position.json','r') as f:
            position_json = json.loads("".join(f.readlines()))
        return position_json['x_create_study_set'],position_json['y_create_study_set'],position_json['x_study_set_name'],position_json['y_study_set_name'],position_json['x_category'],position_json['y_category'],position_json['x_ok'],position_json['y_ok'],position_json['x_add_phrases'],position_json['y_add_phrases'],position_json['x_search_bar'],position_json['y_search_bar'],position_json['x_plus'],position_json['y_plus'],position_json['x_finish'],position_json['y_finish'],position_json['x_additionally_add_phrases'],position_json['y_additionally_add_phrases']

    def create_empty_set(self,set_name):
        self.device.shell(f'input tap {self.x_create_study_set} {self.y_create_study_set}')
        while self.is_showing_dialog():
            sleep(2*WATTING_TIME)
        self.device.shell(f'input tap {self.x_study_set_name} {self.y_study_set_name}')
        self.device.shell(f'input text "{set_name}"')
        self.device.shell(f'input tap {self.x_category} {self.y_category}')
        self.device.shell(f'input tap {self.x_ok} {self.y_ok}')
        self.device.shell(f'input tap {self.x_add_phrases} {self.y_add_phrases}')        
        self.device.shell(f'input tap {self.x_search_bar} {self.y_search_bar}')
        self.device.shell(f'input text "get this show on the row"')
        self.device.shell('input keyevent 66')
        while self.is_showing_dialog():
            sleep(2*WATTING_TIME)
        self.device.shell(f'input tap {self.x_plus} {self.y_plus}')
        self.device.shell(f'input tap {self.x_finish} {self.y_finish}')
        while self.is_showing_dialog():
            sleep(2*WATTING_TIME)
        
    def remove_old_set_word_files(self):
        full_files_name = glob.glob("set_word/*")
        for file_name in full_files_name:
            if "origin_word_list.txt" not in file_name:
                os.system(f'rm {file_name}')
            
    def add_word_list_to_ELSA(self):
        for i in range(START_INDEX):
            os.system(f'rm set_word/set_word_number_{i+1}')
        for x in range(START_INDEX,self.number_of_set):
            set_name = f"{BASE_SET_NAME} {x+1}"
            self.create_empty_set(set_name)
            with open(f'set_word/set_word_number_{x+1}','r') as f:
                list_word = f.readlines()
            sleep(2*WATTING_TIME)
            for idx in range(WORD_PER_SET):
                self.take_screenshot()
                self.device.shell(f'input tap {self.x_additionally_add_phrases} {self.y_additionally_add_phrases}')
                self.device.shell(f'input tap {self.x_search_bar} {self.y_search_bar}')
                print(idx,len(list_word))
                phrase = str(list_word[idx])
                print(phrase)
                self.device.shell(f'input text "{phrase}"')
                self.device.shell('input keyevent 66')
                while(self.is_showing_dialog()):
                    sleep(2*WATTING_TIME)
                self.device.shell(f'input tap {self.x_plus} {self.y_plus}')
                while(self.is_showing_dialog()):
                    sleep(WATTING_TIME)
            print(f'input keyevent 4')
            os.system(f'rm set_word/set_word_number_{x+1}')
            self.device.shell(f'input keyevent 4')
            sleep(10*WATTING_TIME)


autoAddELSA = AutoAddELSA()
autoAddELSA.remove_old_set_word_files()
autoAddELSA.split_set_word_files()
autoAddELSA.add_word_list_to_ELSA()