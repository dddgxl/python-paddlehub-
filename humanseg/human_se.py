import os.path
from os.path import exists
from os import mkdir

from paddlehub import Module

from PIL import Image
import numpy as np

from PyQt6.QtWidgets import QApplication ,QFileDialog,QPushButton
from PyQt6 import uic,QtGui
from PyQt6.QtCore import QCoreApplication

import sys
import cv2
import shutil



def image_read_from_chinese_path(image_file_name):#读取中文路径

    image_numpy_data = cv2.imdecode(np.fromfile(image_file_name, dtype=np.uint8), -1)
    # 返回numpy的ndarray
    return image_numpy_data

def seg(filename):#人像分割函数
    module = Module(name = "deeplabv3p_xception65_humanseg")
    if not exists('./cache'):
        mkdir('./cache')
    image_numpy_data = image_read_from_chinese_path(filename)#借用np寻找中文路径
    # res = module.segmentation(paths=[filename], output_dir='./output', visualization=True)
    res = module.segmentation(images=[image_numpy_data], output_dir='./cache', visualization=True)
    outputFilename = res[0]['save_path']


    outputFilename = outputFilename.replace('/', '\\')#输出路径格式化
    return outputFilename


def selecctfile ():
    fd = QFileDialog()
    fd.setFileMode(QFileDialog.FileMode.ExistingFiles)#
    fd.setDirectory('c:\\')
    fd.setNameFilter('图片文件(*.jpg *.png)')
    imgName, imgType = fd.getOpenFileName()#imgName 为图片路径
    if imgName:#图片上传并处理
        print(imgName)
        #图片上传过程
        jpg = QtGui.QPixmap(imgName).scaled(ui.label_3.width(), ui.label_3.height())
        ui.label_3.setPixmap(jpg)
        #图片处理过程
        global temp_jpg
        temp_jpg = seg(filename=imgName)
        jpg = QtGui.QPixmap(temp_jpg).scaled(ui.label_3.width(), ui.label_3.height())
        ui.label_3.setPixmap(jpg)
        # print(temp_jpg)


def delete_files_in_folder(folder_path):#删除文件代码
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)



def on_download():
    global temp_jpg
    global save_file_path
    image_numpy_data = image_read_from_chinese_path(temp_jpg)
    # print(temp_jpg)
    save_file_path,_ = QFileDialog.getSaveFileName(parent=None,caption='保存生成的图片',directory = 'c:\\',filter="保存为png格式")

    if save_file_path:
        print(save_file_path)
        with open('./output/final.jpg', 'rb') as img_file:
            shutil.copyfile(img_file.name, save_file_path)


        ui.label_3.clear()

        # parent_directory = os.path.dirname(temp_jpg)
        #
        # delete_files_in_folder(parent_directory)



def on_blue():
    save_path = './output/final.jpg'
    global temp_jpg
  # 读入图片
    base_image = Image.open('./src/blue.jpg').convert('RGB')#背景图片
    base_image = base_image.resize((1875, 2500))
    fore_image = Image.open(temp_jpg).resize(base_image.size)#前景图片，抠出来的人物图片
    #统一裁剪 2000x2500
    # 图片加权合成
    scope_map = np.array(fore_image)[:, :, -1] / 255
    scope_map = scope_map[:, :, np.newaxis]
    scope_map = np.repeat(scope_map, repeats=3, axis=2)
    res_image = np.multiply(scope_map, np.array(fore_image)[:, :, :3]) + np.multiply((1 - scope_map),np.array(base_image))


    # 保存图片
    res_image = Image.fromarray(np.uint8(res_image))
    res_image.save(save_path)
    # ui界面中显示图片
    jpg = QtGui.QPixmap(save_path).scaled(ui.label_3.width(), ui.label_3.height())
    ui.label_3.setPixmap(jpg)
def on_red():
    save_path = './output/final.jpg'
    global temp_jpg
    # 读入图片
    base_image = Image.open('./src/red.jpg').convert('RGB')  # 背景图片
    base_image = base_image.resize((1875, 2500))
    fore_image = Image.open(temp_jpg).resize(base_image.size)  # 前景图片，抠出来的人物图片
    # 统一裁剪 2000x2500
    # 图片加权合成
    scope_map = np.array(fore_image)[:, :, -1] / 255
    scope_map = scope_map[:, :, np.newaxis]
    scope_map = np.repeat(scope_map, repeats=3, axis=2)
    res_image = np.multiply(scope_map, np.array(fore_image)[:, :, :3]) + np.multiply((1 - scope_map),
                                                                                     np.array(base_image))

    # 保存图片
    res_image = Image.fromarray(np.uint8(res_image))
    res_image.save(save_path)
    # ui界面中显示图片
    jpg = QtGui.QPixmap(save_path).scaled(ui.label_3.width(), ui.label_3.height())
    ui.label_3.setPixmap(jpg)

def on_white():
    save_path = './output/final.jpg'
    global temp_jpg
    # 读入图片
    base_image = Image.open('./src/white.jpg').convert('RGB')  # 背景图片
    base_image = base_image.resize((1875,2500))
    fore_image = Image.open(temp_jpg).resize(base_image.size)  # 前景图片，抠出来的人物图片
    # 统一裁剪 2000x2500
    # 图片加权合成
    scope_map = np.array(fore_image)[:, :, -1] / 255
    scope_map = scope_map[:, :, np.newaxis]
    scope_map = np.repeat(scope_map, repeats=3, axis=2)
    res_image = np.multiply(scope_map, np.array(fore_image)[:, :, :3]) + np.multiply((1 - scope_map),
                                                                                     np.array(base_image))

    # 保存图片
    res_image = Image.fromarray(np.uint8(res_image))
    res_image.save(save_path)
    # ui界面中显示图片
    jpg = QtGui.QPixmap(save_path).scaled(ui.label_3.width(), ui.label_3.height())
    ui.label_3.setPixmap(jpg)


def close_application():
    print("程序即将关闭，这里可以执行清理工作或保存设置")
    dic = './cache'
    delete_files_in_folder(dic)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ui = uic.loadUi(("./test.ui"))
    ui.show()
    pushButton: QPushButton = ui.pushButton
    pushButton.clicked.connect(selecctfile)

    pushButton_download: QPushButton = ui.pushButton_2
    pushButton_download.clicked.connect(on_download)

    pushButton_blue: QPushButton = ui.pushButton_4
    pushButton_blue.clicked.connect(on_blue)

    pushButton_white: QPushButton = ui.pushButton_3
    pushButton_white.clicked.connect(on_white)

    pushButton_red: QPushButton = ui.pushButton_5
    pushButton_red.clicked.connect(on_red)

    QCoreApplication.instance().aboutToQuit.connect(close_application)
    button = QPushButton("关闭程序")
    button.clicked.connect(app.exit)  # 点击按钮时关闭程序
    sys.exit(app.exec())


    print()
