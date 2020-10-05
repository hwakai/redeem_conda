import os
import numpy as np
import math
import csv
from staticImport import *
from PyQt5Import import *
from gpiBase import *
from classDef import DataTransParameterClass
import MySQLdb as connector


# =======================================================================================================
#   スーパークラス ServerBaseClass
# =======================================================================================================
class ServerBaseClass(GpiBaseClass):
    def __init__(self):  # 初期化
        try:
            GpiBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.SERVER = None  # サーバー初期化
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   サーバー変数をセットする
    # ---------------------------------------------------------------------------------------------------
    def setServer(self, SERVER):
        try:
            GP.SVR.parameter[SERVER].setClassVar(self)  # サーバー変数セット

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   DBのテーブル作成
    # ---------------------------------------------------------------------------------------------------
    def createDBTable(self, SERVER, object, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            td = object.tableDesc  # テーブルデスクリプションを転写
            TABLE_NAME = object.PREFIX + object.TABLE_NAME  # 前置句を付けたテーブル名をセット
            columnNr = td.columnNr  # コラム数
            query = QueryClass()  # ベースクエリを転写
            query.add("create table " + TABLE_NAME + "(")  # クエリー作成
            PRIMARY = []  # プライマリーキーをヌルにする
            for column in range(columnNr):  # コラム数をすべて実行
                COLUMN_NAME = td.colName[column]  # NAMEを取得
                COLUMN_TYPE = td.colType[column]  # TYPEを取得
                IS_NULLABL = td.isNullable[column]  # IS_NULLABLを取得
                COLUMN_KEY = td.colKey[column]  # KEYを取得
                if IS_NULLABL == "YES":  # IS_NULLABLが"YES"の時
                    query.add(COLUMN_NAME + " " + COLUMN_TYPE + ",")  # クエリーにNAMEとTYPEを追加
                else:  # IS_NULLABLが"YES"でない時
                    query.add(COLUMN_NAME + " " + COLUMN_TYPE + " NOT NULL,")  # クエリーにNAMEとTYPEとNOT NULLを追加
                if COLUMN_KEY == "PRI":  # COLUMN_KEYが"PRI"の時
                    PRIMARY += [COLUMN_NAME]  # PRIMARYにCOLUMN_NAMEを追加

            if len(PRIMARY) > 0:  # PRIMARYが有る時
                PRIMARY = ",".join(PRIMARY)  # PRIMARYを','でセパレートしたテキストに変換
                query.add("PRIMARY KEY(" + PRIMARY + "));")  # クエリーにPRIMARYを追加
            else:  # PRIMARYが無い時
                query.queryList[-1] = query.queryList[-1][:-1] + ");"  # 最後の','を削除して);を加える

            channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
            cursor.execute("SET FOREIGN_KEY_CHECKS=0")  # 外部参照チェックをしない
            cursor.execute("drop table if exists " + TABLE_NAME)  # テーブルが有ったら削除
            query.execute(cursor)  # クエリを実行する
            channel.commit()  # 書き込みコミット
            channel.close()  # DBを閉じる
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   テーブルの有無を返す
    # ---------------------------------------------------------------------------------------------------
    def existsTable(self, SERVER, object):
        try:
            if object.TABLE_NAME is not None:  # テーブル名が有る時
                channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
                if cursor is not None:  # カーソルが有る時
                    query = QueryClass2("SHOW TABLES")  # クエリー作成
                    query.execute(cursor)  # クエリを実行する
                    description = cursor.fetchall()  # すべて読み込む
                    description = np.array(description, 'O').reshape(-1)  # 一次元のnumpy配列化
                    description = [desc.upper() for desc in description]  # すべてアッパーに修正
                    description = np.array(description, 'O')  # 一次元のnumpy配列化
                    channel.close()  # DBをクローズ
                    if len(description) > 0:  # テーブル名リストが有る時
                        TABLE_NAME = object.PREFIX + object.TABLE_NAME  # 前置句を付けたテーブル名をセット
                        description = description[description == TABLE_NAME.upper()]  # 完全に一致するテーブル名のリスト
                        if len(description) > 0:  # テーブル名が有る時
                            return True  # 真を返す
            return False  # 偽を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return False  # 偽を返す

    # ---------------------------------------------------------------------------------------------------
    #  行数を取得
    # ---------------------------------------------------------------------------------------------------
    def getCount(self, SERVER, object, p=None):
        try:
            self.startNewLevel(p)  # 計測開始時間セット
            if self.existsTable(SERVER, object):  # DBにテーブルが有る時
                channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
                TABLE_NAME = object.PREFIX + object.TABLE_NAME  # 前置句を付けたテーブル名をセット
                query = QueryClass()  # クエリを生成
                query.add("SELECT count(*) FROM " + TABLE_NAME)  # クエリを生成
                query.execute(cursor)  # クエリを実行する
                dataList = cursor.fetchall()  # すべて行読み込む
                channel.close()  # DBクローズ
                if len(dataList) > 0:  # レーザーリストが有る時
                    count = dataList[0][0]  # カウント取得
                    emit(p)  # 進捗バーにシグナルを送る
                    return self.returnData(count)  # 実行時間を表示してからデータを返す
            emit(p)  # 進捗バーにシグナルを送る
            return self.returnData(0)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return 0  # 0を返す

    # ---------------------------------------------------------------------------------------------------
    #   指定したレーザーIDとエラーコードの説明文を取得
    # ---------------------------------------------------------------------------------------------------
    def getDescription(self, laserId, errorCode):
        try:
            ERM = GP.CONT.COMB.ERM  # ERMの転写
            if self.existsTable(GP.SERVER.LOC_RDM_DBS, ERM):  # テーブルが有る時
                errorCode = "'" + errorCode + "'"  # エラーコードをストリングにする
                laserId = str(laserId)  # レーザーIDをストリングにする
                channel, cursor = self.DBSServer.openLocServer()  # DBをオープンする
                # データ読み込み
                query = QueryClass2("select DISTINCT DESCRIPTION FROM " + GP.CONT.COMB_TABLE.ERM)  # クエリー作成
                query.add("where LASER_ID = " + laserId)  # クエリー作成
                query.add("and ERROR_CODE = " + errorCode)  # クエリー作成
                query.execute(cursor)  # クエリを実行する
                description = cursor.fetchall()  # すべて読み込む
                channel.close()  # DBをクローズ
                if len(description) > 0:  # 説明文が有る時
                    return description[0][0]  # 説明文を返す
            return ""  # 空文を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return ""  # 空文を返す

    # ---------------------------------------------------------------------------------------------------
    #   テーブル名リストをDBから作る
    # ---------------------------------------------------------------------------------------------------
    def makeTableNameList(self, SERVER):
        try:
            channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
            if cursor is not None:
                query = QueryClass2("show tables")  # クエリー作成
                query.execute(cursor)  # クエリを実行する
                # テーブルセット
                tableNameList = cursor.fetchall()  # すべて読み込む
                channel.close()  # DBをクローズ
                if len(tableNameList) > 0:  # テーブル名リストが有る時
                    tableNameList = [name[0].upper() for name in tableNameList]  # アッパーケースにする
                    tableNameList = np.array(tableNameList)  # numpy配列化
                    return tableNameList  # テーブル名リストを返す
            return None

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   テーブルの最新のN行を削除する
    # ---------------------------------------------------------------------------------------------------
    def deleteTableRows(self, SERVER, object, rows, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if self.existsTable(SERVER, object):  # テーブルが有る時
                if object.DATE_FIELD != "":  # 日付フィールドが有る時
                    TABLE_NAME = object.PREFIX + object.TABLE_NAME  # 前置句を付けたテーブル名をセット
                    query = QueryClass2("DELETE FROM " + TABLE_NAME)  # クエリー作成
                    query.add("ORDER BY " + object.DATE_FIELD + " DESC")  # ORDER BY
                    query.add("LIMIT " + str(rows))  # LIMIT
                channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
                query.execute(cursor)  # クエリを実行する
                channel.commit()  # 書き込みコミット
                channel.close()  # DBクローズ
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   テーブルに含まれるレーザーIDリスト作成
    # ---------------------------------------------------------------------------------------------------
    def getLaserIdList(self, SERVER, object, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            if self.existsTable(SERVER, object):                                                        # テーブルとレーザーリストが有る時
                channel, cursor = self.openServer(SERVER)                                               # サーバーをオープンしてチャンネルとcursorを取得
                if cursor is not None:                                                                  # カーソルが有る時
                    TABLE_NAME = object.PREFIX + object.TABLE_NAME                                      # 前置句を付けたテーブル名をセット
                    query = QueryClass2("SELECT DISTINCT LASER_ID FROM " + TABLE_NAME)                  # クエリー作成
                    query.execute(cursor)                                                               # クエリを実行する
                    laserIdList = cursor.fetchall()                                                     # すべて読み込む
                    laserIdList = np.unique(laserIdList)
                    channel.close()                                                                     # DBクローズ
                    return self.returnList(laserIdList, p)                                              # 実行時間を表示してからデータを返す
            return self.returnNone(p)                                                                   # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # 例外を表示
            return None                                                                                 # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   レーザーID毎の最終書き込み日時のレーザー辞書を取得する
    # ---------------------------------------------------------------------------------------------------
    def getLatestDic(self, SERVER, object, filterList, p=None):
        try:
            if filterList is not None:  # レーザーリストが有る時
                self.startNewLevel(len(filterList), p)  # 新しいレベルの進捗開始
                if self.existsTable(SERVER, object):  # DBにテーブルが有る時
                    dateField = object.DATE_FIELD  # 日付フィールド取得
                    baseQuery = QueryClass2("SELECT DISTINCT")  # SELECT
                    baseQuery.add("LASER_ID," + dateField)  # SELECT
                    TABLE_NAME = object.PREFIX + object.TABLE_NAME  # 前置句を付けたテーブル名をセット
                    baseQuery.add("FROM " + TABLE_NAME)  # FROM
                    laserDic = {}  # レーザー辞書初期化
                    channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
                    for LASER_ID in filterList:  # レーザーIDリストをすべて実行
                        query = CopyQueryClass(baseQuery)  # ベースクエリを転写
                        query.add("WHERE LASER_ID = " + str(LASER_ID))  # WHERE
                        query.add("ORDER BY " + dateField + " DESC")  # ORDER
                        query.add("LIMIT 1")  # LIMIT
                        query.execute(cursor)  # クエリを実行する
                        dataList = cursor.fetchall()  # すべて読み込みリストにする
                        if len(dataList) > 0:  # データリストが有る時
                            laserDic[LASER_ID] = dataList  # レーザー辞書に追加
                        emit(p)  # 進捗バーにシグナルを送る
                    channel.close()  # DBクローズ
                    return self.returnList(laserDic, p)  # 実行時間を表示してからデータを返す
            emit(p)  # 進捗バーにシグナルを送る
            return self.returnNone()  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   最終書き込み日時を取得する
    # ---------------------------------------------------------------------------------------------------
    def getLatestDateTime(self, SERVER, object, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if self.existsTable(SERVER, object):  # DBにテーブルが有る時
                latestDateTime = None  # レーザー辞書初期化
                dateField = "BASE." + object.DATE_FIELD  # 日付フィールド取得
                query = QueryClass("SELECT DISTINCT")  # SELECT
                query.add(dateField)  # FIELD
                TABLE_NAME = object.PREFIX + object.TABLE_NAME  # 前置句を付けたテーブル名をセット
                query.add("FROM " + TABLE_NAME + " BASE")  # FROM
                query.add("ORDER BY " + dateField + " DESC")  # ORDER
                query.add("LIMIT 1")  # LIMIT
                channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
                query.execute(cursor)  # クエリを実行する
                dataList = cursor.fetchall()  # すべて読み込みリストにする
                if len(dataList) > 0:  # データリストが有る時
                    latestDateTime = dataList[0][0]  # 最終書き込み日時をセット
                channel.close()  # DBクローズ
                return self.returnData(latestDateTime, p)  # 実行時間を表示してからデータを返す
            return self.returnNone(p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   保存データをDBにセーブ
    # ---------------------------------------------------------------------------------------------------
    def saveBaseData(self, SERVER, object, baseType, p=None):
        try:
            self.startNewLevel(3, p)  # 新しいレベルの進捗開始
            if GP.SVR.FILEServer.saveToCsvFile(object.targetPath, object, baseType, p):  # レーザー辞書をファイルに書き込む
                self.createDBTable(SERVER, object, p)  # テーブル作成
                self.objectFileToDB(SERVER, object, p)  # ファイルをDBに書き込む
                return self.returnResult(True, p)  # 実行時間を表示してから結果を返す
            return self.returnResult(False, p)  # 実行時間を表示してから結果を返す

        except Exception as e:  # 例外
            return self.returnResultError(e, p)  # エラーを表示してからFalseを返す

    # ---------------------------------------------------------------------------------------------------
    #  オブジェクトファイルからローカルDBのテーブル作成（項目修正有り）
    # ---------------------------------------------------------------------------------------------------
    def objectFileToLoaclDB(self, object, p=None):
        try:
            logPath = object.targetPath  # ファイルパス
            self.fileToDB(GP.SERVER.LOC_RDM_DBS, object, logPath, p)

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #  オブジェクトファイルからDBのテーブル作成
    # ---------------------------------------------------------------------------------------------------
    def objectFileToDB(self, SERVER, object, p=None):
        try:
            logPath = object.targetPath  # オブジェクトファイルパス
            self.fileToDB(SERVER, object, logPath, p)  # 指定したパスのオブジェクトファイルからDBのテーブル作成

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #  ファイル行数を取得
    # ---------------------------------------------------------------------------------------------------
    def getFileRows(self, logPath):
        try:
            size = os.path.getsize(logPath)
            if size > 10000000:
                texts = 0  # テキスト数を初期化
                with open(file=logPath, mode="r", encoding="utf-8") as readFile:  # "utf-8"でファイルをオープン
                    readFile.readline()  # 一行読み込み
                    for i in range(100):
                        texts += len(readFile.readline())
                    rows = int(size / texts * 100)
            else:
                with open(file=logPath, mode="r", encoding="utf-8") as readFile:  # "utf-8"でファイルをオープン
                    rows = len(readFile.readlines()) - 1  # ファイル行数を取得する
            return rows

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #  指定したパスのオブジェクトファイルからDBのテーブル作成
    # ---------------------------------------------------------------------------------------------------
    def fileToDB(self, SERVER, object, logPath, p=None):
        try:
            tempPath = object.targetTempPass  # テンポラリーパス
            dirName = os.path.dirname(tempPath)  # ディレクトリ名
            if not os.path.exists(dirName):  # ディレクトリの有無を確認
                os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
            rows = self.getFileRows(logPath)  # ファイル行数を取得
            block = self.getFileBlock(object)  # ファイルブロック長を取得
            blocks = math.ceil(rows / block)  # ブロック数
            self.startNewLevel(blocks, p)  # 新しいレベルの進捗開始
            query = self.makeFileToDBQuery(object, tempPath)  # クエリー作成
            with open(file=logPath, mode="r", encoding="utf-8") as readFile:  # "utf-8"でファイルをオープン
                rowData = readFile.readline()  # ヘッダー読み飛ばし
                for i in range(int(blocks * 1.2)):  # ブロックをすべて実行
                    dataList = [readFile.readline() for j in range(block)]  # ブロック長だけファイルから読み込む
                    dataList = np.array(dataList, 'O')  # numpy配列化
                    dataList = dataList[dataList != ""]  # 空白行を除く
                    if len(dataList) > 0:  # データリストが有る時
                        with open(file=tempPath, mode="w", encoding="utf-8") as writeFile:  # "utf-8"でファイルをオープン
                            writeFile.writelines(dataList)  # データリストをファイルに書き込む
                        self.deleteObject(dataList)  # オブジェクトを削除してメモリーを解放する
                        channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
                        query.execute(cursor)  # クエリを実行する
                        channel.commit()  # 書き込みコミット
                        channel.close()  # DBを閉じる
                        os.remove(tempPath)  # 一時ファイル削除
                    emit(p)  # 進捗バーにシグナルを送る
            self.endLevel(p)  # 現レベルの終了
            pass

        except Exception as e:  # 例外
            self.showError(e, p)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #  オリジナルからDB作成（項目修正有り）
    # ---------------------------------------------------------------------------------------------------
    def makeFileToDBQuery(self, object, logPath):
        try:
            tableDesc = object.tableDesc  # テーブルデスクリプションを転写
            TABLE_NAME = object.PREFIX + object.TABLE_NAME  # 前置句を付けたテーブル名をセット
            # *******************************************************************************************
            # load data infile
            # *******************************************************************************************
            query = QueryClass()  # クエリー作成
            query.add("load data infile '" + logPath + "' IGNORE into table " + TABLE_NAME)  # クエリー作成
            query.add("character set utf8")  # クエリー作成
            query.add("fields terminated by '\\t'")  # クエリー作成
            query.add("lines terminated by " + GP.SEP_CRLF)  # クエリー作成
            query.add(tableDesc.getAtColumnName())  # ＠付きのカラム名ストリングをクエリーに追加
            # *******************************************************************************************
            # set
            # *******************************************************************************************
            query.add("set")  # クエリー作成
            for column in range(tableDesc.columnNr):  # コラム数をすべて実行
                COLUMN_NAME = tableDesc.colName[column]  # コラム名を取得
                COLUMN_TYPE = tableDesc.colType[column]  # コラムタイプを取得
                ATCOLUMN_NAME = "@" + COLUMN_NAME  # クエリーに仮コラム名追加
                func = "nullif(" + "nullif(" + ATCOLUMN_NAME + ",'NULL'),'')"  # ファンクション
                if "char" in COLUMN_TYPE:  # COLUMN_TYPEに"char"が有る時
                    func = "replace(" + func + "," + '"' + "'" + '"' + "," + '"' + '"' + ")"
                elif "text" in COLUMN_TYPE:
                    func = "replace(" + func + "," + '"' + "'" + '"' + "," + '"' + '"' + ")"
                else:
                    pass
                query.add(COLUMN_NAME + " = " + func + ",")  # クエリーを加える
            query.queryList[-1] = query.queryList[-1][:-1]  # 最後の','を削除する
            return query  # クエリーを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   クエリーからCSVファイルを作成する。フィルターをかけるか否かで分ける
    # ---------------------------------------------------------------------------------------------------
    def makeFileFromDB(self, SERVER, object, p=None):
        try:
            if self.existsTable(SERVER, object):  # DBにテーブルが有る時
                baseQuery = self.makeObjectQuery(object)  # オブジェクトのフィールド名からセレクトクエリーを作成
                return self.makeCsvFileFromQuery(SERVER, object, baseQuery, p)  # クエリーからCSVファイルを作成する

        except Exception as e:  # 例外
            return False  # 偽を返す

    # ---------------------------------------------------------------------------------------------------
    #   クエリーからCSVファイルを作成する。フィルターをかけるか否かで分ける
    # ---------------------------------------------------------------------------------------------------
    def makeFilterFileFromDB(self, SERVER, object, filterList, p=None):
        try:
            if self.existsTable(SERVER, object):  # DBにテーブルが有る時
                baseQuery = self.makeObjectQuery(object)  # オブジェクトのフィールド名からセレクトクエリーを作成
                if filterList is not None and "LASER_ID" in object.tableDesc.colName:  # フィルターリストが有りかつLASER_IDが有る時
                    return self.makeFilterCsvFileFromQuery(SERVER, object, baseQuery, filterList,
                                                           p)  # クエリーからフィルタをかけたCSVファイルを作成する
                else:  # フィルターリストが有る時
                    return self.makeCsvFileFromQuery(SERVER, object, baseQuery, p)  # クエリーからCSVファイルを作成する

        except Exception as e:  # 例外
            return False  # 偽を返す
            pass

    # ---------------------------------------------------------------------------------------------------
    #   クエリーからCSVファイルを作成する　0.8秒
    # ---------------------------------------------------------------------------------------------------
    def makeCsvFileFromQuery(self, SERVER, object, query, p=None):
        try:
            written = False                                                                             # 書き込みフラグを初期化
            logPath = object.targetPath                                                                 # ファイルパス
            dirName = os.path.dirname(logPath)                                                          # ディレクトリ名
            if not os.path.exists(dirName):                                                             # ディレクトリの有無を確認
                os.makedirs(dirName)                                                                    # 途中のディレクトリを含めてディレクトリを作成
            with open(file=logPath, mode="w", encoding="utf-8") as f:                                   # "utf-8"でファイルをオープン
                writer = csv.writer(f, delimiter="\t", lineterminator='\n')                             # テーブルデスクリプションを書き込む
                writer.writerow(object.tableDesc.colName)                                               # CSVライター設定
                channel, cursor = self.openServer(SERVER)                                               # サーバーをオープンしてチャンネルとcursorを取得
                if cursor is not None:                                                                  # カーソルが有る時
                    query.execute(cursor)                                                               # クエリを実行する
                    count = cursor.rowcount                                                             # 行数取得
                    block = self.getFileBlock(object)                                                   # ファイルブロック長を取得
                    blocks = math.ceil(count / block)                                                   # ブロック数
                    self.startNewLevel(blocks, p)                                                       # 新しいレベルの進捗開始
                    dataList = cursor.fetchmany(block)                                                  # block行読み込む
                    while len(dataList) > 0:                                                            # データリストが有る時
                        dataList = np.array(dataList, 'O')                                              # numpy配列化
                        if len(dataList) > 0:                                                           # データリストが有る時
                            writer.writerows(dataList)                                                  # レーザーIDデータ書き込み
                            written = True                                                              # 書き込み完了フラグを真にする
                            self.deleteObject(dataList)                                                 # メモリーを解放
                        dataList = cursor.fetchmany(block)                                              # block行読み込む
                        emit(p)                                                                         # 進捗バーにシグナルを送る
                    channel.クローズ
                return self.returnResultclose()                                                         # DB(True, p)  # 実行時間を表示してから結果を返す
            emit(p)                                                                                     # 進捗バーにシグナルを送る
            return self.returnResult(False)                                                             # 実行時間を表示してから結果を返す

        except Exception as e:                                                                          # 例外
            return self.returnResultError(e, p)                                                         # エラーを表示してからFalseを返す

    # ---------------------------------------------------------------------------------------------------
    #   DBからフィルターをかけたCSVファイルを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeFilterCsvFileFromQuery(self, SERVER, object, baseQuery, filterList, p=None):
        try:
            if object.TABLE_NAME == GP.CONT.ERR.TABLE_NAME:                                             # テーブル名がERRORの時
                addQuery = self.makeGrErrorQuery(GP.GR_ERR_LIST)                                        # グループエラークエリ作成
                return self.makeFilterCsvFileFromQuerySub(SERVER, object, baseQuery, addQuery, filterList,
                                                          p)                                            # DBサーバーからCSVファイルを作る
            else:  # テーブル名がERROR以外の時
                return self.makeFilterCsvFileFromQuerySub(SERVER, object, baseQuery, None, filterList,
                                                          p)                                            # DBサーバーからCSVファイルを作る

        except Exception as e:                                                                          # 例外
            return self.returnResultError(e, p)                                                         # エラーを表示してからFalseを返す

    # ---------------------------------------------------------------------------------------------------
    #   DBからフィルターをかけたCSVファイルを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeFilterCsvFileFromQuerySub(self, SERVER, object, baseQuery, addQuery, filterList, p=None):
        try:
            strPath = object.targetPath  # ファイルパス
            dirName = os.path.dirname(strPath)  # ディレクトリ名
            if not os.path.exists(dirName):  # ディレクトリの有無を確認
                os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
            rows = len(filterList)  # レーザーID数
            block = self.getLaserBlock(object)  # ファイルブロック長を取得
            blocks = math.ceil(rows / block)  # ブロック数
            self.startNewLevel(blocks, p)  # 新しいレベルの進捗開始
            channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
            # CSV を作成
            written = False  # 書き込みフラグを初期化
            with open(file=strPath, mode="w", encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                writer = csv.writer(f, delimiter="\t", lineterminator='\n')  # CSVライター設定
                writer.writerow(object.tableDesc.colName)  # テーブルデスクリプションを書き込む
                filterList = np.array(filterList)
                for i in range(blocks):  # ブロックをすべて実行
                    partList = filterList[block * i:(block) * (i + 1)]  # 部分フィルタ作成
                    whereQuery = self.makeFilterQuery(partList)  # フィルタクエリ作成
                    whereQuery.add(addQuery)  # グループエラークエリ作成
                    query = baseQuery.insertWhereQuery(whereQuery)  # WHEREクエリー挿入
                    query.execute(cursor)  # クエリを実行する
                    dataList = cursor.fetchall()  # すべて読み込む
                    if len(dataList) > 0:  # データリストが有る時
                        writer.writerows(dataList)  # レーザーIDデータ書き込み
                        written = True  # 書き込み完了フラグを真にする
                        self.deleteObject(dataList)  # メモリーを解放
                    emit(p)  # 進捗バーにシグナルを送る
            channel.close()  # DBクローズ
            return self.returnResult(written, p)  # 実行時間を表示してから結果を返す

        except Exception as e:  # 例外
            return self.returnResultError(e, p)  # エラーを表示してからFalseを返す

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトからクエリーを使ってレーザーIDリストに有るレーザー辞書を読み込む。
    #   filterListがNoneの時はすべて読み込む
    # ---------------------------------------------------------------------------------------------------
    def makeFilterLaserDicFromQuery(self, SERVER, object, baseQuery, filterList, p=None):
        try:
            self.startNewLevel(2, p)                                                                    # 新しいレベルの進捗開始
            flatList = self.makeFilterFlatListFromQuery(SERVER, object, baseQuery, filterList, p)       # クエリーからフラットリストを作成する
            if flatList is not None:
                laserIndex = np.unique(flatList[:, object.LASER_ID])                                    # レーザーインデックスを取得
                self.startNewLevel(len(laserIndex), p)                                                  # 新しいレベルの進捗開始
                laserDic = {}                                                                           # レーザー辞書を初期化
                for laserId in laserIndex:                                                              # レーザーンデックスをすべて実行
                    laserData = flatList[flatList[:, object.LASER_ID] == laserId]                       # レーザーデータを取得
                    if len(laserData) > 0:                                                              # データリストが有る時
                        laserDic[laserId] = laserData                                                   # オブジェクトタイプのNUMPY配列に変換してレーザー辞書に格納
                    emit(p)                                                                             # 進捗バーにシグナルを送る
                self.endLevel(p)                                                                        # 現レベルの終了
                return self.returnList(laserDic, p)                                                     # 実行時間を表示してからデータを返す
            return self.returnNone(p)                                                                   # Noneを表示してからNoneを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトからクエリーを使ってレーザーIDリストに有るピリオッド辞書を読み込む。
    #   filterListがNoneの時はすべて読み込む
    #---------------------------------------------------------------------------------------------------
    def makePeriodDicFromQuery(self, SERVER, object, baseQuery, p=None):
        try:
            self.startNewLevel(2, p)                                                                    # 新しいレベルの進捗開始
            flatList = self.makeFlatListFromQuery(SERVER, object, baseQuery, p)                         # クエリーからフラットリストを作成する
            if flatList is not None:                                                                    # フラットリストが有る時
                periodIndex = np.array(flatList[:,[object.LASER_ID,object.PERIOD]],'int')               # ピリオッドインデックスを取得
                periodIndex = np.unique(periodIndex, axis=0)                                            # ユニークにする
                self.startNewLevel(len(periodIndex), p)                                                 # 新しいレベルの進捗開始
                periodDic = {}                                                                          # ピリオッド辞書を初期化
                for laserId, period in periodIndex:                                                     # レーザーリストをすべて実行
                    periodData = flatList[(flatList[:,object.LASER_ID] == laserId) &
                                            (flatList[:,object.PERIOD] == period)]                      # ピリオッドデータを抽出
                    if len(periodData) > 0:                                                             # ピリオッドデータが有る時
                        periodDic[laserId, period] = periodData                                         # ピリオッド辞書に登録
                    emit(p)                                                                             # 進捗バーにシグナルを送る
                self.endLevel(p)                                                                        # 現レベルの終了
                return self.returnList(periodDic, p)                                                    # 実行時間を表示してからデータを返す
            return self.returnNone(p)                                                                   # Noneを表示してからNoneを返す

        except Exception as e:                                                                          # 例外 
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトからクエリーを使ってレーザーIDリストに有るピリオッド辞書を読み込む。
    #   filterListがNoneの時はすべて読み込む
    #---------------------------------------------------------------------------------------------------
    def makeFilterPeriodDicFromQuery(self, SERVER, object, baseQuery, filterList, p=None):
        try:
            self.startNewLevel(2, p)                                                                    # 新しいレベルの進捗開始
            flatList = self.makeFilterFlatListFromQuery(SERVER, object, baseQuery, filterList, p)       # クエリーからフラットリストを作成する
            if flatList is not None:                                                                    # フラットリストが有る時
                periodIndex = np.array(flatList[:,[object.LASER_ID,object.PERIOD]],'int')               # ピリオッドインデックスを取得
                periodIndex = np.unique(periodIndex, axis=0)                                            # ユニークにする
                self.startNewLevel(len(periodIndex), p)                                                 # 新しいレベルの進捗開始
                periodDic = {}                                                                          # ピリオッド辞書を初期化
                for laserId, period in periodIndex:                                                     # レーザーリストをすべて実行
                    periodData = flatList[(flatList[:,object.LASER_ID] == laserId) &
                                            (flatList[:,object.PERIOD] == period)]                      # ピリオッドデータを抽出
                    if len(periodData) > 0:                                                             # ピリオッドデータが有る時
                        periodDic[laserId, period] = periodData                                         # ピリオッド辞書に登録
                    emit(p)                                                                             # 進捗バーにシグナルを送る
                self.endLevel(p)                                                                        # 現レベルの終了
                return self.returnList(periodDic, p)                                                    # 実行時間を表示してからデータを返す
            return self.returnNone(p)                                                                   # Noneを表示してからNoneを返す

        except Exception as e:                                                                          # 例外 
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   クエリーからフラットリストを作成する。DB読み込みのベースメソッド
    # ---------------------------------------------------------------------------------------------------
    def makeFlatListFromQuery(self, SERVER, object, query, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
            query.execute(cursor)  # クエリを実行する
            dataList = cursor.fetchall()  # すべて行読み込む
            channel.close()  # DBをクローズ
            dataList = np.array(dataList, 'O')  # NUMPY配列化
            return self.returnList(dataList, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   指定したDBからクエリーを使ってフラットリストを作成する。DB読み込みのベースメソッド
    # ---------------------------------------------------------------------------------------------------
    def makeFilterFlatListFromQuery(self, SERVER, object, baseQuery, filterList, p=None):
        try:
            rows = len(filterList)  # レーザーID数
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
            whereQuery = self.makeFilterQuery(filterList)  # WHEREクエリ作成
            query = baseQuery.insertWhereQuery(whereQuery)  # WHEREクエリー挿入
            query.execute(cursor)  # クエリを実行する
            laserList = cursor.fetchall()  # すべて読み込みリストにする
            channel.close()  # DBをクローズ
            laserList = np.array(laserList, 'O')  # NUMPY配列化
            return self.returnList(laserList, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   指定したDBからクエリーを使ってフラットリストを作成する。DB読み込みのベースメソッド
    # ---------------------------------------------------------------------------------------------------
    def makeFilterFlatListFromQueryBlock(self, SERVER, object, baseQuery, filterList, p=None):
        try:
            rows = len(filterList)  # レーザーID数
            block = self.getLaserBlock(object)  # ファイルブロック長を取得
            blocks = math.ceil(rows / block)  # ブロック数
            self.startNewLevel(blocks, p)  # 新しいレベルの進捗開始
            channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
            filterList = np.array(filterList)  # numpy配列化
            laserList = []  # ブロックリスト初期化
            for i in range(blocks):  # ブロックをすべて実行
                partList = filterList[block * i:(block) * (i + 1)]  # 部分フィルタ作成
                whereQuery = self.makeFilterQuery(partList)  # フィルタクエリ作成
                query = baseQuery.insertWhereQuery(whereQuery)  # WHEREクエリー挿入
                query.execute(cursor)  # クエリを実行する
                blockList = cursor.fetchall()  # すべて読み込む
                if len(blockList) > 0:  # ブロックリストが有る時
                    laserList += list(blockList)  # レーザーリストに抽出データを追加
                    self.deleteObject(blockList)  # メモリーを解放
                emit(p)  # 進捗バーにシグナルを送る
            channel.close()  # DBをクローズ
            laserList = np.array(laserList, 'O')  # NUMPY配列化
            return self.returnList(laserList, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   クエリーからフィルターをかけたDBを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeFilterDBFromQuery(self, SERVER, object, query, filterList, p=None):
        try:
            self.startNewLevel(2, p)  # 新しいレベルの進捗開始
            if self.makeFilterCsvFileFromQuery(SERVER, object, query, filterList, p):  # クエリーからフィルタをかけたCSVファイル作成に成功した時
                self.makeDBFromObjectFile(SERVER, object, p)  # オブジェクトファイルからローカルDBを作成
                return self.returnResult(True, p)  # 実行時間を表示してから結果を返す
            return self.returnResult(False, p)  # 実行時間を表示してから結果を返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   クエリーからDBを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeDBFromQuery(self, SERVER, object, query, p=None):
        try:
            self.startNewLevel(2, p)  # 新しいレベルの進捗開始
            if self.makeCsvFileFromQuery(SERVER, object, query, p):  # クエリーからCSVファイル作成に成功した時
                self.makeDBFromObjectFile(SERVER, object, p)  # オブジェクトファイルからローカルDBを作成
                return self.returnResult(True, p)  # 実行時間を表示してから結果を返す
            return self.returnResult(False, p)  # 実行時間を表示してから結果を返す

        except Exception as e:  # 例外
            return self.returnResultError(e, p)  # エラーを表示してからFalseを返す

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトファイルからDBを作成
    # ---------------------------------------------------------------------------------------------------
    def makeDBFromObjectFile(self, SERVER, object, p=None):
        try:
            self.startNewLevel(2, p)  # 新しいレベルの進捗開始
            self.createDBTable(SERVER, object, p)  # テーブル作成
            self.objectFileToDB(SERVER, object, p)  # ファイルをDBに書き込む
            self.endLevel(p)  # 現レベルの終了
            pass

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   レーザー単位の追加ファイルを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeLaserAddFile(self, SERVER, object, incPath, filterList, latestDateList, p=None):
        try:
            dirName = os.path.dirname(incPath)  # ディレクトリ名
            if not os.path.exists(dirName):  # ディレクトリの有無を確認
                os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
            if self.existsTable(SERVER, object):  # DBにテーブルが有る時
                dateField = object.DATE_FIELD  # 日付フィールド取得
                baseQuery = self.makeObjectQuery(object)  # オブジェクトのフィールド名からセレクトクエリーを作成
                rows = len(filterList)  # レーザーID数
                self.startNewLevel(rows, p)  # 新しいレベルの進捗開始
                channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
                written = False  # 書き込みフラグをセット
                with open(file=incPath, mode="w", encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                    writer = csv.writer(f, delimiter="\t", lineterminator='\n')  # CSVライター設定
                    for LASER_ID in filterList:  # レーザーIDリストをすべて実行
                        if LASER_ID in latestDateList:  # 最終日時データが有る時
                            laserId, latestDateTime = latestDateList[LASER_ID][0]  # 最終日時データを取得
                            query = CopyQueryClass(baseQuery)  # ベースクエリを転写
                            query.add("WHERE LASER_ID = " + str(LASER_ID))  # WHERE
                            query.add("AND " + dateField + " > '" + str(latestDateTime) + "'")  # WHERE
                            query.execute(cursor)  # クエリを実行する
                            dataList = cursor.fetchall()  # すべて読み込みリストにする
                            if len(dataList) > 0:  # データリストが有る時
                                writer.writerows(dataList)  # データリストをまとめて書き込み
                                written = True  # 書き込みフラグをセット
                        else:  # 最終日付データが無い時
                            query = CopyQueryClass(baseQuery)  # ベースクエリを転写
                            query.add("WHERE LASER_ID = " + str(LASER_ID))  # WHERE
                            query.execute(cursor)  # クエリを実行する
                            dataList = cursor.fetchall()  # すべて読み込みリストにする
                            if len(dataList) > 0:  # データリストが有る時
                                writer.writerows(dataList)  # データリストをまとめて書き込み
                                written = True  # 書き込みフラグをセット
                        emit(p)  # 進捗バーにシグナルを送る
                channel.close()  # DBをクローズ
                return self.returnResult(written, p)  # 実行時間を表示してから結果を返す
            emit(p)
            return self.returnResult(None)  # Noneを表示してから結果を返す

        except Exception as e:  # 例外
            return self.returnResultError(e, p)  # エラーを表示してからFalseを返す

    # ---------------------------------------------------------------------------------------------------
    #   最終書き込み時刻から追加ファイルを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeAddFile(self, SERVER, object, incPath, latestDateTime, dateField, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            self.setServer(SERVER)  # サーバー変数をセットする
            dirName = os.path.dirname(incPath)  # ディレクトリ名
            if not os.path.exists(dirName):  # ディレクトリの有無を確認
                os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
            res = False  # dataListを返す
            if self.existsTable(SERVER, object):  # DBにテーブルが有る時
                dateField = object.DATE_FIELD  # 日付フィールド取得
                baseQuery = self.makeObjectQuery(object)  # オブジェクトのフィールド名からセレクトクエリーを作成
                channel, cursor = self.openServer(SERVER)  # サーバーをオープンしてチャンネルとcursorを取得
                latestDate = latestDateTime.date()  # 日にちを取得
                query = CopyQueryClass(baseQuery)  # ベースクエリを転写
                query.add("WHERE BASE." + dateField + " >= '" + str(latestDate) + "'")  # WHERE
                with open(file=incPath, mode="w", encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                    writer = csv.writer(f, delimiter="\t", lineterminator='\n')  # CSVライター設定
                    query.execute(cursor)  # クエリを実行する
                    dataList = cursor.fetchall()  # すべて読み込みリストにする
                    if len(dataList) > 0:  # データリストが有る時
                        writer.writerows(dataList)  # データリストをまとめて書き込み
                        res = True  # dataListを返す
                channel.close()  # DBをクローズ
            return self.returnResult(res, p)  # 実行時間を表示してから結果を返す

        except Exception as e:  # 例外
            return self.returnResultError(e, p)  # エラーを表示してからFalseを返す
