import os
import time
import numpy as np
import MySQLdb as connector
from PyQt5Import import *
from kerasImport import *
from staticImport import *
import inspect
from staticImport import *
from functools import partial
from commonBase import QObjectPackClass
from commonBase import CommonBaseClass
import pathlib
from classDef import ParameterClass
from distutils.util import strtobool


# =======================================================================================================
#   スーパークラス グリッドクラス
# =======================================================================================================
class GridClass(QGridLayout):
    def __init__(self, parent, horizontalSpacing, verticalSpacing):  # 初期化
        try:
            QGridLayout.__init__(self, None)  # スーパークラスの初期化
            self.setHorizontalSpacing(horizontalSpacing)  # グリッドスペース設定
            self.setVerticalSpacing(verticalSpacing)  # グリッドスペース設定
            self.curRow = 0  # 現在の行
            self.curCol = 0  # 現在の列

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   クリア
    # ---------------------------------------------------------------------------------------------------
    def clear(self):
        try:
            for i in range(self.count()):  # アイテムの数をすべて実行
                item = self.itemAt(i)  # アイテムを取得
                if item.layout() is not None:  # アイテムがレイアウトの時
                    layout = item.layout()  # レイアウト取得
                    for j in range(layout.count()):  # レイアウトのアイテムの数をすべて実行
                        if layout.itemAt(j).widget() is not None:  # アイテムがウイジェットの時
                            layout.itemAt(j).widget().deleteLater()  # ウイジェットを遅延削除
                elif item.widget() is not None:  # アイテムがウイジェットの時
                    item.widget().deleteLater()  # ウイジェットを遅延削除
            while self.itemAt(0) is not None:  # アイテムの数をすべて実行
                self.removeItem(self.itemAt(0))  # アイテムを取り除く

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ラインエディットレイアウト設定·
    # ---------------------------------------------------------------------------------------------------
    def addLineEdit(self, parent, varType, method, title):
        try:
            label = QLabel(title)  # ラベルを生成してオブジェクトにセット
            object = QLineEdit()  # ラインエディットを生成してオブジェクトにセット
            pack = QObjectPackClass(object, method, varType)  # オブジェクトパックを生成
            parent.lineEditList.append(pack)  # 親ウイジェットのラインエディットリストにオブジェクトパックをアペンド
            exec("self.lineEdit_" + method + " = object")  # メソッド名を付けたコンボボックスにオブジェクトをセット
            self.addWidget(label, self.curRow, 0)  # グリッド(curRow,0)にラベルをセット
            self.addWidget(object, self.curRow, 1)  # グリッド(curRow,1)にラベルをセット
            self.curRow += 1  # 現在の行を更新

        except Exception as e:  # 例外
            printError(e)  # 例外を表示


