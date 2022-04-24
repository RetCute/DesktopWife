#茉子天下第一可爱!
#Bilibili: Retrocal
#QQ: 3288025626
#写的确实烂因为第一次用pyqt5

import sys
from ctypes import windll
import os
import json
import random
import webbrowser
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets

class Config:
    Cdelay = None
    actions = None
    indeximg = None
    folder = None
    icon = None
    length = None
    width = None

def configLoader():
    filelist = os.listdir('settings')
    conifgs = []
    for file in filelist:
        if '.json' in file:
            conifgs.append(file)
    sleep(2)
    print('[INFO]Obtained the conifg list successfully!')
    return conifgs

def LoadConfig(conf):
    index = 1
    conlist = []
    sleep(2)
    for file in conf:
        try:
            res = open(f'settings/{file}', 'r').read()
            info = json.loads(res.encode('gbk'))
            author = info['author']
            name = info['name']
            print(f'[{str(index)}] {name} by {author} | {file}')
            conlist.append(info)
        except:
            print(f'LoadError: Cannot Load {file}!')
            pass
        index += 1
    try:
        Mode = input('>>>>Select A File>>>>')
        conifg = conlist[int(Mode) - 1]
        Config.Cdelay = conifg['delay']
        Config.folder = conifg['folder']
        Config.indeximg = conifg['index']
        Config.actions = conifg['actions']
        Config.icon = conifg['icon']
        Config.length = conifg['length']
        Config.width = conifg['width']
    except:
        print('LoadError:Cannot reset conifg.Exiting...')
        sleep(5)
        sys.exit()
    windll.kernel32.SetConsoleTitleW(f'Desktopwife by retrocal | conifg:{conifg["name"]} by {conifg["author"]}')
    sleep(2)
    print('[INFO]Loaded conifg successfully')

def checkResource(ftime):
    if ftime:
        if os.path.exists('resource'):
            print('[INFO]Resource folder found!')
            sleep(2)
        else:
            print('Resource Folder Not Found!Exiting...')
            sleep(5)
            sys.exit()
    else:
        files = os.listdir(f'resource/{Config.folder}')
        if Config.indeximg in files and Config.icon in files:
            pass
        else:
            print('[Warning]Icon file or index image not found！')
            print('Exiting...')
            sleep(3)
            sys.exit()
        for img in Config.actions:
            if img in files:
                pass
            else:
                print(f'[Warning]{img} not found')
                print('Exiting...')
                sleep(3)
                sys.exit()

def About():
    webbrowser.open_new_tab("https://retrocal.xyz")

class Main(QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.folder = 'resource'
        self.actions = Config.actions
        self.CreateWindow()
        print('[INFO]Window have been created')

    def CreateWindow(self):
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        self.img = QLabel(self)
        self.actionDatas = []
        self.initActions()
        self.index = 0
        self.setPic(Config.indeximg)
        self.resize(Config.length, Config.width)
        self.show()
        self.running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.act)
        self.timer.start(Config.Cdelay)
        self.randomPos()

    def loadImgs(self, filenames):
        imglist = []
        for item in filenames:
            img = QImage()
            img.load(f'{self.folder}/{Config.folder}/'+item)
            imglist.append(img)
        return imglist

    def initActions(self):
        imgs = self.loadImgs(self.actions)
        self.actionDatas.append(imgs)

    def act(self):
        if not self.running:
            self.index = 0
            self.running = True
        self.runActions(self.actionDatas[0])

    def setPic(self, pic):
        img = QImage()
        img.load(f'{self.folder}/{Config.folder}/' + pic)
        self.img.setPixmap(QPixmap.fromImage(img))

    def runActions(self, imgs):
        if self.index >= len(imgs):
            self.index = 0
            self.running = False
        self.img.setPixmap(QPixmap.fromImage(imgs[self.index]))
        self.index += 1

    def randomPos(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())*random.random(), (screen.height()-size.height())*random.random())

    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

class Mozi(QWidget):
    def __init__(self):
        windll.kernel32.SetConsoleTitleW('Desktopwife v1.0 by Retrocal')
        QtWidgets.QWidget.__init__(self)
        checkResource(True)
        configs = configLoader()
        LoadConfig(configs)
        checkResource(False)
        about = QAction("About", self, triggered=About)
        quit = QAction("Exit", self, triggered=self.close)
        self.Mozi = Main()
        self.Menu = QMenu(self)
        self.Menu.addAction(about)
        self.Menu.addAction(quit)
        self.Icon = QSystemTrayIcon(self)
        self.Icon.setIcon(QIcon(f"resource/{Config.folder}/{Config.icon}"))
        self.Icon.setContextMenu(self.Menu)
        self.Icon.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Mozi()
    sys.exit(app.exec_())