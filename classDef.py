import os
import numpy as np
from staticImport import *
from distutils.util import strtobool

#=======================================================================================================
#   スーパークラス パラメータクラス
#=======================================================================================================
class ParameterClass():
    def __init__(self, logPath):                                                                        # 初期化
        try:
            self.logPath =logPath                                                                       # ログファイル名

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   パラメーターをインスタンス変数に転写する
    #---------------------------------------------------------------------------------------------------
    def setClassVar(self, object):
        try:
            for objectName in self.nameList:                                                            # ローカル変数名リストをすべて実行
                exec("object." + objectName + " = self." + objectName)                                  # オブジェクトのインスタンス変数のセット
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   ログファイルのデータを読み込む
    #---------------------------------------------------------------------------------------------------
    def loadData(self):
        try:
            if self.logPath is not None:                                                                # ログパスが有る時
                if os.path.isfile(self.logPath) and os.path.getsize(self.logPath) > 0:                  # ファイルが有る時
                    with open(file=self.logPath,mode="r",encoding="utf-8") as f:                        # "utf-8"でファイルをオープン
                        for objectName in self.nameList:                                                # オブジェクト名リストをすべて実行
                            exec("self.object = " + "self." + objectName)                               # インスタンス変数のセット
                            if type(self.object) == type([]):                                           # タイプが"list"の時
                                for i, data in enumerate(self.object):                                  # リストをすべて実行
                                    self.var = f.readline()                                             # ファイルから一行読み込む
                                    self.var = self.var.strip()                                         # 改行を取り除く
                                    if type(data) == type(''):                                          # タイプが"str"の時
                                        self.object[i] = self.var                                       # インスタンス変数のセット
                                    elif type(data) == type(0):                                         # タイプが"int"の時
                                        self.object[i] = int(self.var)                                  # インスタンス変数のセット
                                    elif type(data) == type(0.0):                                       # タイプが"float"の時
                                       self.object[i] = float(self.var)                                 # インスタンス変数のセット
                                    elif type(data) == type(True):                                      # タイプが"bool"の時
                                        self.object[i] = bool(strtobool(self.var))                      # インスタンス変数のセット
                                    else:                                                               # その他の時
                                        self.object[i] = self.var                                       # インスタンス変数のセット
                            else:                                                                       # タイプが"list"でない時
                                ttt = type(self.object)
                                self.var = f.readline()                                                 # ファイルから一行読み込む
                                self.var = self.var.strip()                                             # 改行を取り除く
                                if type(self.object) == type(''):                                       # タイプが"str"の時
                                    exec("self." + objectName + " = self.var")                          # インスタンス変数のセット
                                elif type(self.object) == type(0):                                      # タイプが"int"の時
                                    exec("self." + objectName + " = int(self.var)")                     # インスタンス変数のセット
                                elif type(self.object) == type(0.0):                                    # タイプが"float"の時
                                    exec("self." + objectName + " = float(self.var)")                   # インスタンス変数のセット
                                elif type(self.object) == type(True):                                   # タイプが"bool"の時
                                    exec("self." + objectName + " = bool(strtobool(self.var))")         # インスタンス変数のセット
                                else:                                                                   # その他の時
                                    exec("self." + objectName + " = self.var")                          # インスタンス変数のセット
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   パラメータをログファイルに書き込む
    #---------------------------------------------------------------------------------------------------
    def saveData(self):
        try:
            if self.logPath is not None:                                                                # ログパスが有る時
                dirName = os.path.dirname(self.logPath)                                                 # ディレクトリ名
                if not os.path.exists(dirName):                                                         # ディレクトリの有無を確認
                    os.makedirs(dirName)                                                                # 途中のディレクトリを含めてディレクトリを作成
                with open(file=self.logPath,mode="w",encoding="utf-8") as f:                            # "utf-8"でファイルをオープン
                    for objectName in self.nameList:                                                    # オブジェクト名リストをすべて実行
                        exec("self.object = " + "self." + objectName)                                   # インスタンス変数の転写
                        if type(self.object) == type([]):                                               # タイプが"list"の時
                            for self.var in self.object:
                                f.write(str(self.var) + "\n")                                           # ファイルに一行書き込む
                        else:                                                                           # タイプが"list"でない時
                            f.write(str(self.object) + "\n")                                            # ファイルに一行書き込む
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

