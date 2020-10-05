from staticImport import *
#from classDef import *
from commonBase import CommonBaseClass

#=======================================================================================================
#   クラス　OriginClass
#=======================================================================================================
class OriginClass():
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None                                                                                   # シングルトンを初期化

    #---------------------------------------------------------------------------------------------------
    #   初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if OriginClass._singleton is None:                                                          # クラス変数の_singletonの有無を確認
                LSM    = CommonBaseClass(GP.CONT.ORIGIN_CONF.LSM  )                                     # LSM生成
                LTM    = CommonBaseClass(GP.CONT.ORIGIN_CONF.LTM  )                                     # LTM生成
                MDM    = CommonBaseClass(GP.CONT.ORIGIN_CONF.MDM  )                                     # MDM生成
                PRE    = CommonBaseClass(GP.CONT.ORIGIN_CONF.PRE  )                                     # PRE生成
                RFLM   = CommonBaseClass(GP.CONT.ORIGIN_CONF.RFLM )                                     # RFLM生成
                RFM    = CommonBaseClass(GP.CONT.ORIGIN_CONF.RFM  )                                     # RFM生成
                ERR    = CommonBaseClass(GP.CONT.ORIGIN_CONF.ERR  )                                     # ERR生成
                GSF    = GasFillClass   (GP.CONT.ORIGIN_CONF.GSF  )                                     # GSF生成
                PLOT   = CommonBaseClass(GP.CONT.ORIGIN_CONF.PLOT )                                     # PLO生成
                WPLOT  = CommonBaseClass(GP.CONT.ORIGIN_CONF.WPLOT)                                     # WPLOT生成
                SRM    = CommonBaseClass(GP.CONT.ORIGIN_CONF.SRM  )                                     # SRM生成
                SRPEX  = CommonBaseClass(GP.CONT.ORIGIN_CONF.SRPEX)                                     # SRPEX生成
                # オブジェクトのインスタンス変数のセット
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                    (name != '__pydevd_ret_val_dict')]                                  # ローカル変数名リストを作成
                self.objectList = []                                                                    # オブジェクトリスト初期化
                self.tableList = []                                                                     # テーブル名リスト初期化
                self.objectDic = {}                                                                     # オブジェクト辞書初期化
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクト名リストに追加
                    exec("self.objectList += [self." + objectName + "]")                                # オブジェクトリストに追加
                    exec("self.tableList += [self." + objectName + ".TABLE_NAME]")                      # テーブル名リストに追加
                    exec("self.objectDic[self." + objectName + ".TABLE_NAME] = self." + objectName)     # オブジェクト辞書に追加
                # すべてのオブジェクトのインスタンス変数をセットする
                for object in self.objectList:
                    for name in self.nameList:
                        exec("object." + name + " = self." + name)                                      # オブジェクトをインスタンス変数に転写する
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        try:
            if OriginClass._singleton is None:                                                          # インスタンス変数の_singletonの有無を確認
                OriginClass._singleton = OriginClass()                                                  # クラスを生成して_singletonにセット
            return OriginClass._singleton                                                               # _singletonを返す

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   すべてのオブジェクトのインスタンス変数をセットする
    #---------------------------------------------------------------------------------------------------
    def setClassVar(self, laserIdList, parameter):
        try:
            parameter.setClassVar(self)                                                                 # メンバーのパラメータデータをセット
            self.MY_LASER_LIST = laserIdList                                                            # レーザーツリーのレーザーIDリストを転写
            for objectName in self.nameList:                                                            # オブジェクト名リストをすべて実行
                exec("self.object = self." + objectName)                                                # オブジェクトを転写する
                parameter.setClassVar(self.object)                                                      # メンバーのパラメータデータをセット
                self.object.MY_LASER_LIST = laserIdList                                                 # メンバーのレーザーIDリストを転写
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

#=======================================================================================================
#   クラス GasFillClass
#=======================================================================================================
class GasFillClass(CommonBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        CommonBaseClass.__init__(self, TABLE_NAME)                                                      # スーパークラスの初期化


