import numpy as np
import math
from sshtunnel import SSHTunnelForwarder
from staticImport import *
import csv
from classDef import *
from serverBase import ServerBaseClass
import MySQLdb as connector
from gpiBase import *

#=======================================================================================================
#   クラス SSH_ChannelClass
#=======================================================================================================
class SSH_ChannelClass():
    def __init__(self, SERVER):                                                                         # 初期化
        try:
            GP.SVR.parameter[SERVER].setClassVar(self)                                                  # サーバー変数セット
            self.DB = connector.connect(                                                                # データベースにコネクトしてインスタンス変数にDBをセット
                host     = self.LOCAL_ADDRESS,                                                          # ホストをローカルホストにする
#                port     = self.server.local_bind_port,                                                 # ポートを取得
                port     = self.LOCAL_PORT,                                                             # ポートを取得
                user     = self.MYSQL_USER,                                                             # ユーザー名
                passwd   = self.MYSQL_PASS,                                                             # パスワード
                database = self.MYSQL_DB,                                                               # データベース名はインスタンスの持つDB名
                charset='utf8')                                                                         # 文字コードをutf8にする
            self.cursor = self.DB.cursor()                                                              # カーソルを生成
            self.set_group_concat_max_len()                                                             # group_concate_max_len を1024から大きくする

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

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
#   クラス ErrorClass
#=======================================================================================================
class SSHServerClass(ServerBaseClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None                                                                                   # シングルトンを初期化

    #---------------------------------------------------------------------------------------------------
    #   初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if SSHServerClass._singleton is None:                                                       # クラス変数の_singletonの有無を確認
                ServerBaseClass.__init__(self)                                                          # スーパークラスの初期化
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if SSHServerClass._singleton is None:                                                           # クラス変数の_singletonの有無を確認
            SSHServerClass._singleton = SSHServerClass()                                                # インスタンスを生成して_singletonにセット
        return SSHServerClass._singleton                                                                # _singletonを返す

    #---------------------------------------------------------------------------------------------------
    #   リモートサーバーを取得する
    #---------------------------------------------------------------------------------------------------
    def getTunnelServer(self, SERVER):
        try:
            self.setServer(SERVER)                                                                      # サーバーセット
            self.server = None                                                                          # 自クラスのサーバーを初期化
            self.server = SSHTunnelForwarder(
                (self.SSH_ADDRESS, self.SSH_PORT),
                ssh_pkey            = self.SSH_PKEY_PATH,
                ssh_username        = self.SSH_USER,
                ssh_password        = self.SSH_PASS,
                remote_bind_address = (self.MYSQL_HOST, self.MYSQL_PORT),
                local_bind_address  = (self.LOCAL_ADDRESS, self.LOCAL_PORT),
            )
            if self.server is not None:                                                                 # サーバーが有る時
                return True                                                                             # 成功を返す
            return False                                                                                # 失敗を返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # エラー表示
            return False                                                                                # 失敗を返す

    #---------------------------------------------------------------------------------------------------
    #   リモートサーバーをオープンする
    #---------------------------------------------------------------------------------------------------
    def openServer(self, SERVER):
        try:
            channel = SSH_ChannelClass(SERVER)                                                          # チャンネルを生成してDBをオープンする
            return channel, channel.cursor                                                              # 生成したチャンネルを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # エラー表示
            return None, None                                                                           # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   テーブル名リストをDBから作る
    #---------------------------------------------------------------------------------------------------
    def makeTableNameListSSH(self, SERVER):
        try:
            if self.getTunnelServer(SERVER):                                                            # SSHサーバーが有る時
                with self.server:                                                                       # サーバーをオープンして実行
                    return self.makeTableNameList(SERVER)                                               # テーブル名リストをDBから作る
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   DBサーバーからCSVファイルを作る
    #---------------------------------------------------------------------------------------------------
    def DB_TO_CSV(self, SERVER, object, p=None):
        try:
            if self.getTunnelServer(SERVER):                                                            # SSHサーバーが有る時
                with self.server:                                                                       # サーバーをオープンして実行
                    self.makeFileFromDB(SERVER, object, p)                                              # DBサーバーからCSVファイルを作る

        except Exception as e:                                                                          # 例外
            return False                                                                                # 偽を返す

    #---------------------------------------------------------------------------------------------------
    #   DBサーバーからフィルターをかけたCSVファイルを作る
    #---------------------------------------------------------------------------------------------------
    def DB_TO_FILTER_CSV(self, SERVER, object, filterList, p=None):
        try:
            if self.getTunnelServer(SERVER):                                                            # SSHサーバーが有る時
                with self.server:                                                                       # サーバーをオープンして実行
                    self.makeFilterFileFromDB(SERVER, object, filterList, p)                                  # DBサーバーからCSVファイルを作る

        except Exception as e:                                                                          # 例外
            return False                                                                                # 偽を返す

    #---------------------------------------------------------------------------------------------------
    #   CSVファイルからDBを作る
    #---------------------------------------------------------------------------------------------------
    def CSV_TO_DB(self, SERVER, object, filterList, p=None):
        try:
            if self.getTunnelServer(SERVER):                                                            # SSHサーバーが有る時
                with self.server:                                                                       # サーバーをオープンして実行
                    return self.makeDBFromObjectFile(SERVER, object, p)                                 # CSVファイルからDBを作る

        except Exception as e:                                                                          # 例外
            return False                                                                                # 偽を返す

    #---------------------------------------------------------------------------------------------------
    #   最後のN行を削除
    #---------------------------------------------------------------------------------------------------
    def DELETE_ROWS(self, SERVER, object, rows, p=None):
        try:
            if self.getTunnelServer(SERVER):                                                            # SSHサーバーが有る時
                with self.server:                                                                       # サーバーをオープンして実行
                    return self.deleteRows(SERVER, object, rows, p)                                     # クエリーからフィルタをかけたCSVファイルを作成する

        except Exception as e:                                                                          # 例外
            return False                                                                                # 偽を返す

    #---------------------------------------------------------------------------------------------------
    #   レーザー単位の追加リストを取得する
    #---------------------------------------------------------------------------------------------------
    def makeLaserAddFileSSH(self, SERVER, object, incPath, filterList, latestDateList, p=None):
        try:
            if self.getTunnelServer(SERVER):                                                            # GIGA検証サーバーを取得する
                with self.server:                                                                       # サーバーをオープンして実行
                    return self.makeLaserAddFile(SERVER, object, incPath, filterList, latestDateList, p)
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   最終書き込み時刻から追加リストを取得する
    #---------------------------------------------------------------------------------------------------
    def makeAddFileSSH(self, SERVER, object, latestDateTime, dateField, p=None):
        try:
            if self.getTunnelServer(SERVER):                                                            # GIGA検証サーバーを取得する
                with self.server:                                                                       # サーバーをオープンして実行
                    return self.makeAddFile(SERVER, object, latestDateTime, dateField, p)               # 最終書き込み時刻から追加リストを取得する
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #  行数を取得
    #---------------------------------------------------------------------------------------------------
    def getCountSSH(self, SERVER, object, p=None):
        try:
            if self.getTunnelServer(SERVER):                                                            # GIGA検証サーバーを取得する
                with self.server:                                                                       # サーバーをオープンして実行
                    return self.getCount(SERVER, object, p)                                             # 行数を取得
            return 0                                                                                    # Noneを返す

        except Exception as e:                                                                          # 例外
            return 0                                                                                    # Noneを返す