#=======================================================================================================
#   クラス データ移行パラメータクラス
#=======================================================================================================
class DataTransParameterClass(ParameterClass):
    _singleton = None
    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if DataTransParameterClass._singleton is None:                                              # シングルトンが無いとき
                ParameterClass.__init__(self, GP.UPDATE_LOG.DATA_TRANS)                                 # スーパークラスの初期化
                SRC_SERVER = GP.SERVER.LOC_RDM_DBS                                                      # サーバー名選択
                DST_SERVER = GP.SERVER.LOC_RDM_DBS                                                      # サーバー名選択
                SEL_FILE  = GP.ALL                                                                      # 選択ファイル名
                SEL_TABLE = GP.ALL                                                                      # 選択テーブル名
                SEL_SOURCE = GP.DATA_SOURCE.ORIGIN                                                      # 選択データソース名
                DELETE_ROWS = 1                                                                         # 削除行数
                FILE_BLOCK = 100                                                                        # ファイルブロック長（ファイル行数）
                LASER_BLOCK = 10                                                                        # レーザーブロック長（レーザーID数）
                USE_OBJECT_BLOCK = True                                                                 # オブジェクトブロック使用フラグ
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                    (name != '__pydevd_ret_val_dict')]                                  # ローカル変数名リストを作成
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                self.loadData()                                                                         # パラメータをログファイルから読込
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if DataTransParameterClass._singleton is None:                                                  # シングルトンが無いとき
            DataTransParameterClass._singleton = DataTransParameterClass()                              # インスタンスを生成してシングルトンにセット
        return DataTransParameterClass._singleton                                                       # シングルトンがを返す

#=======================================================================================================
#   クラス FDR　REDEEM SSHパラメータクラス
#=======================================================================================================
class FdrRdmSSHParameterClass(ParameterClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None

    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if FdrRdmSSHParameterClass._singleton is None:                                              # シングルトンが無いとき
                ParameterClass.__init__(self, GP.CONF_LOG.FDR_RDM_SSH)                                  # スーパークラスの初期化
                SSH_ADDRESS   =  '192.168.100.125'                                                      # SSH アドレス
                SSH_PORT      =  22                                                                     # SSH ポート
                SSH_USER      =  'root'                                                                 # SSH ユーザー
                SSH_PASS      =  'root'                                                                 # SSH パスワード
                SSH_PKEY_PATH =  ''                                                                     # SSH PKEY_PATH
                MYSQL_HOST    =  '192.168.100.124'                                                      # MYSQL アドレス
                MYSQL_PORT    =  3306                                                                   # MYSQL ポート
                MYSQL_USER    =  'root'                                                                 # MYSQL ユーザー
                MYSQL_PASS    =  'allright'                                                             # MYSQL パスワード
                MYSQL_DB      =  'redeemut'                                                             # MYSQL DB名
                LOCAL_ADDRESS =  '127.0.0.1'                                                            # MYSQL LOCAL BIND アドレス
                LOCAL_PORT    =  13306                                                                  # MYSQL LOCAL BIND ポート
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                   (name != '__pydevd_ret_val_dict')]                                   # ローカル変数名リストを作成
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                self.loadData()                                                                         # ログファイルのデータを読み込む
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if FdrRdmSSHParameterClass._singleton is None:                                                  # シングルトンが無いとき
            FdrRdmSSHParameterClass._singleton = FdrRdmSSHParameterClass()                              # インスタンスを生成してシングルトンにセット
        return FdrRdmSSHParameterClass._singleton                                                       # シングルトンがを返す

#=======================================================================================================
#   クラス ユーザーパラメータクラス
#=======================================================================================================
class FdrRdmDBSParameterClass(ParameterClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None

    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if FdrRdmDBSParameterClass._singleton is None:                                              # シングルトンが無いとき
                ParameterClass.__init__(self, GP.CONF_LOG.FDR_RDM_DBS)                                  # スーパークラスの初期化
                MYSQL_HOST    =  '192.168.100.124'                                                      # MYSQL アドレス
                MYSQL_PORT    =  3306                                                                   # MYSQL ポート
                MYSQL_USER    =  'root'                                                                 # MYSQL ユーザー
                MYSQL_PASS    =  'allright'                                                             # MYSQL パスワード
                MYSQL_DB      =  'redeemut'                                                             # MYSQL DB名
                LOCAL_ADDRESS =  '127.0.0.1'                                                            # MYSQL LOCAL BIND アドレス
                LOCAL_PORT    =  13306                                                                  # MYSQL LOCAL BIND ポート
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                   (name != '__pydevd_ret_val_dict')]                                   # ローカル変数名リストを作成
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                self.loadData()                                                                         # ログファイルのデータを読み込む
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if FdrRdmDBSParameterClass._singleton is None:                                                  # シングルトンが無いとき
            FdrRdmDBSParameterClass._singleton = FdrRdmDBSParameterClass()                              # インスタンスを生成してシングルトンにセット
        return FdrRdmDBSParameterClass._singleton                                                       # シングルトンがを返す

