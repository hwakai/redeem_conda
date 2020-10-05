import numpy as np
import os
from PyQt5Import import *
from static import *
from analysisBase import AnalysisBaseClass
from configView import LocConfigViewClass
from configView import FdrConfigViewClass
from configView import GpiConfigViewClass
from qtBase import QtBaseClass
from qtBase import ProgressWindowClass
from comb import CombClass
from origin import OriginClass

from classDef import ParameterClass
from classDef import CommonParameterClass
from viewBase import ViewBaseClass
from gpiBase import *


# =======================================================================================================
#   分析設定ビュークラス
# =======================================================================================================
class AnalysisConfigViewClass(AnalysisBaseClass):
    # ---------------------------------------------------------------------------------------------------
    # インスタンス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None

    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, parent):  # 初期化
        try:
            if AnalysisConfigViewClass._singleton is None:  # シングルトンが無いとき
                AnalysisBaseClass.__init__(self, parent.TABLE_NAME)  # スーパークラスの初期化
                self.parentObject = parent  # 親クラスの転写
                self.title = "表示設定"  # タブタイトル
                self.layout = self.createLayout()  # レイアウト生成
                self.setLayout(self.layout)  # レイアウトを自分にセット
                self.setSizePolicy(  # サイズポリシー設定
                    QSizePolicy.Expanding,  # 幅可変
                    QSizePolicy.Expanding)  # 高さ可変

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self, parent=None):
        if AnalysisConfigViewClass._singleton is None:  # シングルトンが無いとき
            AnalysisConfigViewClass._singleton = AnalysisConfigViewClass(
                parent)  # AnalysisConfigViewClassを生成してシングルトンにセット
        return AnalysisConfigViewClass._singleton  # シングルトンがを返す

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト生成
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            self.tabs = QTabWidget()  # タブウィジェット生成
            #            self.tabs.resize(300,180)                                                                  # タブサイズ設定

            # タブ生成
            self.commonTab = CommonTabClass(self, "共通パラメータ")  # 共通タブ生成
            self.locConfigTab = LocConfigViewClass(self, "ローカルサーバー通信設定")  # ローカルサーバー設定タブ生成
            self.fdrConfigTab = FdrConfigViewClass(self, "方正サーバー通信設定")  # 方正サーバー設定タブ生成
            self.gpiConfigTab = GpiConfigViewClass(self, "GPIサーバー通信設定")  # GPIサーバー設定タブ生成
            self.combDbTab = CombDbTabClass(self, "中間処理DB")  # 中間処理DDBタブ生成
            self.partsCombDbTab = PCombDbTabClass(self, "部品中間処理DB")  # 部品中間処理DDBタブ生成

            # タブリストにタブを登録
            self.tabList = []  # 空のタブリスト生成
            self.tabList.append(self.commonTab)  # 共通タブ追加
            self.tabList.append(self.locConfigTab)  # ローカルサーバー設定タブ追加
            self.tabList.append(self.fdrConfigTab)  # 方正サーバー設定タブ追加
            self.tabList.append(self.gpiConfigTab)  # GPIサーバー設定タブ追加
            self.tabList.append(self.combDbTab)  # 中間処理DBタブ追加
            self.tabList.append(self.partsCombDbTab)  # 部品処理DBタブ追加
            # タブをタブリストに追加
            for tab in self.tabList:  # タブリストをすべて実行
                self.tabs.addTab(tab, tab.title)  # タブをタブリストに追加

            # Add tabs to widget
            main = QVBoxLayout()  # 垂直レイアウト生成
            self.setLabelStyle2(main, self.title, "gray", "white", 50, "25pt")  # 表題ラベル
            main.addWidget(self.tabs)  # 垂直レイアウトにタブウィジェットを追加
            return main  # レイアウトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトとメソッドの結合を解除
    # ---------------------------------------------------------------------------------------------------
    def disconnectButtons(self):
        try:
            for tab in self.tabList:  # タブリストをすべて実行
                tab.disconnectButtons()  # タブのオブジェクトとメソッドを結合

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス 共通パラメータタブクラス
# =======================================================================================================
class CommonTabClass(AnalysisBaseClass):
    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, parent, title):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, parent.TABLE_NAME)  # スーパークラスの初期化
            self.parentObject = parent  # 親クラスの転写
            self.title = title  # タブのタイトル
            self.progress = ProgressWindowClass()  # プログレスクラス
            self.parameter = CommonParameterClass.getInstance()  # パラメータ
            self.treeWidget = GP.TREE.COMMON  # ツリー ウイジェット転写
            viewLayout = self.makeViewLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout = self.createTreeLayout(title, self.treeWidget, viewLayout)  # ツリーレイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.connectButtons2()  # タブのオブジェクトとメソッドを結合
            self.setStyleSheet("background:lightblue; color:red;font-size:9pt" + ";")  # オブジェクトのスタイルを設定する

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ビューレイアウト生成
    # ---------------------------------------------------------------------------------------------------
    def makeViewLayout(self):
        try:
            viewLayout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            viewLayout.setAlignment(Qt.AlignTop)  # 上詰め
            blockList = self.flatRange(10, 990, 10) + self.flatRange(1000, 100000, 1000)  # ブロックアイテムリスト
            serverList = GP.SERVER.nameList  # サーバーアイテムリスト
            self.setLabelStyle2(viewLayout, "分析パラメータ", "gray", "white", 40, "12pt")  # 表題ラベル
            self.setIntCombo(viewLayout, ["FETCH_BLOCK", "DB読込ブロック長"], blockList)  # CH予測値表示フィルターレベル
            self.setIntCombo(viewLayout, ["CH_AGE_LEVEL", "CHフィルターレベル"], self.flatRange(1, 8))  # CH予測値表示フィルターレベル
            self.setIntCombo(viewLayout, ["LN_AGE_LEVEL", "LNフィルターレベル"], self.flatRange(1, 8))  # LN予測値表示フィルターレベル
            self.setStrCombo(viewLayout, ["SERVER", "サーバー"], serverList)  # サーバー選択
            return viewLayout  # ビューレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   クラス 中間処理DBパラメータクラス
