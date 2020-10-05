import inspect
import datetime
import time
import math
import gc
import numpy as np
from static import *
from PyQt5.QtWidgets import QWidget
from PyQt5Import import *

# =======================================================================================================
#   クラス　QueryClass
# =======================================================================================================
class QueryClass():
    def __init__(self):
        try:
            self.queryList = []  # クエリリスト初期化
            self.rows = 0  # コラム名初期化

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   指定した名前のコラム番号を返す
    # ---------------------------------------------------------------------------------------------------
    def initialize(self):
        try:
            self.queryList = []  # クエリリスト初期化
            self.rows = 0  # 行数初期化

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   クエリーを追加
    # ---------------------------------------------------------------------------------------------------
    def add(self, query):
        try:
            if query is not None:  # クエリーが有る時
                if type(query) == type([]):  # PYTHON配列の時
                    self.queryList += query  # リストをクエリリストに追加
                elif type(query) == type(''):  # ストリングの時
                    self.queryList += [query]  # テキストをクエリリストに追加
                elif type(query) == QueryClass:  # 配列の時
                    self.queryList += query.queryList  # クエリリストをクエリリストに追加
                elif type(query) == QueryClass2:  # QueryClass2の時
                    self.queryList += query.queryList  # クエリリストをクエリリストに追加
                elif type(query) == np.ndarray:  # numpy配列の時
                    self.queryList += list(query)  # numpy配列をクエリリストに追加
                self.rows += 1  # 行数加算

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   クエリを作成して返す
    # ---------------------------------------------------------------------------------------------------
    def getQuery(self):
        try:
            query = GP.CRLF.join(self.queryList)  # クエリ作成
            return query  # クエリを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   クエリーを実行する
    # ---------------------------------------------------------------------------------------------------
    def execute(self, cursor):
        try:
            query = GP.CRLF.join(self.queryList)  # クエリを作成
            cursor.execute(query)  # クエリーを実行する

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   WHEREクエリーをクエリーに追加する
    # ---------------------------------------------------------------------------------------------------
    def insertWhereQuery(self, whereQuery):
        try:
            inserted = False  # 挿入済フラグをリセット
            oldList = self.queryList  # クエリリストを転写
            self.queryList = []  # クエリリストを新規に初期化
            for line in oldList:  # リストをすべて実行
                line = line.upper()  # アッパーにする
                if ('GROUP BY ' in line or 'ORDER BY' in line or 'LIMIT ' in line[
                                                                             :6]) and inserted == False:  # GROUPかORDERかLIMITが有る時
                    self.add(whereQuery)  # WHEREクエリを追加
                    self.add(line)  # ラインを追加
                    inserted = True  # 挿入済フラグをセット
                else:  # GROUPかORDERかLIMIT以外の時
                    self.add(line)  # ラインを追加
            if inserted == False:  # 未挿入の場合
                self.add(whereQuery)  # WHEREクエリを追加
            newQuery = QueryClass()
            newQuery.queryList = self.queryList
            self.queryList = oldList
            return newQuery

        except Exception as e:  # 例外
            printError(e)  # エラー表示
            return None  # Noneを返す


# =======================================================================================================
#   クラス　QueryClass2
# =======================================================================================================
class QueryClass2(QueryClass):
    def __init__(self, query):
        try:
            QueryClass.__init__(self)  # スーパークラスの初期化
            self.add(query)  # クエリリスト初期化

        except Exception as e:  # 例外
            printError(e)  # 例外を表示


# =======================================================================================================
#   クラス　CopyQueryClass
# =======================================================================================================
class CopyQueryClass(QueryClass):
    def __init__(self, query):
        try:
            QueryClass.__init__(self)  # スーパークラスの初期化
            self.queryList = query.queryList.copy()  # クエリリスト初期化
            self.rows = query.rows  # コラム名初期化

        except Exception as e:  # 例外
            printError(e)  # 例外を表示


# =======================================================================================================
#   クラス　TableDescClass
# =======================================================================================================
class TableDescClass():
    def __init__(self):  # スーパークラスの初期化
        self.tableName = ""  # テーブル名初期化
        self.columnNr = 0  # コラム数初期化
        self.colName = []  # コラム名初期化
        self.colType = []  # コラムタイプ初期化
        self.isNullable = []  # isNullable初期化
        self.colKey = []  # コラムキー初期化
        self.colDefault = []  # コラムデフォールト初期化
        self.extra = []  # エクストラ初期化

    # ---------------------------------------------------------------------------------------------------
    #   カラムを追加する
    # ---------------------------------------------------------------------------------------------------
    def addColumn(self, v_colName, v_colType, v_isNullable, v_colKey, v_colDefault, v_extra):
        self.colName.append(v_colName)  # コラム名アペンド
        self.colType.append(v_colType)  # コラムタイプアペンド
        self.isNullable.append(v_isNullable)  # isNullableアペンド
        self.colKey.append(v_colKey)  # コラムキーアペンド
        self.extra.append(v_extra)  # エクストラアペンド
        self.columnNr = self.columnNr + 1  # コラム数更新　

    # ---------------------------------------------------------------------------------------------------
    #   descTableからすべてのカラムを追加する
    # ---------------------------------------------------------------------------------------------------
    def appendAllColumn(self, row):
        self.columnNr = self.columnNr + 1  # コラム数更新　
        self.tableName = row[0]  # コラム名アペンド
        self.colName.append(row[1])  # コラム名アペンド
        self.colType.append(row[2])  # コラムタイプアペンド
        self.isNullable.append(row[3])  # isNullableアペンド
        self.colKey.append(row[4])  # コラムキーアペンド
        self.colDefault.append(row[5])  # コラムデフォールトアペンド
        self.extra.append(row[6])  # エクストラアペンド

    # ---------------------------------------------------------------------------------------------------
    #   指定した名前のコラム番号を返す
    # ---------------------------------------------------------------------------------------------------
    def getColumnNo(self, name):
        try:
            if name in self.colName:  # 指定した名前がコラム名に有る時
                return self.colName.index(name)  # コラム番号を返す
            else:  # 指定した名前がコラム名に無い時
                return None  # Noneを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   指定した名前のコラムタイプを返す
    # ---------------------------------------------------------------------------------------------------
    def getColumnType(self, name):
        try:
            if name in self.colName:  # 指定した名前がコラム名に有る時
                index = self.colName.index(name)  # コラム番号を取得
                if index is not None:  # コラム番号が有る時
                    return self.colType[index]  # コラムタイプを返す
            else:
                return None

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   DBデータをデスクリプションの定義に従って配列にセットする
    # ---------------------------------------------------------------------------------------------------
    def getRowData(self, strLine):
        try:
            rowData = strLine.split("\t")  # 文字列をタブで分けて配列にする
            rowData = np.array(rowData, dtype='O')  # オブジェクトタイプのnumpy配列ににする
            for column in range(self.columnNr):  # コラムをすべて実行
                sdata = rowData[column]  # ストリングを取得
                COLUMN_TYPE = self.colType[column]  # コラムタイプを取得
                if "decimal" in COLUMN_TYPE:  # コラムタイプに"decimal"が有る時
                    sdata = float(sdata)  # floatに変換
                elif "int" in COLUMN_TYPE:  # コラムタイプに"int"が有る時
                    sdata = int(sdata)  # intに変換
                elif "bigint" in COLUMN_TYPE:  # コラムタイプに"bigint"が有る時
                    sdata = int(sdata)  # intに変換
                elif "float" in COLUMN_TYPE:  # コラムタイプに"float" in"が有る時
                    sdata = float(sdata)  # floatに変換
                elif "double" in COLUMN_TYPE:  # コラムタイプに"double"が有る時
                    sdata = float(sdata)  # floatに変換
                elif "date" in COLUMN_TYPE:  # コラムタイプに"date"が有る時
                    sdata = datetime.datetime.strptime(sdata, '%Y-%m-%d')  # datetimeに変換
                elif "datetime" in COLUMN_TYPE:  # コラムタイプに"datetime"が有る時
                    sdata = datetime.datetime.strptime(sdata, '%Y-%m-%d %H:%M')  # datetimeに変換
                else:  # その他の時
                    pass  # 何もしない
                rowData[column] = sdata  # 配列に変換した値をセット
            return rowData  # 配列を返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   カラム名ストリングを返す (field0,\r\nfield1,,\r\nfield2,...,\r\nfieldn)
    # ---------------------------------------------------------------------------------------------------
    def getColumnName(self, base):
        try:
            colName = np.array(self.colName, dtype='O')  # numpy配列化
            baseColName = base + '.' + colName  # 頭に'base.'を付加する
            return (","+GP.CRLF).join(baseColName)  # ,と改行で結合した文字列を返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   カラム名クエリを返す
    # ---------------------------------------------------------------------------------------------------
    def getColumnList(self, base):
        try:
            query = QueryClass()  # クエリ生成
            colName = np.array(self.colName, dtype='O')  # numpy配列化
            colName = base + '.' + colName  # 頭に'base.'を付加する
            colName[:-1] = colName[:-1] + ','  # 最後に','を付加する
            query.queryList = list(colName)  # クエリリストにセット
            return query  # クエリを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   カラム名クエリを返す
    # ---------------------------------------------------------------------------------------------------
    def getColumnList2(self):
        try:
            query = QueryClass()  # クエリ生成
            colName = np.array(self.colName, dtype='O')  # numpy配列化
            colName[:-1] = colName[:-1] + ','  # 最後に','を付加する
            query.queryList = list(colName)  # クエリリストにセット
            return query  # クエリを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ＠付きのカラム名ストリングを返す (@field0,\r\n@field1,,\r\n@field2,...,\r\n@fieldn)
    # ---------------------------------------------------------------------------------------------------
    def getAtColumnName(self):
        try:
            colName = np.array(self.colName, dtype='O')  # numpy配列化
            atColName = '@' + colName  # 頭に@を付加する
            return "(" + (","+GP.CRLF).join(atColName) + ")"  # ,と改行で結合して（）で囲んだ文字列を返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   colName = @colNam ストリングを返す (field0=@field0,\r\nfield1=@field1,\r\nfield2=@field2,..,\r\n,fieldn=@fieldn)
    # ---------------------------------------------------------------------------------------------------
    def getEqualAtColumnName(self):
        try:
            query = QueryClass()  # クエリ生成
            colName = np.array(self.colName, dtype='O')  # numpy配列化
            colName = colName + " = " + '@' + colName  # colName = @colNamに整形
            colName[:-1] += ','  # ,を追加
            return colName  # カラム配列を返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   カラム名リストを返す (base.field0 as field0,\r\n...,\r\nfieldn)
    # ---------------------------------------------------------------------------------------------------
    def getBaseColumnName(self, mergeTableDesc, base, skip):
        try:
            query = QueryClass()  # クエリ生成
            for i in range(self.columnNr):
                if i >= skip:  # 先頭のスキップ行数
                    name = self.colName[i]  # コラム名
                    colType = self.colType[i]  # コラムタイプ
                    if name in mergeTableDesc.colName:  # マージ先のコラム名リストに有る時
                        mergeColType = mergeTableDesc.getColumnType(name)  # マージ先のコラムタイプ
                        if not ('int' in colType):  # コラムタイプが整数でない時
                            if 'int' in mergeColType:  # マージ先のコラムタイプが整数の時
                                string = "CAST(" + base + "." + name + " as unsigned) as " + name  # unsignedに変換クエリー作成
                            else:  # コラムタイプが整数でない時
                                string = base + "." + name + " as " + name  # クエリー作成
                        else:  # コラムタイプが整数でない時
                            string = base + "." + name + " as " + name  # クエリー追加
                        query.add(string + ",")  # クエリー追加
            return query  # クエリー配列を返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示


# =======================================================================================================
#   スーパークラス　GPIベースクラス
# =======================================================================================================
class GpiBaseClass(QWidget):
    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, TABLE_NAME):
        try:
            QWidget.__init__(self, None)
            self.TABLE_NAME = TABLE_NAME  # テーブル名（学習データに関しては仮設定）
            self.DBSDIR = None  # データベース名初期化
            self.SOURCE = None  # ソース名初期化
            self.FILE_BLOCK = None  # ファイルブロック長セット
            self.LASER_BLOCK = None  # レーザーブロック長セット
            self.DESC_NAME = None  # ディスクリプション名初期化
            self.DESC_FILE_NAME = None  # ディスクリプション定義ファイル名初期化
            self.DATE_FIELD = None  # 日付フィールド初期化
            self.tableDesc = None  # テーブルデスクリプションを初期化
            self.PREFIX = ""  # テーブル名の前置句
            self.LENGTH = 0  # コラム長初期化
            if TABLE_NAME is not None and TABLE_NAME != '':  # テーブル名が有る時
                CONF_TABLE = self.getConfTable(TABLE_NAME)  # 設定テーブルをセット
                if CONF_TABLE is not None:  # 設定テーブルが有る時
                    self.DBSDIR = CONF_TABLE.DBSDIR[TABLE_NAME]  # データベース名セット
                    self.SOURCE = CONF_TABLE.SOURCE[TABLE_NAME]  # ソース名セット
                    self.DESC_NAME = CONF_TABLE.DESC_NAME[TABLE_NAME]  # ディスクリプション名セット
                    self.FILE_BLOCK = CONF_TABLE.FILE_BLOCK[TABLE_NAME]  # ファイルブロック長セット
                    self.LASER_BLOCK = CONF_TABLE.LASER_BLOCK[TABLE_NAME]  # レーザーブロック長セット
                    if self.DESC_NAME is not None and self.DESC_NAME != '':  # ディスクリプション名が有る時
                        self.DESC_FILE_NAME = CONF_TABLE.DESC_FILE_NAME[TABLE_NAME]  # ディスクリプション定義ファイル名セット
                        if self.DESC_FILE_NAME is not None and self.DESC_FILE_NAME != '':  # ディスクリプション名が有る時
                            self.tableDesc = self.getTableDescFromDesc()  # テーブルデスクリプションをセット
                            if self.tableDesc is not None:  # テーブルデスクリプションが有る時
                                self.LENGTH = self.tableDesc.columnNr  # コラム長セット
                                for field in self.tableDesc.colName:  # テーブルデスクリプションをすべて実行
                                    for i, field in enumerate(self.tableDesc.colName):  # テーブルデスクリプションをすべて実行
                                        exec("self." + field + " = " + str(i))  # フィールド番号変数設定
                    self.DATE_FIELD = CONF_TABLE.DATE_FIELD[TABLE_NAME]  # 日付フィールドセット
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   property(param)
    # ---------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------
    # ターゲットディレクトリ
    # ---------------------------------------------------------------------------------------------------
    @property
    def targetDir(self):  # ターゲットディレクトリ
        return GP.UPLOADDIR + self.DBSDIR + "/" + self.SOURCE + "/"  # ターゲットディレクトリを返す

    # ---------------------------------------------------------------------------------------------------
    # ターゲットパス
    # ---------------------------------------------------------------------------------------------------
    @property
    def targetPath(self):  # ターゲットパス
        if self.DBSDIR is not None and self.SOURCE is not None:
            tgtDir = GP.UPLOADDIR + self.DBSDIR + "/" + self.SOURCE + "/"  # ターゲットディレクトリ作成
            strPath = tgtDir + self.TABLE_NAME + ".log"  # ターゲットパス作成
            return strPath  # ターゲットパスを返す
        return None

    # ---------------------------------------------------------------------------------------------------
    # ターゲットパス
    # ---------------------------------------------------------------------------------------------------
    @property
    def targetPathInc(self):  # ターゲットパス
        tgtDir = GP.UPLOADDIR + self.DBSDIR + "/" + self.SOURCE + "/"  # ターゲットディレクトリ作成
        strPath = tgtDir + self.TABLE_NAME + ".inc"  # ターゲットパス作成
        return strPath  # ターゲットパスを返す

    @property
    def targetTempPass(self):  # ターゲットパス
        tgtDir = GP.UPLOADDIR + self.DBSDIR + "/" + self.SOURCE + "/"  # ターゲットディレクトリ作成
        strPath = tgtDir + self.TABLE_NAME + ".tmp"  # ターゲットパス作成
        return strPath  # ターゲットパスを返す

    # ---------------------------------------------------------------------------------------------------
    # テーブルリストを作成してから テーブルを作成する
    # ---------------------------------------------------------------------------------------------------
    def getTableDescFromDesc(self):
        try:
            descTable = self.makeDescTableFromCsv()  # ダンプのdescTableを作成する
            if descTable is not None:
                tableDescList = self.makeTableDesc(descTable)  # テーブルデスクリプションリスト作成
                tableDesc = self.getTableDesc(tableDescList)  # テーブルデスクリプションを取得
                return tableDesc
            self.showNone()  # Noneを表示

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    # tableDesc作成
    # ---------------------------------------------------------------------------------------------------
    def makeTableDesc(self, descTable):
        try:
            rowNo = 0  # 行番号初期化
            tableNo = -1  # テーブル番号初期化
            previousName = ""  # 直前の値を初期化
            tableDescList = []  # テーブルデスクリプションリスト初期化
            for row in descTable:  # descTable内    のすべての行を実行
                if rowNo > 0:  # 行番号を確認
                    TABLE_NAME = row[0]  # TABLE_NAME
                    COLUMN_NAME = row[1]  # COLUMN_NAME
                    if TABLE_NAME != previousName:  # TABLE_NAMEと直前の値を確認
                        previousName = TABLE_NAME  # 直前の値をTABLE_NAMEに更新する
                        tableNo = tableNo + 1  # テーブル番号加算
                        td = TableDescClass()  # テーブルデスクリプション生成
                        td.appendAllColumn(row)  # テーブルデスクリプションにコラム追加
                        tableDescList.append(td)  # テーブルデスクリプションリストにテーブルデスクリプションを追加
                    else:  # TABLE_NAMEと直前の値が同じ時
                        td.appendAllColumn(row)  # テーブルデスクリプションにコラム追加
                rowNo = rowNo + 1  # 行番号加算
            return tableDescList  # テーブルデスクリプションリストを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   指定した名前のtableDescを返す
    # ---------------------------------------------------------------------------------------------------
    def getTableDesc(self, tableDescList):
        try:
            tableDesc = None  # テーブルデスクリプション初期化
            for td in tableDescList:  # テーブルデスクリプションリストをすべて実行
                if td.tableName == self.DESC_NAME:  # テーブルデスクリプションのテーブル名がデスクリプション名の時
                    td.tableName = self.TABLE_NAME  # テーブルデスクリプションのテーブル名をテーブル名にする
                    tableDesc = td  # テーブルデスクリプション転写
                    break  # ブレーク
            return tableDesc  # テーブルデスクリプションを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   descTableをCSVから作成する
    # ---------------------------------------------------------------------------------------------------
    def makeDescTableFromCsv(self):
        try:
            strPath = GP.UPLOADDIR + self.DBSDIR + "/" + self.DESC_FILE_NAME  # Description File Pass
            # データの読み込み
            with open(file=strPath, encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                descTable = []  # デスクリプションテーブル初期化
                for strLine in f:  # 一行毎にファイルをすべて読み込む
                    strLine = "".join(strLine.splitlines())  # 改行を削除
                    arrLine = strLine.split("\t")  # strLineをタブで区切りarrLineに格納
                    descTable.append(arrLine)  # デスクリプションテーブルにアペンド
                return descTable  # デスクリプションテーブルを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   呼び出し元のメソッド名を返す
    # ---------------------------------------------------------------------------------------------------
    def getParentMethodName(self, p=None):
        try:
            curframe = inspect.currentframe()  # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
            method = calframe[1][3]  # 呼び出し元の関数名
            return method  # 関数名を返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   このクラス名を返す
    # ---------------------------------------------------------------------------------------------------
    def getClassName(self):
        try:
            return self.__class__.__name__  # クラス名を返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #        実行時間表示(秒)
    # ---------------------------------------------------------------------------------------------------
    def showElapsedTime(self, curframe, calframe, text, p=None):
        try:
            title = calframe[1][3]  # 呼び出し元の関数名
            if p is not None:
                endTime = time.time()  # 終了時刻取得
                elapsed = round(endTime - p.startTime[p.level], 6)  # 実行時間を計算
                print(title + text + str(p.level) + " 実行時間 = " + str(elapsed) + "秒")                 # タイトルと実行時間を表示
            else:
                print(title + text)                                                                     # タイトルと実行時間を表示

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #        実行時間表示(秒)
    # ---------------------------------------------------------------------------------------------------
    def endLevel(self, p=None):
        try:
            curframe = inspect.currentframe()  # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
            self.showElapsedTime(curframe, calframe, " END   ", p)  # 実行時間表示(秒)
            if p is not None:   p.endLevel()

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #         エラー時実行時間表示(秒)
    # ---------------------------------------------------------------------------------------------------
    def showError(self, e, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            print("Exception", e.args)                                                                  # 例外を表示
            self.showElapsedTime(curframe, calframe, " ERROR ", p)                                      # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #         エラー表示
    # ---------------------------------------------------------------------------------------------------
    def printError(self, e):
        curframe = inspect.currentframe()  # カレントのフレーム取得
        calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
        title = calframe[1][3]  # 呼び出し元の関数名
        print("Exception", e.args)  # 例外を表示
        print(title + " ERROR")  # タイトルを表示
        return

    # ---------------------------------------------------------------------------------------------------
    #         None時実行時間表示(秒)
    # ---------------------------------------------------------------------------------------------------
    def showNone(self, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   プログレスウインドウのstartNewLevelを呼ぶ
    # ---------------------------------------------------------------------------------------------------
    def startNewLevel(self, maxCount, p=None):
        try:
            if p is not None:
                p.level += 1  # 進捗レベル更新
                p.startTime[p.level] = time.time()  # タイマー番号の開始時刻を現在の時刻にセット
                curframe = inspect.currentframe()  # カレントのフレーム取得
                calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
                title = calframe[1][3]  # 呼び出し元の関数名
                print(title + " STRAT " + str(p.level))  # タイトルを表示
                functionName = calframe[1][3]  # 呼び出し元の関数名
                className = self.getClassName()  # クラス名取得
                className = className.replace("Class", "")  # "Class"を削除
                text = className + ":"  # テキストにクラス名セット
                text += functionName + " "  # テキストに関数名追加
                try:
                    if self.TABLE_NAME is not None:  # テーブル名が有る時
                        text += self.TABLE_NAME + " "  # テキストにテーブル名追加
                except Exception as e:  # 例外
                    pass
                p.showCurrLevel(maxCount, text)  # カレントのレベルを表示
                QApplication.processEvents()  # プロセスイベントを呼んで制御をイベントループに返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   データが有る時は実行時間を表示してからデータを返す
    #   データが無い時はNoneを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnData(self, retData, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            if retData is not None:  # データが有る時
                self.showElapsedTime(curframe, calframe, " END  ", p)                                   # タイトルと実行時間を表示
                if p is not None:   p.endLevel()
                return retData                                                                          # データを返す
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None                                                                                 # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   データが有る時は実行時間を表示してからデータを返す
    #   データが無い時はNoneを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnList(self, retData, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            if retData is not None and len(retData) > 0:                                                # データが有る時
                self.showElapsedTime(curframe, calframe, " END  ", p)                                   # タイトルと実行時間を表示
                if p is not None:   p.endLevel()
                return retData                                                                          # データを返す
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e,p)                                                                        # エラー表示
            return None                                                                                 # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   データが有る時は実行時間を表示してからデータを返す
    #   データが無い時はNoneを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnList2(self, retData0, retData1, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            if retData0 is not None and len(retData0) > 0 and retData1 is not None:                     # データが有る時
                self.showElapsedTime(curframe, calframe, " END  ", p)                                   # タイトルと実行時間を表示
                if p is not None:   p.endLevel()
                return retData0, retData1                                                               # データを返す
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None, None                                                                           # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return None, None                                                                           # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   データが有る時は実行時間を表示してから結果を返す
    #   データが無い時はNoneを表示してからFalseを返す
    # ---------------------------------------------------------------------------------------------------
    def returnResult(self, result, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            if result is not None:                                                                      # データが有る時
                self.showElapsedTime(curframe, calframe, " END  ", p)                                   # タイトルと実行時間を表示
                if p is not None:   p.endLevel()
                return result                                                                           # データを返す
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return False                                                                                # 失敗を返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return False  # 失敗を返す

    # ---------------------------------------------------------------------------------------------------
    #   Noneを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnNone(self, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            self.showElapsedTime(curframe, calframe, " NONE ", p)                                       # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   Noneを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnNone2(self, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            self.showElapsedTime(curframe, calframe, " NONE ", p)  # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None, None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None, None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   エラーを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnError(self, e, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            print("Exception", e.args)                                                                  # 例外を表示
            self.showElapsedTime(curframe, calframe, " ERROR ", p)                                      # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   エラーを表示してからNoneを返す
    # ---------------------------------------------------------------------------------------------------
    def returnError2(self, e, p=None):
        try:
            curframe = inspect.currentframe()  # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
            print("Exception", e.args)                                                                  # 例外を表示
            self.showElapsedTime(curframe, calframe, " ERROR ", p)                                      # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return None, None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None, None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   エラーを表示してからFalseを返す
    # ---------------------------------------------------------------------------------------------------
    def returnResultError(self, e, p=None):
        try:
            curframe = inspect.currentframe()  # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
            print("Exception", e.args)                                                                  # 例外を表示
            self.showElapsedTime(curframe, calframe, " ERROR ", p)                                      # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return False  # Falseを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return False  # Falseを返す

    # ---------------------------------------------------------------------------------------------------
    #   データが有る時は実行時間を表示してから結果を返す
    #   データが無い時はNoneを表示してからFalseを返す
    # ---------------------------------------------------------------------------------------------------
    def returnError2(self, e, p=None):
        try:
            curframe = inspect.currentframe()                                                           # カレントのフレーム取得
            calframe = inspect.getouterframes(curframe, 4)                                              # 呼び出し元のフレーム取得
            print("Exception", e.args)  # 例外を表示
            self.showElapsedTime(curframe, calframe, " ERROR ", p)                                      # タイトルと実行時間を表示
            if p is not None:   p.endLevel()
            return (None, None)  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return (None, None)  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトを削除してメモリーを解放する
    # ---------------------------------------------------------------------------------------------------
    def deleteObject(self, object):
        try:
            del object  # フラットベースを削除
            gc.collect()  # メモリーを解放する

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   テーブル名から設定テーブルを取得
    # ---------------------------------------------------------------------------------------------------
    def getConfTable(self, TABLE_NAME):
        try:
            TABLE = None  # テーブルを初期化
            if TABLE_NAME in GP.CONT.ORIGIN_CONF.tableNameList:  # テーブル名がGP.CONT.ORIGIN_TABLEに有る時
                TABLE = GP.CONT.ORIGIN_CONF  # GP.CONT.ORIGIN_TABLEをテーブルにセット
            elif TABLE_NAME in GP.CONT.COMB_CONF.tableNameList:  # テーブル名がGP.CONT.COMB_TABLEに有る時
                TABLE = GP.CONT.COMB_CONF  # GP.CONT.COMB_TABLEをテーブルにセット
            elif TABLE_NAME in GP.CONT.TREE_CONF.tableNameList:  # テーブル名がGP.CONT.TREE_CONFに有る時
                TABLE = GP.CONT.TREE_CONF  # GP.CONT.TREE_CONFをテーブルにセット
            elif GP.PCONT.CH.getConfTable(TABLE_NAME) is not None:  # テーブル名がGP.PCONT.CH.PCOMB_CONFに有る時
                TABLE = GP.PCONT.CH.getConfTable(TABLE_NAME)  # GP.PCONT.CH.PCOMB_CONFをテーブルにセット
            elif GP.PCONT.LN.getConfTable(TABLE_NAME) is not None:  # テーブル名がGP.PCONT.CH.PCOMB_CONFに有る時
                TABLE = GP.PCONT.LN.getConfTable(TABLE_NAME)  # テーブルにセット
            elif GP.PCONT.PPM.getConfTable(TABLE_NAME) is not None:  # テーブル名がGP.PCONT.CH.PCOMB_CONFに有る時
                TABLE = GP.PCONT.MM.getConfTable(TABLE_NAME)  # テーブルをセット
            elif GP.PCONT.PPM.getConfTable(TABLE_NAME) is not None:  # テーブル名がGP.PCONT.CH.PCOMB_CONFに有る時
                TABLE = GP.PCONT.MM.getConfTable(TABLE_NAME)  # テーブルをセット
            return TABLE  # 設定テーブルリストを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   サーバーがDBSの時真を返す
    # ---------------------------------------------------------------------------------------------------
    def isDBS(self, SERVER):
        try:
            TYPE = GP.SERVER.TYPE[SERVER]  # サーバータイプ取得
            if TYPE == GP.SERVER_TYPE.DBS:  # サーバータイプがDBサーバーの時
                return True  # 真を返す
            else:  # それ以外の時
                return False  # 偽を返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   サーバーがSSHの時真を返す
    # ---------------------------------------------------------------------------------------------------
    def isSSH(self, SERVER):
        try:
            TYPE = GP.SERVER.TYPE[SERVER]  # サーバータイプ取得
            if TYPE == GP.SERVER_TYPE.SSH:  # サーバータイプがSSHサーバーの時
                return True  # 真を返す
            else:  # それ以外の時
                return False  # 偽を返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトのフィールド名からセレクトクエリーを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeObjectQuery(self, object):
        try:
            if object.tableDesc is not None:
                TABLE_NAME = object.PREFIX + object.TABLE_NAME  # 前置句を付けたテーブル名をセット
                query = QueryClass()
                query.add("SELECT DISTINCT")  # SELECT
                query.add(object.tableDesc.getColumnList("BASE"))  # FIELDS
                query.add("FROM " + TABLE_NAME + " BASE")  # FROM
                return query  # クエリを返す
            self.showNone()  # None表示
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return False  # 失敗を返す

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトのフィールド名からセレクトクエリーを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeObjectQueryNoDistinct(self, object):
        try:
            if object.tableDesc is not None:
                TABLE_NAME = object.PREFIX + object.TABLE_NAME  # 前置句を付けたテーブル名をセット
                query = QueryClass()
                query.add("SELECT")  # SELECT
                query.add(object.tableDesc.getColumnList("BASE"))  # FIELDS
                query.add("FROM " + TABLE_NAME + " BASE")  # FROM
                return query  # クエリを返す
            self.showNone()  # None表示
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return False  # 失敗を返す

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトのフィールド名からセレクトクエリーを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeObjectQuery2(self, object):
        try:
            TABLE_NAME = object.PREFIX + object.TABLE_NAME  # 前置句を付けたテーブル名をセット
            query = QueryClass()
            query.add("SELECT")  # SELECT
            query.add(object.tableDesc.getColumnList2())  # FIELDS
            query.add("FROM " + TABLE_NAME)  # FROM
            return query  # クエリを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return False  # 失敗を返す

    # ---------------------------------------------------------------------------------------------------
    #   ファイルブロック長を返す
    # ---------------------------------------------------------------------------------------------------
    def getFileBlock(self, object):
        try:
            if GP.CONT.dataTransParameter.USE_OBJECT_BLOCK:  # オブジェクトブロック長を使う時
                block = object.FILE_BLOCK  # オブジェクトブロック長を転写
            else:  # オブジェクトブロックを使わない時
                block = GP.CONT.dataTransParameter.FILE_BLOCK  # パラメータブロックを転写
            return block  # ファイルブロック長を返す
        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   レーザーIDブロック長を返す
    # ---------------------------------------------------------------------------------------------------
    def getLaserBlock(self, object):
        try:
            if GP.CONT.dataTransParameter.USE_OBJECT_BLOCK:  # オブジェクトブロック長を使う時
                block = object.LASER_BLOCK  # オブジェクトブロック長を転写
            else:  # オブジェクトブロックを使わない時
                block = GP.CONT.dataTransParameter.LASER_BLOCK  # パラメータブロックを転写
            return block  # ファイルブロック長を返す
        except Exception as e:  # 例外
            self.printshowErrorError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   フィルターリストからWHEREクエリを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeFilterQuery(self, filterList):
        try:
            query = QueryClass()  # クエリー生成
            query.add("WHERE (")  # WHERE (
            qq = np.empty(len(filterList), 'O')  # クエリ配列生成
            qq[:] = "BASE.LASER_ID = "  # "BASE.LASER_ID = "埋め込み
            qq += np.array(filterList, 'str')  # レーザーID追加
            qq[0:-1] += " OR"  # "OR"追加
            query.add(qq)  # クエリ配列をクエリーオブジェクトに追加
            query.add(")")  # ')'
            return query  # クエリーオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   フィルターリストからWHEREクエリを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeFilterPeriodQuery(self, periodList):
        try:
            query = QueryClass()  # クエリー生成
            query.add("WHERE (")  # WHERE (
            qq = np.empty(len(periodList), 'O')  # クエリ配列生成
            qq[:] = "BASE.LASER_ID = "  # "BASE.LASER_ID = "埋め込み
            qq += np.array(periodList[:, self.LASER_ID], 'str')  # レーザーID追加
            qq += " AND BASE.PERIOD = "  # "BASE.PERIOD = "埋め込み
            qq += np.array(periodList[:, self.PERIOD], 'str')  # ピリオッド追加
            qq[0:-1] += " OR"  # "OR"追加
            query.add(qq)  # クエリ配列をクエリーオブジェクトに追加
            query.add(")")  # ')'
            return query  # クエリーオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   フィルターリストからWHEREクエリを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeGrErrorQuery(self, ERROR_LABEL):
        try:
            query = QueryClass()  # クエリーオブジェクト生成
            keys = ERROR_LABEL.GROUP_DIC.keys()  # キー取得
            errorList = [name[1:] for name in keys]  # エラーリスト生成
            query.add("AND (")  # AND
            qq = np.empty(len(errorList), 'O')  # クエリ配列生成
            qq[:] = "ERROR_CODE = "  # "ERROR_CODE = "埋め込み
            qq += errorList  # エラーリスト追加
            qq[0:-1] += " OR"  # "OR"追加
            qq[-1] += ")"  # ")"追加
            query.add(qq)  # クエリ配列をクエリーオブジェクトに追加
            return query  # クエリーオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   モデルコンボを取得する
    # ---------------------------------------------------------------------------------------------------
    def getModelComb(self, PARTS, periodData):
        try:
            MODEL_COMB = None  # モデルコンボを初期化
            if PARTS.LEARN_UNIT == GP.LEARN_UNIT.TYPE_CODE:  # 学習単位がタイプコードの時
                TYPE_CODE = periodData[self.TYPE_CODE]  # タイプコード取得
                TYPE_CODE = TYPE_CODE.replace('-', '_')  # '-'を'_'に置換
                if TYPE_CODE in PARTS.MODEL_DIC:  # モデル辞書に有る時
                    MODEL_COMB = PARTS.MODEL_DIC[TYPE_CODE]  # モデルコンボを選択
            elif PARTS.LEARN_UNIT == GP.LEARN_UNIT.TYPE_ID:  # 学習単位がタイプIDの時
                LASER_TYPE_ID = periodData[self.LASER_TYPE_ID]  # タイプID取得
                LASER_TYPE_ID = LASER_TYPE_ID.replace('-', '_')  # '-'を'_'に置換
                if LASER_TYPE_ID in PARTS.MODEL_DIC:  # モデル辞書に有る時
                    MODEL_COMB = PARTS.MODEL_DIC[LASER_TYPE_ID]  # モデルコンボを選択
            else:  # 学習単位がレーザーIDの時
                if GP.LEARN_UNIT.LASER_ID in PARTS.MODEL_DIC:  # モデル辞書に有る時
                    MODEL_COMB = PARTS.MODEL_DIC[GP.LEARN_UNIT.LASER_ID]  # モデルコンボを選択
            if MODEL_COMB is not None:  # モデルコンボが有る時
                return MODEL_COMB  # モデルコンボを返す
            self.showNone()  # None表示
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   期待値を区間平均する
    # ---------------------------------------------------------------------------------------------------
    def getLabelIntervalMean(self, train, predict, RED_SPAN):
        try:
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            length = len(train)  # 訓練データ長
            n = math.ceil(length / RED_SPAN)  # 区間数
            labelPredict = []  # 期待値の区間平均リスト初期化
            for i in range(n):  # サンプル数をすべて実行
                mean = predict[i * RED_SPAN:(i + 1) * RED_SPAN].mean(axis=0)  # 区間の平均値取得
                labelPredict += [list(train[i * RED_SPAN, :X_BASE]) + list(mean)]  # 区間平均リストに追加
            labelPredict = np.array(labelPredict, 'O')  # numpy配列化
            return labelPredict  # 期待値の区間平均を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   期待値を取得
    # ---------------------------------------------------------------------------------------------------
    def getExpect(self, predict):
        try:
            OUT_LIST = GP.CONT.OUT_LIST  # 出力リスト転写
            outList = np.array(OUT_LIST.LIST, 'int')  # 出力ラベルリストをセット
            expect = predict[:, :] * outList  # 期待値を計算
            expect = np.sum(expect[:, :], axis=1)  # 期待値を計算
            expect = np.array(expect, 'int').reshape(-1, 1)  # 期待値を返す
            return expect  #

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   期待値を取得
    # ---------------------------------------------------------------------------------------------------
    def getExpect2(self, predict):
        try:
            OUT_LIST = GP.CONT.OUT_LIST  # 出力リスト転写
            outList = np.array(OUT_LIST.LIST, 'int')  # 出力ラベルリストをセット
            expect = predict[:, :] * outList  # 期待値を計算
            expect = np.sum(expect[:, :], axis=1)  # 期待値を計算
            expect = np.array(expect, 'int').reshape(-1)  # 期待値を返す
            return expect  #

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   期待値を区間平均する
    # ---------------------------------------------------------------------------------------------------
    def getIntervalMeanExpect(self, train, expect, RED_SPAN):
        try:
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            length = len(train)  # 訓練データ長
            n = math.ceil(length / RED_SPAN)  # 区間数
            predict = []  # 期待値の区間平均リスト初期化
            for i in range(n):  # サンプル数をすべて実行
                mean = int(expect[i * RED_SPAN:(i + 1) * RED_SPAN].mean())  # 区間の平均値取得
                predict += [list(train[i * RED_SPAN, :X_BASE]) + [mean]]  # 区間平均リストに追加
            predict = np.array(predict, 'O')  # numpy配列化
            return predict  # 期待値の区間平均を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   クラス　LaserTreeClass
# =======================================================================================================
class LaserTreeClass(GpiBaseClass):
    # ---------------------------------------------------------------------------------------------------
    #   クラス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None  # シングルトンクラス変数

    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self):  # 初期化
        try:
            if LaserTreeClass._singleton is None:  # シングルトンが無いとき
                GpiBaseClass.__init__(self, GP.CONT.TREE_CONF.LASER)  # スーパークラスの初期化

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if LaserTreeClass._singleton is None:  # シングルトンが無いとき
            LaserTreeClass._singleton = LaserTreeClass()  # インスタンスを生成してシングルトンにセット
        return LaserTreeClass._singleton  # シングルトンがを返す


# =======================================================================================================
#   クラス　シングルトン　TrnClass TrainClassのフィールド番号だけ設定
# =======================================================================================================
class TrnClass(GpiBaseClass):
    # ---------------------------------------------------------------------------------------------------
    #   クラス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None  # シングルトン初期化

    # ---------------------------------------------------------------------------------------------------
    #   初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self):  # 初期化
        try:
            if TrnClass._singleton is None:  # クラス変数の_singletonの有無を確認
                GpiBaseClass.__init__(self, GP.CONT.COMB_CONF.TRN)  # スーパークラスの初期化

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if TrnClass._singleton is None:  # インスタンス変数の_singletonの有無を確認
            TrnClass._singleton = TrnClass()  # クラスを生成して_singletonにセット
        return TrnClass._singleton  # _singletonを返す

    # ---------------------------------------------------------------------------------------------------
    #   予測値を取得
    # ---------------------------------------------------------------------------------------------------
    def getPredictOne2(self, PARTS, train, RED_SPAN, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            # モデルの読み込み
            PRB = PARTS.PRB  # PRBを転写
            MODEL_DIC = PARTS.MODEL_DIC  # モデル辞書の転写
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            if train is not None:  # ピリオッドデータが有る時
                MODEL_COMB = self.getModelComb(PARTS, train[0])  # モデルコンボを取得する
                MODEL = MODEL_COMB.SAVE_MODEL.MODEL  # モデルを転写
                reduce = PRB.reducePredictData(train, RED_SPAN)  # データを削減する
                normal = PRB.normalize(reduce, MODEL_COMB.SAVE_DATA.MINMAX_DATA)  # ピリオッドデータを正規化
                prdData = MODEL.predict(normal)  # モデルから予測値取得
                if PARTS.TYPE == GP.LEARN_TYPE.EVT:  # 学習タイプがイベントの時
                    prdData = PRB.makeGrPredictData(prdData)  # フラグがONの時予想値データをグループ化
                predict = np.concatenate([reduce[:, :X_BASE], prdData], axis=1)  # 予測データを作成
                normal = np.concatenate([reduce[:, :X_BASE], normal], axis=1)  # 正規化データを作成
                return self.returnList2((normal, predict), p)  # 実行時間を表示してからデータを返す
            return self.returnNone((None, None), p)  # Noneを表示してから(None,None)を返す

        except Exception as e:  # 例外
            self.showError(e, p)  # 例外を表示
            return self.returnError2(e, p)  # エラーを表示してから(None,None)を返す

