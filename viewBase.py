import numpy as np
import os
from staticImport import *
from qtBase import QtBaseClass

#=======================================================================================================
#   スーパークラス ビューベースクラス
#=======================================================================================================
class ViewBaseClass(QtBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        try:
            QtBaseClass.__init__(self, TABLE_NAME)                                                      # スーパークラスの初期化
            pass

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   ファイルからテーブルをサーバーに書き込む
    #---------------------------------------------------------------------------------------------------
    def fileToServer(self, SERVER, SOURCE, FILE, p=None):
        try:
            if GP.SERVER.WRITE_ENABLE[SERVER]:                                                          # 書き込み可の時
                DBSDIR = GP.SERVER.DBSDIR[SERVER]                                                       # DBディレクトリ名を取得する
                SOURCE_CLASS_LIST = GP.SVR.SOURCE_CLASS[SOURCE]                                         # 選択ソース名からGP.CONTのソースリストを取得する
                for SOURCE_CLASS in SOURCE_CLASS_LIST:                                                  # ソースリストをすべて実行する
                    if FILE in SOURCE_CLASS.objectDic:                                                  # ファイルがソースに有る時
                        object = SOURCE_CLASS.objectDic[FILE]                                           # オブジェクトを取得
                        self.csvToDb(object, SERVER, p)                                                 # CVCからDBを作成
            pass

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   サーバーからテーブルをファイルに書き込む
    #---------------------------------------------------------------------------------------------------
    def serverToFile(self, SERVER, SOURCE, TABLE, p=None):
        try:
            DBSDIR = GP.SERVER.DBSDIR[SERVER]                                                           # DBディレクトリ名を取得する
            SOURCE_CLASS_LIST = GP.SVR.SOURCE_CLASS[SOURCE]                                             # 選択ソース名からGP.CONTのソースリストを取得する
            for SOURCE_CLASS in SOURCE_CLASS_LIST:                                                      # ソースリストをすべて実行する
                if TABLE in SOURCE_CLASS.objectDic:                                                     # テーブルがソースに有る時
                    object = SOURCE_CLASS.objectDic[TABLE]                                              # オブジェクトを取得
                    if SERVER == GP.SERVER.LOC_RDM_DBS or object.DBSDIR == DBSDIR:                      # 書き込み先がローカルサーバーかオブジェクトのDB名の時
                        tableNameList = self.getServerTableList(SERVER, SOURCE)                         # テーブル名リストを取得
                        self.startNewLevel(1, p)                                                        # 新しいレベルの進捗開始
                        if object.TABLE_NAME in tableNameList:                                          # オブジェクトがテーブル名リストに有る時
                            if self.isDBS(SERVER):                                                      # サーバータイプがDBサーバーの時
                                result = GP.SVR.DBSServer.makeFileFromDB(SERVER, object, p)             # テーブルリストをDBサーバーから作る
                            elif self.isSSH(SERVER):                                                    # サーバータイプがSSHサーバーの時
                                result = GP.SVR.SSHServer.DB_TO_CSV(SERVER, object, p)                  # テーブルリストをSSHサーバーから作る
                        self.endLevel(p)                                                                # 現レベルの終了
            emit(p)
            pass

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                           # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   サーバーからフィルターをかけたテーブルをファイルに書き込む
    #---------------------------------------------------------------------------------------------------
    def serverToFilterFile(self, SERVER, SOURCE, TABLE, p=None):
        try:
            DBSDIR = GP.SERVER.DBSDIR[SERVER]                                                           # DBディレクトリ名を取得する
            SOURCE_CLASS_LIST = GP.SVR.SOURCE_CLASS[SOURCE]                                             # 選択ソース名からGP.CONTのソースリストを取得する
            filterList = self.treeWidget.laserIdList                                                    # レーザーIDリスト取得
            for SOURCE_CLASS in SOURCE_CLASS_LIST:                                                      # ソースリストをすべて実行する
                if TABLE in SOURCE_CLASS.objectDic:                                                     # テーブルがソースに有る時
                    object = SOURCE_CLASS.objectDic[TABLE]                                              # オブジェクトを取得
                    if SERVER == GP.SERVER.LOC_RDM_DBS or object.DBSDIR == DBSDIR:                      # 書き込み先がローカルサーバーかオブジェクトのDB名の時
                        tableNameList = self.getServerTableList(SERVER, SOURCE)                         # テーブル名リストを取得
                        self.startNewLevel(1, p)                                                        # 新しいレベルの進捗開始
                        if object.TABLE_NAME in tableNameList:                                          # オブジェクトがテーブル名リストに有る時
                            if self.isDBS(SERVER):                                                      # サーバータイプがDBサーバーの時
                                result = GP.SVR.DBSServer.makeFilterFileFromDB(SERVER, object, filterList, p)      # テーブルリストをDBサーバーから作る
                            elif self.isSSH(SERVER):                                                    # サーバータイプがSSHサーバーの時
                                result = GP.SVR.SSHServer.DB_TO_FILTER_CSV(SERVER, object, filterList, p)      # テーブルリストをSSHサーバーから作る
                        self.endLevel(p)                                                                # 現レベルの終了
            emit(p)
            pass

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   テーブルから最後のN行を削除
    #---------------------------------------------------------------------------------------------------
    def deleteRows(self, SERVER, SOURCE, TABLE, rows, p=None):
        try:
            DBSDIR = GP.SERVER.DBSDIR[SERVER]                                                           # DBディレクトリ名を取得する
            SOURCE_CLASS_LIST = GP.SVR.SOURCE_CLASS[SOURCE]                                             # 選択ソース名からGP.CONTのソースリストを取得する
            for SOURCE_CLASS in SOURCE_CLASS_LIST:                                                      # ソースリストをすべて実行する
                if TABLE in SOURCE_CLASS.objectDic:                                                     # テーブルがソースに有る時
                    object = SOURCE_CLASS.objectDic[TABLE]                                              # オブジェクトを取得
                    if SERVER == GP.SERVER.LOC_RDM_DBS or object.DBSDIR == DBSDIR:                      # 書き込み先がローカルサーバーかオブジェクトのDB名の時
                        tableNameList = self.getServerTableList(SERVER, SOURCE)                         # テーブル名リストを取得
                        self.startNewLevel(1, p)                                                        # 新しいレベルの進捗開始
                        if object.TABLE_NAME in tableNameList:                                          # オブジェクトがテーブル名リストに有る時
                            if self.isDBS(SERVER):                                                      # サーバータイプがDBサーバーの時
                                result = GP.SVR.DBSServer.deleteTableRows(SERVER, object, rows, p)      # テーブルリストをDBサーバーから作る
                            elif self.isSSH(SERVER):                                                    # サーバータイプがSSHサーバーの時
                                if (SERVER == GP.SERVER.FDR_RDM_SSH):
                                    result = GP.SVR.SSHServer.DELETE_TABLE_ROWS(SERVER, object, rows, p)      # テーブルリストをSSHサーバーから作る
                        self.endLevel(p)                                                                # 現レベルの終了
            emit(p)
            pass

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   テーブル名選択コンボボックスセット
    #---------------------------------------------------------------------------------------------------
    def setTableName(self, comboBox, tableNameList, initialText):
        try:
            # コネクト済みの時は切断
            if self.connected:                                                                          # コネクトフラグを確認
                comboBox.currentTextChanged.disconnect()                                                # comboBox_SELECT_NAMEを切断
            comboBox.clear()                                                                            # コンボボックスをクリア
            comboBox.addItem(GP.ALL)                                                                    # コンボボックスに'ALL'を挿入
            if tableNameList is not None:                                                               # テーブルリストが有る時
                comboBox.addItems(tableNameList)                                                        # コンボボックスにアイテムを挿入
                comboBox.setCurrentText(initialText)                                                    # 現在のコンボボックスに値をパラメータの値をセット
                self.NAME = comboBox.currentText()                                                      # パラメータの値をコンボボックスから再設定
            # コネクト済みの時は再接続
            if self.connected:                                                                          # コネクトフラグを確認
                comboBox.currentTextChanged.connect(self.saveParam)                                     # comboBox_SELECT_NAMEを再接続

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   サーバーテーブル名選択コンボボックスセット
    #---------------------------------------------------------------------------------------------------
    def setServerTableName(self, comboBox, SERVER, SOURCE, initialText):
        try:
            tableNameList = self.getServerTableList(SERVER, SOURCE)                                     # テーブル名リストを取得
            self.setTableName(comboBox, tableNameList, initialText)                                     # テーブル名選択コンボボックスセット
            pass

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   サーバーテーブル名リストを返す
    #---------------------------------------------------------------------------------------------------
    def getServerTableList(self, SERVER, SOURCE):
        try:
            serverTableList = self.makeServerTableList(SERVER)                                          # サーバーテーブル名リストを取得
            SOURCE_CLASS_LIST = GP.SVR.SOURCE_CLASS[SOURCE]                                             # 選択ソース名からGP.CONTのソースリストを取得する
            tableNameList = []                                                                          # テーブルリストを初期化
            for SOURCE_CLASS in SOURCE_CLASS_LIST:                                                      # ソースリストをすべて実行
                objectTableList = SOURCE_CLASS.tableList                                                # オブジェクトテーブル名リストを取得
                if serverTableList is not None and len(objectTableList) > 0:                            # テーブルリストが有る時
                    tableNameList += list(serverTableList[np.in1d(serverTableList, objectTableList)])   # オブジェクト名リストに有るものを抽出
            if len(tableNameList) > 0:                                                                  # テーブルリストが有る時
                return np.array(tableNameList, 'str')                                                   # テーブルリストを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   サーバーテーブル名リストを作成する
    #---------------------------------------------------------------------------------------------------
    def makeServerTableList(self, SERVER):
        try:
            if self.isDBS(SERVER):                                                                      # サーバータイプがDBサーバーの時
                tableNameList = GP.SVR.DBSServer.makeTableNameList(SERVER)                              # テーブルリストをDBサーバーから作る
            elif self.isSSH(SERVER):                                                                    # サーバータイプがSSHサーバーの時
                tableNameList = GP.SVR.SSHServer.makeTableNameListSSH(SERVER)                           # テーブルリストをSSHサーバーから作る
            if tableNameList is not None:                                                               # テーブルリストが有る時
                return tableNameList                                                                    # テーブルリストを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   ファイル名選択コンボボックスセット
    #---------------------------------------------------------------------------------------------------
    def setFileName(self, comboBox, SOURCE, initialText):
        try:
            tableNameList = self.getFileTableList(SOURCE)                                               # ファイルテーブル名リストを取得
            self.setTableName(comboBox, tableNameList, initialText)                                     # テーブル名選択コンボボックスセット
            pass

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   ファイルテーブル名リストを返す
    #---------------------------------------------------------------------------------------------------
    def getFileTableList(self, SOURCE):
        try:
            SOURCE_CLASS_LIST = GP.SVR.SOURCE_CLASS[SOURCE]                                             # 選択ソース名からGP.CONTのソースリストを取得する
            fileTableList = []                                                                          # テーブルリストを初期化
            for SOURCE_CLASS in SOURCE_CLASS_LIST:                                                      # ソースリストをすべて実行
                objctList = SOURCE_CLASS.objectList                                                     # オブジェクトテーブル名リストを取得
                for object in objctList:                                                                # オブジェクトリストをすべて実行
                    inputDir = GP.UPLOADDIR + object.DBSDIR + "/" + SOURCE + "/"                        # ターゲットディレクトリを返す
                    files = os.listdir(inputDir)                                                        # ファイル名リスト取得
                    files = [var for var in files if ".log" in var]                                     # テーブル名リストを取得
                    files = [var.replace(".log","") for var in files]                                   # テーブル名リストを取得
                    files = [var for var in files if var == object.TABLE_NAME]                          # テーブル名リストを取得
                    fileTableList += files                                                              # テーブル名リストに追加
            if len(fileTableList) > 0:                                                                  # テーブルリストが有る時
                fileTableList = np.array(fileTableList)                                                 # numpy配列化
                return fileTableList                                                                    # テーブルリストを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   CSVからローカルDBサーバーに書き込み
    #---------------------------------------------------------------------------------------------------
    def csvToDb(self, object, SERVER, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            if self.isDBS(SERVER):                                                                      # サーバータイプがDBサーバーの時
                GP.SVR.DBSServer.makeDBFromObjectFile(SERVER, object, p)                                # オブジェクトファイルからDBを作成
            elif self.isSSH(SERVER):                                                                    # サーバータイプがSSHサーバーの時
                GP.SVR.SSHServer.CSV_TO_DB(SERVER, object, p)                                           # オブジェクトファイルからDBを作成
            self.endLevel(p)                                                                            # 現レベルの終了
            pass

        except Exception as e:                                                                          # 例外                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            pass