#=======================================================================================================
#   クラス ユーザーパラメータクラス
#=======================================================================================================
class GpiRdmSSHParameterClass(ParameterClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None

    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if GpiRdmSSHParameterClass._singleton is None:                                              # シングルトンが無いとき
                ParameterClass.__init__(self,  GP.CONF_LOG.GPI_RDM_SSH)                                 # スーパークラスの初期化
                SSH_ADDRESS   = '210.251.68.90'                                                         # SSH アドレス
                SSH_PORT      = 22                                                                      # SSH ポート
                SSH_USER      = 'root'                                                                  # SSH ユーザー
                SSH_PASS      = 'qwer!"#$ap1'                                                           # SSH パスワード
                SSH_PKEY_PATH = ''                                                                      # SSH PKEY_PATH
                MYSQL_HOST    = '10.42.2.134'                                                           # MYSQL アドレス
                MYSQL_PORT    =  3306                                                                   # MYSQL ポート
                MYSQL_USER    = 'redeem'                                                                # MYSQL ユーザー
                MYSQL_PASS    = 'gIga9r15oot'                                                           # MYSQL パスワード
                MYSQL_DB      = 'redeem'                                                                # MYSQL DB名
                LOCAL_ADDRESS = '127.0.0.1'                                                             # MYSQL LOCAL BIND アドレス
                LOCAL_PORT    = 13306                                                                   # MYSQL LOCAL BIND ポート
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                   (name != '__pydevd_ret_val_dict')]                                   # ローカル変数名リストを作成
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                self.loadData()                                                                         # ログファイルのデータを読み込む
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if GpiRdmSSHParameterClass._singleton is None:                                                  # シングルトンが無いとき
            GpiRdmSSHParameterClass._singleton = GpiRdmSSHParameterClass()                              # インスタンスを生成してシングルトンにセット
        return GpiRdmSSHParameterClass._singleton                                                       # シングルトンがを返す

#=======================================================================================================
#   クラス ユーザーパラメータクラス
#=======================================================================================================
class GpiRdmSSHTestParameterClass(ParameterClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None

    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if GpiRdmSSHTestParameterClass._singleton is None:                                          # シングルトンが無いとき
                ParameterClass.__init__(self, GP.CONF_LOG.GPI_RDM_SSH_TEST)                             # スーパークラスの初期化
                SSH_ADDRESS   = '210.251.68.88'                                                         # SSH アドレス
                SSH_PORT      = 22                                                                      # SSH ポート
                SSH_USER      = 'root'                                                                  # SSH ユーザー
                SSH_PASS      = 'qwer!"#$ap0'                                                           # SSH パスワード
                SSH_PKEY_PATH = ''                                                                      # SSH PKEY_PATH
                MYSQL_HOST    = '10.42.2.136'                                                           # MYSQL アドレス
                MYSQL_PORT    = 3306                                                                    # MYSQL ポート
                MYSQL_USER    = 'redeem'                                                                # MYSQL ユーザー
                MYSQL_PASS    = 'gpi2Red01R5oot'                                                        # MYSQL パスワード
                MYSQL_DB      = 'redeem'                                                                # MYSQL DB名
                LOCAL_ADDRESS = '127.0.0.1'                                                             # MYSQL LOCAL BIND アドレス
                LOCAL_PORT    = 13306                                                                   # MYSQL LOCAL BIND ポート
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                   (name != '__pydevd_ret_val_dict')]                                   # ローカル変数名リストを作成
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                self.loadData()                                                                         # ログファイルのデータを読み込む
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if GpiRdmSSHTestParameterClass._singleton is None:                                              # シングルトンが無いとき
            GpiRdmSSHTestParameterClass._singleton = GpiRdmSSHTestParameterClass()                      # インスタンスを生成してシングルトンにセット
        return GpiRdmSSHTestParameterClass._singleton                                                   # シングルトンがを返す

