from ppadb.client import Client
import os
import cv2
import glob
import numpy as np

SHOWING_DIALOG = 210

class ADBHelper():
    def __init__(self) -> None:
        adb = Client()
        devices = adb.devices()
        if (len(devices) == 0):
            raise Exception("CHECK YOUR ADB SET UP STEP")
        self.device = devices[0]

    def click_at_point(self, x, y):
        self.device.shell(f'input tap {x} {y}')

    def input_text(self, text):
        self.device.shell(f'input text "{text}"')

    def click_enter_keyboard(self):
        self.device.shell('input keyevent 66')

    def navigate_backward(self):
        self.device.shell('input keyevent 4')

    def is_showing_dialog(self):
        # sleep(0.03)
        self.take_screenshot()
        image = cv2.imread('images/screencap.png', cv2.IMREAD_GRAYSCALE)
        sum_all_pixel = np.sum(image[0:image.shape[0], 0:image.shape[1]])
        number_of_pixel = (image.shape[0]*image.shape[1])
        return sum_all_pixel / number_of_pixel < SHOWING_DIALOG

    def take_screenshot(self):
        os.system('adb exec-out screencap -p > images/screencap.png')

    def remove_old_set_word_files(self):
        full_files_name = glob.glob("set_word/*")
        for file_name in full_files_name:
            if "origin_word_list.txt" not in file_name:
                os.system(f'rm {file_name}')
