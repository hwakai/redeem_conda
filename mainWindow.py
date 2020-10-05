import numpy as np
from PyQt5Import import *
from qtBase import QtBaseClass

from staticImport import *
from classDef import *
from treeWidget import TreeClass
from origin import OriginClass
from comb import CombClass
from pComb import PCombClass
from ageView import AgeTableViewClass
from updateView import UpdateViewClass
from learnView import LearnViewClass

from analysisConfigView import AnalysisConfigViewClass
from analysisConfigView import CommonTabClass
from qtBase import ProgressWindowClass

from analysisBase import *
from commonBase import CommonBaseClass
from fileServer import FILEServerClass
from sshServer import SSHServerClass
from dbServer import DBServerClass
from gpiBase import TrnClass
from gpiBase import LaserTreeClass
from modelComb import *
from ageLearn import *
from evtLearn import *

#=======================================================================================================
#   初期ビュークラス
#=======================================================================================================
class InitialViewClass(AnalysisBaseClass):
    #---------------------------------------------------------------------------------------------------
    # クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None

    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if InitialViewClass._singleton is None:                                                     # シングルトンが無いとき
                AnalysisBaseClass.__init__(self, None)                                                  # スーパークラスの初期化
                self.title = "初期画面"                                                                 # タブタイトル
                self.layout = self.createLayout()                                                       # レイアウト生成
                self.setLayout(self.layout)                                                             # レイアウトを自分にセット
                self.resize(1500,700)
                self.setSizePolicy(                                                                     # サイズポリシー設定
                    QSizePolicy.Expanding,                                                              # 幅可変
                    QSizePolicy.Expanding)                                                              # 高さ可変

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if InitialViewClass._singleton is None:                                                         # シングルトンが無いとき
            InitialViewClass._singleton = InitialViewClass()                                            # InitialViewClassを生成してシングルトンにセット
        return InitialViewClass._singleton                                                              # シングルトンがを返す

    #---------------------------------------------------------------------------------------------------
    #   レイアウト生成
    #---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            mLayout = QVBoxLayout()                                                                     # メインレイアウト生成（垂直レイアウト）            self.setLabelStyle2(main, "共通パラメータ", "gray", "white", 40, "12pt")                    # 表題ラベル

            # 直接DB処理メニュー
            self.setLabelStyle2(mLayout, "DASHBOARD", "gray", "white", 40, "20pt")                      # 表題ラベル
            label = QLabel()                                                                            # キャンバスからimgArrayとpilImageとqImageとqPixmapをセット
            mQImage = QImage("GIGA.png")
            label.qPixmap = QPixmap.fromImage(mQImage)                                                  # QPixmapに変換
#            mQImage.load("GIGA.png")
            mLayout.addWidget(label)                                                                    # 上詰め
            mLayout.setAlignment(Qt.AlignTop)                                                           # 上詰め
            return mLayout                                                                              # メインレイアウトを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示

#=======================================================================================================
#   クラス ユーザーパラメータクラス
#=======================================================================================================
class MainParameterClass(ParameterClass):
    def __init__(self):                                                                                 # 初期化
        try:
            ParameterClass.__init__(self, GP.MAIN_LOG.MAIN)                                             # スーパークラスの初期化
            LEARN_UNIT = GP.LEARN_UNIT.TYPE_ID                                                          # 学習単位
            MAIN_CH    = True                                                                           # CHメイン
            MAIN_LN    = False                                                                          # LNメイン
            MAIN_PPM   = False                                                                          # PPMメイン
            MAIN_MM    = False                                                                          # MMメイン
            self.nameList = [name for name in locals().keys()
                            if (name != 'self') and
                                (name != '__pydevd_ret_val_dict')]                                      # ローカル変数名リストを作成
            for objectName in self.nameList:                                                            # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)                                         # オブジェクトのインスタンス変数のセット
            self.loadData()                                                                             # パラメータをログファイルから読込
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