#=======================================================================================================
#   クラス ユーザーパラメータクラス
#=======================================================================================================
class GpiRdmDBSParameterClass(ParameterClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None

    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if GpiRdmDBSParameterClass._singleton is None:                                              # シングルトンが無いとき
                ParameterClass.__init__(self, GP.CONF_LOG.GPI_RDM_DBS)                                  # スーパークラスの初期化
                MYSQL_HOST    = '10.42.2.134'                                                           # MYSQL アドレス
                MYSQL_PORT    = 3306                                                                    # MYSQL ポート
                MYSQL_USER    = 'redeem'                                                                # MYSQL ユーザー
                MYSQL_PASS    = 'gIga9r15oot'                                                           # MYSQL パスワード
                MYSQL_DB      = 'redeem'                                                                # MYSQL DB名
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                   (name != '__pydevd_ret_val_dict')]                                   # ローカル変数名リストを作成
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                self.loadData()                                                                         # ログファイルのデータを読み込む
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if GpiRdmDBSParameterClass._singleton is None:                                                  # シングルトンが無いとき
            GpiRdmDBSParameterClass._singleton = GpiRdmDBSParameterClass()                              # インスタンスを生成してシングルトンにセット
        return GpiRdmDBSParameterClass._singleton                                                       # シングルトンがを返す

#=======================================================================================================
#   クラス ローカルREDEEMサーバーパラメータクラス
#=======================================================================================================
class LocRdmDBSParameterClass(ParameterClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None

    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if LocRdmDBSParameterClass._singleton is None:                                              # シングルトンが無いとき
                ParameterClass.__init__(self, GP.CONF_LOG.LOC_RDM_DBS)                                  # スーパークラスの初期化
                MYSQL_HOST    = '127.0.0.1'                                                             # MYSQL アドレス
                MYSQL_PORT    = 3306                                                                    # MYSQL ポート
                MYSQL_USER    = 'root'                                                                  # MYSQL ユーザー
                MYSQL_PASS    = 'rednoa'                                                                # MYSQL パスワード
                MYSQL_DB      = REDEEM                                                                  # MYSQL DB名
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                   (name != '__pydevd_ret_val_dict')]                                   # ローカル変数名リストを作成
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                self.loadData()                                                                         # ログファイルのデータを読み込む
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if LocRdmDBSParameterClass._singleton is None:                                                  # シングルトンが無いとき
            LocRdmDBSParameterClass._singleton = LocRdmDBSParameterClass()                              # インスタンスを生成してシングルトンにセット
        return LocRdmDBSParameterClass._singleton                                                       # シングルトンがを返す

#=======================================================================================================
#   クラス ダミーREDEEM DBサーバーパラメータクラス
#=======================================================================================================
class DmyRdmDBSParameterClass(ParameterClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None

    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if DmyRdmDBSParameterClass._singleton is None:                                              # シングルトンが無いとき
                ParameterClass.__init__(self, GP.CONF_LOG.DMY_RDM_DBS )                                 # スーパークラスの初期化
                MYSQL_HOST    = '127.0.0.1'                                                             # MYSQL アドレス
                MYSQL_PORT    = 3306                                                                    # MYSQL ポート
                MYSQL_USER    = 'root'                                                                  # MYSQL ユーザー
                MYSQL_PASS    = 'rednoa'                                                                # MYSQL パスワード
                MYSQL_DB      = 'redeemdmy'                                                             # MYSQL DB名
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                   (name != '__pydevd_ret_val_dict')]                                   # ローカル変数名リストを作成
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                self.loadData()                                                                         # パラメータをログファイルから読込
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if DmyRdmDBSParameterClass._singleton is None:                                                  # シングルトンが無いとき
            DmyRdmDBSParameterClass._singleton = DmyRdmDBSParameterClass()                              # インスタンスを生成してシングルトンにセット
        return DmyRdmDBSParameterClass._singleton                                                       # シングルトンがを返す

#=======================================================================================================
#   クラス ユーザーパラメータクラス
#=======================================================================================================
class CommonParameterClass(ParameterClass):
    _singleton = None
    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if CommonParameterClass._singleton is None:                                                 # シングルトンが無いとき
                ParameterClass.__init__(self, GP.ANAL_LOG.COMMON)                                       # スーパークラスの初期化
                FETCH_BLOCK = 10000                                                                     # DB読込ブロック長
                CH_AGE_LEVEL = 0                                                                        # CH予測値表示フィルターレベル
                LN_AGE_LEVEL = 0                                                                        # LN予測値表示フィルターレベル
                SERVER = GP.SERVER.LOC_RDM_DBS                                                          # サーバー選択
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                   (name != '__pydevd_ret_val_dict')]                                   # ローカル変数名リストを作成
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                self.loadData()                                                                         # パラメータをログファイルから読込
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if CommonParameterClass._singleton is None:                                                     # シングルトンが無いとき
            CommonParameterClass._singleton = CommonParameterClass()                                    # インスタンスを生成してシングルトンにセット
        return CommonParameterClass._singleton                                                          # シングルトンがを返す

