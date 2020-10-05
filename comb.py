import os
import datetime
import math
import numpy as np
import csv
from staticImport import *
from gpiBase import *
from PyQt5Import import *
from commonBase import CommonBaseClass

#=======================================================================================================
#   クラス　CombClass
#=======================================================================================================
class CombClass():
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None                                                                                   # シングルトン初期化

    #---------------------------------------------------------------------------------------------------
    #   初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if CombClass._singleton is None:                                                            # クラス変数の_singletonの有無を確認
                # オブジェクト生成
                PEX     = PartsExchangeClass  (GP.CONT.COMB_CONF.PEX)                                   # PEX生成
                PWB     = PlotWPlotClass      (GP.CONT.COMB_CONF.PWB)                                   # PWB生成
                ERM     = ErrorMasterClass    (GP.CONT.COMB_CONF.ERM)                                   # ERM生成
                GFP     = GasFilPeriodClass   (GP.CONT.COMB_CONF.GFP)                                   # GFP生成
                RPB     = ReplacementBaseClass(GP.CONT.COMB_CONF.RPB)                                   # RPB生成
                LST     = LaserTypeClass      (GP.CONT.COMB_CONF.LST)                                   # LST生成
                # オブジェクトのインスタンス変数のセット
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                    (name != '__pydevd_ret_val_dict')]                                  # ローカル変数名リストを作成
                self.objectList = []                                                                    # オブジェクトリスト初期化
                self.tableList = []                                                                     # テーブル名リスト初期化
                self.objectDic = {}                                                                     # オブジェクト辞書初期化
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                    exec("self.objectList += [self." + objectName + "]")                                # オブジェクトリストに追加
                    exec("self.tableList += [self." + objectName + ".TABLE_NAME]")                      # テーブル名リストに追加
                    exec("self.objectDic[self." + objectName + ".TABLE_NAME] = self." + objectName)     # オブジェクト辞書に追加
                # すべてのオブジェクトのインスタンス変数をセットする
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    for name in self.nameList:                                                          # オブジェクト名リストをすべて実行
                        exec("self." + objectName + "." + name + " = self." + name)                     # オブジェクトをインスタンス変数に転写する
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if CombClass._singleton is None:                                                                # クラス変数の_singletonの有無を確認
            CombClass._singleton = CombClass()                                                          # クラスを生成して_singletonにセット
        return CombClass._singleton                                                                     # _singletonを返す

    #---------------------------------------------------------------------------------------------------
    #   オブジェクトリストを返す
    #---------------------------------------------------------------------------------------------------
    def getObjectList(self, DBSDIR, TABLE_NAME):
        try:
            objectList = []                                                                             # オブジェクトリスト
            for objectName in self.nameList:                                                            # オブジェクト名リストをすべて実行
                exec("self.object = self." + objectName)                                                # オブジェクトを転写する
                if (DBSDIR == self.object.DBSDIR):                                                      # 選択されたテーブル名がオブジェクトのテーブル名かALLの時
                    if (TABLE_NAME == self.object.TABLE_NAME) or (TABLE_NAME == GP.ALL):                # 選択されたテーブル名がオブジェクトのテーブル名かALLの時
                        objectList += [self.object]                                                     # オブジェクトリストに追加
            return objectList                                                                           # オブジェクトリスト を返す

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   すべてのオブジェクトのインスタンス変数をセットする
    #---------------------------------------------------------------------------------------------------
    def setClassVar(self, laserIdList, parameter):
        try:
            parameter.setClassVar(self)                                                                 # メンバーのパラメータデータをセット
            self.MY_LASER_LIST = laserIdList                                                            # レーザーIDリストを転写
            for objectName in self.nameList:                                                            # オブジェクト名リストをすべて実行
                exec("self.object = self." + objectName)                                                # オブジェクトを転写する
                parameter.setClassVar(self.object)                                                      # メンバーのパラメータデータをセット
                self.object.MY_LASER_LIST = laserIdList                                                 # メンバーのレーザーIDリストを転写
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

