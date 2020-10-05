import os
import numpy as np
from PyQt5Import import *
from staticImport import *
from qtBase import QtBaseClass
from comb import CombClass
from resultView import AgeResultViewClass
from resultView import EvtResultViewClass
from resultView import MonitorViewClass
from ageLearn import AgeLearnClass
from evtLearn import EvtLearnClass

from ctypes import *
# import win32gui
# import win32con
# import win32print
# import win32ui

from classDef import AgeLearnParameterClass
from classDef import EvtLearnParameterClass
from qtBase import CheckWindowClass
from modelComb import ModelCombClass


# =======================================================================================================
#   クラス 学習ビュークラス
# =======================================================================================================
class LearnViewClass(QtBaseClass):
    # ---------------------------------------------------------------------------------------------------
    # クラス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None

    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, parent):  # 初期化
        try:
            if LearnViewClass._singleton is None:  # シングルトンが無いとき
                QtBaseClass.__init__(self, None)  # スーパークラスの初期化
                self.layout = self.createMainLayout()  # レイアウトを生成する
                self.setLayout(self.layout)  # レイアウトをセット
                self.setSizePolicy(  # サイズポリシー設定
                    QSizePolicy.Expanding,  # 幅可変
                    QSizePolicy.Expanding)  # 高さ可変

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self, parent=None):
        if LearnViewClass._singleton is None:  # シングルトンが無いとき
            LearnViewClass._singleton = LearnViewClass(parent)  # インスタンスを生成してシングルトンにセット
        return LearnViewClass._singleton  # シングルトンがを返す

    # ---------------------------------------------------------------------------------------------------
    #   メインレイアウト生成
    # ---------------------------------------------------------------------------------------------------
    def createMainLayout(self):
        try:
            self.tabs = QTabWidget()  # タブウィジェット生成

            # タブ生成
            self.ageLearnTab = AgeLearnViewClass("年齢学習", GP.LEARN_LOG.AGE_LEARN)  # 年齢学習タブ生成
            self.evtLearnTab = EvtLearnViewClass("イベント学習", GP.LEARN_LOG.EVT_LEARN)  # イベント学習タブ生成

            # タブリストにタブを登録
            self.tabList = []  # 空のタブリスト生成
            self.tabList.append(self.ageLearnTab)  # 年齢学習タブ追加
            self.tabList.append(self.evtLearnTab)  # イベント学習タブ追加
            # タブをタブリストに追加
            for tab in self.tabList:  # タブリストをすべて実行
                self.tabs.addTab(tab, tab.title)  # タブをタブリストに追加

            # Add tabs to widget
            mLayout = QVBoxLayout(self)  # 垂直レイアウト生成
            mLayout.addWidget(self.tabs)  # 垂直レイアウトにタブウィジェットを追加
            return mLayout  # メインレイアウトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス 年齢学習タブクラス