# =======================================================================================================
class CombDbParameterClass(ParameterClass):
    def __init__(self):  # 初期化
        try:
            ParameterClass.__init__(self, GP.ANAL_LOG.COMB)  # スーパークラスの初期化
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
            self.loadData()  # パラメータをログファイルから読込
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示


# =======================================================================================================
#   クラス 中間処理DBタブクラス
# =======================================================================================================
class CombDbTabClass(QtBaseClass):
    def __init__(self, parent, title):  # 初期化
        try:
            QtBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.title = title  # タブのタイトル
            self.progress = ProgressWindowClass()  # 進捗ダイアローグ生成
            self.parameter = CombDbParameterClass()  # パラメータ
            self.treeWidget = GP.TREE.COMB  # ツリー ウイジェット転写
            viewLayout = self.makeViewLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout = self.createTreeLayout(title, self.treeWidget, viewLayout)  # ツリーレイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.connectButtons2()  # タブのオブジェクトとメソッドを結合

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ビューレイアウト
    # ---------------------------------------------------------------------------------------------------
    def makeViewLayout(self):
        try:
            viewLayout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            viewLayout.setAlignment(Qt.AlignTop)  # 上詰め
            self.setLabelStyle2(viewLayout, "パラメータ", "gray", "white", 40, "12pt")  # 表題ラベル
            buttonLayout = QVBoxLayout()  # 釦レイアウト1生成（垂直レイアウト）
            buttonLayout.setAlignment(Qt.AlignTop)  # 上詰め
            self.setExeButton(buttonLayout, ["MAKE_LST", "LaserTypeClass"])  # LST(LaserTypeClass)作成 COMB_LASER_TYPE
            self.setExeButton(buttonLayout, ["MAKE_ERM", "ErrorMasterClass"])  # ERM(ErrorMasterClass)作成 COMB_ERR_MST
            self.setExeButton(buttonLayout,
                              ["MAKE_RPB", "ReplacementBaseClass"])  # RPB(ReplacementBaseClass)作成 COMB_RPL_BASE
            self.setExeButton(buttonLayout, ["MAKE_PWB", "PlotWPlotClass"])  # PWB(PlotWPlotClass)作成 COMB_PLOT_WPLOT
            self.setExeButton(buttonLayout,
                              ["MAKE_PEX", "PartsExchangeClass"])  # PEX(PartsExchangeClass)作成 COMB_PARTS_EXCHANGE
            self.setExeButton(buttonLayout,
                              ["MAKE_GFP", "GasFilPeriodClass"])  # GFP(GasFilPeriodClass)作成 COMB_GASFIL_PERIOD
            self.setExeButton(buttonLayout, ["MAKE_ALL", "すべて作成"])  # W DF以 外をすべて作成
            viewLayout.addLayout(buttonLayout)  # メインレイアウトに釦レイアウトを加える
            return viewLayout  # ビューレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   初期化
    # ---------------------------------------------------------------------------------------------------
    def INITIALIZE(self):
        try:
            laserIdList = self.treeWidget.laserIdList
            GP.CONT.COMB.setClassVar(laserIdList, self.parameter)  # COMBメンバーのパラメータデータをセット
            GP.CONT.ORIGIN.setClassVar(laserIdList, self.parameter)  # ORIGINメンバーのパラメータデータをセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ***************************************************************************************************
    #   メニュー
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   LST(LaserTypeClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_LST(self):
        self.INITIALIZE()  # 初期設定
        GP.CONT.LST.makeBase(self.progress)  # LSTのベースリストを作成
        pass

    # ---------------------------------------------------------------------------------------------------
    #   ERM(ErrorMasterClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_ERM(self):
        try:
            self.INITIALIZE()  # 初期設定
            GP.CONT.ERM.makeBase(self.progress)  # ERMのベースリストを作成
            pass

        except Exception as e:  # 例外                                                                          # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   RPB(ReplacementBaseClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_RPB(self):
        self.INITIALIZE()  # 初期設定
        GP.CONT.RPB.makeBase(self.progress)  # RPBのベースリストを作成

    # ---------------------------------------------------------------------------------------------------
    #   PWB(PlotWPlotClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_PWB(self):
        self.INITIALIZE()  # 初期設定
        GP.CONT.PWB.makeBase(self.progress)  # PWBのベースリストを作成
        pass

    # ---------------------------------------------------------------------------------------------------
    #   PEX(PartsExchangeClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_PEX(self):
        self.INITIALIZE()  # 初期設定
        GP.CONT.PEX.makeBase(self.progress)  # PEXのベースリストを作成

    # ---------------------------------------------------------------------------------------------------
    #   GFP(GasFilPeriodClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_GFP(self):
        try:
            self.INITIALIZE()  # 初期設定
            GP.CONT.GFP.makeBase(self.progress)  # GFPのベースリストを作成
            pass

        except Exception as e:  # 例外                                                                          # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ERM(ErrorMasterClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_ALL(self):
        try:
            self.INITIALIZE()  # 初期設定
            p = self.progress  # 進捗ダイアローグを転写
            self.startNewLevel(6, p)  # 新しいレベルの進捗開始
            GP.CONT.LST.makeBase(p)  # LSTのベースリストを作成
            GP.CONT.ERM.makeBase(p)  # ERMのベースリストを作成
            GP.CONT.RPB.makeBase(p)  # RPBのベースリストを作成
            GP.CONT.PWB.makeBase(p)  # PWBのベースリストを作成
            GP.CONT.PEX.makeBase(p)  # PEXのベースリストを作成
            GP.CONT.GFP.makeBase(p)  # GFPのベースリストを作成
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # 例外を表示
            pass


# =======================================================================================================
#   クラス パラメータクラス
# =======================================================================================================
class PCombDbParameterClass(ParameterClass):
    def __init__(self):  # 初期化
        try:
            ParameterClass.__init__(self, GP.ANAL_LOG.PCOMB)  # スーパークラスの初期化
            MINLEN = 1000  # PRB抽出時の最小長さ
            SEL_PARTS = GP.ALL  # 選択部品名
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
            self.loadData()  # パラメータをログファイルから読込
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示


# =======================================================================================================
#   クラス部品別中間処理DBタブクラス
# =======================================================================================================
class PCombDbTabClass(QtBaseClass):
    def __init__(self, parent, title):  # 初期化
        try:
            QtBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.title = title  # タブのタイトル
            self.progress = ProgressWindowClass()  # 進捗ダイアローグ生成
            self.parameter = PCombDbParameterClass()  # パラメータ
            self.treeWidget = GP.TREE.PCOMB  # ツリー ウイジェット転写
            viewLayout = self.makeViewLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout = self.createTreeLayout(title, self.treeWidget, viewLayout)  # ツリーレイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.connectButtons2()  # タブのオブジェクトとメソッドを結合

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ビューレイアウト
    # ---------------------------------------------------------------------------------------------------
    def makeViewLayout(self):
        try:
            viewLayout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            viewLayout.setAlignment(Qt.AlignTop)  # 上詰め
            partsRange = [GP.ALL, GP.PARTS.CH, GP.PARTS.LN, GP.PARTS.PPM, GP.PARTS.MM]
            self.setLabelStyle2(viewLayout, "パラメータ", "gray", "white", 40, "12pt")  # 表題ラベル
            self.setIntCombo(viewLayout, ["MINLEN", "CHPRB抽出時最小長さ"], self.flatRange(0, 10000, 100))  # CHPRB抽出時の最小長さ
            self.setStrCombo(viewLayout, ["SEL_PARTS", "選択部品名"], partsRange)  # 選択部品名
            buttonLayout = QHBoxLayout()  # 釦レイアウト生成（水平レイアウト）
            buttonLayout1 = QVBoxLayout()  # 釦レイアウト1生成（垂直レイアウト）
            buttonLayout1.setAlignment(Qt.AlignTop)  # 上詰め
            self.setExeButton(buttonLayout1, ["MAKE_PTB", "部品ベース作成"])  # PTB(ChPartsBaseClass)作成 COMB_CH_BASE
            self.setExeButton(buttonLayout1, ["MAKE_PRB", "ピリオッドベース作成"])  # PRB(ChPeriodBaseClass)作成 COMB_CH_PERIOD_BASE
            self.setExeButton(buttonLayout1, ["MAKE_JBB", "ジョブベース作成"])  # JBB(ChJobBaseClass)作成 COMB_CH_JOB_BASE
            self.setExeButton(buttonLayout1, ["MAKE_ERB", "エラーベース作成"])  # ERB(ChErrorBaseClass)作成 COMB_CH_ERROR_BASE
            self.setExeButton(buttonLayout1, ["MAKE_GSB", "ガスベース作成"])  # GSB(GasBaseClass)作成 COMB_GAS_BASE
            self.setExeButton(buttonLayout1, ["MAKE_ALL", "すべて作成"])  # すべて作成
            buttonLayout.addLayout(buttonLayout1)  # 釦レイアウトに釦レイアウト１を加える
            viewLayout.addLayout(buttonLayout)  # メインレイアウトに釦レイアウトを加える
            return viewLayout  # ビューレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   メンバーのパラメータデータをセット
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self, PARTSCONT):
        try:
            laserIdList = self.treeWidget.laserIdList
            GP.CONT.ORIGIN.setClassVar(laserIdList, self.parameter)  # ORIGINメンバーのパラメータデータをセット
            GP.CONT.COMB.setClassVar(laserIdList, self.parameter)  # COMBメンバーのパラメータデータをセット
            PARTSCONT.PCOMB.setClassVar(laserIdList, self.parameter)  # PCOMBメンバーのパラメータデータをセット
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   PTBを読み込んでからオブジェクトの作成
    # ---------------------------------------------------------------------------------------------------
    def makePTBObject(self, PARTSCONT, object, p):
        try:
            self.startNewLevel(3, p)                                                                    # 新しいレベルの進捗開始
            self.setClassVar(PARTSCONT)                                                                 # メンバーのパラメータデータをセット
            PARTSCONT.PTB.makeBase(p)                                                                   # CH_PARTS_BASEのベースリストを作成
            if PARTSCONT.PTB.loadFlatBase(p):                                                           # PTBフラットベース読込に成功した時
                object.makeBase(p)                                                                      # オブジェクトのベースリストを作成
            self.endLevel(p)                                                                            # 現レベルの終了
            pass

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # 例外を表示

    # ***************************************************************************************************
    #   メニュー
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   PTB(PartsBaseClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_PTB(self):
        try:
            p = self.progress  # 進捗ダイアローグを転写
            if self.SEL_PARTS == GP.ALL:  # ALLの時
                self.startNewLevel(len(GP.PCONT.objectList), p)  # 新しいレベルの進捗開始
                for PARTSCONT in GP.PCONT.objectList:  # 部品コンテナのオブジェクトリストをすべて実行
                    self.setClassVar(PARTSCONT)  # メンバーのパラメータデータをセット
                    GP.CURPARTS = PARTSCONT
                    PARTSCONT.PTB.makeBase(p)  # PTBのベースリストを作成
                self.endLevel(p)                                                                        # 現レベルの終了
            else:  # ALLでない時
                self.startNewLevel(1, p)  # 新しいレベルの進捗開始
                PARTSCONT = GP.PCONT.objectDic[self.SEL_PARTS]  # 部品オブジェクトを取得
                self.setClassVar(PARTSCONT)  # メンバーのパラメータデータをセット
                GP.CURPARTS = PARTSCONT
                PARTSCONT.PTB.makeBase(p)  # PTBのベースリストを作成
                self.endLevel(p)                                                                        # 現レベルの終了
            pass

        except Exception as e:  # 例外                                                                          # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   PRB(PeriodBaseClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_PRB(self):
        try:
            p = self.progress  # 進捗ダイアローグを転写
            if self.SEL_PARTS == GP.ALL:  # ALLの時
                self.startNewLevel(len(GP.PCONT.objectList) * 3, p)  # 新しいレベルの進捗開始
                for PARTSCONT in GP.PCONT.objectList:  # 部品コンテナのオブジェクトリストをすべて実行
                    GP.CURPARTS = PARTSCONT
                    self.makePTBObject(PARTSCONT, PARTSCONT.PRB, p)  # PTBを読み込んでからオブジェクトの作成
                self.endLevel(p)                                                                        # 現レベルの終了
            else:  # ALLでない時
                self.startNewLevel(3, p)  # 新しいレベルの進捗開始
                PARTSCONT = GP.PCONT.objectDic[self.SEL_PARTS]  # 部品オブジェクトを取得
                GP.CURPARTS = PARTSCONT
                self.makePTBObject(PARTSCONT, PARTSCONT.PRB, p)  # PTBを読み込んでからオブジェクトの作成
                self.endLevel(p)                                                                        # 現レベルの終了
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   JBB(JobBaseClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_JBB(self):
        try:
            p = self.progress                                                                           # 進捗ダイアローグを転写
            if self.SEL_PARTS == GP.ALL:                                                                # ALLの時
                self.startNewLevel(len(GP.PCONT.objectList) * 3, p)                                     # 新しいレベルの進捗開始
                for PARTSCONT in GP.PCONT.objectList:                                                   # 部品コンテナのオブジェクトリストをすべて実行
                    GP.CURPARTS = PARTSCONT
                    self.makePTBObject(PARTSCONT, PARTSCONT.JBB, p)                                     # PTBを読み込んでからオブジェクトの作成
                self.endLevel(p)                                                                        # 現レベルの終了
            else:                                                                                       # ALLでない時
                self.startNewLevel(1, p)                                                                # 新しいレベルの進捗開始
                PARTSCONT = GP.PCONT.objectDic[self.SEL_PARTS]                                          # 部品オブジェクトを取得
                GP.CURPARTS = PARTSCONT
                self.makePTBObject(PARTSCONT, PARTSCONT.JBB, p)                                         # PTBを読み込んでからオブジェクトの作成
                self.endLevel(p)                                                                        # 現レベルの終了
            pass

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ERB(ErrorBaseClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_ERB(self):
        try:
            p = self.progress  # 進捗ダイアローグを転写
            if self.SEL_PARTS == GP.ALL:  # ALLの時
                self.startNewLevel(len(GP.PCONT.objectList) * 3, p)  # 新しいレベルの進捗開始
                for PARTSCONT in GP.PCONT.objectList:  # メンバーのパラメータデータをセット
                    self.setClassVar(PARTSCONT)  # メンバーのパラメータデータをセット
                    GP.CURPARTS = PARTSCONT
                    PARTSCONT.ERB.makeBase(p)  # COMB_CH_ERROR_BASEを作成する
                self.endLevel(p)                                                                        # 現レベルの終了
            else:  # ALLでない時
                self.startNewLevel(1, p)  # 新しいレベルの進捗開始
                PARTSCONT = GP.PCONT.objectDic[self.SEL_PARTS]  # 部品オブジェクトを取得
                self.setClassVar(PARTSCONT)  # メンバーのパラメータデータをセット
                GP.CURPARTS = PARTSCONT
                PARTSCONT.ERB.makeBase(p)  # COMB_CH_ERROR_BASEを作成する
                self.endLevel(p)                                                                        # 現レベルの終了
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   MAKE_GSB(GasBaseClass)作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_GSB(self):
        try:
            p = self.progress  # 進捗ダイアローグを転写
            if self.SEL_PARTS == GP.ALL:  # ALLの時
                self.startNewLevel(len(GP.PCONT.objectList) * 3, p)  # 新しいレベルの進捗開始
                for PARTSCONT in GP.PCONT.objectList:  # 部品コンテナのオブジェクトリストをすべて実行
                    GP.CURPARTS = PARTSCONT
                    self.makePTBObject(PARTSCONT, PARTSCONT.GSB, p)  # PTBを読み込んでからオブジェクトの作成
                self.endLevel(p)                                                                        # 現レベルの終了
            else:  # ALLでない時
                self.startNewLevel(1, p)  # 新しいレベルの進捗開始
                PARTSCONT = GP.PCONT.objectDic[self.SEL_PARTS]  # 部品オブジェクトを取得
                GP.CURPARTS = PARTSCONT
                self.makePTBObject(PARTSCONT, PARTSCONT.GSB, p)  # PTBを読み込んでからオブジェクトの作成
                self.endLevel(p)                                                                        # 現レベルの終了
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   すべて作成
    # ---------------------------------------------------------------------------------------------------
    def MAKE_ALL(self):
        try:
            p = self.progress  # 進捗ダイアローグを転写
            if self.SEL_PARTS == GP.ALL:  # ALLの時
                self.startNewLevel(len(GP.PCONT.objectList), p)  # 新しいレベルの進捗開始
                for PARTSCONT in GP.PCONT.objectList:  # 部品コンテナのオブジェクトリストをすべて実行
                    self.setClassVar(PARTSCONT)  # メンバーのパラメータデータをセット
                    self.startNewLevel(len(PARTSCONT.PCOMB.objectList) + 2, p)  # 新しいレベルの進捗開始
                    GP.CURPARTS = PARTSCONT
                    PARTSCONT.PTB.makeBase(p)  # CH_PARTS_BASEのベースリストを作成
                    if PARTSCONT.PTB.loadFlatBase(p):  # PTBフラットベース読込に成功した時
                        for object in PARTSCONT.PCOMB.objectList:  # オブジェクトリストをすべて実行
                            if object.TABLE_NAME != PARTSCONT.PTB.TABLE_NAME:  # PTBで無い時
                                object.makeBase(p)  # オブジェクトのベースリストを作成
                    self.endLevel(p)                                                                    # 現レベルの終了
                self.endLevel(p)                                                                        # 現レベルの終了
            else:  # ALLでない時
                PARTSCONT = GP.PCONT.objectDic[self.SEL_PARTS]  # 部品オブジェクトを取得
                self.setClassVar(PARTSCONT)  # メンバーのパラメータデータをセット
                self.startNewLevel(len(PARTSCONT.PCOMB.objectList) + 2, p)  # 新しいレベルの進捗開始
                GP.CURPARTS = PARTSCONT
                PARTSCONT.PTB.makeBase(p)  # CH_PARTS_BASEのベースリストを作成
                if PARTSCONT.PTB.loadFlatBase(p):  # PTBフラットベース読込に成功した時
                    for object in PARTSCONT.PCOMB.objectList:  # オブジェクトリストをすべて実行
                        if object.TABLE_NAME != PARTSCONT.PTB.TABLE_NAME:  # PTBで無い時
                            object.makeBase(p)  # オブジェクトのベースリストを作成
                self.endLevel(p)                                                                        # 現レベルの終了
            pass

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # 例外を表示
            pass