#=======================================================================================================
#   クラス メインウインドウ
#=======================================================================================================
class MainWindow(AnalysisBaseClass):
    updateSignal = pyqtSignal()                                                                         # レーザーリスト変更時シグナル
    def __init__(self):                                                                                 # 初期化
        try:
            AnalysisBaseClass.__init__(self, None)                                                      # スーパークラスの初期化
            self.preReadDone = False                                                                    # 事前読み込みフラグを偽にする
            self.title = "GIGAPHOTON CHAMBER DIAGNOSTIC"                                                # タブのタイトル
            self.parameter = MainParameterClass()                                                       # メインパラメーターをクラス変数に転写する
            self.learnParameter   = AgeLearnParameterClass.getInstance()                                # パラメータ
            self.setContainer()                                                                         # コンテナ設定
            commonTreeWidget = GP.TREE.COMMON                                                           # マスターツリーウイジェットの取得
            commonTreeWidget.slaveList += [GP.TREE.AGE_RESULT]                                          # スレーブーリストに追加
            self.treeWidget = GP.TREE.AGE_RESULT                                                        # ツリー ウイジェット生成
            self.layout = self.createLayout()                                                           # レイアウト生成
            self.setLayout(self.layout)                                                                 # レイアウトを自分にセット
            self.resize(1000, 600)                                                                      # サイズセット
            self.move(0,0)                                                                              # 起点セット
#            self.setWindowFlags(Qt.WindowStaysOnTopHint)                                               # 常に最前面に表示
            self.loadParameters()                                                                       # パラメータのデータをオブジェクトと自分にセット
            self.setWindowState(Qt.WindowMaximized)                                                     # 最大化
            self.connectButtons3()                                                                      # タブのオブジェクトとメソッドを結合
            QApplication.processEvents()                                                                # プロセスイベントを呼んで制御をイベントループに返す
            self.subDoneFlag = True                                                                     # 事前読み込みフラグを真にする
            self.commonParam = CommonParameterClass.getInstance()                                       # 共通パラメーターを転写する

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   コンテナ設定
    #---------------------------------------------------------------------------------------------------
    def setContainer(self):
        try:
            # COMBコンテナ設定
            # サーバーコンテナ設定
            GP.SVR.FILEServer = FILEServerClass.getInstance()                                           # FILEサーバー
            GP.SVR.SSHServer = SSHServerClass.getInstance()                                             # SSHサーバー
            GP.SVR.DBSServer = DBServerClass.getInstance()                                              # DBサーバー
            GP.SVR.locRdmDBS = LocRdmDBSParameterClass
            GP.SVR.parameter[GP.SERVER.FDR_RDM_DBS     ] = FdrRdmDBSParameterClass.getInstance()        # FDR REDEEM DBサーバーパラメータクラスセット
            GP.SVR.parameter[GP.SERVER.GPI_RDM_DBS     ] = GpiRdmDBSParameterClass.getInstance()        # GPI REDEEM DBサーバーパラメータクラスセット
            GP.SVR.parameter[GP.SERVER.DMY_RDM_DBS     ] = DmyRdmDBSParameterClass.getInstance()        # DUMMY REDEEM DBサーバーパラメータクラスセット
            GP.SVR.parameter[GP.SERVER.LOC_RDM_DBS     ] = LocRdmDBSParameterClass.getInstance()        # LOCAL REDEEM DBサーバーパラメータクラスセット

            GP.SVR.parameter[GP.SERVER.FDR_RDM_SSH     ] = FdrRdmSSHParameterClass.getInstance()        # LOCAL REDEEM DBサーバーパラメータクラスセット
            GP.SVR.parameter[GP.SERVER.GPI_RDM_SSH     ] = GpiRdmSSHParameterClass.getInstance()        # LOCAL REDEEM DBサーバーパラメータクラスセット
            GP.SVR.parameter[GP.SERVER.GPI_RDM_SSH_TEST] = GpiRdmSSHTestParameterClass.getInstance()    # LOCAL REDEEM DBサーバーパラメータクラスセット

            # CONTコンテナ設定
            GP.CONT.MAIN_PARAMETER = self.parameter                                                     # メインウインドウパラメータ
            GP.CONT.setCOMB(OriginClass.getInstance(), CombClass.getInstance())                         # CombClass取得
            GP.CONT.TRN = TrnClass.getInstance()                                                        # TrnClass取得
            GP.CONT.LTR = LaserTreeClass.getInstance()                                                  # レーザーツリークラスを転写
            GP.CONT.commonParam = CommonParameterClass.getInstance()                                    # 共通パラメータを転写
            GP.CONT.dataTransParameter = DataTransParameterClass.getInstance()                          # データ移行パラメータを転写

            # PCOMBコンテナ設定
            GP.PCONT.setPCOMB(PCombClass.getInstance())                                                 # PCOMB設定