#=======================================================================================================
#   クラス チャンバー年齢学習パラメータクラス
#=======================================================================================================
class LearnAgeParameterClass(ParameterClass):
    def __init__(self, logPath):                                                                        # 初期化
        try:
            ParameterClass.__init__(self, logPath)                                                      # スーパークラスの初期化
            AGE_BASE      = GP.AGE_BASE.TARGET                                                          # 年齢基準
            HIDDEN_LAYERS = 5                                                                           # 隠れ層数
            DROPOUT       = 0.05                                                                        # ドロップアウト
            LEARN_PARTS   = GP.PARTS.CH                                                                 # 学習部品
            LEARN_UNIT    = GP.LEARN_UNIT.TYPE_ID                                                       # 学習単位
            USE_ABNORMAL  = False                                                                       # 異常値使用フラグ
            SAVE_FLAG     = False                                                                       # 保存フラグ
            SAMPLES       = 10000                                                                       # ラベル毎のデータ数
            SAMPLE_RATIO_0 = 0.7                                                                        # 上位のデータサンプル割合）
            SAMPLE_RATIO_N = 0.9                                                                        # 次回以後上位のデータサンプル割合）
            INIT_EPOCHS   = 30                                                                          # 初期エポック数
            CUT_EPOCHS    = 30                                                                          # カットエポック数
            CUT_TRIALS    = 4                                                                           # カット回数
            BATCH_SIZE    = 100                                                                         # バッチサイズ
            VERBOSE       = 0                                                                           # VERBOSE
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                                (name != 'logPath') and
                                (name != '__pydevd_ret_val_dict')]                                      # ローカル変数名リストを作成
            for objectName in self.nameList:                                                            # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)                                         # オブジェクトのインスタンス変数のセット
            self.loadData()                                                                             # パラメータをログファイルから読込
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

#=======================================================================================================
#   クラス チャンバー年齢学習パラメータクラス
#=======================================================================================================
class AgeLearnParameterClass(LearnAgeParameterClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None
    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if AgeLearnParameterClass._singleton is None:                                               # シングルトンが無いとき
                LearnAgeParameterClass.__init__(self, GP.LEARN_LOG.AGE_LEARN)                           # スーパークラスの初期化
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if AgeLearnParameterClass._singleton is None:                                                   # シングルトンが無いとき
            AgeLearnParameterClass._singleton = AgeLearnParameterClass()                                # インスタンスを生成してシングルトンにセット
        return AgeLearnParameterClass._singleton                                                        # シングルトンがを返す

#=======================================================================================================
#   クラス チャンバーイベント学習パラメータクラス
#=======================================================================================================
class EvtLearnParameterClass(ParameterClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None

    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if EvtLearnParameterClass._singleton is None:                                               # シングルトンが無いとき
                ParameterClass.__init__(self, GP.LEARN_LOG.EVT_LEARN)                                   # スーパークラスの初期化
                SAMPLE_RATIO_0 = 0.3                                                                    # 上位のデータサンプル割合）
                SAMPLE_RATIO_N = 0.1                                                                    # 次回以後上位のデータサンプル割合）
                ABN_LEN = 200                                                                           # 異常データサンプル数(最後からのサンプル数)
                ABN_SAMPLE = 3000                                                                       # REG以外のラベル毎のデータ数
                EPOCHS = [500,200]                                                                      # エポック数
                HIDDEN_LAYERS = 10                                                                      # 隠れ層数
                LEARN_UNIT = GP.LEARN_UNIT.TYPE_ID                                                          # 学習単位
                NRM_LEN = 1000                                                                          # 正常データサンプル数（ランダムサンプル数）
                NRM_SAMPLE = 6000                                                                       # チャンバー定期交換ラベル(REG)のデータ数
                SAVE_FLAG = False                                                                       # 保存フラグ
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                   (name != '__pydevd_ret_val_dict')]                                   # ローカル変数名リストを作成
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                self.loadData()                                                                         # パラメータをログファイルから読込
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if EvtLearnParameterClass._singleton is None:                                                   # シングルトンが無いとき
            EvtLearnParameterClass._singleton = EvtLearnParameterClass()                                # インスタンスを生成してシングルトンにセット
        return EvtLearnParameterClass._singleton                                                        # シングルトンがを返す

