from operator import pos
import matplotlib.pyplot as plt
from multiprocessing.connection import wait
from ppadb.client import Client
import cv2
import matplotlib.pyplot as plt
from time import sleep
import os
import json
import numpy as np

SHOWING_DIALOG = 210

class GetIconPosition():
    def __init__(self):
        self.point = ()

    def getCoord(self, icon_name):
        self.take_screenshot()
        self.img = cv2.imread(f'images/screencap.png')
        self.fig = plt.figure()
        self.fig.add_subplot(111)
        self.fig.canvas.set_window_title(f'click at {icon_name}')
        plt.title(f'click at {icon_name}')
        # figManager = plt.get_current_fig_manager()
        # figManager.window.showMaximized()
        plt.imshow(self.img)
        self.fig.canvas.mpl_connect(
            'button_press_event', self.__onclick__)
        plt.show()
        return self.point

    def __onclick__(self, click):
        self.point = (click.xdata, click.ydata)
        plt.close(self.fig)
        return self.point

    def take_screenshot(self):
        os.system('adb exec-out screencap -p > images/screencap.png')

    def is_showing_dialog(self):
        sleep(0.03)
        self.take_screenshot()
        image = cv2.imread('images/screencap.png', cv2.IMREAD_GRAYSCALE)
        sum_all_pixel = np.sum(image[0:image.shape[0], 0:image.shape[1]])
        number_of_pixel = (image.shape[0]*image.shape[1])
        print(sum_all_pixel / number_of_pixel)
        return sum_all_pixel / number_of_pixel < SHOWING_DIALOG


def main():

    adb = Client()
    devices = adb.devices()
    if(len(devices) == 0):
        print('no device dettach')
    device = devices[0]

    icon_position_object = GetIconPosition()

    list_icon_position = 'create_study_set', 'study_set_name', 'category', 'ok', 'add_phrases', 'search_bar', 'plus', 'finish', 'additionally_add_phrases'
    position_dict = dict()

    for icon_name in list_icon_position:
        icon_point = icon_position_object.getCoord(icon_name)
        print(icon_point)
        position_dict[f'x_{icon_name}'] = icon_point[0]
        position_dict[f'y_{icon_name}'] = icon_point[1]
        
        if icon_name != 'additionally_add_phrases':
            device.shell(f'input tap {icon_point[0]} {icon_point[1]}')
        
        if icon_name == 'study_set_name':
            device.shell(f'input text "TEST TO GET ICON POSITION"')
            device.shell('input keyevent 66')
            while(icon_position_object.is_showing_dialog()):
                sleep(1)

        if icon_name == 'search_bar':
            device.shell(f'input text "get this show on the road"')
            device.shell('input keyevent 66')
            while(icon_position_object.is_showing_dialog()):
                sleep(1)

        if icon_name == 'finish':
            while(icon_position_object.is_showing_dialog()):
                sleep(1)
        sleep(1)

    position_json = json.dumps(position_dict)
    with open('position.json','w') as f:
        f.writelines(position_json)

with open('position.json','r') as f:
    position_json = json.loads("".join(f.readlines()))
# print(position_json)
main()
for key in position_json.keys():
    print(key,position_json[key])

list_key = ",".join([key for key in position_json.keys()])
print(list_key)