#            GP.MIXCONT.setPCOMB(PCombClass.getInstance())                                               # MIXCONT設定

            # SVRコンテナ設定
            GP.SVR.SOURCE_CLASS[GP.DATA_SOURCE.ORIGIN] = [GP.CONT.ORIGIN]                               # ソースクラスをセット
            GP.SVR.SOURCE_CLASS[GP.DATA_SOURCE.COMB]   = [GP.CONT.COMB]                                 # ソースクラスをセット
            GP.SVR.SOURCE_CLASS[GP.DATA_SOURCE.PCOMB]  = [GP.PCONT.CH.PCOMB, GP.PCONT.LN.PCOMB, GP.PCONT.PPM.PCOMB, GP.PCONT.MM.PCOMB]         # ソースクラスをセット

            # TREEコンテナ設定
            GP.TREE = TreeClass(GP.CONT.TREE_CONF.LASER)                                                        # TreeClass取得

            # 学習クラスコンテナ設定
            ageLearn = AgeLearnClass.getInstance()                                                              # AGE学習クラス
            evtLearn = EvtLearnClass.getInstance()                                                              # EVT学習クラス
            GP.PCONT.CH.AGE.LEARN_CLASS = ageLearn.CH_LEARN                                                     # AGE学習クラス
            GP.PCONT.LN.AGE.LEARN_CLASS = ageLearn.LN_LEARN                                                     # AGE学習クラス
            GP.PCONT.PPM.AGE.LEARN_CLASS = ageLearn.PPM_LEARN                                                   # AGE学習クラス
            GP.PCONT.MM.AGE.LEARN_CLASS = ageLearn.MM_LEARN                                                     # AGE学習クラス
            GP.PCONT.CH.EVT.LEARN_CLASS   = evtLearn.CH_LEARN                                                   # EVT学習クラス
            for object in GP.PCONT.objectList:                                                                  # オブジェクトリストをすべて実行
                if type(object) == PartsContainerClass:                                                         # 部品コンテナクラスの時
                    PARTS = object.PARTS                                                                        # 部品転写
                    for i, conf in enumerate(object.AGE.LEARN_CONF.objectList):                                 # AGEオブジェクトリストをすべて実行
                        object.AGE.MODEL_COMB_LIST[i] = ModelCombClass(PARTS, i, GP.LEARN_TYPE.AGE, conf)       # モデルコンボリスト生成
                    for i, conf in enumerate(object.EVT.LEARN_CONF.objectList):                                 # EVTオブジェクトリストをすべて実行
                        object.EVT.MODEL_COMB_LIST[i] = ModelCombClass(PARTS, i, GP.LEARN_TYPE.EVT, conf)       # モデルコンボリスト生成
            pass

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    #---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            PCONT = GP.PCONT
            # メインレイアウト
            main = QVBoxLayout()                                                                        # メインレイアウト生成（垂直レイアウト）
            main.setAlignment(Qt.AlignTop)                                                              # 上詰め
            self.setLabelStyle2(main, self.title, "gray", "white", 50, "25pt")                          # 表題ラベル
            # メイン本体レイアウト
            main_body = QHBoxLayout()                                                                   # メインレイアウト本体生成（垂直レイアウト）
            # メニューレイアウト
            menu = QVBoxLayout()                                                                        # メニューレイアウト生成（垂直レイアウト）
            menu.setAlignment(Qt.AlignTop)                                                              # 上詰め
            object = self.setLabelStyle2(menu, "MENU", "gray", "white", 40, "20pt")                     # メニュー表題ラベル
            object.setFixedWidth(GP.MENU_WIDTH)                                                         # 固定サイズに設定
            # メニュー本体レイアウト
            menu_body = QVBoxLayout()                                                                   # メニュー本体レイアウト生成（垂直レイアウト）
            menu_body.setAlignment(Qt.AlignTop)                                                         # 上詰め
            self.setMenuButton(menu_body, ["UPDATE"     , "データ更新"    ])                            # データ更新釦
            self.setMenuButton(menu_body, ["ANA_CONFIG ", "パラメータ設定"])                            # パラメータ設定釦
            self.setMenuButton(menu_body, ["LEARNING"   , "学習"          ])                            # 学習釦
            self.setStrCombo  (menu_body, ["LEARN_UNIT"    , "学習単位"         ], [GP.LEARN_UNIT.TYPE_CODE,GP.LEARN_UNIT.TYPE_ID,GP.LEARN_UNIT.LASER_ID])    # 学習単位
            self.setMenuButton(menu_body, ["AGE_RESULT_VIEW", "年齢分析結果表示"])                      # 分析結果表示釦
            self.setRadioGroup(menu_body, {"MAIN_CH":"CH","MAIN_LN":"LN","MAIN_PPM":"PPM","MAIN_MM":"MM"}, '主部品選択') # 表示部品選択フラグ
            menu.addLayout(menu_body)                                                                   # メニューレイアウトにメニュー本体レイアウトを追加
            self.tree_layout = QVBoxLayout()                                                            # メニュー本体レイアウト生成（垂直レイアウト）
            self.tree_layout.addWidget(self.treeWidget)                                                 # メインレイアウト本体にメインツリービューを追加
            menu.addLayout(self.tree_layout)                                                            # メニューレイアウトにメニュー本体レイアウトを追加
            main_body.addLayout(menu)                                                                   # メインレイアウト本体にメニューレイアウトを追加
            # ビューレイアウト
            self.viewLayout = QVBoxLayout()                                                             # ビューレイアウト生成（垂直レイアウト）
            self.viewLayout.setAlignment(Qt.AlignTop)                                                   # 上詰め
            # ビュー本体レイアウト
            self.curView = InitialViewClass.getInstance()                                               # 初期画面
            self.curView.show()                                                                         # 初期画面表示
            self.viewLayout.addWidget(self.curView)                                                     # メインレイアウト本体にメニューレイアウトを追加
            main_body.addLayout(self.viewLayout)                                                        # メイン本体レイアウトにビューレイアウトを追加
            main.addLayout(main_body)                                                                   # メインレイアウトにメイン本体レイアウト本体を追加
            return main                                                                                 # メインレイアウトを返す

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #***************************************************************************************************
    #   イベント処理
    #***************************************************************************************************
    #---------------------------------------------------------------------------------------------------
    #   メニュー本体をクリア
    #---------------------------------------------------------------------------------------------------
    def clearView(self):
        try:
            if AgeTableViewClass.getInstance().canvas is not None:                                      # 年齢一覧ビューが有る時
                AgeTableViewClass.getInstance().canvas.clearPredictView()                               # 年齢一覧ビューのクローズ処理
            # ビューを見えなくする
            self.curView.setVisible(False)
            # ビューレイアウトのアイテムをすべて取り除く
            while self.viewLayout.itemAt(0) is not None:                                                # アイテムが有る限り実行
                self.viewLayout.removeItem(self.viewLayout.itemAt(0))                                   # アイテムを取り除く

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   データ更新クラス表示
    #---------------------------------------------------------------------------------------------------
    def UPDATE(self):
        try:
            curView = UpdateViewClass.getInstance(self)                                                 # 設定タブ生成
            self.clearView()                                                                            # ビューレイアウト本体の要素を削除
            self.curView = curView
            self.viewLayout.addWidget(self.curView)                                                     # ビューに加える
            self.curView.show()                                                                         # 分析設定ビュー表示

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   分析設定ビュー表示
    #---------------------------------------------------------------------------------------------------
    def ANA_CONFIG(self):
        try:
            curView = AnalysisConfigViewClass.getInstance(self)                                         # 分析設定ビュー生成
            self.clearView()                                                                            # ビューレイアウト本体の要素を削除
            self.curView = curView
            self.viewLayout.addWidget(self.curView)                                                     # ビューレイアウトに加える
            self.curView.show()                                                                         # 分析設定ビュー表示

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   学習ビュークラス表示
    #---------------------------------------------------------------------------------------------------
    def LEARNING(self):
        try:
            curView = LearnViewClass.getInstance(self)                                                  # 学習ビュー生成
            self.clearView()                                                                            # ビューレイアウト本体の要素を削除
            self.curView = curView                                                                      # 学習ビュー生成
            self.viewLayout.addWidget(self.curView)                                                     # ビューレイアウトに加える
            self.curView.show()                                                                         # 分析設定ビュー表示

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   学習単位変更時処理
    #---------------------------------------------------------------------------------------------------
    def LEARN_UNIT_EVENT(self):
        return

    #---------------------------------------------------------------------------------------------------
    #   部品コンテナのセット
    #---------------------------------------------------------------------------------------------------
    def setPartsConteiner(self, PARTSCONT, TYPE):
        try:
            LEARN_UNIT = self.parameter.LEARN_UNIT                                                      # 学習単位をセットする
            laserIdList = self.treeWidget.laserIdList                                                   # レーザーIDリストを転写
            unitNameList = self.treeWidget.getUnitNameList(LEARN_UNIT)                                  # 学習単位名リストを取得する
            PARTSCONT.LEVEL = self.CH_AGE_LEVEL                                                                         # 学習レベルをセット
            PARTSCONT.TYPE = TYPE                                                                       # 学習タイプをセット
            PARTSCONT.LEARN_UNIT = LEARN_UNIT                                                           # CH学習単位をセット
            PARTSCONT.PCOMB.setClassVar(laserIdList, self.commonParam)                                  # 学習パラメーターを更新する
            PARTSCONT.MODEL_DIC = self.loadModelDic(PARTSCONT, unitNameList)                            # セーブデータとモデルのセット
            pass

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   モデル辞書の読み込み
    #---------------------------------------------------------------------------------------------------
    def loadModelDic(self, PARTSCONT, unitNameList):
        try:
            MODEL_DIC  = {}                                                                             # MODEL辞書初期化
            laserIdList = self.treeWidget.laserIdList                                                   # レーザーIDリストを転写
            LEARN_UNIT = PARTSCONT.LEARN_UNIT                                                           # 学習単位
            LEVEL = PARTSCONT.LEVEL                                                                     # 学習レベル
            TYPE = PARTSCONT.TYPE                                                                       # 学習タイプ
            PARTS = PARTSCONT.PARTS
            if TYPE == GP.LEARN_TYPE.AGE:
                LTYPE = PARTSCONT.AGE
            elif TYPE == GP.LEARN_TYPE.EVT:
                LTYPE = PARTSCONT.EVT
            for UNIT_NAME in unitNameList:                                                              # 学習名をすべて
                LEARN_NAME = LTYPE.LEARN_CONF.objectList[LEVEL]                                         # 学習名をセット
                MODEL_COMB = ModelCombClass(PARTS, LEVEL, TYPE, LEARN_NAME)                             # モデルコンボを生成
                MODEL_COMB.setClassVar(laserIdList, self.parameter)                                     # 学習単位と学習単位名をセット
                MODEL_COMB.setLearnUnit(LEARN_UNIT, UNIT_NAME)                                          # 学習単位と学習単位名をセット
                MODEL_COMB.loadModel()                                                                  # セーブデータとモデルを読み込む
                MODEL_DIC[UNIT_NAME] = MODEL_COMB                                                       # MODEL辞書に登録
            return MODEL_DIC

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   主部品コンテナを返す
    #---------------------------------------------------------------------------------------------------
    def getMainPartsContaier(self, parts):
        try:
            for PARTS in GP.MIXCONT.PARTS_LIST:                                                         # 部品コンテナリストをすべて実行
                if PARTS.PARTS == parts:                                                                # コンテナの部品名が主部品の時
                    return PARTS                                                                        # 主部品コンテナを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   年齢分析結果表示
    #---------------------------------------------------------------------------------------------------
    def AGE_RESULT_VIEW(self):
        try:
            self.commonParam.setClassVar(self)                                                          # 年齢パラメーターをクラス変数に転写する
            laserIdList = self.treeWidget.laserIdList                                                   # レーザーIDリストを転写
            TYPE = GP.LEARN_TYPE.AGE                                                                    # 学習タイプをセット
            GP.CONT.setLabelList(TYPE)                                                                  # 出力ラベルリストをセット
            ageView = AgeTableViewClass.getInstance()                                                   # 年齢ビューセット
            if self.parameter.MAIN_CH:                                                                  # 主部品がCHの時
                GP.MIXCONT.MAIN_PARTS = self.getMainPartsContaier(GP.PARTS.CH)                          # 主部品コンテナをセット
            elif self.parameter.MAIN_LN:                                                                # 主部品がLNの時
                GP.MIXCONT.MAIN_PARTS = self.getMainPartsContaier(GP.PARTS.LN)                          # 主部品コンテナをセット
            elif self.parameter.MAIN_PPM:                                                               # 主部品がPPMの時
                GP.MIXCONT.MAIN_PARTS = self.getMainPartsContaier(GP.PARTS.PPM)                         # 主部品コンテナをセット
            elif self.parameter.MAIN_MM:                                                                # 主部品がMMの時
                GP.MIXCONT.MAIN_PARTS = self.getMainPartsContaier(GP.PARTS.MM)                          # 主部品コンテナをセット
            for PARTSCONT in GP.MIXCONT.PARTS_LIST:                                                     # 部品コンテナリストをすべて実行
                self.setPartsConteiner(PARTSCONT, TYPE)                                                 # カレント部品コンテナのセット
                PARTSCONT.PCOMB.setClassVar(laserIdList, self.learnParameter)                           # 学習単位と学習単位名をセット
            ageView.setClassVar()                                                                       # 年齢一覧ビューパラメータセット
            ageView.showMaxArgTable()                                                                   # 最大年齢テーブル表示
            self.clearView()                                                                            # ビューレイアウトの要素を削除
            self.curView = ageView                                                                      # 年齢ビューセット
            self.viewLayout.addWidget(self.curView)                                                     # ビューレイアウトに加える
            self.curView.show()                                                                         # 分析設定ビュー表示

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   クローズ処理
    #---------------------------------------------------------------------------------------------------
    def closeEvent(self, e):
        try:
            ageView = AgeTableViewClass.getInstance()                                                   # 年齢一覧ビュー取得
            if ageView.canvas is not None:                                                              # キャンバスが有る時
                ageView.canvas.clearPredictView()                                                       # 予測値ビューのクローズ処理
        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

