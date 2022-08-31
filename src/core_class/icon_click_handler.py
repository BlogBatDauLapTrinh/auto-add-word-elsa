import matplotlib.pyplot as plt
import cv2
from time import sleep
import os
import numpy as np

SHOWING_DIALOG = 210

class IconClickHandler():
    def __init__(self):
        self.point = ()

    def get_clicked_position(self, icon_name):
        self.take_screenshot()
        self.img = cv2.cvtColor(cv2.imread(
            f'images/screencap.png'), cv2.COLOR_BGR2RGB)
        self.fig = plt.figure()
        self.fig.canvas.set_window_title('SET UP ICON POSITION')
        plt.title(f'click at {icon_name}')
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