# =======================================================================================================
#   スーパークラス QtBaseClass
# =======================================================================================================
class QtBaseClass(CommonBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        CommonBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
        self.comboBoxList = []  # コンボボックスリストを初期化
        self.checkBoxList = []  # チェックボックスリストを初期化
        self.lineEditList = []  # ラインエディットリストを初期化
        self.pushButtonList = []  # プッシュボタンリストを初期化
        self.checkGroupList = []  # チェックグループリストを初期化
        self.sliderList = []  # スライダーリストを初期化
        self.connected = False  # 接続済フラグを初期化

    # ***************************************************************************************************
    #   コネクト処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトとメソッドを結合
    # ---------------------------------------------------------------------------------------------------
    def connectButtons2(self):
        try:
            # パラメータ保存メソッドと結合
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                pack.qObject.currentTextChanged.connect(self.saveParam)  # コンボボックスをパラメータ保存メソッドと結合
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                pack.qObject.clicked.connect(self.saveParam)  # チェックボックスをパラメータ保存メソッドと結合
            for pack in self.lineEditList:  # ラインエディットリストをすべて実行
                pack.qObject.textEdited.connect(self.saveParam)  # ラインエディットをパラメータ保存メソッドと結合
            # 関数呼び出しメソッドと結合
            for pack in self.pushButtonList:  # プッシュボタンリストをすべて実行
                exec(
                    "self.pushButton_" + pack.method + ".clicked.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            for pack in self.checkGroupList:  # プッシュボタンリストをすべて実行
                exec("pack.qObject.buttonClicked.connect(self." + pack.method + ")")  # チェックグループボックスを関数呼び出しメソッドと結合
            self.connected = True  # コネクト済にする
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトとメソッドを結合
    # ---------------------------------------------------------------------------------------------------
    def connectButtons3(self):
        try:
            # パラメータ保存メソッドと結合
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                pack.qObject.currentTextChanged.connect(self.saveParam)  # コンボボックスをパラメータ保存メソッドと結合
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                pack.qObject.clicked.connect(self.saveParam)  # チェックボックスをパラメータ保存メソッドと結合
            for pack in self.lineEditList:  # ラインエディットリストをすべて実行
                pack.qObject.textEdited.connect(self.saveParam)  # ラインエディットをパラメータ保存メソッドと結合
            # 関数呼び出しメソッドと結合
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                exec("pack.qObject.currentTextChanged.connect(self." + pack.method + "_EVENT)")  # コンボボックスを関数呼び出しメソッドと結合
            for pack in self.pushButtonList:  # プッシュボタンリストをすべて実行
                exec(
                    "self.pushButton_" + pack.method + ".clicked.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            self.connected = True  # コネクト済にする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトとメソッドを結合
    # ---------------------------------------------------------------------------------------------------
    def connectButtons(self):
        try:
            # パラメータ保存メソッドと結合
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                pack.qObject.currentTextChanged.connect(self.saveMethod)  # コンボボックスをパラメータ保存メソッドと結合
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                pack.qObject.clicked.connect(self.saveMethod)  # チェックボックスをパラメータ保存メソッドと結合
            for pack in self.lineEditList:  # ラインエディットリストをすべて実行
                pack.qObject.textEdited.connect(self.saveMethod)  # ラインエディットをパラメータ保存メソッドと結合
            # 関数呼び出しメソッドと結合
            for pack in self.pushButtonList:  # プッシュボタンリストをすべて実行
                exec(
                    "self.pushButton_" + pack.method + ".clicked.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            self.connected = True  # コネクト済にする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトを関数呼び出しメソッドと結合
    # ---------------------------------------------------------------------------------------------------
    def connectButtonsMethod(self):
        try:
            # パラメータ保存メソッドと結合
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                exec("pack.qObject.currentTextChanged.connect(self." + pack.method + ")")  # コンボボックスを関数呼び出しメソッドと結合
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                exec("pack.qObject.clicked.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            for pack in self.lineEditList:  # ラインエディットリストをすべて実行
                exec("pack.qObject.textEdited.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            for pack in self.pushButtonList:  # プッシュボタンリストをすべて実行
                exec("pack.qObject.clicked.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            for pack in self.checkGroupList:  # プッシュボタンリストをすべて実行
                exec("pack.qObject.buttonClicked.connect(self." + pack.method + ")")  # チェックグループボックスを関数呼び出しメソッドと結合
            self.connected = True  # コネクト済にする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レーザー選択釦結合
    # ---------------------------------------------------------------------------------------------------
    def connectLaserSelButton(self):
        try:
            # パラメータ保存メソッドと結合
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                exec("pack.qObject.currentTextChanged.connect(self." + pack.method + ")")  # コンボボックスを関数呼び出しメソッドと結合
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                exec("pack.qObject.clicked.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            for pack in self.lineEditList:  # ラインエディットリストをすべて実行
                exec("pack.qObject.textEdited.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            for pack in self.pushButtonList:  # プッシュボタンリストをすべて実行
                exec("pack.qObject.clicked.connect(partial(self." + pack.method + "," + str(
                    pack.no) + "))")  # プッシュボタンを関数呼び出しメソッドと結合
            self.connected = True  # コネクト済にする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトとメソッドの結合解除してからリストをクリアする
    # ---------------------------------------------------------------------------------------------------
    def disconnectButtons(self):
        try:
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                pack.qObject.disconnect()  # コンボボックスの結合解除
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                pack.qObject.disconnect()  # チェックボックの結合解除
            for pack in self.lineEditList:  # ラインエディットリストをすべて実行
                pack.qObject.disconnect()  # ラインエディットの結合解除
            for pack in self.pushButtonList:  # プッシュボタンリストをすべて実行
                pack.qObject.disconnect()  # プッシュボタンの結合解除
            self.comboBoxList.clear()  # プッシュボタンリストをクリア
            self.checkBoxList.clear()  # プッシュボタンリストをクリア
            self.lineEditList.clear()  # プッシュボタンリストをクリア
            self.pushButtonList.clear()  # プッシュボタンリストをクリア
            self.checkGroupList.clear()  # チェックグループボタンリストをクリア
            self.connected = False  # 未コネクトにする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ***************************************************************************************************
    #   基本処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   指定した開始番号から指定した終了番号まで指定した間隔でテキストタイプのフラットなリストを返す
    # ---------------------------------------------------------------------------------------------------
    def flatRange(self, start, end, interval=1):
        try:
            n = int((end - start) / interval + 1)  # 要素数
            rangeList = []  # レンジリストを初期化
            for i in range(n):  # 要素数をすべて実行
                rangeList.append(str(round(start + interval * i, 3)))  # レンジリストにストリング化して追加
            return rangeList  # レンジリストを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   説明文付きのエラーラベルを返す
    # ---------------------------------------------------------------------------------------------------
    def getDescLabel(self, LASER_ID, label):
        try:
            descLabel = label  # 描画ラベル
            if label in GP.GR_ERR_LIST.LIST:  # ラベルリストに有る時
                description = GP.SVR.DBSServer.getDescription(LASER_ID, label)  # 説明文取得
                descLabel = label + ":" + description  # 描画ラベルに説明文を追加
            return descLabel  # 説明文付きのエラーラベルを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ファイルからブーリアンを読み込む
    # ---------------------------------------------------------------------------------------------------
    def readBool(self, f):
        try:
            var = f.readline()  # ファイルから一行読み込む
            var = var.strip()  # 改行を取り除く
            return var == "True"  # ブーリアン返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return False  # Falseを返す

    # ---------------------------------------------------------------------------------------------------
    #   ファイルからフロートを読み込む
    # ---------------------------------------------------------------------------------------------------
    def readFloat(self, f):
        try:
            var = f.readline()  # ファイルから一行読み込む
            var = var.strip()  # 改行を取り除く
            return float(var)  # float返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ファイルから整数を読み込む
    # ---------------------------------------------------------------------------------------------------
    def readInt(self, f):
        try:
            var = f.readline()  # ファイルから一行読み込む
            var = var.strip()  # 改行を取り除く
            return int(var)  # intを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ファイルからテキストを読み込む
    # ---------------------------------------------------------------------------------------------------
    def readStr(self, f):
        try:
            var = f.readline()  # ファイルから一行読み込む
            var = var.strip()  # 改行を取り除く
            return var  # テキストを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ファイルに一行書き込む
    # ---------------------------------------------------------------------------------------------------
    def writeOne(self, f, var):
        try:
            f.write(str(var) + "\n")  # ファイルに一行書き込む

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   文字列がintか返す
    # ---------------------------------------------------------------------------------------------------
    def isIntStr(self, str):
        try:
            int(str)  # float変換
            return True  # 例外が起きなければ真を返す
        except ValueError:  # 例外が起きた時
            return False  # 偽を返す

    # ---------------------------------------------------------------------------------------------------
    #   文字列がfloatか返す
    # ---------------------------------------------------------------------------------------------------
    def isFloatStr(self, str):
        try:
            float(str)  # float変換
            return True  # 例外が起きなければ真を返す
        except ValueError:  # 例外が起きた時
            return False  # 偽を返す

    # ---------------------------------------------------------------------------------------------------
    #   メソッド名とオブジェクトタイプからObjectを返す
    # ---------------------------------------------------------------------------------------------------
    def getObject(self, objectType, method):
        try:
            exec("self.obj = self." + objectType + "_" + method)  # オブジェクトを取得 self.XXX変数でないと無効
            return self.obj  # オブジェクトを返す

        except ValueError:  # 例外が起きた時
            return False  # 偽を返す

    # ***************************************************************************************************
    #   パラメータ処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   パラメータに値をセット
    # ---------------------------------------------------------------------------------------------------
    def setParamVar(self, param, pack, var):
        try:
            if pack.varType == "str":  # タイプが"str"の時
                exec("param." + pack.method + "=var")  # パラメータに値をセット
            elif pack.varType == "int":  # タイプが"int"の時
                if not self.isIntStr(var): var = '0'  # 文字列がintでない時はvarを'0'にする
                exec("param." + pack.method + "=int(var)")  # パラメータに値をセット
            elif pack.varType == "float":  # タイプが"floatの時
                if not self.isFloatStr(var): var = '0.0'  # 文字列がfloatでない時はvarを'0'にする
                exec("param." + pack.method + "=float(var)")  # パラメータに値をセット
            elif pack.varType == "bool":  # タイプが"boolの時
                if type(var) != bool: var = False  # 文字列がfloatでない時はvarを'0'にする
                exec("param." + pack.method + "= var")  # パラメータに値をセット

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   パラメータをオブジェクトとファイルに書き込む
    # ---------------------------------------------------------------------------------------------------
    def setParametersToObject(self):
        try:
            # コンボボックス
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                exec("self.var = self.parameter." + pack.method)  # ラインエディットかからパラメータに値をセット
                pack.qObject.setCurrentText(str(self.var))  # Qオブジェクトにパラメータの値をセット
                aaa = pack.qObject.currentText()
                pass

            # チェックボックス
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                exec("self.var = self.parameter." + pack.method)  # ラインエディットかからパラメータに値をセット
                pack.qObject.setChecked(self.var)  # Qオブジェクトにパラメータの値をセット
            # ラインエディット
            for pack in self.lineEditList:  # ラインエディットリストをすべて実行
                exec("self.var = self.parameter." + pack.method)  # ラインエディットかからパラメータに値をセット
                pack.qObject.setText(str(self.var))  # Qオブジェクトにパラメータの値をセット
            # スライダー
            for pack in self.sliderList:  # スライダーリストをすべて実行
                exec("self.var = self.parameter." + pack.method)  # ラインエディットかからパラメータに値をセット
                pack.qObject.setValue(self.var)  # Qオブジェクトにパラメータの値をセット
            # ファイルに書き込む
            self.parameter.saveData()  # オブジェクトのデータをファイルに書き込む
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   パラメータをオブジェクトから読み込む
    # ---------------------------------------------------------------------------------------------------
    def setParametersFromObject(self):
        try:
            # コンボボックス
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                self.var = pack.qObject.currentText()  # Qオブジェクトの値を取得
                self.setParamVar(self.parameter, pack, self.var)  # パラメータにセット
            # チェックボックス
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                var = pack.qObject.isChecked()  # Qオブジェクトの値を取得
                self.setParamVar(self.parameter, pack, var)  # パラメータにセット
            # ラインエディット
            for pack in self.lineEditList:  # ラインエディットリストをすべて実行
                var = pack.qObject.text()  # Qオブジェクトの値を取得
                self.setParamVar(self.parameter, pack, var)  # パラメータにセット
            # スライダー
            for pack in self.sliderList:  # スライダーリストをすべて実行
                var = pack.qObject.value()  # Qオブジェクトの値を取得
                self.setParamVar(self.parameter, pack, var)  # パラメータにセット
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #    パラメータのデータをオブジェクトと自分にセット
    # ---------------------------------------------------------------------------------------------------
    def loadParameters(self):
        try:
            self.setParametersToObject()  # パラメータをオブジェクトとファイルに書き込み
            self.parameter.setClassVar(self)  # メンバーのパラメータデータをセット
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトのデータをパラメータとファイルにセット
    # ---------------------------------------------------------------------------------------------------
    def saveParam(self):
        try:
            self.setParametersFromObject()  # オブジェクトのデータをパラメータとファイルにセット
            self.parameter.saveData()  # パラメータをログファイルに書き込む
            self.parameter.setClassVar(self)  # メンバーのパラメータデータをセット
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ルートノードを取得する
    # ---------------------------------------------------------------------------------------------------
    def getRoot(self, flatList):
        try:
            if flatList is not None and len(flatList) > 0:  # チェックリストが有る時
                rootList = flatList[(flatList[:, self.TREE_NODE] == GP.NODE.ROOT)]  # ツリーノードが指定された値のリスト抽出
                if rootList is not None and len(rootList) > 0:  # ツリーリストが有る時
                    root = rootList[0]  # ルートノードを取得
                    return root  # ルートノードを返す
            self.showNone()  # None表示
            return None  # ツリー辞書が無い時はNoneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ***************************************************************************************************
    #   ウィジェット処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   カラープッシュボタン設定
    # ---------------------------------------------------------------------------------------------------
    def setColorButton(self, layout, item, background, color):
        try:
            method, text = item
            object = QPushButton(text)  # プッシュボタンを生成してオブジェクトにセット
            stype = "background:" + background + ";"  # バックカラー
            stype += "color:" + color + ";"  # カラー
            stype += "font-size:10pt;"  # フォントサイズ
            object.setStyleSheet(stype);  # オブジェクトのスタイルを設定する
            layout.addWidget(object)  # layoutに生成したオブジェクトを追加
            pack = QObjectPackClass(object, method, 'bool')  # Qオブジェクトパックを生成
            self.pushButtonList.append(pack)  # プッシュボタンメソッドリストにオブジェクトパックをアペンド
            exec("self.pushButton_" + method + " = object")  # メソッド名を付けたプッシュボタンにオブジェクトをセット
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   選択プッシュボタン設定
    # ---------------------------------------------------------------------------------------------------
    def setSelButton(self, layout, item):
        try:
            object = self.setColorButton(layout, item, "lightgreen", "black")  # カラープッシュボタン設定
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   メソッドプッシュボタン設定
    # ---------------------------------------------------------------------------------------------------
    def setExeButton(self, layout, item):
        try:
            object = self.setColorButton(layout, item, "lightblue", "black")  # カラープッシュボタン設定
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   プロットプッシュボタン設定
    # ---------------------------------------------------------------------------------------------------
    def setPlotButton(self, layout, item):
        try:
            object = self.setColorButton(layout, item, "pink", "black")  # カラープッシュボタン設定
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   メニュープッシュボタン設定
    # ---------------------------------------------------------------------------------------------------
    def setMenuButton(self, layout, item):
        try:
            method, text = item
            fontSize = "10pt"
            object = QPushButton(text, self)  # プッシュボタンを生成してオブジェクトにセット
            object.setStyleSheet("background:lightblue; color:black;font-size:" + fontSize + ";")  # オブジェクトのスタイルを設定する
            #            object.setFixedSize(150,20)                                                                # 固定サイズに設定
            object.setFixedWidth(GP.MENU_WIDTH)  # 固定サイズに設定
            layout.addWidget(object)  # layoutに生成したオブジェクトを追加
            pack = QObjectPackClass(object, method, 'bool')  # Qオブジェクトパックを生成
            self.pushButtonList.append(pack)  # プッシュボタンメソッドリストにオブジェクトパックをアペンド
            exec("self.pushButton_" + method + " = object")  # メソッド名を付けたプッシュボタンにオブジェクトをセット
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   メニュープッシュボタン設定
    # ---------------------------------------------------------------------------------------------------
    def setPredButton(self, layout, item):
        try:
            method, text = item
            fontSize = "10pt"
            object = QPushButton(text)  # プッシュボタンを生成してオブジェクトにセット
            object.setStyleSheet("background:lightblue; color:black;font-size:" + fontSize + ";")  # オブジェクトのスタイルを設定する
            object.setFixedWidth(GP.PRED_BUTTON_WIDTH)  # 固定サイズに設定
            layout.addWidget(object)  # layoutに生成したオブジェクトを追加
            pack = QObjectPackClass(object, method, 'bool')  # Qオブジェクトパックを生成
            self.pushButtonList.append(pack)  # プッシュボタンメソッドリストにオブジェクトパックをアペンド
            exec("self.pushButton_" + method + " = object")  # メソッド名を付けたプッシュボタンにオブジェクトをセット
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   コンボボックス設定
    # ---------------------------------------------------------------------------------------------------
    def setComboBox(self, layout, method, varType):
        try:
            self.object = QComboBox(self)  # コンボボックスを生成してオブジェクトにセット
            layout.addWidget(self.object)  # layoutに生成したオブジェクトを追加
            pack = QObjectPackClass(self.object, method, varType)  # Qオブジェクトパックを生成
            self.comboBoxList.append(pack)  # コンボボックスリストにQオブジェクトパックをアペンド
            exec("self.comboBox_" + method + " = self.object")  # メソッド名を付けたコンボボックスにオブジェクトをセット
            return self.object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ラインエディット設定
    # ---------------------------------------------------------------------------------------------------
    def setLineEdit(self, layout, method, t):
        try:
            self.object = QLineEdit(self)  # ラインエディットを生成してオブジェクトにセット
            fontSize = "10pt"
            object.setStyleSheet("background:lightblue; color:black;font-size:" + fontSize + ";")  # オブジェクトのスタイルを設定する
            layout.addWidget(self.object)  # layoutに生成したオブジェクトを追加
            self.lineEditList.append(self.object)  # ラインエディットリストに生成したオブジェクトをアペンド
            self.lineEditMethod.append(method)  # ラインエディットメソッドリストににメソッド名をアペンド
            self.lineEditType.append(t)  # ラインエディットタイプリストにタイプ名をアペンド
            exec("self.lineEdit_" + method + " = self.object")  # メソッド名を付けたコンボボックスにオブジェクトをセット
            return self.object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   チェックボックス設定
    # ---------------------------------------------------------------------------------------------------
    def setCheckBox(self, layout, item):
        try:
            method, text = item  # メソッドとテキストの分離
            self.object = QCheckBox(text)  # チェックボックスを生成してオブジェクトにセット
            layout.addWidget(self.object)  # layoutに生成したオブジェクトを追加
            self.object.setChecked(True)  # チェックボックスをチェックする
            pack = QObjectPackClass(self.object, method, 'bool')  # Qオブジェクトパックを生成
            self.checkBoxList.append(pack)  # チェックボックスリストにQオブジェクトパックをアペンド
            exec("self.checkBox_" + method + " = self.object")  # メソッド名を付けたチェックボックスにオブジェクトをセット
            return self.object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ラジオボタン設定
    # ---------------------------------------------------------------------------------------------------
    def setRadioButton(self, layout, item):
        try:
            method, text = item  # メソッドとテキストの分離
            self.object = QRadioButton(text)  # ラジオボタンを生成してオブジェクトにセット
            layout.addWidget(self.object)  # layoutに生成したオブジェクトを追加
            self.object.setChecked(True)  # チェックボックスをチェックする
            pack = QObjectPackClass(self.object, method, 'bool')  # Qオブジェクトパックを生成
            self.checkBoxList.append(pack)  # チェックボックスリストにQオブジェクトパックをアペンド
            exec("self.checkBox_" + method + " = self.object")  # メソッド名を付けたチェックボックスにオブジェクトをセット
            return self.object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   チェックボックス設定
    # ---------------------------------------------------------------------------------------------------
    def setCheckBoxGrid(self, grid, row, column, item, color):
        try:
            method, text = item  # メソッドとテキストの分離
            self.object = QCheckBox(text)  # チェックボックスを生成してオブジェクトにセット
            grid.addWidget(self.object, row, column)  # layoutに生成したオブジェクトを追加
            self.object.setChecked(True)  # チェックボックスをチェックする
            pack = QObjectPackClass(self.object, method, 'bool')  # Qオブジェクトパックを生成
            self.checkBoxList.append(pack)  # チェックボックスリストにQオブジェクトパックをアペンド
            exec("self.checkBox_" + method + " = self.object")  # メソッド名を付けたチェックボックスにオブジェクトをセット
            return self.object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   チェックボックス設定
    # ---------------------------------------------------------------------------------------------------
    def setCheckBoxGrid2(self, grid, row, column, method):
        try:
            self.object = QCheckBox(method, self)  # チェックボックスを生成してオブジェクトにセット
            grid.addWidget(self.object, row, column)  # layoutに生成したオブジェクトを追加
            self.object.setChecked(True)  # チェックボックスをチェックする
            pack = QObjectPackClass(self.object, method, 'bool')  # Qオブジェクトパックを生成
            self.checkBoxList.append(pack)  # チェックボックスリストにQオブジェクトパックをアペンド
            exec("self.checkBox_" + method + " = self.object")  # メソッド名を付けたチェックボックスにオブジェクトをセット
            return self.object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ラベル設定
    # ---------------------------------------------------------------------------------------------------
    def setLabel(self, layout, text):
        try:
            object = QLabel(text, self)  # ラベルを生成してオブジェクトにセット
            fontSize = "10pt"
            object.setStyleSheet("background:#EEE;color:black;font-size:" + fontSize + ";")  # オブジェクトのスタイルを設定する
            layout.addWidget(object)  # layoutに生成したオブジェクトを追加
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   文字カラーを指定したラベル設定
    # ---------------------------------------------------------------------------------------------------
    def setLabelColor(self, layout, text, color):
        try:
            object = QLabel(text, self)  # ラベルを生成してオブジェクトにセット
            layout.addWidget(object)  # layoutに生成したオブジェクトを追加
            fontSize = "10pt"
            object.setStyleSheet(
                "background:lightblue; color:" + color + ";font-size:" + fontSize + ";")  # オブジェクトのスタイルを設定する
            object.setStyleSheet("color:" + color + ";");  # オブジェクトのスタイルを設定する
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   文字カラーを指定したラベル設定
    # ---------------------------------------------------------------------------------------------------
    def setLabelColorGrid(self, grid, row, column, text, color):
        try:
            object = QLabel(text, self)  # ラベルを生成してオブジェクトにセット
            fontSize = "10pt"
            object.setStyleSheet(
                "background:lightblue; color:" + color + ";font-size:" + fontSize + ";")  # オブジェクトのスタイルを設定する
            grid.addWidget(object, row, column)  # layoutに生成したオブジェクトを追加
            object.setStyleSheet("color:" + color + ";");  # オブジェクトのスタイルを設定する
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   スタイルを指定したラベル設定
    # ---------------------------------------------------------------------------------------------------
    def setLabelStyle(self, layout, text, background, color, align):
        try:
            object = QLabel(text, self)  # ラベルを生成してオブジェクトにセット
            layout.addWidget(object)  # layoutに生成したオブジェクトを追加
            fontSize = "10pt"
            object.setStyleSheet(
                "background:" + background + "; color:" + color + ";font-size:" + fontSize + ";");  # オブジェクトのスタイルを設定する
            object.setAlignment(align)  # 指定したアライメントにセット
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   スタイルを指定したラベル設定
    # ---------------------------------------------------------------------------------------------------
    def setLabelStyle(self, layout, text, background, color, align):
        try:
            object = QLabel(text, self)  # ラベルを生成してオブジェクトにセット
            layout.addWidget(object)  # layoutに生成したオブジェクトを追加
            fontSize = "10pt"
            object.setStyleSheet(
                "background:" + background + "; color:" + color + ";font-size:" + fontSize + ";");  # オブジェクトのスタイルを設定する
            object.setAlignment(align)  # 指定したアライメントにセット
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   スタイルを指定したラベル設定
    # ---------------------------------------------------------------------------------------------------
    def setLabelStyle2(self, layout, text, background, color, height, fontSize):
        try:
            object = QLabel(text, self)  # ラベルを生成してオブジェクトにセット
            layout.addWidget(object)  # layoutに生成したオブジェクトを追加
            object.setStyleSheet(
                "background:" + background + "; color:" + color + ";font-size:" + fontSize + ";");  # オブジェクトのスタイルを設定する
            object.setAlignment(Qt.AlignCenter)  # 指定したアライメントにセット
            object.setFixedHeight(height)  # 指定したアライメントにセット
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   プログレスバー設定
    # ---------------------------------------------------------------------------------------------------
    def setProgressBar(self, layout, height):
        try:
            object = QProgressBar()  # プログレスバー生成
            object.setFixedHeight(height)  # 固定高さ
            object.setSizePolicy(  # サイズポリシー設定
                QSizePolicy.Expanding,  # 幅可変
                QSizePolicy.Fixed)  # 高さ拡張
            layout.addWidget(object)  # プログレスバー0をメインレイアウトに追加
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ***************************************************************************************************
    #   レイアウト処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   ツリーレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createTreeLayout(self, title, treeWidget, viewLayout):
        try:
            # メインレイアウト
            main = QVBoxLayout()  # メインレイアウト生成（垂直レイアウト）
            main.setAlignment(Qt.AlignTop)  # 上詰め
            self.setLabelStyle2(main, title, "gray", "white", 40, "12pt")  # 表題ラベル
            # メイン本体レイアウト
            main_body = QHBoxLayout()  # メインレイアウト本体生成（垂直レイアウト）
            main_body.addWidget(treeWidget)  # メインレイアウト本体にツリー ウイジェットを追加
            main_body.addLayout(viewLayout)  # メイン本体レイアウトにビューレイアウトを追加
            main.addLayout(main_body)  # メインレイアウトにメイン本体レイアウト本体を追加
            return main  # メインレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   チェックボックスレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setCheckLayout(self, layout, methodDic):
        try:
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            for item in methodDic.items():  # メソッド辞書をすべて実行
                checkBox = self.setCheckBox(hLayout, item)  # チェックボックス設定
            layout.addLayout(hLayout)  # layoutに水平レイアウトを追加

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   チェックボックスグループ設定
    # ---------------------------------------------------------------------------------------------------
    def setCheckGroup(self, layout, methodDic, title):
        try:
            groupBox = QGroupBox(title)
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            for item in methodDic.items():  # メソッド辞書をすべて実行
                checkBox = self.setCheckBox(hLayout, item)  # チェックボックス設定
            groupBox.setLayout(hLayout)  # 釦グループに追加
            groupBox.setStyleSheet(
                "QGroupBox {"
                "background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1,"
                "stop:0 #c0c0c0, stop:1 #ffffff);"
                "border:2px solid gray; border-radius:3px; margin-top:4ex;"
                "}"
                "QGroupBox::title {"
                "subcontrol-origin:margin; subcontrol-position:top center; padding:0 3px;"
                "}")
            layout.addWidget(groupBox)  # layoutに水平レイアウトを追加

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ラジオボタングループ設定
    # ---------------------------------------------------------------------------------------------------
    def setRadioGroup(self, layout, methodDic, title):
        try:
            groupBox = QGroupBox(title)
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            for item in methodDic.items():  # メソッド辞書をすべて実行
                radioButton = self.setRadioButton(hLayout, item)  # ラジオボタン設定
            groupBox.setLayout(hLayout)  # 釦グループに追加
            groupBox.setStyleSheet(
                "QGroupBox {"
                "background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1,"
                "stop:0 #c0c0c0, stop:1 #ffffff);"
                "border:2px solid gray; border-radius:3px; margin-top:4ex;"
                "}"
                "QGroupBox::title {"
                "subcontrol-origin:margin; subcontrol-position:top center; padding:0 3px;"
                "}")
            layout.addWidget(groupBox)  # layoutに水平レイアウトを追加

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #    ボタングループレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setButtonGroup(self, layout, groupMethod, methodDic):
        try:
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            self.buttonGroup = QButtonGroup()  # 釦グループ生成
            for method, text in methodDic.items():  # メソッド辞書をすべて実行
                self.object = QPushButton(text)  # プッシュボタンを生成してオブジェクトにセット
                self.object.setFixedWidth(int(GP.AGE_SEL))  # 固定サイズに設定
                hLayout.addWidget(self.object)  # layoutに生成したオブジェクトを追加
                exec("self.checkBox_" + method + " = self.object")  # メソッド名を付けたチェックボックスにオブジェクトをセット
                self.object.setCheckable(True)
                self.buttonGroup.addButton(self.object)  # 釦グループに追加
                self.buttonGroup.setExclusive(True)  # 排他にセット
            #                self.object.setStyleSheet(
            #                    "background-color:yellow; color:red;  border-radius:8px;"
            #                    "border-color:blue; border-style:solid; border-width:4px;")
            self.buttonGroup.buttons()[0].setChecked(True)  # 最初のチェックボックスをチェック
            pack = QObjectPackClass(self.buttonGroup, groupMethod, 'bool')  # Qオブジェクトパックを生成
            self.checkGroupList.append(pack)  # チェックボックスリストにQオブジェクトパックをアペンド
            layout.addLayout(hLayout)  # layoutに水平レイアウトを追加

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   コンボボックスレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setComboLayout(self, layout, method, text, t, valueList):
        try:
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            label = self.setLabel(hLayout, text)  # ラベルを生成
            comboBox = self.setComboBox(hLayout, method, t)  # コンボボックスを生成
            for value in valueList:  # アイテムリストをすべて実行
                comboBox.addItem(value)  # コンボボックスにアイテムを挿入
            layout.addLayout(hLayout)  # layoutに水平レイアウトを追加

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   コンボボックスレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setComboLayout2(self, layout, item, t, valueList):
        try:
            method, text = item  # メソッドとテキストの分離
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            label = self.setLabel(hLayout, text)  # ラベルを生成
            comboBox = self.setComboBox(hLayout, method, t)  # コンボボックスを生成
            for value in valueList:  # 値リストをすべて実行
                comboBox.addItem(value)  # コンボボックスに値を挿入
            layout.addLayout(hLayout)  # layoutに水平レイアウトを追加

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ストリング型コンボボックスレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setStrCombo(self, layout, item, itemList):
        try:
            self.setComboLayout2(layout, item, "str", itemList)  # コンボボックスレイアウト設定を呼び出す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   コンボボックスレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setComboLayoutFix(self, layout, item, t, itemList):
        try:
            method, text = item  # メソッドとテキストの分離
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            label = self.setLabel(hLayout, text)  # ラベルを生成
            label.setFixedWidth(int(GP.MENU_WIDTH / 2 - 10))  # 固定サイズに設定
            comboBox = self.setComboBox(hLayout, method, t)  # コンボボックスを生成
            for item in itemList:  # アイテムリストをすべて実行
                comboBox.addItem(item)  # コンボボックスにアイテムを挿入
                comboBox.setFixedWidth(int(GP.MENU_WIDTH / 2 - 10))  # 固定サイズに設定
            layout.addLayout(hLayout)  # layoutに水平レイアウトを追加

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ストリング型コンボボックスレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setStrComboFix(self, layout, item, itemList):
        try:
            self.setComboLayoutFix(layout, item, "str", itemList)  # コンボボックスレイアウト設定を呼び出す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   整数型コンボボックスレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setIntCombo(self, layout, item, itemList):
        try:
            self.setComboLayout2(layout, item, "int", itemList)  # コンボボックスレイアウト設定を呼び出す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   浮動小数型コンボボックスレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setFloatCombo(self, layout, item, itemList):
        try:
            self.setComboLayout2(layout, item, "float", itemList)  # コンボボックスレイアウト設定を呼び出す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ラインエディットレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setLineEditLayout(self, layout, method, t):
        try:
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            label = self.setLabel(hLayout, method)  # ラベルを生成
            lineEdit = self.setLineEdit(hLayout, method, t)  # ラインエディットを生成
            layout.addLayout(hLayout)  # layoutに水平レイアウトを追加

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ラインエディットグリッドレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setLineEditGrid(self, layout, row, method, t):
        try:
            label = QLabel(method, self)  # ラベルを生成してオブジェクトにセット
            lineEdit = QLineEdit(self)  # ラインエディットを生成してオブジェクトにセット
            self.lineEditList.append(lineEdit)  # ラインエディットリストに生成したオブジェクトをアペンド
            self.lineEditMethod.append(lineEdit)  # ラインエディットメソッドリストににメソッド名をアペンド
            self.lineEditType.append(t)  # ラインエディットタイプリストにタイプ名をアペンド
            exec("self.lineEdit_" + method + " = lineEdit")  # メソッド名を付けたコンボボックスにオブジェクトをセット
            layout.addWidget(label, row, 0)  # グリッド(row,0)にラベルをセット
            layout.addWidget(lineEdit, row, 1)  # グリッド(row,1)にラベルをセット

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス プログレスウインドウ
# =======================================================================================================
class ProgressWindowClass(QtBaseClass):
    def __init__(self):  # 初期化
        try:
            QtBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.levels = 6  # レベル数
            self.startTime = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 実行時間計測用配列
            self.setParent(None)  # スーパークラスをNoneに設定
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.mySize = QSize(500, 100)  # ウインドウサイズセット
            self.resize(self.mySize)  # ウインドウサイズ設定
            deskTopSize = self.getDesktopSize()  # デスクトップサイズ取得
            self.move(deskTopSize.width() - 30 - self.mySize.width(), 110)  # ウインドウ位置設定
            #            self.setWindowFlags(Qt.Window|Qt.WindowCloseButtonHint|Qt.WindowStaysOnTopHint)             # ウインドウフラグ設定
            self.level = -1  # 進捗レベル初期化
            self.progressCount = [0] * self.levels  # 現レベルの進捗度初期化
            self.maxCount = [0] * self.levels  # 現レベルの最大カウント

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            # メインレイアウト
            title = "ステータス"  # 表題
            subTitle = "処理終了までお待ち下さい"  # サブタイトル
            main = QVBoxLayout()  # メインレイアウト生成（垂直レイアウト）
            main.setAlignment(Qt.AlignTop)  # 上詰め
            self.subTitleLabel = ["サブステータス"] * self.levels  # サブタイトルラベル配列生成
            self.progressBar = [None] * self.levels  # プログレスバー配列生成
            for i in range(self.levels):  # レベルをすべて実行
                subTitleLabel = self.setLabelStyle2(main, subTitle, "gray", "white", 25, "10pt")  # サブタイトルラベル生成
                progressBar = self.setProgressBar(main, 20)  # プログレスバー生成
                self.subTitleLabel[i] = subTitleLabel  # サブタイトルラベー配列にセット
                self.progressBar[i] = progressBar  # プログレスバー配列にセット
                self.subTitleLabel[i].hide()  # サブタイトルラベー配列にセット
                self.progressBar[i].hide()  # プログレスバー配列にセット
            return main  # メインレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   カレントのレベルを表示
    # ---------------------------------------------------------------------------------------------------
    def showCurrLevel(self, maxCount, subTitle):
        try:
            self.maxCount[self.level] = maxCount + 1  # 現レベルの最大カウント
            self.progressCount[self.level] = 1  # 現レベルの進捗度初期化
            self.subTitleLabel[self.level].setText(subTitle)  # サブタイトルセット
            self.progressBar[self.level].setRange(0, maxCount + 1)  # プログレスバーのレンジセット
            self.subTitleLabel[self.level].setVisible(True)  # サブタイトルラベーを表示
            self.progressBar[self.level].setVisible(True)  # プログレスバーを表示
            self.progressBar[self.level].setValue(1)  # プログレスバーのバリューをセット
            for i in range(self.level + 1, self.levels):  # 現レベル以後をリセット
                self.progressBar[i].setValue(0)  # プログレスバーのバリューをセット
            self.show()  # 進捗ダイアローグを開く

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   カレントのレベルを隠す
    # ---------------------------------------------------------------------------------------------------
    def hideCurrLevel(self):
        try:
            self.subTitleLabel[self.level].setText("")  # サブタイトル消去
            self.subTitleLabel[self.level].hide()  # サブタイトルラベルを隠す
            self.progressBar[self.level].hide()  # プログレスバーを隠す
            QApplication.processEvents()  # プロセスイベントを呼んで制御をイベントループに返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ***************************************************************************************************
    #   イベント処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   新レベル開始シグナルイベント処理
    # ---------------------------------------------------------------------------------------------------
    def startNewLevel(self, maxCount, subText):
        try:
            self.level += 1  # 進捗レベル更新
            self.showCurrLevel(maxCount, subText)  # カレントのレベルを表示
            QApplication.processEvents()  # プロセスイベントを呼んで制御をイベントループに返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   現レベル終了シグナルイベント処理
    # ---------------------------------------------------------------------------------------------------
    def endLevel(self):
        try:
            if self.progressCount[self.level] != self.maxCount[self.level]:  # 進捗カウントが最大カウントに達していない時
                self.progressCount[self.level] = self.maxCount[self.level] - 1  # 進捗カウントを終了カウント－１にする
                self.emit()  # プログレスシグナル処理を呼ぶ
            if self.level == 0:  # 進捗レベルが0の時
                self.level -= 1  # 進捗レベル更新
                self.close()  # 閉じる
            else:  # 進捗レベルが1以上の時
                self.hideCurrLevel()  # カレントのレベルを隠す
                self.level -= 1  # 進捗レベル更新
                self.emit()  # 上位レベルの進捗を進める
                self.resize(self.mySize)  # ウインドウサイズ設定
            QApplication.processEvents()  # プロセスイベントを呼んで制御をイベントループに返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   プログレスシグナルイベント処理
    # ---------------------------------------------------------------------------------------------------
    def emit(self, n=1):
        try:
            self.progressCount[self.level] += n  # 現レベルの進捗度初期化
            self.progressBar[self.level].setValue(self.progressCount[self.level])  # プログレスバーのバリューをセット
            QApplication.processEvents()  # プロセスイベントを呼んで制御をイベントループに返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス CH年齢予測値パラメータクラス
# =======================================================================================================
class CheckWindowParameterClass(ParameterClass):
    # ---------------------------------------------------------------------------------------------------
    #   クラス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None

    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, logPath, listPack):  # 初期化
        try:
            ParameterClass.__init__(self, logPath)  # スーパークラスの初期化
            self.listPack = listPack
            flagList = [True] * listPack.length  # データ選択フラグ初期化
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != 'logPath') and
                             (name != 'listPack') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
            self.loadData()  # タブパラメータをファイルから読み込み
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# =======================================================================================================
#   クラス チェックウインドウ
# =======================================================================================================
class CheckWindowClass(QtBaseClass):
    def __init__(self, title, logPath, listPack, crList):  # 初期化
        try:
            QtBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.title = title  # タイトル
            #            self.setWindowTitle(self.title)                                                             # ウインドウのタイトルセット
            self.listPack = listPack  # リスト
            self.crList = crList  # Xデータ段落設定リスト設定(リストの項目の値毎に段落替え)
            self.parameter = CheckWindowParameterClass(logPath, listPack)  # パラメータ
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.connectButtons2()  # レイアウトのメンバーのコネクションをセット
            self.setMinimumWidth(260)  # ウインドウサイズ設定
            self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        #            self.setWindowModality(Qt.WindowModal)                                                      # モーダルにする

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトのデータをフラグリストにセット
    # ---------------------------------------------------------------------------------------------------
    def saveFlags(self):
        try:
            for i, pack in enumerate(self.checkBoxList):  # チェックボックスリストをすべて実行
                self.flagList[i] = pack.qObject.isChecked()  # チェックボックスの値をフラグリストにセット

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            mLayout = QVBoxLayout()  # メインレイアウト（垂直レイアウト）生成
            self.setLabelStyle(mLayout, self.title, "gray", "white", Qt.AlignCenter)  # 表題ラベル
            # クリアボタン
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            clearButton = self.setSelButton(hLayout, ['CLEAR_ALL', "クリア"])  # オールクリア釦を作成
            setButton = self.setSelButton(hLayout, ['SET_ALL', "セット"])  # オールセット釦を作成
            mLayout.addLayout(hLayout)  # 水平レイアウトをレイアウトに加える
            # チェックボックス
            self.checkBox_flagList = [None] * self.listPack.length  # エポック数配列
            groupBox = QGroupBox()  # 垂直レイアウト生成
            spaceing = 10  # グリッド間隔
            grid = QGridLayout(self)  # グリッドレイアウト生成
            grid.setSpacing(spaceing)  # グリッドスペース設定
            column = 0  # 列初期化
            for n in range(len(self.crList) - 1):  # 段落設定リストを一つ前まで実行
                row = 0  # 行初期化
                begin = self.crList[n]  # 開始
                end = self.crList[n + 1]  # 終了
                for i in range(begin, end):  # 開始から終了までのデータリストを実行
                    text = self.listPack.LIST[i]  # テキスト取得
                    method = "flagList[" + str(i) + "]"  # メソッド作成
                    color = self.listPack.QT_COLOR_LIST[i]  # QT用カラー取得
                    label = self.setLabelColorGrid(grid, row, column, "●", color)  # ラベルを作成
                    label.setAlignment(Qt.AlignRight)  # 指定したアライメントにセット
                    checkBox = self.setCheckBoxGrid(grid, row, column + 1, [method, text], color)  # チェックボックスを作成
                    row += 1  # 行加算
                column += 2  # 列加算
            groupBox.setLayout(grid)  # hLayoutにgridを加える
            mLayout.addWidget(groupBox)  # メインレイアウトに水平レイアウトを加える
            mLayout.setAlignment(Qt.AlignTop)  # 上詰め
            return mLayout  # メインレイアウトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   チェックボックスを全てリセット
    # ---------------------------------------------------------------------------------------------------
    def CLEAR_ALL(self):
        try:
            self.parameter.flagList = [False] * len(self.flagList)  # パラメータのフラグリストをすべて偽にする
            self.parameter.setClassVar(self)  # フラグリストに転写
            self.setParametersToObject()  # オブジェクトのデータをフラグリストにセット

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   チェックボックスを全てセット
    # ---------------------------------------------------------------------------------------------------
    def SET_ALL(self):
        try:
            self.parameter.flagList = [True] * len(self.flagList)  # パラメータのフラグリストをすべて偽にする
            self.parameter.setClassVar(self)  # フラグリストに転写
            self.setParametersToObject()  # オブジェクトのデータをフラグリストにセット

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

