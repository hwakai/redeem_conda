import sys
from PyQt5Import import *
from mainWindow import MainWindow
import multiprocessing

#=======================================================================================================
#   開始
#=======================================================================================================
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainWindow = MainWindow()                                                                       # メインウインドウ生成
        mainWindow.show()                                                                               # ウインドウ表示
        sys.exit(app.exec_())                                                                           # アプリケーション開始、戻ってきたら終了
        pass

    except Exception as e:                                                                              # 例外                                                                          # 例外                                                                          # 例外
        print(e)                     			                                                        # 例外を表示
        pass

# CREATE DATABASE redeem DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