# =======================================================================================================
class AgeLearnViewClass(QtBaseClass):
    def __init__(self, title, strPath):  # 初期化
        try:
            QtBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.parameter = AgeLearnParameterClass.getInstance()  # パラメータ
            self.monitorView = MonitorViewClass(title + "モニター", self.parameter)  # 学習結果モニタービュー転写
            self.resultView = AgeResultViewClass.getInstance()  # 学習結果ビューを生成
            self.treeWidget = GP.TREE.AGE_LEARN  # ツリー ウイジェット転写
            self.title = title  # タブのタイトル
            self.strPath = strPath  # パラメータ保存パス
            viewLayout = self.makeViewLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout = self.createTreeLayout(self.title, self.treeWidget, viewLayout)  # ツリーレイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.connectButtons2()  # レイアウトのメンバーのコネクションをセット
            self.learn = None  # 学習クラス初期化

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #  ビューレイアウト作成
    # ---------------------------------------------------------------------------------------------------
    def makeViewLayout(self):
        try:
            # 配列作成
            self.comboBox_RANDOM_SCALE = [None, None]  # ランダム分散係数配列
            # ビューレイアウト
            viewLayout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            viewLayout.setAlignment(Qt.AlignTop)  # 上詰め
            batchSizeRange = self.flatRange(1, 99, 1) + self.flatRange(100, 990, 10) + self.flatRange(1000, 9900,
                                                                                                      100)  # ミニバッチサイズレンジ
            self.setLabelStyle2(viewLayout, "パラメータ", "gray", "white", 40, "12pt")  # 表題ラベル
            self.setStrCombo(viewLayout, ["AGE_BASE", "年齢基準"], [GP.AGE_BASE.MAX, GP.AGE_BASE.TARGET])  # 年齢基準
            self.setIntCombo(viewLayout, ["HIDDEN_LAYERS", "隠れ層数"], self.flatRange(0, 100))  # 隠れ層数
            self.setFloatCombo(viewLayout, ["DROPOUT", "ドロップアウト"], self.flatRange(0.001, 1, 0.001))  # ドロップアウト
            self.setStrCombo(viewLayout, ["LEARN_PARTS", "学習部品"], GP.PARTS.nameList)  # 分析選択
            self.setStrCombo(viewLayout, ["LEARN_UNIT", "学習単位"],
                             [GP.LEARN_UNIT.TYPE_CODE, GP.LEARN_UNIT.TYPE_ID, GP.LEARN_UNIT.LASER_ID])  # 学習単位
            self.setIntCombo(viewLayout, ["SAMPLES", "ラベル毎のデータ数"], self.flatRange(100, 100000, 100))  # ラベル毎のデータ数

            self.setIntCombo(viewLayout, ["VERBOSE", "VERBOSE"], self.flatRange(0, 2))  # VERBOSE
            self.setCheckBox(viewLayout, ["USE_ABNORMAL", "異常値使用"])  # 異常値使用フラグ
            self.setCheckBox(viewLayout, ["SAVE_FLAG", "保存"])  # 保存フラグ
            EPOCHS_itemList = self.flatRange(1, 500, 1)  # エポックアイテムリスト
            self.setIntCombo(viewLayout, ["BATCH_SIZE", "バッチサイズ"], batchSizeRange)  # ミニバッチサイズ
            self.setIntCombo(viewLayout, ["INIT_EPOCHS", "初期エポック数"], EPOCHS_itemList)  # エポック数
            self.setIntCombo(viewLayout, ["CUT_EPOCHS", "カットエポック数"], EPOCHS_itemList)  # エポック数
            self.setIntCombo(viewLayout, ["CUT_TRIALS", "カット回数"], self.flatRange(0, 300))  # カット回数
            self.setFloatCombo(viewLayout, ["SAMPLE_RATIO_0", "初回サンプル割合"],
                               self.flatRange(0.0, 1.0, 0.01))  # 初回上位のデータサンプル割合
            self.setFloatCombo(viewLayout, ["SAMPLE_RATIO_N", "以後サンプル割合"],
                               self.flatRange(0.0, 1.0, 0.01))  # 次回以後上位のデータサンプル割合
            # 前期学習
            buttonLayout = QHBoxLayout()  # 釦レイアウト生成（水平レイアウト）
            buttonLayout1 = QVBoxLayout()  # 釦レイアウト1生成（垂直レイアウト）
            buttonLayout1.setAlignment(Qt.AlignTop)  # 上詰め
            self.setExeButton(buttonLayout1, ["MAKE_LEARN_BEFORE", "前期学習データ生成"])  # 前期学習データ生成
            self.setExeButton(buttonLayout1, ["LEARN_BEFORE", "前期学習"])  # 前期学習
            self.setExeButton(buttonLayout1, ["ADDLEARN_BEFORE", "前期追加学習"])  # 前期追加学習
            self.setExeButton(buttonLayout1, ["CUTLEARN_BEFORE", "前期カットモデル学習"])  # 前期カットモデル学習
            self.setPlotButton(buttonLayout1, ["PLOT_BEFORE", "前期学習結果表示"])  # 前期学習結果表示
            buttonLayout.addLayout(buttonLayout1)  # 釦レイアウトに釦レイアウト１を加える
            # 後期学習
            buttonLayout2 = QVBoxLayout()  # 釦レイアウト２生成（垂直レイアウト）
            buttonLayout2.setAlignment(Qt.AlignTop)  # 上詰め
            self.setExeButton(buttonLayout2, ["MAKE_LEARN_AFTER", "後期学習データ生成"])  # 後期学習データ生成
            self.setExeButton(buttonLayout2, ["LEARN_AFTER", "後期学習"])  # 後期学習
            self.setExeButton(buttonLayout2, ["ADDLEARN_AFTER", "後期追加学習"])  # 後期追加学習
            self.setExeButton(buttonLayout2, ["CUTLEARN_AFTER", "後期カットモデル学習"])  # 後期カットモデル学習
            self.setPlotButton(buttonLayout2, ["PLOT_AFTER", "後期学習結果表示"])  # 後期学習結果表示
            buttonLayout.addLayout(buttonLayout2)  # 釦レイアウトに釦レイアウト3を加える
            # 学習結果
            buttonLayout3 = QVBoxLayout()  # 釦レイアウト２生成（垂直レイアウト）
            buttonLayout3.setAlignment(Qt.AlignTop)  # 上詰め
            self.setPlotButton(buttonLayout3, ["PRINT", "学習結果印刷"])  # Xデータマージ学習結果表示（フィルターレベル0）
            buttonLayout.addLayout(buttonLayout3)  # 釦レイアウトに釦レイアウト２を加える
            viewLayout.addLayout(buttonLayout)  # メインレイアウトに釦レイアウトを加える
            return viewLayout  # ビューレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   インスタント変数セット
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self):
        try:
            if self.LEARN_PARTS == GP.PARTS.CH:  # 学習部品がCHの時
                CURPARTS = GP.PCONT.CH  # 学習部品をセット
            elif self.LEARN_PARTS == GP.PARTS.LN:  # 学習部品がLNの時
                CURPARTS = GP.PCONT.LN  # 学習部品をセット
            elif self.LEARN_PARTS == GP.PARTS.PPM:  # 学習部品がPPMの時
                CURPARTS = GP.PCONT.PPM  # 学習部品をセット
            elif self.LEARN_PARTS == GP.PARTS.MM:  # 学習部品がMMの時
                CURPARTS = GP.PCONT.MM  # 学習部品をセット
            else:
                return False  # 失敗を返す
            self.learnParam = self.parameter  # パラメータ
            GP.CURPARTS = CURPARTS  # 学習部品
            TYPE = GP.LEARN_TYPE.AGE  # 学習タイプセット
            self.treeWidget = GP.TREE.AGE_LEARN  # ツリー ウイジェット転写
            laserIdList = self.treeWidget.laserIdList  # レーザーIDリスト転写
            LEARN_UNIT = self.parameter.LEARN_UNIT  # 学習単位を取得
            GP.CONT.setLabelList(TYPE)  # 出力ラベルリストをセット
            UNIT_NAME = self.treeWidget.getUnitName(self.parameter.LEARN_UNIT)  # 学習単位名を取得
            if UNIT_NAME is not None:  # 学習単位名が有効な時
                CURPARTS.TYPE = TYPE  # 学習タイプセット
                CURPARTS.LEARN = CURPARTS.AGE.LEARN_CLASS  # 学習クラスをセット
                CURPARTS.LEARN.stop = False  # 学習クラスのストップフラグ初期化
                CURPARTS.PCOMB.setClassVar(laserIdList, self.parameter)  # 学習パラメーターを更新する
                CURPARTS.LEARN_UNIT = LEARN_UNIT  # 学習単位をセット
                CURPARTS.UNIT_NAME = UNIT_NAME  # 学習単位名をセット
                CURPARTS.AGE.setClassVar(laserIdList, self.parameter)  # 学習パラメーターを更新する
                CURPARTS.AGE.setLearnUnit(LEARN_UNIT, UNIT_NAME)  # 学習単位と学習単位名をセット
                CURPARTS.MODEL_COMB_LIST = CURPARTS.AGE.MODEL_COMB_LIST  # モデルコンボをセット
                for MODEL_COMB in CURPARTS.MODEL_COMB_LIST:  # 学習名をすべて
                    MODEL_COMB.setClassVar(laserIdList, self.parameter)  # 学習単位と学習単位名をセット
                return True  # 成功を返す
            return False  # 失敗を返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ***************************************************************************************************
    #   メニュー
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   学習データ生成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_LEARN_BEFORE(self):
        try:
            if self.setClassVar():  # 初期設定に成功した時
                GP.CURPARTS.LEARN.makeLearnData()  # 学習データ生成
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   前期年齢学習
    # ---------------------------------------------------------------------------------------------------
    def LEARN_BEFORE(self):
        try:
            if self.setClassVar():  # 初期設定に成功した時
                GP.CURPARTS.LEARN.learn(0, self.monitorView)  # 前期年齢学習

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   前期年齢追加学習
    # ---------------------------------------------------------------------------------------------------
    def ADDLEARN_BEFORE(self):
        try:
            if self.setClassVar():  # 初期設定に成功した時
                GP.CURPARTS.LEARN.addLearn(0, self.monitorView)  # 前期年齢追加学習

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   前期カットモデル学習
    # ---------------------------------------------------------------------------------------------------
    def CUTLEARN_BEFORE(self):
        try:
            if self.setClassVar():  # 初期設定に成功した時
                GP.CURPARTS.LEARN.learnCutModel(0, self.monitorView)  # 前期カットモデル学習

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   後期学習データ生成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_LEARN_AFTER(self):
        try:
            if self.setClassVar():  # 初期設定に成功した時
                GP.CURPARTS.LEARN.makeLearnDataAfter(3)  # 後期学習データ生成
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   後期年齢学習
    # ---------------------------------------------------------------------------------------------------
    def LEARN_AFTER(self):
        try:
            if self.setClassVar():  # 初期設定に成功した時
                GP.CURPARTS.LEARN.learn(3, self.monitorView)  # 後期年齢学習

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   後期年齢追加学習
    # ---------------------------------------------------------------------------------------------------
    def ADDLEARN_AFTER(self):
        try:
            if self.setClassVar():  # 初期設定に成功した時
                GP.CURPARTS.LEARN.addLearn(3, self.monitorView)  # 後期年齢追加学習

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   後期カットモデル学習
    # ---------------------------------------------------------------------------------------------------
    def CUTLEARN_AFTER(self):
        try:
            if self.setClassVar():  # 初期設定に成功した時
                GP.CURPARTS.LEARN.learnCutModel(3, self.monitorView)  # 後期カットモデル学習

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   前期年齢学習結果プロット
    # ---------------------------------------------------------------------------------------------------
    def PLOT_BEFORE(self):
        try:
            if self.setClassVar():  # 初期設定に成功した時
                self.parameter.setClassVar(self.resultView)  # イベントデータをインスタンス変数に転写する
                GP.CURPARTS.MODEL_COMB = GP.CURPARTS.MODEL_COMB_LIST[2]  # モデルコンボを転写
                self.resultView.redraw()  # 学習結果ビューを表示
                self.resultView.show()  # 学習結果ビューを表示

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   後期年齢学習結果プロット
    # ---------------------------------------------------------------------------------------------------
    def PLOT_AFTER(self):
        try:
            if self.setClassVar():  # 初期設定に成功した時
                self.parameter.setClassVar(self.resultView)  # イベントデータをインスタンス変数に転写する
                GP.CURPARTS.MODEL_COMB = GP.CURPARTS.MODEL_COMB_LIST[5]  # モデルコンボを転写
                self.resultView.redraw()  # 学習結果ビューを表示
                self.resultView.show()  # 学習結果ビューを表示

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   印刷テスト
    # ---------------------------------------------------------------------------------------------------
    def PRINT(self):
        user32 = windll.user32
        user32.MessageBoxA(0, "Hello, MessageBox!", "Python to Windows API", 0x00000040)
        return
        self.printTest()  # 初期設定

    # ---------------------------------------------------------------------------------------------------
    #   印刷テスト
    # ---------------------------------------------------------------------------------------------------
    def printTest(self, sentence):
        INCH = 1440
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
        hDC.StartDoc('TestPrint')
        hDC.StartPage()
        hDC.SetMapMode(win32con.MM_TWIPS)
        hDC.DrawText(sentence, (0, INCH * -1, INCH * 8, INCH * -2), win32con.DT_CENTER)
        hDC.EndPage()
        hDC.EndDoc()