#=======================================================================================================
#   スーパークラス　COMBベースクラス
#=======================================================================================================
class CombBaseClass(CommonBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        CommonBaseClass.__init__(self, TABLE_NAME)                                                      # スーパークラスの初期化

    #---------------------------------------------------------------------------------------------------
    #   srcListにチャンバー交換期間を加えたピリオッド辞書を作成する。
    #---------------------------------------------------------------------------------------------------
    def extractPeriodDic(self, srcList, IDX, minLen, p=None):
        try:
            if self.periodBase is not None:
                self.startNewLevel(len(self.periodBase), p)                                             # 新しいレベルの進捗開始
                periodDic = {}                                                                          # ピリオッド辞書を初期化
                for (LASER_ID, PERIOD), periodData in self.periodBase.items():                          # ピリオッドベース辞書をすべて実行
                    if LASER_ID in srcList:                                                             # ソースリストをすべｔ実行
                        srcData = srcList[LASER_ID]                                                     # ソースレーザーデータを取得
                        begin = periodData[0,self.PERIOD_BEGIN_DATE_TIME]                               # ピリオッド開始ショット
                        end   = periodData[0,self.PERIOD_END_DATE_TIME]                                 # ピリオッド終了ショット
                        extract = srcData[(srcData[:,IDX] >= begin) & (srcData[:,IDX] < end)]           # ピリオッド内のインデックスを取得
                        if len(extract) > minLen:                                                       # インデックスが有る時
                            periodDic[LASER_ID, PERIOD] = extract                                       # ピリオッド辞書リストに登録
                    emit(p)                                                                             # 進捗バーにシグナルを送る
                return self.returnList(periodDic, p)                                                    # 実行時間を表示してからデータを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   テーブルからピリオッド単位でリストに読み込む
    #---------------------------------------------------------------------------------------------------
    def getField(self, source, LASER_ID, PERIOD, FIELD):
        try:
            periodData = self.getPeriodData(source, LASER_ID, PERIOD)                                   # レーザー辞書からピリオッドデータを取得
            if periodData is not None:                                                                  # レーザーIDがピリオッドデータに有る時
                fieldList = periodData[:, FIELD]                                                        # フィールドのリストを取得
                return fieldList                                                                        # フィールドのリストをを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   テーブルからピリオッド単位でリストに読み込む
    #---------------------------------------------------------------------------------------------------
    def getFieldList(self, source, LASER_ID, periodList, FIELD):
        try:
            fieldList = []
            for period in periodList:
                data = self.getField(source, LASER_ID, period, FIELD)
                if data is not None:
                    fieldList += list(data)
            if len(fieldList) == len(periodList):                                                       # レーザーIDがピリオッドデータに有る時
                return fieldList                                                                        # フィールドのリストをを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

#=======================================================================================================
#   クラス LaserTypeClass
#=======================================================================================================
class LaserTypeClass(CombBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        CombBaseClass.__init__(self, TABLE_NAME)                                                        # スーパークラスの初期化

    #---------------------------------------------------------------------------------------------------
    #   レーザーID単位でクエリーを実行してDBに挿入する。CSVファイもを作る
    #   ツリーの基本データなのでレーザーIDリストは使わない
    #---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            baseQuery = self.makeBaseQuery()                                                            # クエリーを作成
            GP.SVR.DBSServer.makeLocDBFromQuery(self, baseQuery, p)                                     # CSVファイルの作成に成功した時
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示

    #---------------------------------------------------------------------------------------------------
    #   クエリを作成
    #---------------------------------------------------------------------------------------------------
    def makeBaseQuery(self):
        try:
            query = QueryClass2("SELECT DISTINCT")
            query.add("BASE.LASER_ID as LASER_ID,")
            query.add("BASE.LASER_TYPE_ID as LASER_TYPE_ID,")
            query.add("LTM.TYPE_CODE as TYPE_CODE")
            query.add("FROM LASER_MST BASE")
            query.add("join LASER_TYPE_MST LTM")
            query.add("on LTM.LASER_TYPE_ID = BASE.LASER_TYPE_ID")
            return query                                                                                # クエリーを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   レーザー辞書からレーザータイプIDを返す
    #---------------------------------------------------------------------------------------------------
    def getLaserTypeId(self, LASER_ID):
        try:
            if self.laserBase is not None:                                                              # レーザーベースが有る時
                if LASER_ID in self.laserBase:                                                          # レーザーIDが有る時
                    data = self.laserBase[LASER_ID][0]                                                  # レーザーのデータ取得
                    TYPE_ID = data[self.LASER_TYPE_ID]                                                  # レーザータイプID取得
                    return TYPE_ID                                                                      # レーザータイプIDを返す
            self.showNone()                                                                            # None表示

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示

    #---------------------------------------------------------------------------------------------------
    #   タイプコードを返す
    #---------------------------------------------------------------------------------------------------
    def getTypeCode(self, LASER_ID):
        try:
            if self.laserBase is not None:                                                              # レーザーベースが有る時
                if LASER_ID in self.laserBase:                                                          # レーザーIDが有る時
                    data = self.laserBase[LASER_ID][0]                                                  # レーザーのデータ取得
                    typeCode = data[self.TYPE_CODE]                                                     # タイプコード取得
                    return typeCode                                                                     # タイプコードを返す
            self.showNone()                                                                            # None表示

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示

#=======================================================================================================
#   クラス ErrorMasterClass
#=======================================================================================================
class ErrorMasterClass(CombBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        CombBaseClass.__init__(self, TABLE_NAME)                                                        # スーパークラスの初期化

    #---------------------------------------------------------------------------------------------------
    #   LASER_IDとERROR_CODEをキーにしてPRD_ERROR内容を記載したDBを作成
    #---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            laserIdList = self.MY_LASER_LIST                                                            # レーザーIDリストを取得
            if laserIdList is not None:                                                                 # レーザーリストが有る時
                baseQuery = self.makeBaseQuery()                                                        # クエリーを作成
                GP.SVR.DBSServer.makeLocFilterDBFromQuery(self, baseQuery, laserIdList, p)              # CSVファイルの作成に成功した時
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示

    #---------------------------------------------------------------------------------------------------
    #   ErrorMaster作成クエリを作る
    #---------------------------------------------------------------------------------------------------
    def makeBaseQuery(self):
        try:
            query = QueryClass2("SELECT DISTINCT")
            query.add("BASE.LASER_ID as LASER_ID,")
            query.add("LASER_TYPE_MST.LASER_TYPE_ID as LASER_TYPE_ID,")
            query.add("PRD_ERROR.TYPE_CODE as TYPE_CODE,")
            query.add("CONCAT('E',PRD_ERROR.ERROR_CODE) as ERROR_CODE,")
            query.add("REPLACE(PRD_ERROR.DESCRIPTION,'\n',' ') as DESCRIPTION,")
            query.add("REPLACE(PRD_ERROR.ERROR_CONTENTS,'\n',' ') as ERROR_CONTENTS_EN,")
            query.add("REPLACE(PRD_ERROR.ERROR_CONTENTS_JP,'\n',' ') as ERROR_CONTENTS_JP,")
            query.add("PRD_ERROR.ERROR_MEASURES as ERROR_MEASURES_EN,")
            query.add("PRD_ERROR.ERROR_MEASURES_JP as ERROR_MEASURES_JP,")
            query.add("PRD_ERROR.ERROR_LEVEL as ERROR_LEVEL")
            query.add("FROM (SELECT LASER_ID,LASER_TYPE_ID FROM LASER_MST) BASE")
            query.add("JOIN (SELECT LASER_TYPE_ID,TYPE_CODE FROM LASER_TYPE_MST) LASER_TYPE_MST")
            query.add("ON LASER_TYPE_MST.LASER_TYPE_ID = BASE.LASER_TYPE_ID")
            query.add("JOIN (SELECT TYPE_CODE,ERROR_CODE,DESCRIPTION,ERROR_CONTENTS,ERROR_CONTENTS_JP,ERROR_MEASURES,ERROR_MEASURES_JP,ERROR_LEVEL FROM PRD_ERROR) PRD_ERROR")
            query.add("ON PRD_ERROR.TYPE_CODE = LASER_TYPE_MST.TYPE_CODE")
            return query                                                                                # クエリーを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   ErrorMaster作成クエリを作る
    #---------------------------------------------------------------------------------------------------
    def makeQueryErrorMaster(self):
        try:
            if self.MY_RANGE.start < self.MY_RANGE.stop:
                start = str(self.MY_RANGE[0])                                                           # 開始レーザーID
                end = str(self.MY_RANGE[-1])                                                            # 終了レーザーID
                query = QueryClass2("SELECT DISTINCT")
                query.add("LASER_MST.LASER_ID as LASER_ID,")
                query.add("LASER_TYPE_MST.LASER_TYPE_ID as LASER_TYPE_ID,")
                query.add("PRD_ERROR.TYPE_CODE as TYPE_CODE,")
                query.add("CONCAT('E',PRD_ERROR.ERROR_CODE) as ERROR_CODE,")
                query.add("PRD_ERROR.DESCRIPTION as DESCRIPTION,")
                query.add("PRD_ERROR.ERROR_CONTENTS as ERROR_CONTENTS_EN,")
                query.add("PRD_ERROR.ERROR_CONTENTS_JP as ERROR_CONTENTS_JP,")
                query.add("PRD_ERROR.ERROR_MEASURES as ERROR_MEASURES_EN,")
                query.add("PRD_ERROR.ERROR_MEASURES_JP as ERROR_MEASURES_JP,")
                query.add("PRD_ERROR.ERROR_LEVEL as ERROR_LEVEL")
                query.add("FROM LASER_MST LASER_MST")
                query.add("join LASER_TYPE_MST LASER_TYPE_MST")
                query.add("on LASER_TYPE_MST.LASER_TYPE_ID = LASER_MST.LASER_TYPE_ID")
                query.add("join .PRD_ERROR PRD_ERROR")
                query.add("on PRD_ERROR.TYPE_CODE = LASER_TYPE_MST.TYPE_CODE")
                query.add("WHERE LASER_ID BETWEEN " + start + " AND " + end)
                return query                                                                            # クエリーを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

#=======================================================================================================
#   クラス ReplacementBaseClass
#=======================================================================================================
class ReplacementBaseClass(CombBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        CombBaseClass.__init__(self, TABLE_NAME)                                                        # スーパークラスの初期化

    #---------------------------------------------------------------------------------------------------
    # レーザーID単位でクエリーを実行してDBに挿入する。CSVファイもを作る
    #---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            laserIdList = self.MY_LASER_LIST                                                            # レーザーIDリストを取得
            if laserIdList is not None:                                                                 # レーザーリストが有る時
                baseQuery = self.makeBaseQuery()                                                        # クエリーを作成
                GP.SVR.DBSServer.makeLocFilterDBFromQuery(self, baseQuery, laserIdList, p)              # CSVファイルの作成に成功した時
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示

    #---------------------------------------------------------------------------------------------------
    #   テーブルからレーザー単位で寿命リストを読み込む
    #---------------------------------------------------------------------------------------------------
    def makeBaseQuery(self):
        try:
            query = QueryClass2("SELECT DISTINCT")                                                      # クエリ作成
            query.add("BASE.LASER_ID AS LASER_ID,")                                                     # LASER_ID
            query.add("REPLACE(REPLACE(REPLACE(REPLACE(")                                               # REPLACE
            query.add("SUBSTRING_INDEX(")                                                               # SUBSTRING_INDEX
            query.add("REPLACE(MDM.PARTS_NAME,'.','')")                                                 # REPLACE
            query.add(",' ',1)")                                                                        # SUBSTRING_INDEX
            query.add(",'/'     ,''       )")                                                           # REPLACE
            query.add(",'WINDOW','WINDOWS')")                                                           # REPLACE
            query.add( ",'IF'   ,'IFC'    )")                                                           # REPLACE
            query.add( ",'-'    ,''       )")                                                           # REPLACE
            query.add( "as MODULE_ID,")                                                                 # MODULE_ID
            query.add("CASE WHEN RFLM.SETTING_LIMIT IS NULL THEN RFM.LIMITDEF")                         # クエリ作成
            query.add("ELSE RFLM.SETTING_LIMIT END AS SETTING_LIMIT,")                                  # SETTING_LIMIT
            query.add("CASE WHEN RFLM.SETTING_TARGET IS NULL THEN RFM.TARGET")                          # クエリ作成
            query.add("ELSE RFLM.SETTING_TARGET END AS SETTING_TARGET")                                 # SETTING_TARGET
            query.add("FROM LASER_MST AS BASE")                                                         # クエリ作成
            query.add("JOIN")                                                                           # クエリ作成
            query.add("(SELECT LASER_TYPE_ID,LIMITDEF,TARGET, MODULE_ID FROM REPLACEMENT_FORECAST_MST)")    # SELECT
            query.add("AS RFM")    # クエリ作成
            query.add("ON RFM.LASER_TYPE_ID = BASE.LASER_TYPE_ID")                                      # クエリ作成
            query.add("LEFT JOIN")                                                                      # ないかもしれないのでLEFT JOIN
            query.add("(SELECT LASER_ID,MODULE_ID,SETTING_LIMIT,SETTING_TARGET FROM REPLACEMENT_FORECAST_LASER_MST)")     # SELECT
            query.add("AS RFLM")                                                                        # ないかもしれないのでLEFT JOIN
            query.add("ON RFLM.LASER_ID = BASE.LASER_ID")                                               # クエリ作成
            query.add("AND RFLM.MODULE_ID = RFM.MODULE_ID")                                             # クエリ作成
            query.add("JOIN MODULE_MST AS MDM")                                                         # クエリ作成
            query.add("ON MDM.MODULE_ID = RFM.MODULE_ID")                                               # クエリ作成
            return query                                                                                # クエリを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # エラー表示
            return None

    #---------------------------------------------------------------------------------------------------
    #   指定したレーザーIDとモジュールIDのLIMITを返す
    #---------------------------------------------------------------------------------------------------
    def getLimit(self, LASER_ID, MODULE_ID):
        try:
            if LASER_ID in self.laserBase:                                                              # レーザーベース辞書に有る時
                limitList = self.laserBase[LASER_ID]                                                    # 寿命リスト
                limitMod = limitList[limitList[:,self.MODULE_ID] == MODULE_ID]                          # チャンバー寿命
                return limitMod[0,self.SETTING_LIMIT]                                                   # LIMITを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   指定したレーザーIDとモジュールIDのTARGETを返す
    #---------------------------------------------------------------------------------------------------
    def getTarget(self, LASER_ID, MODULE_ID):
        try:
            if LASER_ID in self.laserBase:                                                              # レーザーベース辞書に有る時
                limitList = self.laserBase[LASER_ID]                                                    # 寿命リスト
                limitMod = limitList[limitList[:,self.MODULE_ID] == MODULE_ID]                          # チャンバー寿命
                if len(limitMod) > 0:
                    return limitMod[0,self.SETTING_TARGET]                                              # TARGETを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   指定したレーザーIDとモジュールIDのレコードを返す
    #---------------------------------------------------------------------------------------------------
    def getModuleData(self, LASER_ID, MODULE_ID):
        try:
            if LASER_ID in self.laserBase:                                                              # レーザーベース辞書に有る時
                limitList = self.laserBase[LASER_ID]                                                    # 寿命リスト
                limitMod = limitList[limitList[:,self.MODULE_ID] == MODULE_ID]                          # チャンバー寿命
                return limitMod[0]                                                                      # チャンバーlimit
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return None                                                                                 # Noneを返す

#=======================================================================================================
#   クラス PlotWPlotClass
#=======================================================================================================
class PlotWPlotClass(CombBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        CombBaseClass.__init__(self, TABLE_NAME)                                                        # スーパークラスの初期化

    #---------------------------------------------------------------------------------------------------
    #   PLOTとWPLOTの合成DBを作成する
    #---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            laserIdList = self.MY_LASER_LIST                                                            # レーザーIDリストを取得
            if laserIdList is not None:                                                                 # レーザーリストが有る時
                baseQuery = self.makeBaseQuery()                                                        # クエリーを作成
                if GP.SVR.DBSServer.makeLocFilterDBFromQuery(self, baseQuery, laserIdList, p):          # CSVファイルの作成に成功した時
                    self.endLevel(p)                                                                    # 現レベルの終了
                    return
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示

    #---------------------------------------------------------------------------------------------------
    #   全部のレーザーのPLOTとWPLOTをマージしたSQL作成
    #---------------------------------------------------------------------------------------------------
    def makeBaseQuery(self):
        try:
            PLOT = GP.CONT.ORIGIN.PLOT
            WPLOT = GP.CONT.ORIGIN.WPLOT
            query = QueryClass()
            query.add("SELECT DISTINCT")
#            query += PLOT.tableDesc.getColumnList(self.tableDesc, "BASE")                        # クエリーにPLOTを追加
#            query += WPLOT.tableDesc.getColumnList(self.tableDesc,"WPLOT")                       # クエリーにWPLOTを追加
            query.add("BASE.LASER_ID as LASER_ID,")
            query.add("BASE.LOG_DATE_TIME as LOG_DATE_TIME,")
            query.add("CAST(BASE.TOTAL_SHOT as unsigned) as TOTAL_SHOT,")
            query.add("BASE.WL_ERROR as WL_ERROR,")
            query.add("BASE.WL_E_AVE as WL_E_AVE,")
            query.add("BASE.WL_E_SIGMA as WL_E_SIGMA,")
            query.add("BASE.BW_AVE as BW_AVE,")
            query.add("BASE.BANDWIDTH as BANDWIDTH,")
            query.add("BASE.PULSE_ENERGY as PULSE_ENERGY,")
            query.add("BASE.PRESENT_HV_VOLTAGE as PRESENT_HV_VOLTAGE,")
            query.add("BASE.CHAMB_PRESS as CHAMB_PRESS,")
            query.add("BASE.ENERGY_SIGMA as ENERGY_SIGMA,")
            query.add("BASE.F2_PARTIAL_PRS as F2_PARTIAL_PRS,")
            query.add("WPLOT.EX_MAX_C as EX_MAX_C,")
            query.add("WPLOT.EX_MAX_F as EX_MAX_F,")
            query.add("WPLOT.FWHMM as FWHMM,")
            query.add("WPLOT.WWLEN_F as WWLEN_F,")
            query.add("WPLOT.WWLEN_C as WWLEN_C")
            query.add("FROM PLOT BASE")
            query.add("INNER JOIN WPLOT WPLOT")
            query.add("on WPLOT.LASER_ID = BASE.LASER_ID")
            query.add("and WPLOT.LOG_DATE_TIME = BASE.LOG_DATE_TIME")
            return query                                                                                # クエリーを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   全部のレーザーのPLOTとWPLOTをマージしたSQL作成
    #---------------------------------------------------------------------------------------------------
    def makeFullQuery(self, filterList):
        try:
            PLOT = GP.CONT.ORIGIN.PLOT
            WPLOT = GP.CONT.ORIGIN.WPLOT
            query = "SELECT DISTINCT" + GP.CRLF
            query += PLOT.tableDesc.getBaseColumnName(self.tableDesc, "BASE", 0)                        # クエリーにPLOTを追加
            query += WPLOT.tableDesc.getBaseColumnName(self.tableDesc,"WPLOT", 2)                       # クエリーにWPLOTを追加
            query = (","+GP.CRLF).join(query) + GP.CRLF                                                        # ,と改行で結合する
            query += "FROM PLOT BASE" + GP.CRLF
            query += "inner join WPLOT WPLOT" + GP.CRLF
            query += "on WPLOT.LASER_ID = BASE.LASER_ID" + GP.CRLF
            query += "and WPLOT.LOG_DATE_TIME = BASE.LOG_DATE_TIME" + GP.CRLF
            whereQuery = self.makeFilterQuery(filterList)
            return query                                                                                # クエリーを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

#=======================================================================================================
#   クラス PartsExchangeClass
#=======================================================================================================
class PartsExchangeClass(CombBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        CombBaseClass.__init__(self, TABLE_NAME)                                                        # スーパークラスの初期化

    #---------------------------------------------------------------------------------------------------
    #   部品交換リストを作成する
    #---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(2, p)                                                                    # 新しいレベルの進捗開始
            laserIdList = self.MY_LASER_LIST                                                            # レーザーIDリストを取得
            if laserIdList is not None:                                                                 # レーザーリストが有る時
                if self.makeCsvFile(laserIdList, p):                                                    # CSVファイルの作成に成功した時
                    GP.SVR.DBSServer.makeLocDBFromObjectFile(self, p)                                   # オブジェクトファイルからローカルDBを作成
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   部品交換リストを作成する
    #---------------------------------------------------------------------------------------------------
    def makeCsvFile(self, filterList, p=None):
        try:
            self.startNewLevel(len(filterList), p)                                                      # 新しいレベルの進捗開始
            written = False                                                                             # 書き込み完了フラグを初期化
            written = False                                                                             # 書き込み完了フラグを初期化
            logPath = self.targetPath                                                                   # ファイルパス
            dirName = os.path.dirname(logPath)                                                          # ディレクトリ名
            if not os.path.exists(dirName):                                                             # ディレクトリの有無を確認
                os.makedirs(dirName)                                                                    # 途中のディレクトリを含めてディレクトリを作成
            with open(file=logPath,mode="w",encoding="utf-8") as f:                                     # "utf-8"でファイルをオープン
                writer = csv.writer(f, delimiter="\t", lineterminator='\n')                             # テーブルデスクリプションを書き込む
                writer.writerow(self.tableDesc.colName)                                                 # CSVライター設定
                channel, cursor = GP.SVR.DBSServer.openLocServer()                                      # ローカルサーバーをオープンしてcursorを取得
                baseQuery = self.makeBaseQuery()                                                        # ベースクエリを作る
                block = self.getFileBlock(self)                                                         # ファイルブロック長を取得
                blockList = []                                                                          # ブロックリスト初期化
                for LASER_ID in filterList:                                                             # ブロックをすべて実行
                    laserList = []                                                                      # レーザーリスト初期化
                    whereQuery = QueryClass()                                                           # クエリー生成
                    whereQuery.add("WHERE BASE.LASER_ID = " + str(LASER_ID))                            # BASEレーザーID
                    query = baseQuery.insertWhereQuery(whereQuery)                                      # WHEREクエリー挿入
                    query.execute(cursor)                                                               # クエリを実行する
                    dataList = cursor.fetchall()                                                        # すべて読み込みリストにする
                    for rowData in dataList:                                                            # データリストをすべて実行
                        rowData = list(rowData)                                                         # アイテムアサインメント用リスト化
                        partsName = GP.PARTS_NAME.getValidPartsName(rowData[self.PARTS_NAME])           # 有効部品名を取得
                        if partsName is not None:                                                       # 部品が有効な時
                            rowData[self.PARTS_NAME] = partsName                                        # 有効部品名をセット
                            if rowData[self.HAPPEN_DATE] is not None:                                   # 発生データが有る時
                                laserList += [rowData]                                                  # レーザーリストに追加
                    blockList +=laserList                                                               # ブロックリストに追加
                    if len(blockList) >= block:                                                         # ブロックリストにデータリストを加える
                        writer.writerows(blockList)                                                     # レーザーIDデータ書き込み
                        written = True                                                                  # 書き込み完了フラグを真にする
                        blockList.clear()                                                               # ブロックリストをクリア
                    self.deleteObject(dataList)                                                         # メモリーをクリア
                    emit(p)                                                                             # 進捗バーにシグナルを送る
                if len(blockList) > 0:
                    writer.writerows(blockList)                                                         # データリストをまとめて書き込み
                    written = True                                                                      # 書き込み完了フラグを真にする
                    self.deleteObject(blockList)                                                        # メモリーをクリア
                channel.close()                                                                         # DBをクローズ
                return self.returnResult(written, p)                                                    # 実行時間を表示してからデータを返す
            return self.returnResult(None, p)                                                           # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnResultError(e, p)                                                         # エラーを表示してからFalseを返す

    #---------------------------------------------------------------------------------------------------
    #   partsExchange作成クエリを作る
    #---------------------------------------------------------------------------------------------------
    def makeBaseQuery(self):
        try:
            SRPEX = GP.CONT.SRPEX
            LTM = GP.CONT.LTM
            query = QueryClass()
            query.add("SELECT DISTINCT")
            query.add("BASE.LASER_ID as LASER_ID,")
            query.add("BASE.LASER_TYPE_ID as LASER_TYPE_ID,")
            query.add("LTM.TYPE_CODE as TYPE_CODE,")
            query.add("IFNULL(SRPEX.INSTALLED_DATE,BASE.END_WORK) as HAPPEN_DATE,")
            query.add("BASE.SR_NO as JOB_NO,")
            query.add("SRPEX.PARTS_NAME as PARTS_NAME,")
            query.add("BASE.CLASS as CLASS,")
            query.add("IFNULL(BASE.SUBJECT_EN,BASE.SUBJECT_JP) as SUBJECT")
            query.add("FROM SR_MAIN BASE")
            query.add("JOIN (SELECT ")
            query.add("SR_NO,PARTS_NAME,INSTALLED_DATE")                                                # FIELDS
            query.add("FROM SR_PARTS_EXCHANGE_TRN) SRPEX")
            query.add("ON BASE.SR_NO = SRPEX.SR_NO")
            query.add("JOIN (SELECT ")
            query.add(LTM.tableDesc.getColumnList2())                                                   # FIELDS
            query.add("FROM LASER_TYPE_MST) LTM")
            query.add("ON LTM.LASER_TYPE_ID = BASE.LASER_TYPE_ID")
            return query

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   partsExchange作成クエリを作る
    #---------------------------------------------------------------------------------------------------
    def makeBaseQuery2(self):
        try:
            SRPEX = GP.CONT.SRPEX
            LTM = GP.CONT.LTM
            query = QueryClass()
            query.add("SELECT DISTINCT")
            query.add("BASE.LASER_ID as LASER_ID,")
            query.add("BASE.LASER_TYPE_ID as LASER_TYPE_ID,")
            query.add("LTM.TYPE_CODE as TYPE_CODE,")
            query.add("SRPEX.INSTALLED_DATE as HAPPEN_DATE,")
            query.add("0 AS HAPPEN_SHOT,")
            query.add("MAX(PWB.LOG_DATE_TIME) AS MAX_DATE,")
            query.add("MAX(PWB.TOTAL_SHOT) AS MAX_SHOT,")
            query.add("BASE.SR_NO as JOB_NO,")
            query.add("BASE.CLASS as CLASS,")
            query.add("SRPEX.PARTS_NAME as PARTS_NAME")
            query.add("FROM SR_MAIN BASE")
            query.add("JOIN (SELECT ")
            query.add(SRPEX.tableDesc.getColumnList2())                                                # FIELDS
            query.add("FROM SR_PARTS_EXCHANGE_TRN) SRPEX")
            query.add("ON BASE.SR_NO = SRPEX.SR_NO")
            query.add("JOIN (SELECT ")
            query.add(LTM.tableDesc.getColumnList2())                                                   # FIELDS
            query.add("FROM LASER_TYPE_MST) LTM")
            query.add("ON LTM.LASER_TYPE_ID = BASE.LASER_TYPE_ID")
            query.add("LEFT JOIN (SELECT LASER_ID, LOG_DATE_TIME, TOTAL_SHOT FROM COMB_PLOT_WPLOT) PWB")
            query.add("ON PWB.LASER_ID = BASE.LASER_ID")
            query.add("AND PWB.LOG_DATE_TIME <= SRPEX.INSTALLED_DATE")
            query.add("GROUP BY BASE.SR_NO")
            query.add("ORDER BY SRPEX.INSTALLED_DATE")
            return query

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   部品交換リストを再作成する
    #---------------------------------------------------------------------------------------------------
    def remakePexList(self, partsName, partsList):
        try:
            periods = len(partsList) + 1
            periodEndDateList = np.empty((periods),dtype = 'O')                                         # ピリオッドデータをオブジェクトタイプで初期化
            periodEndDateList[:-1] = partsList[:,self.HAPPEN_DATE]                                      # 次の行に前の行の発生日時をセット
            periodEndDateList[-1] = GP.MAX_DATE                                                         # 最終行にピリオッド終了日時セット
            PEX_DATA = []                                                                               # 部品交換リストを初期化
            PERIOD_END = []                                                                             # ピリオッド終リストを初期化
            if partsName == 'CH':                                                                       # 部品名が'CH'の時
                for i in range(periods):                                                                # 部品交換リストをすべて実行
                    periodEnd = periodEndDateList[i]                                                    # ピリオッド終了リストを取得
                    if i < periods - 1:
                        data = partsList[i]                                                                 # 部品交換リストをを取得
                        partsClass = data[self.CLASS]                                                   # クラスを取得
                        if partsClass != '01' and partsClass != '05':                                   # クラスが01と05で無い時
                            PEX_DATA += list([data])                                                    # 部品交換リストに追加
                            PERIOD_END += list([periodEnd])                                             # 部品交換リストに追加
                    else:
                        PERIOD_END += list([periodEnd])                                                 # 部品交換リストに追加
            elif partsName == 'F2T':
                for i in range(periods):                                                                # 部品交換リストをすべて実行
                    periodEnd = periodEndDateList[i]                                                    # ピリオッド終了リストを取得
                    if i < periods - 1:
                        data = partsList[i]                                                             # 部品交換リストをを取得
                        partsClass = data[self.CLASS]                                                   # クラスを取得
                        if partsClass != '01' and partsClass != '05':                                   # クラスが01と05で無い時
                            PEX_DATA += list([data])                                                    # 部品交換リストに追加
                            PERIOD_END += list([periodEnd])                                             # ピリオッド終リストに追加
                        PERIOD_END += list([periodEnd])                                                 # 部品交換リストに追加
            else:
                PEX_DATA = partsList                                                                    # 部品交換リストをセット
                PERIOD_END = periodEndDateList                                                          # ピリオッド終リストをセット
            return np.array(PEX_DATA,'O'), np.array(PERIOD_END,'O')                                     # 部品交換リストとピリオッド終リストを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return None

#=======================================================================================================
#   クラス GasFilPeriodClass
#=======================================================================================================
class GasFilPeriodClass(CombBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        CombBaseClass.__init__(self, TABLE_NAME)                                                        # スーパークラスの初期化

    #---------------------------------------------------------------------------------------------------
    # ガス交換期間番号と開始/終了時間を持ったDBを作成
    #---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(4, p)                                                                    # 新しいレベルの進捗開始
            if GP.CONT.GSF.loadLaserDic(p):                                                             # GSFレーザー辞書をDBから読み込む
                if self.makeCsvFile(p):                                                                 # CSVファイルの作成に成功した時
                    GP.SVR.DBSServer.makeLocDBFromObjectFile(self, p)                                   # オブジェクトファイルからローカルDBを作成
                GP.CONT.GSF.releaseBase(p)                                                              # メモリーの解放
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示

    #---------------------------------------------------------------------------------------------------
    #   CSVファイルの作成
    #---------------------------------------------------------------------------------------------------
    def makeCsvFile(self, p=None):
        try:
            GSF = GP.CONT.GSF                                                                           # GSFを転写
            self.startNewLevel(len(GSF.laserBase), p)                                                   # 新しいレベルの進捗開始
            written = False                                                                             # 書き込み完了フラグを初期化
            laserDic = {}                                                                               # レーザー辞書を初期化
            logPath = self.targetPath                                                                   # ファイルパス
            dirName = os.path.dirname(logPath)                                                          # ディレクトリ名
            if not os.path.exists(dirName):                                                             # ディレクトリの有無を確認
                os.makedirs(dirName)                                                                    # 途中のディレクトリを含めてディレクトリを作成
            with open(file=logPath,mode="w",encoding="utf-8") as f:                                     # "utf-8"でファイルをオープン
                writer = csv.writer(f, delimiter="\t", lineterminator='\n')                             # テーブルデスクリプションを書き込む
                writer.writerow(self.tableDesc.colName)                                                 # CSVライター設定
                for LASER_ID, GSF_Data in  GSF.laserBase.items():                                       # GSFレーザー辞書をすべて実行
                    INTERVAL_NO = 0                                                                     # インターバル番号を初期化
                    length = len(GSF_Data)                                                              # GSFレーザーデータの長さ
                    pData = np.empty((length + 1,self.END_SHOT+1),dtype = 'O')                          # ピリオッドデータをオブジェクトタイプで初期化
                    pData[:,self.LASER_ID] = LASER_ID                                                   # レーザーIDセット
                    pData[:,self.INTERVAL_NO] = np.array([np.arange(length+1)])                         # インターバル番号セット
                    pData[0,self.START_DATE_TIME] = GP.MIN_DATE                                         # 一行目の開始日時セット
                    pData[1:,self.START_DATE_TIME] = GSF_Data[:,GSF.LOG_DATE_TIME]                      # 二行目以降の開始日時セット
                    pData[:length,self.END_DATE_TIME] = GSF_Data[:,GSF.LOG_DATE_TIME]                   # 最終行の前の行までの終了日時をセット
                    pData[length,self.END_DATE_TIME] = GP.MAX_DATE                                      # 最終行の終了日時をセット
                    pData[0,self.START_SHOT] = 0                                                        # 一行目の開始ショットセット
                    pData[1:,self.START_SHOT] = GSF_Data[:,GSF.TOTAL_SHOT].astype('int')                # 二行目以降の開始ショットセット
                    pData[:length,self.END_SHOT] = GSF_Data[:,GSF.TOTAL_SHOT].astype('int')             # 最終行の前の行までの終了ショットをセット
                    pData[length,self.END_SHOT] = GP.MAX_SHOT                                           # 最終行の終了ショットをセット
                    writer.writerows(pData)                                                             # レーザーIDデータ書き込み
                    written = True                                                                      # 書き込み完了フラグを真にする
                    self.deleteObject(pData)                                                            # メモリーを解放
                    emit(p)                                                                             # 進捗バーにシグナルを送る
            return self.returnResult(written, p)                                                        # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnResultError(e, p)                                                         # エラーを表示してからFalseを返す

    #---------------------------------------------------------------------------------------------------
    #   チャンバーが突発終了したレーザーリスト作成
    #---------------------------------------------------------------------------------------------------
    def getChamberBreakList(self, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            channnel, cursor = self.openLocServer()                                                     # ローカルDBをオープンしてcursorを取得
            TABLE_NAME = self.TABLE_NAME                                                                # テーブル名を転写
            laserIdList = []                                                                            # レーザーIDリスト初期化
            if self.MY_RANGE.start < self.MY_RANGE.stop:
                start = str(self.MY_RANGE[0])                                                           # 開始レーザーID
                end = str(self.MY_RANGE[-1])                                                            # 終了レーザーID
                query = QueryClass2("SELECT DISTINCT LASER_ID,PERIOD,PERIOD_CLASS")                                 # クエリを作成する
                query.add("FROM " + TABLE_NAME + " WHERE PERIOD_CLASS != '00'")                         # クエリを作成する
                query.add("and LASER_ID BETWEEN " + start + " AND " + end)                              # クエリを作成する
                query.add("ORDER BY LASER_ID")                                                          # クエリを作成する
                query.execute(cursor)                                                                   # クエリを実行する
                rowData = cursor.fetchone()                                                             # 一行読み込む
                while rowData is not None:                                                              # データが有る限り繰り返す
                    laserIdList.append([int(rowData[0]), int(rowData[1]), rowData[2]])                  # レーザーIDリストにアペンド
                    rowData = cursor.fetchone()                                                         # 一行読み込む
                channnel.close()                                                                        # DBクローズ
            laserIdList = np.array(laserIdList,'O')                                                     # レーザーIDリストをオブジェクトタイプに変換
            return self.returnList(laserIdList)                                                         # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # 例外を表示

