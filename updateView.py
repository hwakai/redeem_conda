import numpy as np
from PyQt5Import import *
from static import *
from qtBase import QtBaseClass
from analysisBase import AnalysisBaseClass
from classDef import *
from qtBase import ProgressWindowClass
from origin import OriginClass
from viewBase import ViewBaseClass


# =======================================================================================================
#   クラス データ更新ビュークラス
# =======================================================================================================
class UpdateViewClass(AnalysisBaseClass):
    # ---------------------------------------------------------------------------------------------------
    # インスタンス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None

    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, parent):  # 初期化
        try:
            if UpdateViewClass._singleton is None:  # シングルトンが無いとき
                AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
                self.parentObject = parent  # 親クラスの転写
                self.title = "データ更新"  # タブタイトル
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
        if UpdateViewClass._singleton is None:  # シングルトンが無いとき
            UpdateViewClass._singleton = UpdateViewClass(parent)  # インスタンスを生成してシングルトンにセット
        return UpdateViewClass._singleton  # シングルトンがを返す

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト生成
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            self.tabs = QTabWidget()  # タブウィジェット生成
            #            self.tabs.resize(300,180)                                                                  # タブサイズ設定

            # タブ生成
            self.dataTransTab = DataTransTabClass(self, "データ移行")  # データ移行タブ生成
            self.rdmUpdateTab = RdmUpdateTabClass(self, "REDEEMデータ更新")  # REDEEM更新タブ生成

            # タブリストにタブを登録
            self.tabList = []  # 空のタブリスト生成
            self.tabList.append(self.rdmUpdateTab)  # REDEEM更新タブ追加
            self.tabList.append(self.dataTransTab)  # データ移行タブ追加
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
#   スーパークラス Redeemデータ更新タブクラス
# =======================================================================================================
class UpdateTabClass(ViewBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            ViewBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.progress = ProgressWindowClass()  # 進捗ダイアローグ生成
            viewLayout = self.makeViewLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout = self.createTreeLayout(self.title, self.treeWidget, viewLayout)  # ツリーレイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.setParametersToObject()  # パラメータをオブジェクトにセット(TABLE_NAMEは未設定)
            self.SET_TABLE_NAME()  # TABLE_NAMEコンボボックスセット
            self.setParametersToObject()  # TABLE_NAMEをオブジェクトにセット
            self.setParametersFromObject()  # オブジェクトのデータをパラメータに再度セット
            self.parameter.saveData()  # オブジェクトのデータをパラメータとファイルに書き込み
            self.parameter.setClassVar(self)  # メンバーのパラメータデータをセット
            self.connectButtons2()  # タブのオブジェクトとメソッドを結合
            self.setSizePolicy(  # サイズポリシー設定
                QSizePolicy.Expanding,  # 幅可変
                QSizePolicy.Expanding)  # 高さ可変
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def makeViewLayout(self):
        try:
            viewLayout = QVBoxLayout()  # メインレイアウト生成（垂直レイアウト）
            # 直接DB処理メニュー                                                                        　　　　
            self.setLabelStyle2(viewLayout, "データ更新", "gray", "white", 40, "20pt")  # 表題ラベル
            self.setStrCombo(viewLayout, ["SRC_SERVER", "サーバー"], self.serverList)  # サーバー選択
            self.setStrCombo(viewLayout, ["SEL_TABLE", "選択テーブル名"], [GP.ALL, "BBB"])  # 選択テーブル名
            self.setSelButton(viewLayout, ["SET_TABLE_NAME", "テーブル名設定"])  # ORG_SEL_NAMEコンボボックスセット
            self.setExeButton(viewLayout, ["UPDATE_LOCAL_SERVER", "ローカルDBを更新"])  # リモートサーバーからオリジナルDBを更新
            viewLayout.setAlignment(Qt.AlignTop)  # 上詰め
            return viewLayout  # メインレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ***************************************************************************************************
    #   メニュー
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   サーバーテーブル名選択コンボボックスセット
    # ---------------------------------------------------------------------------------------------------
    def SET_TABLE_NAME(self):
        try:
            self.parameter.setClassVar(self)  # パラメータをインスタンス変数に転写する
            comboBox = self.comboBox_SEL_TABLE
            SERVER = self.SRC_SERVER  # サーバーを転写
            SOURCE = GP.DATA_SOURCE.ORIGIN  # 選択ソース名からGP.CONTのソースを取得する
            initialText = self.SEL_TABLE  # 初期テキスト
            self.setServerTableName(comboBox, SERVER, SOURCE, initialText)  # ファイル名選択コンボボックスセット

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   リモートサーバーからオリジナルDBを更新
    # ---------------------------------------------------------------------------------------------------
    def UPDATE_LOCAL_SERVER(self):
        try:
            laserIdList = self.treeWidget.laserIdList  # レーザーIDリスト取得
            if laserIdList is not None:  # レーザーリストが有る時
                SRC_SERVER = self.SRC_SERVER  # 読込元サーバーの転写
                SOURCE = GP.DATA_SOURCE.ORIGIN  # ソース名
                SEL_TABLE = self.SEL_TABLE  # 選択テーブルを転写
                p = self.progress  # 進捗ダイアローグを転写
                if SEL_TABLE == GP.ALL:  # 選択テーブル名がALLの時
                    tableNameList = self.getFileTableList(SOURCE)  # ファイルテーブル名リストを取得
                else:  # 選択テーブル名がALLで無い時
                    tableNameList = [SEL_TABLE]  # 選択テーブルをセット
                self.startNewLevel(len(tableNameList), p)  # 新しいレベルの進捗開始
                for table in tableNameList:  # テーブル名リストをすべて実行
                    if self.isDBS(SRC_SERVER):  # サーバータイプがDBサーバーの時
                        self.updateServerDBS(SRC_SERVER, SOURCE, table, laserIdList, p)  # サーバーからテーブルをファイルに書き込む
                    elif self.isSSH(SRC_SERVER):  # サーバータイプがSSHサーバーの時
                        self.updateServerSSH(SRC_SERVER, SOURCE, table, laserIdList, p)  # サーバーからテーブルをファイルに書き込む
            self.endLevel(p)  # 現レベルの終了
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e, p)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   リモートサーバーからオリジナルDBを更新
    # ---------------------------------------------------------------------------------------------------
    def updateServerDBS(self, SERVER, SOURCE, TABLE, filterList, p=None):
        try:
            localDBS = GP.SERVER.LOC_RDM_DBS  # ローカルDBS転写
            FILEServer = GP.SVR.FILEServer  # ファイルサーバー転写
            DBSServer = GP.SVR.DBSServer  # DBSサーバー転写
            object = GP.CONT.ORIGIN.objectDic[TABLE]  # オブジェクトを取得
            incPath = object.targetPathInc  # 追加パスを取得
            colName = object.tableDesc.colName  # コラム名リスト
            if object.DATE_FIELD == "":  # 日付フィールドが無い時はDBをすべて更新する
                # 日付フィールドが無い時はテーブルをすべて更新する
                self.startNewLevel(4, p)  # 新しいレベルの進捗開始
                localCount = DBSServer.getCount(localDBS, object, p)  # ローカルサーバーのカウントを取得する
                serverCount = DBSServer.getCount(SERVER, object, p)  # サーバーのカウントを取得する
                if serverCount > 0 and localCount != serverCount:  # カウントが違う時
                    if self.existsTable(SERVER, object):  # DBにテーブルが有る時
                        baseQuery = self.makeObjectQuery(object)  # オブジェクトのフィールド名からセレクトクエリーを作成
                        DBSServer.makeCsvFileFromQuery(SERVER, object, baseQuery, p)  # クエリーからCSVファイルを作成する
                        DBSServer.makeDBFromObjectFile(localDBS, object, p)  # オブジェクトファイルからDBを作成
                self.endLevel(p)  # 現レベルの終了
            else:  # 日付フィールドが有る時
                res = False  # 結果を初期化
                if "LASER_ID" in colName:  # フィールドにLASER_IDが有る時
                    # LASER_IDが有る時はレーザー毎の最終書き込み日時以後のデータを追加する
                    self.startNewLevel(2, p)  # 新しいレベルの進捗開始
                    latestDateList = DBSServer.getLatestDic(localDBS, object, filterList, p)  # ローカルサーバーの最終書き込み日時を取得する
                    if latestDateList is not None:
                        res = DBSServer.makeLaserAddFile(SERVER, object, incPath, filterList, latestDateList,
                                                         p)  # レーザー単位の追加リストを取得する
                    self.endLevel(p)  # 現レベルの終了
                else:
                    # LASER_IDが無い時は最終書き込み日時以後のデータを追加する
                    self.startNewLevel(2, p)  # 新しいレベルの進捗開始
                    latestDateTime = DBSServer.getLatestDateTime(localDBS, object, p)  # ローカルサーバーの最終書き込み日時を取得する
                    if latestDateTime is not None:  # 最終書き込み日時が有る時
                        res = DBSServer.makeAddFile(SERVER, object, incPath, filterList, latestDateList,
                                                    p)  # 最終書き込み時刻から追加リストを取得する
                    self.endLevel(p)  # 現レベルの終了
                if res:
                    self.startNewLevel(2, p)  # 新しいレベルの進捗開始
                    FILEServer.mergeFile(object, incPath, p)  # 追加ファイルをログファイルにマージする
                    DBSServer.fileToDB(localDBS, object, incPath, p)  # オリジナルからDB作成（項目修正有り）
                    self.endLevel(p)  # 現レベルの終了
            emit(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   リモートサーバーからオリジナルDBを更新
    # ---------------------------------------------------------------------------------------------------
    def updateServerSSH(self, SERVER, SOURCE, TABLE, filterList, p=None):
        try:
            localDBS = GP.SERVER.LOC_RDM_DBS  # ローカルDBS転写
            FILEServer = GP.SVR.FILEServer  # ファイルサーバー転写
            DBSServer = GP.SVR.DBSServer  # DBSサーバー転写
            SSHServer = GP.SVR.SSHServer  # SSHサーバー転写
            object = GP.CONT.ORIGIN.objectDic[TABLE]  # オブジェクトを取得
            incPath = object.targetPathInc  # 追加パスを取得
            colName = object.tableDesc.colName  # コラム名リスト
            if object.DATE_FIELD == "":  # 日付フィールドが無い時はDBをすべて更新する
                # 日付フィールドが無い時はテーブルをすべて更新する
                self.startNewLevel(4, p)  # 新しいレベルの進捗開始
                localCount = DBSServer.getCount(localDBS, object, p)  # ローカルサーバーのカウントを取得する
                serverCount = SSHServer.getCountSSH(SERVER, object, p)  # サーバーのカウントを取得する
                if localCount != serverCount:  # カウントが違う時
                    SSHServer.DB_TO_CSV(SERVER, object, p)  # サーバーからテーブルをファイルに書き込む
                    DBSServer.makeDBFromObjectFile(localDBS, object, p)  # オブジェクトファイルからDBを作成
                self.endLevel(p)  # 現レベルの終了
            else:  # 日付フィールドが有る時
                res = False  # 結果を初期化
                if "LASER_ID" in colName:  # フィールドにLASER_IDが有る時
                    # LASER_IDが有る時はレーザー毎の最終書き込み日時以後のデータを追加する
                    self.startNewLevel(2, p)  # 新しいレベルの進捗開始
                    latestDateList = DBSServer.getLatestDic(localDBS, object, filterList, p)  # ローカルサーバーの最終書き込み日時を取得する
                    if latestDateList is not None:
                        res = SSHServer.makeLaserAddFileSSH(SERVER, object, incPath, filterList, latestDateList,
                                                            p)  # レーザー単位の追加ファイルを作成する
                    self.endLevel(p)  # 現レベルの終了
                else:
                    # LASER_IDが無い時は最終書き込み日時以後のデータを追加する
                    self.startNewLevel(2, p)  # 新しいレベルの進捗開始
                    latestDateTime = DBSServer.getLatestDateTime(localDBS, object, p)  # ローカルサーバーの最終書き込み日時を取得する
                    if latestDateTime is not None:  # 最終書き込み日時が有る時
                        res = SSHServer.makeAddFileSSH(SERVER, object, incPath, filterList, latestDateList,
                                                       p)  # 最終書き込み時刻から追加リストを取得する
                    self.endLevel(p)  # 現レベルの終了
                if res:
                    self.startNewLevel(2, p)  # 新しいレベルの進捗開始
                    FILEServer.mergeFile(object, incPath, p)  # 追加ファイルをログファイルにマージする
                    DBSServer.fileToDB(localDBS, object, incPath, p)  # オリジナルからDB作成（項目修正有り）
                    self.endLevel(p)  # 現レベルの終了
            emit(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示


# =======================================================================================================
#   クラス REDEEM更新パラメータクラス
# =======================================================================================================
class RdmUpdateParameterClass(ParameterClass):
    def __init__(self):  # 初期化
        try:
            ParameterClass.__init__(self, GP.UPDATE_LOG.RDM)  # スーパークラスの初期化
            SRC_SERVER = GP.SERVER.DMY_RDM_DBS  # サーバー名選択
            SEL_TABLE = GP.ALL  # 選択テーブル名
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # ローカル変数名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
            self.loadData()  # パラメータをログファイルから読込

        except Exception as e:  # 例外
            printError(e)  # 例外を表示


# =======================================================================================================
#   クラス Redeemデータ更新タブクラス
# =======================================================================================================
class RdmUpdateTabClass(UpdateTabClass):
    def __init__(self, parent, title):  # 初期化
        try:
            self.parentObject = parent  # 親クラスの転写
            self.title = title  # タブのタイトル
            self.strPath = GP.UPDATE_LOG.RDM  # ログパス
            self.parameter = RdmUpdateParameterClass()  # パラメータ
            self.treeWidget = GP.TREE.RDM_UD  # ツリー ウイジェット転写
            self.serverList = GP.SERVER.redeemList()  # サーバーアイテムリスト作成
            UpdateTabClass.__init__(self, None)  # スーパークラスの初期化

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass


# =======================================================================================================
#   クラス データ移行タブクラス
# =======================================================================================================
class DataTransTabClass(ViewBaseClass):
    def __init__(self, parent, title):  # 初期化
        try:
            ViewBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.parentObject = parent  # 親クラスの転写
            self.title = title  # タブのタイトル
            self.progress = ProgressWindowClass()  # 進捗ダイアローグ生成
            self.parameter = DataTransParameterClass.getInstance()  # パラメータ
            self.treeWidget = GP.TREE.DATA_TR  # 機種選択ツリービュー作成
            viewLayout = self.makeViewLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout = self.createTreeLayout(title, self.treeWidget, viewLayout)  # ツリーレイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.setParametersToObject()  # パラメータをオブジェクトにセット(FILE_NAME,TABLE_NAMEは未設定)
            self.SET_FILE_NAME()  # FILE_NAMEコンボボックスセット
            self.SET_TABLE_NAME()  # TABLE_NAMEコンボボックスセット
            self.setParametersToObject()  # FILE_NAME,TABLE_NAMEをオブジェクトにセット
            self.setParametersFromObject()  # オブジェクトのデータをパラメータに再度セット
            self.parameter.saveData()  # オブジェクトのデータをパラメータとファイルに書き込み
            self.parameter.setClassVar(self)  # メンバーのパラメータデータをセット
            self.connectButtons2()  # タブのオブジェクトとメソッドを結合
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #       ビューレイアウト作成
    # ---------------------------------------------------------------------------------------------------
    def makeViewLayout(self):
        try:
            srcList = GP.SERVER.nameList  # SRCサーバーアイテムリスト作成
            dstList = GP.SERVER.dstList()  # DSTサーバーアイテムリスト作成
            blockRange = self.flatRange(1, 9, 1) + self.flatRange(10, 90, 10) + self.flatRange(100, 900,
                                                                                               100) + self.flatRange(
                1000, 9000, 1000) + self.flatRange(10000, 90000, 10000) + self.flatRange(100000, 1000000,
                                                                                         100000)  # データソース名選択
            viewLayout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            viewLayout.setAlignment(Qt.AlignTop)  # 上詰め
            self.setLabelStyle2(viewLayout, "パラメータ", "gray", "white", 40, "12pt")  # 表題ラベル
            self.setStrCombo(viewLayout, ["SRC_SERVER", "SRCサーバー"], srcList)  # SRCサーバー選択
            self.setStrCombo(viewLayout, ["DST_SERVER", "DSTサーバー"], dstList)  # DSTサーバー選択
            self.setStrCombo(viewLayout, ["SEL_FILE", "選択ファイル名"], [GP.ALL, "BBB"])  # 選択ファイル名
            self.setStrCombo(viewLayout, ["SEL_TABLE", "選択テーブル名"], [GP.ALL, "BBB"])  # 選択テーブル名
            self.setStrCombo(viewLayout, ["SEL_SOURCE", "データソース名"], GP.DATA_SOURCE.nameList)  # データソース名選択
            self.setIntCombo(viewLayout, ["DELETE_ROWS", "削除行数"], blockRange)  # 削除行数
            self.setIntCombo(viewLayout, ["FILE_BLOCK", "ファイルブロック長"], blockRange)  # ファイルブロック長
            self.setIntCombo(viewLayout, ["LASER_BLOCK", "レーザーブロック長"], blockRange)  # アップロードブロック長
            self.setCheckBox(viewLayout, ["USE_OBJECT_BLOCK", "オブジェクトブロック使用"])  # オブジェクトブロック使用フラグ
            self.setSelButton(viewLayout, ["SET_FILE_NAME", "ファイル名設定"])  # ORG_SEL_NAMEコンボボックスセット
            self.setSelButton(viewLayout, ["SET_TABLE_NAME", "SRC DB テーブル名設定"])  # ORG_SEL_NAMEコンボボックスセット
            self.setExeButton(viewLayout, ["FILE_TO_SERVER", "ファイルからサーバーに書き込む"])  # CSVからローカルDBサーバーに書き込み
            self.setExeButton(viewLayout, ["SERVER_TO_FILE", "サーバーからファイルに書き込む"])  # DBからCSVファイルを作成
            self.setExeButton(viewLayout, ["SERVER_TO_SERVER", "サーバーからサーバーに書き込む"])  # DBからDBファイルを作成
            self.setExeButton(viewLayout, ["DELETE_ROW", "最後のN行を削除"])  # 最後のN行を削除
            return viewLayout  # ビューレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ***************************************************************************************************
    #   メニュー
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   FILE_NAMEコンボボックスセット
    # ---------------------------------------------------------------------------------------------------
    def SET_FILE_NAME(self):
        try:
            self.parameter.setClassVar(self)  # パラメータをインスタンス変数に転写する
            comboBox = self.comboBox_SEL_FILE  # コンボボックス
            initialText = self.SEL_FILE  # 初期テキスト
            SOURCE = self.SEL_SOURCE  # 選択ソース名からGP.CONTのソースを取得する
            self.setFileName(comboBox, SOURCE, initialText)  # ファイル名選択コンボボックスセット
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   TABLE_NAMEコンボボックスセット
    # ---------------------------------------------------------------------------------------------------
    def SET_TABLE_NAME(self):
        try:
            self.parameter.setClassVar(self)  # パラメータをインスタンス変数に転写する
            comboBox = self.comboBox_SEL_TABLE
            SERVER = self.SRC_SERVER  # サーバーを転写
            SOURCE = self.SEL_SOURCE  # 選択ソース名からGP.CONTのソースを取得する
            initialText = self.SEL_TABLE  # 初期テキスト
            self.setServerTableName(comboBox, SERVER, SOURCE, initialText)  # ファイル名選択コンボボックスセット
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   サーバーからファイルに書き込む
    # ---------------------------------------------------------------------------------------------------
    def SERVER_TO_FILE(self):
        try:
            self.parameter.setClassVar(self)  # パラメータをインスタンス変数に転写する
            SERVER = self.SRC_SERVER  # 書き込み先サーバーの転写
            SOURCE = self.SEL_SOURCE  # 選択ソース名
            SEL_TABLE = self.SEL_TABLE  # 選択テーブル名
            p = self.progress  # 進捗ダイアローグを転写
            if SEL_TABLE == GP.ALL:  # 選択テーブル名がALLの時
                tableNameList = self.getFileTableList(SOURCE)  # ファイルテーブル名リストを取得
            else:  # 選択テーブル名がALLで無い時
                tableNameList = [SEL_TABLE]  # 選択テーブルをセット
            self.startNewLevel(len(tableNameList), p)  # 新しいレベルの進捗開始
            for table in tableNameList:  # テーブル名リストをすべて実行
                if (table == GP.CONT.ORIGIN_CONF.LSM or  # LSMの時または
                        table == GP.CONT.ORIGIN_CONF.LTM or  # LTMの時または
                        table == GP.CONT.ORIGIN_CONF.MDM):  # MDMの時
                    self.serverToFile(SERVER, SOURCE, table, p)  # サーバーからテーブルをファイルに書き込む
                else:
                    self.serverToFilterFile(SERVER, SOURCE, table, p)  # サーバーからテーブルをフィルタ0をかけたファイルに書き込む
            self.endLevel(p)  # 現レベルの終了
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e, p)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ファイルからサーバーに書き込み
    # ---------------------------------------------------------------------------------------------------
    def FILE_TO_SERVER(self):
        try:
            SERVER = self.DST_SERVER  # 書き込み先サーバーの転写
            SOURCE = self.SEL_SOURCE  # 選択ソース名からGP.CONTのソースを取得する
            SEL_FILE = self.SEL_FILE  # 選択ファイル名
            p = self.progress  # 進捗ダイアローグを転写
            if SEL_FILE == GP.ALL:  # 選択ファイル名がALLの時
                tableNameList = self.getFileTableList(SOURCE)  # テーブル名リストを取得
            else:  # 選択テーブル名がALLで無い時
                tableNameList = [SEL_FILE]  # 選択テーブルをセット
            self.startNewLevel(len(tableNameList), p)  # 新しいレベルの進捗開始
            for fileName in tableNameList:  # ファイルテーブル名リストをすべて実行
                self.fileToServer(SERVER, SOURCE, fileName, p)  # サーバーからテーブルをファイルに書き込む
            self.endLevel(p)  # 現レベルの終了
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e, p)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   サーバーからサーバーに書き込み
    # ---------------------------------------------------------------------------------------------------
    def SERVER_TO_SERVER(self):
        try:
            laserIdList = self.treeWidget.laserIdList  # レーザーIDリスト取得
            SRC_SERVER = self.SRC_SERVER  # 読込元サーバーの転写
            DST_SERVER = self.DST_SERVER  # 書き込み先サーバーの転写
            SEL_TABLE = self.SEL_TABLE  # 選択テーブル名
            p = self.progress  # 進捗ダイアローグを転写
            if SRC_SERVER != DST_SERVER:  # 読込元と書き込み先が違う時
                if GP.SERVER.WRITE_ENABLE[DST_SERVER]:  # 書き込み可の時
                    SOURCE = self.SEL_SOURCE  # 選択ソース名
                    if SEL_TABLE == GP.ALL:  # 選択テーブル名がALLの時
                        tableNameList = self.getFileTableList(SOURCE)  # ファイルテーブル名リストを取得
                    else:  # 選択テーブル名がALLで無い時
                        tableNameList = [SEL_TABLE]  # 選択テーブルをセット
                    self.startNewLevel(len(tableNameList), p)  # 新しいレベルの進捗開始
                    for table in tableNameList:  # テーブル名リストをすべて実行
                        if (table == GP.CONT.ORIGIN_CONF.LSM or  # LSMの時または
                                table == GP.CONT.ORIGIN_CONF.LTM or  # LTMの時または
                                table == GP.CONT.ORIGIN_CONF.MDM):  # MDMの時
                            self.serverToFile(SRC_SERVER, SOURCE, table, p)  # サーバーからテーブルをファイルに書き込む
                        else:
                            self.serverToFilterFile(SRC_SERVER, SOURCE, table, p)  # サーバーからテーブルをフィルタ0をかけたファイルに書き込む
                        self.fileToServer(DST_SERVER, SOURCE, table, p)  # サーバーからテーブルをファイルに書き込む
                    self.endLevel(p)  # 実行時間表示
            emit(p)  # 実行時間表示
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e, p)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   最後のN行を削除
    # ---------------------------------------------------------------------------------------------------
    def DELETE_ROW(self):
        try:
            self.parameter.setClassVar(self)  # パラメータをインスタンス変数に転写する
            SERVER = self.SRC_SERVER  # 書き込み先サーバーの転写
            SOURCE = self.SEL_SOURCE  # 選択ソース名
            SEL_TABLE = self.SEL_TABLE  # 選択テーブル名
            p = self.progress  # 進捗ダイアローグを転写
            if SEL_TABLE == GP.ALL:  # 選択テーブル名がALLの時
                tableNameList = self.getFileTableList(SOURCE)  # ファイルテーブル名リストを取得
            else:  # 選択テーブル名がALLで無い時
                tableNameList = [SEL_TABLE]  # 選択テーブルをセット
            self.startNewLevel(len(tableNameList), p)  # 新しいレベルの進捗開始
            for table in tableNameList:  # テーブル名リストをすべて実行
                self.deleteRows(SERVER, SOURCE, table, self.DELETE_ROWS, p)  # サーバーからテーブルをファイルに書き込む
            self.endLevel(p)  # 現レベルの終了
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e, p)  # 例外を表示
            pass