# =======================================================================================================
#   クラス イベント学習ビューベースクラス
# =======================================================================================================
class EvtLearnViewClass(QtBaseClass):
    def __init__(self, title, strPath):  # 初期化
        try:
            QtBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.parameter = EvtLearnParameterClass.getInstance()  # パラメータ
            self.monitorView = MonitorViewClass(title + "モニター", self.parameter)  # 学習結果モニタービュー転写
            self.resultView = EvtResultViewClass.getInstance()  # 学習結果ビューを生成
            self.treeWidget = GP.TREE.EVT_LEARN  # 機種選択ツリービュー転写
            self.title = title  # タブのタイトル
            self.strPath = strPath  # パラメータ保存パス
            viewLayout = self.makeViewLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout = self.createTreeLayout(title, self.treeWidget, viewLayout)  # ツリーレイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.connectButtons2()  # レイアウトのメンバーのコネクションをセット
            self.learn = None  # 学習クラス初期化

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ビューレイアウト生成
    # ---------------------------------------------------------------------------------------------------
    def makeViewLayout(self):
        try:
            # 配列作成
            self.comboBox_EPOCHS = [None, None]  # エポック数配列
            self.comboBox_RANDOM_SCALE = [None, None]  # ランダム分散係数配列
            # ビューレイアウト
            viewLayout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            viewLayout.setAlignment(Qt.AlignTop)  # 上詰め
            self.setLabelStyle2(viewLayout, "パラメータ", "gray", "white", 40, "12pt")  # 表題ラベル
            self.setIntCombo(viewLayout, ["HIDDEN_LAYERS", "隠れ層数"], self.flatRange(0, 100))  # 隠れ層数
            self.setStrCombo(viewLayout, ["LEARN_UNIT", "学習単位"],
                             [GP.LEARN_UNIT.TYPE_CODE, GP.LEARN_UNIT.TYPE_ID, GP.LEARN_UNIT.LASER_ID])  # 学習単位
            self.setCheckBox(viewLayout, ["SAVE_FLAG", "保存"])  # 保存フラグ
            # LEVEL0
            self.setExeButton(viewLayout, ["LEARN_LEVEL0", "レベル0の学習"])  # レベル0の学習
            EPOCHS_itemList = self.flatRange(1, 99) + self.flatRange(100, 10000, 100)  # エポックアイテムリスト
            self.setIntCombo(viewLayout, ["EPOCHS[0]", "エポック数[0]"], EPOCHS_itemList)  # エポック数（フィルターレベル0）
            self.setIntCombo(viewLayout, ["NRM_LEN", "正常データサンプル数"],
                             self.flatRange(10, 2000, 10))  # 正常データサンプル数（ランダムサンプル数）
            self.setIntCombo(viewLayout, ["ABN_LEN", "異常データサンプル"],
                             self.flatRange(10, 1000, 10))  # 異常データサンプル数(最後からのサンプル数)
            self.setIntCombo(viewLayout, ["NRM_SAMPLE", "正常ラベルのデータ数"], self.flatRange(100, 100000, 100))  # 正常ラベルのデータ数
            self.setIntCombo(viewLayout, ["ABN_SAMPLE", "異常ラベルのデータ数"], self.flatRange(100, 100000, 100))  # 異常ラベル毎のデータ数
            # LEVEL 1
            self.setIntCombo(viewLayout, ["EPOCHS[1]", "エポック数[1]"], EPOCHS_itemList)  # エポック数（フィルターレベル1）
            self.setFloatCombo(viewLayout, ["SAMPLE_RATIO_0", "初回サンプル割合"],
                               self.flatRange(0.0, 1.0, 0.01))  # 初回上位のデータサンプル割合
            self.setFloatCombo(viewLayout, ["SAMPLE_RATIO_N", "以後サンプル割合"],
                               self.flatRange(0.0, 1.0, 0.01))  # 次回以後上位のデータサンプル割合
            buttonLayout = QHBoxLayout()  # 釦レイアウト生成（水平レイアウト）
            buttonLayout1 = QVBoxLayout()  # 釦レイアウト1生成（垂直レイアウト）
            buttonLayout1.setAlignment(Qt.AlignTop)  # 上詰め
            self.setExeButton(buttonLayout1, ["MAKE_LEARN_DATA", "学習データ生成"])  # 学習データ生成
            self.setExeButton(buttonLayout1, ["LEARN_LEVEL0", "レベル0の学習"])  # レベル0の学習
            self.setExeButton(buttonLayout1, ["ADDLEARN_LEVEL0", "レベル0の追加学習"])  # レベル0の追加学習
            buttonLayout.addLayout(buttonLayout1)  # 釦レイアウトに釦レイアウト１を加える
            buttonLayout2 = QVBoxLayout()  # 釦レイアウト２生成（垂直レイアウト）
            buttonLayout2.setAlignment(Qt.AlignTop)  # 上詰め
            self.setPlotButton(buttonLayout2, ["PLOT0", "レベル0の学習結果"])  # 学習結果表示（フィルターレベル0）
            buttonLayout.addLayout(buttonLayout2)  # 釦レイアウトに釦レイアウト２を加える
            viewLayout.addLayout(buttonLayout)  # メインレイアウトに釦レイアウトを加える
            return viewLayout  # ビューレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   インスタント変数セット
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self):
        try:
            if self.LEARN_PARTS == GP.PARTS.CH:  # 学習部品がCHの時
                CURPARTS = GP.PCONT.CH  # 学習部品をセット
            elif self.LEARN_PARTS == GP.PARTS.LN:  # 学習部品がLNの時
                CURPARTS = GP.PCONT.LN  # 学習部品をセット
            elif self.LEARN_PARTS == GP.PARTS.PPM:  # 学習部品がPPMの時
                CURPARTS = GP.PCONT.PPM  # 学習部品をセット
            elif self.LEARN_PARTS == GP.PARTS.MM:  # 学習部品がMMの時
                CURPARTS = GP.PCONT.MM  # 学習部品をセット
            else:
                return False  # 失敗を返す
            self.learnParam = self.parameter  # パラメータ
            GP.CURPARTS = CURPARTS  # 学習部品
            TYPE = GP.LEARN_TYPE.AGE  # 学習タイプセット
            self.treeWidget = GP.TREE.EVT_LEARN  # ツリー ウイジェット転写
            laserIdList = self.treeWidget.laserIdList  # レーザーIDリスト転写
            LEARN_UNIT = self.parameter.LEARN_UNIT  # 学習単位を取得
            GP.CONT.setLabelList(TYPE)  # 出力ラベルリストをセット
            UNIT_NAME = self.treeWidget.getUnitName(self.parameter.LEARN_UNIT)  # 学習単位名を取得
            if UNIT_NAME is not None:  # 学習単位名が有効な時
                CURPARTS.TYPE = TYPE  # 学習タイプセット
                CURPARTS.LEARN = CURPARTS.AGE.LEARN_CLASS  # 学習クラスをセット
                CURPARTS.LEARN.stop = False  # 学習クラスのストップフラグ初期化
                CURPARTS.PCOMB.setClassVar(laserIdList, self.parameter)  # 学習パラメーターを更新する
                CURPARTS.LEARN_UNIT = LEARN_UNIT  # 学習単位をセット
                CURPARTS.UNIT_NAME = UNIT_NAME  # 学習単位名をセット
                CURPARTS.EVT.setClassVar(laserIdList, self.parameter)  # 学習パラメーターを更新する
                CURPARTS.EVT.setLearnUnit(LEARN_UNIT, UNIT_NAME)  # 学習単位と学習単位名をセット
                return True  # 成功を返す
            return False  # 失敗を返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ***************************************************************************************************
    #   メニュー
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   学習データ生成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_LEARN_DATA(self):
        try:
            if self.setClassVar(0):  # 初期設定に成功した時
                GP.CURPARTS.LEARN.makeLearnData()  # 学習データ生成

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レベル0イベント学習
    # ---------------------------------------------------------------------------------------------------
    def LEARN_LEVEL0(self):
        try:
            if self.setClassVar(0):  # 初期設定に成功した時
                GP.CURPARTS.LEARN.learn(self.monitorView)  # 年齢学習

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レベル0イベント追加学習
    # ---------------------------------------------------------------------------------------------------
    def ADDLEARN_LEVEL0(self):
        try:
            if self.setClassVar(0):  # 初期設定に成功した時
                GP.CURPARTS.LEARN.addLearn(self.monitorView)  # 年齢追加学習

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   年齢学習0結果プロット
    # ---------------------------------------------------------------------------------------------------
    def PLOT0(self):
        try:
            LEVEL = 0
            self.setClassVar(LEVEL)  # 初期設定
            self.parameter.setClassVar(self.resultView)  # イベントデータをインスタンス変数に転写する
            self.resultView.redraw(LEVEL)  # 学習結果ビューを表示
            self.resultView.show()  # 学習結果ビューを表示

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass
