import numpy as np
import math
import datetime
from staticImport import *
import csv
from classDef import *
from serverBase import ServerBaseClass
import MySQLdb
from gpiBase import *

#=======================================================================================================
#   クラス DBS_ChannelClass
#=======================================================================================================
class DBS_ChannelClass():
    def __init__(self, SERVER):                                                                         # 初期化
        try:
            self.cursor = None                                                                          # カーソルを初期化
            self.DB = None                                                                              # データベースを初期化
            GP.SVR.parameter[SERVER].setClassVar(self)                                                  # サーバー変数セット
            self.DB = MySQLdb.connect(                                                                  # データベースにコネクトしてインスタンス変数にDBをセット
                host     = self.MYSQL_HOST,                                                             # ホストをローカルホストにする
                port     = self.MYSQL_PORT,                                                             # ポートを3306にする。固定
                user     = self.MYSQL_USER,                                                             # ユーザーはDBを生成した時のユーザー名
                password = self.MYSQL_PASS,                                                             # パスワードはDBを生成した時のパスワード
                database = self.MYSQL_DB,                                                               # データベース名はインスタンスの持つDB名
                charset='utf8')                                                                         # 文字コードは'utf8'にする
            self.cursor = self.DB.cursor()                                                              # カーソルを生成
            self.set_group_concat_max_len()                                                             # group_concate_max_len を1024から大きくする
            pass

        except Exception as e:                                                                          # 例外 
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #　チャンネルクローズ
    #---------------------------------------------------------------------------------------------------
    def close(self):
        try:
            if self.cursor is not None:                                                                 # カーソルインスタンス変数が有るとき
                self.DB.close()                                                                         # カーソルをクローズ
                self.DB = None                                                                          # カーソルインスタンス変数を初期化
            if self.DB is not None:                                                                     # DBインスタンス変数が有るとき
                self.DB.close()                                                                         # DBをクローズ
                self.DB = None                                                                          # DBインスタンス変数を初期化

        except Exception as e:                                                                          # 例外 
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #　コミット
    #---------------------------------------------------------------------------------------------------
    def commit(self):
        try:
            self.DB.commit()                                                                            # 書き込みコミット

        except Exception as e:                                                                          # 例外 
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    # group_concate_max_len を1024から大きくする
    #---------------------------------------------------------------------------------------------------
    def set_group_concat_max_len(self):
        try:
            query = QueryClass2("set session group_concat_max_len = 10000000")                          # クエリ作成
            cursor = self.DB.cursor()                                                                   # cursor取得
            query.execute(cursor)                                                                       # クエリを実行する
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")                                                 # クエリを実行する
            self.DB.commit()                                                                            # 書き込みコミット

        except Exception as e:                                                                          # 例外 
            printError(e)                                                                               # 例外を表示

#=======================================================================================================
#   クラス DBServerClass
#=======================================================================================================
class DBServerClass(ServerBaseClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None                                                                                   # シングルトンを初期化

    #---------------------------------------------------------------------------------------------------
    #   初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if DBServerClass._singleton is None:                                                        # クラス変数の_singletonの有無を確認
                ServerBaseClass.__init__(self)                                                          # スーパークラスの初期化
            pass

        except Exception as e:                                                                          # 例外 
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if DBServerClass._singleton is None:                                                            # クラス変数の_singletonの有無を確認
            DBServerClass._singleton = DBServerClass()                                                  # クラスを生成して_singletonにセット
        return DBServerClass._singleton                                                                 # _singletonを返す

    #---------------------------------------------------------------------------------------------------
    #   DBをオープンしてcursorを返す
    #---------------------------------------------------------------------------------------------------
    def openServer(self, SERVER):
        try:
            channel = DBS_ChannelClass(SERVER)                                                          # チャンネルを生成してDBをオープンする
            return channel, channel.cursor                                                              # 生成したチャンネルを返す

        except MySQLdb.Error as e:                                                                    # 例外 
            self.printError(e)                                                                          # 例外を表示
            return None, None                                                                           # Noneを返す

    #***************************************************************************************************
    #   ローカルサーバー処理メソッド
    #***************************************************************************************************
    #---------------------------------------------------------------------------------------------------
    #   ローカルサーバーのテーブルの有無を返す
    #---------------------------------------------------------------------------------------------------
    def existsLocTable(self, object):
        try:
            return self.existsTable(GP.SERVER.LOC_RDM_DBS, object)                                      # テーブルの有無を返す

        except Exception as e:                                                                          # 例外 
            return False                                                                                # 偽を返す

    #---------------------------------------------------------------------------------------------------
    #   ローカルサーバーをオープンしてcursorを返す
    #---------------------------------------------------------------------------------------------------
    def openLocServer(self):
        try:
            return self.openServer(GP.SERVER.LOC_RDM_DBS)                                               # LOC_RDM_DBSをオープンしてcursorを返す

        except MySQLdb.Error as e:                                                                    # 例外 
            return None, None                                                                           # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   クエリーからフィルターをかけたローカルDBを作成する
    #---------------------------------------------------------------------------------------------------
    def makeLocFilterDBFromQuery(self, object, baseQuery, filterList, p=None):
        try:
            return self.makeFilterDBFromQuery(GP.SERVER.LOC_RDM_DBS, object, baseQuery, filterList, p)  # クエリーからDBを作成する

        except Exception as e:                                                                          # 例外 
            pass

    #---------------------------------------------------------------------------------------------------
    #   クエリーからローカルDBを作成する
    #---------------------------------------------------------------------------------------------------
    def makeLocDBFromQuery(self, object, baseQuery, p=None):
        try:
            return self.makeDBFromQuery(GP.SERVER.LOC_RDM_DBS, object, baseQuery, p)        # クエリーからDBを作成する

        except Exception as e:                                                                          # 例外 
            pass

    #---------------------------------------------------------------------------------------------------
    #   テーブルに含まれるレーザーIDリスト作成
    #---------------------------------------------------------------------------------------------------
    def getLocLaserIdList(self, object, p=None):
        try:
            return self.getLaserIdList(GP.SERVER.LOC_RDM_DBS, object, p)                                # テーブルに含まれるレーザーIDリスト作成

        except Exception as e:                                                                          # 例外 
            self.printError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   ローカルDBからクエリーを使ってフラットリストを作成する。DB読み込みのベースメソッド
    #   filterListがNoneの時は全て読み込む
    #---------------------------------------------------------------------------------------------------
    def makeLocFlatListFromQuery(self, object, baseQuery, p=None):
        try:
            return self.makeFlatListFromQuery(GP.SERVER.LOC_RDM_DBS, object, baseQuery, p)              # 指定したDBからクエリーを使ってフラットリストを作成する

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   ローカルDBからクエリーを使ってフラットリストを作成する。DB読み込みのベースメソッド
    #   filterListがNoneの時は全て読み込む
    #---------------------------------------------------------------------------------------------------
    def makeLocFilterFlatListFromQuery(self, object, baseQuery, filterList, p=None):
        try:
            return self.makeFilterFlatListFromQuery(GP.SERVER.LOC_RDM_DBS, object, baseQuery, filterList, p)  # 指定したDBからクエリーを使ってフラットリストを作成する

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトのデータをローカルサーバーに書き込む
    #---------------------------------------------------------------------------------------------------
    def makeLocDBFromObject(self, object, baseType, p=None):
        try:
            return self.saveBaseData(GP.SERVER.LOC_RDM_DBS, object, baseType, p)                        # オブジェクトのデータをローカルサーバーに書き込む

        except Exception as e:                                                                          # 例外 
            pass


    #---------------------------------------------------------------------------------------------------
    #   オブジェクトファイルからローカルDBを作成
    #---------------------------------------------------------------------------------------------------
    def makeLocDBFromObjectFile(self, object, p=None):
        try:
            self.makeDBFromObjectFile(GP.SERVER.LOC_RDM_DBS, object, p)                                 # オブジェクトファイルからDBを作成

        except Exception as e:                                                                          # 例外 
            pass

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトからクエリーを使ってフラットなリストを取得。
    #---------------------------------------------------------------------------------------------------
    def getLocFlatList(self, object, p=None):
        try:
            query = self.makeObjectQuery(object)                                                        # オブジェクトのフィールド名からセレクトクエリーを作成
            if query is not None:
                SERVER = GP.SERVER.LOC_RDM_DBS                                                          # ローカルサーバーセット
                if self.existsTable(SERVER, object):                                                    # DBにテーブルが有る時
                    return self.makeFlatListFromQuery(SERVER, object, query, p)                         # クエリーからフラットリストを作成する
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトからクエリーを使ってフラットなリストを取得。
    #---------------------------------------------------------------------------------------------------
    def getLocFlatListNoDistinct(self, object, p=None):
        try:
            query = self.makeObjectQueryNoDistinct(object)                                              # オブジェクトのフィールド名からセレクトクエリーを作成
            if query is not None:
                SERVER = GP.SERVER.LOC_RDM_DBS                                                          # ローカルサーバーセット
                if self.existsTable(SERVER, object):                                                    # DBにテーブルが有る時
                    return self.makeFlatListFromQuery(SERVER, object, query, p)                         # クエリーからフラットリストを作成する
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #  オブジェクトからクエリーを使ってレーザーIDリストに有るフラットなリストを取得。(DBチェック有り)
    #---------------------------------------------------------------------------------------------------
    def getLocFlatListFromQuery(self, object, query, p=None):
        try:
            SERVER = GP.SERVER.LOC_RDM_DBS                                                              # ローカルサーバーセット
            if self.existsTable(SERVER, object):                                                        # DBにテーブルが有る時
                return self.makeFlatListFromQuery(SERVER, object, query, p)                             # クエリーからフラットリストを作成する
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトからクエリーを使ってフラットなリストを取得。
    #---------------------------------------------------------------------------------------------------
    def getLocFilterFlatList(self, object, filterList, p=None):
        try:
            query = self.makeObjectQuery(object)                                                        # オブジェクトのフィールド名からセレクトクエリーを作成
            SERVER = GP.SERVER.LOC_RDM_DBS                                                              # ローカルサーバーセット
            if self.existsTable(SERVER, object):                                                        # DBにテーブルが有る時
                return self.makeFilterFlatListFromQuery(SERVER, object, query, filterList, p)           # フラットリストを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトからクエリーを使ってフラットなリストを取得。
    #---------------------------------------------------------------------------------------------------
    def getLocFilterFlatListBlock(self, object, filterList, p=None):
        try:
            query = self.makeObjectQuery(object)                                                        # オブジェクトのフィールド名からセレクトクエリーを作成
            SERVER = GP.SERVER.LOC_RDM_DBS                                                              # ローカルサーバーセット
            if self.existsTable(SERVER, object):                                                        # DBにテーブルが有る時
                return self.makeFilterFlatListFromQueryBlock(SERVER, object, query, filterList, p)      # フラットリストを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #  オブジェクトからクエリーを使ってレーザーIDリストに有るフラットなリストを取得。(DBチェック有り)
    #---------------------------------------------------------------------------------------------------
    def getLocFilterFlatListFromQuery(self, object, query, filterList, p=None):
        try:
            SERVER = GP.SERVER.LOC_RDM_DBS                                                              # ローカルサーバーセット
            if self.existsTable(SERVER, object):                                                        # DBにテーブルが有る時
                return self.makeFilterFlatListFromQuery(SERVER, object, query, filterList, p)           # フラットリストを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトからクエリーを使ってレーザーIDリストに有るレーザー辞書を読み込む。
    #   filterListがNoneの時はすべて読み込む
    #---------------------------------------------------------------------------------------------------
    def getLocFilterLaserDicFromQuery(self, object, query, filterList, p=None):
        try:
            SERVER = GP.SERVER.LOC_RDM_DBS                                                              # ローカルサーバーセット
            if self.existsTable(SERVER, object):                                                        # DBにテーブルが有る時
                return self.makeFilterLaserDicFromQuery(SERVER, object, query, filterList, p)           # オブジェクトからクエリーを使ってフィルター内のレーザー辞書を読み込む。
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトからクエリーを使ってレーザーIDリストに有るピリオッド辞書を読み込む。
    #---------------------------------------------------------------------------------------------------
    def getLocPeriodDicFromQuery(self, object, query, p=None):
        try:
            SERVER = GP.SERVER.LOC_RDM_DBS                                                              # ローカルサーバーセット
            if self.existsTable(SERVER, object):                                                        # DBにテーブルが有る時
                return self.makePeriodDicFromQuery(SERVER, object, query, p)                            # クエリーを使ってレーザーIDリストに有るフラットなリストを取得
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトからクエリーを使ってレーザーIDリストに有るピリオッド辞書を読み込む。
    #---------------------------------------------------------------------------------------------------
    def getFilterLocPeriodDicFromQuery(self, object, query, filterList, p=None):
        try:
            SERVER = GP.SERVER.LOC_RDM_DBS                                                              # ローカルサーバーセット
            if self.existsTable(SERVER, object):                                                        # DBにテーブルが有る時
                return self.makeFilterPeriodDicFromQuery(SERVER, object, query, filterList, p)          # クエリーを使ってレーザーIDリストに有るフラットなリストを取得
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外 
            return None                                                                                 # Noneを返す

    #-------------------------------------------------------------------------------------------------------
    #   フラットベースからレーザーデータを返す
    #-------------------------------------------------------------------------------------------------------
    def getLocLaserData(self, object, LASER_ID):
        try:
            SERVER = GP.SERVER.LOC_RDM_DBS                                                              # ローカルサーバーセット
            channnel = DBS_ChannelClass(SERVER)                                                         # DBをオープンする
            query = object.makeObjectQuery(object)                                                      # クエリーを作成
            query.add("WHERE BASE.LASER_ID = " + str(LASER_ID))                                         # レーザーID
            query.execute(channnel.cursor)                                                              # クエリを実行する
            dataList = channnel.cursor.fetchall()                                                       # すべて読み込みリストにする
            channnel.close()                                                                            # DBクローズ
            if len(dataList) > 0:                                                                       # データリストが有る時
                self.deleteObject(dataList)                                                             # メモリーをクリア
                return np.array(dataList, 'O')                                                          # レーザーデータを返す
            return None                                                                                 # レーザーデータが無い時はNoneを返す

        except Exception as e:                                                                          # 例外 
            self.printError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #-------------------------------------------------------------------------------------------------------
    #   与えられた期間の中のデータ数を返す
    #-------------------------------------------------------------------------------------------------------
    def getLocElements(self, object, LASER_ID):
        try:
            SERVER = GP.SERVER.LOC_RDM_DBS                                                              # ローカルサーバーセット
            channnel = DBS_ChannelClass(SERVER)                                                         # DBをオープンする
            query = object.makeObjectQuery(object)                                                      # クエリーを作成
            query.add("WHERE BASE.LASER_ID = " + str(LASER_ID))                                         # レーザーID
            query.execute(channnel.cursor)                                                              # クエリを実行する
            dataList = channnel.cursor.fetchall()                                                       # すべて読み込みリストにする
            channnel.close()                                                                            # DBクローズ
            if len(dataList) > 0:                                                                       # データリストが有る時
                self.deleteObject(dataList)                                                             # メモリーをクリア
                return np.array(dataList, 'O')                                                          # レーザーデータを返す
            return None                                                                                 # レーザーデータが無い時はNoneを返す

        except Exception as e:                                                                          # 例外 
            self.printError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

