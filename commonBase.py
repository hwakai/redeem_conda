import numpy as np
import datetime
import os
import time
import math
import csv
import MySQLdb as connector
from PyQt5Import import *
from staticImport import *
from kerasImport import *
import pickle
import gc
import copy
from gpiBase import *
from classDef import CommonParameterClass

#=======================================================================================================
#   共通スーパークラス　CommonBaseClass
#=======================================================================================================
class CommonBaseClass(GpiBaseClass):
    #---------------------------------------------------------------------------------------------------
    # 初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        try:
            GpiBaseClass.__init__(self, TABLE_NAME)                                                     # スーパークラスの初期化
            self.flatBase = None                                                                        # 事前読み込みフラットベース
            self.laserBase = None                                                                       # 作業用レーザーベース辞書
            self.periodBase = None                                                                      # 作業用ピリオッドベース辞書
            self.basePack = None                                                                        # 作業用ベースデータパック
            self.DB = None                                                                              # データベース

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示

    #---------------------------------------------------------------------------------------------------
    #   レーザー辞書からピリオッドデータを返す
    #---------------------------------------------------------------------------------------------------
    def getPeriodData(self, baseType, LASER_ID, PERIOD):
        try:
            if baseType == GP.BASE_TYPE.F_BASE:                                                         # ソースがフラットリストの時
                laserData= self.flatBase[self.flatBase[:,self.LASER_ID] == LASER_ID]                    # レーザデータ取得
                periodData = laserData[laserData[:,self.PERIOD] == PERIOD]                              # ピリオッドデータの取得
                if len(periodData) > 0:                                                                 # ピリオッドが有る時
                    return periodData                                                                   # ピリオッドデータを返す
            if baseType == GP.BASE_TYPE.L_BASE:                                                         # ソースがレーザー辞書の時
                if self.laserBase is not None:                                                          # レーザーベース辞書が有る時
                    if LASER_ID in self.laserBase:                                                      # レーザーIDの有無を確認
                        laserData = self.laserBase[LASER_ID]                                            # レーザーデータの取得
                        periodData = laserData[laserData[:,self.PERIOD] == PERIOD]                      # ピリオッドデータの取得
                        if len(periodData) > 0:                                                         # ピリオッドが有る時
                            return periodData                                                           # ピリオッドデータを返す
            elif baseType == GP.BASE_TYPE.P_BASE:                                                       # ソースがピリオッド辞書の時
                if self.periodBase is not None:                                                         # ピリオッドベース辞書が有る時
                    if (LASER_ID, PERIOD) in self.periodBase:                                           # レーザーIDの有無を確認
                        periodData = self.periodBase[LASER_ID, PERIOD]                                  # ピリオッドデータの取得
                        return periodData                                                               # ピリオッドデータを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #  レーザーIDリストを返す
    #---------------------------------------------------------------------------------------------------
    def getLaserIdList(self, baseType):
        try:
            laserIdList = None                                                                          # レーザーIDリストを初期化
            if baseType == GP.BASE_TYPE.F_BASE:                                                         # ソースがフラットベースの時
                if self.flatBase is not None:                                                           # フラットベースが有る時
                    laserIdList = self.flatBase[:,self.LASER_ID]                                        # レーザーIDリストを作成
            elif baseType == GP.BASE_TYPE.L_BASE:                                                       # ソースがレーザー辞書の時
                if self.laserBase is not None:                                                          # レーザー辞書が有る時
                    laserIdList = list(self.laserBase.keys())                                           # レーザーIDリストを作成
            elif baseType == GP.BASE_TYPE.P_BASE:                                                       # ソースがピリオッド辞書の時
                if self.periodBase is not None:                                                         # ピリオッド辞書が有る時
                    periodList = np.array(self.laserBase.keys(),'int')                                  # ピリオッドリストを作成
                    laserIdList = periodList[:,0]                                                       # レーザーIDリストを作成
            if laserIdList is not None:                                                                 # レーザーIDリストが有る時
                laserIdList = np.unique(laserIdList)                                                    # レーザーIDリストをユニークにする
                return np.array(laserIdList,'int')                                                      # レーザーIDリストを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   行データの読み込み
    #---------------------------------------------------------------------------------------------------
    def getDataPackByRow2(self, rowData, N):
        try:
            trainList = []
            if self.PRB.periodBase is not None:                                                         # CHPRAのピリオッドデータが有る時
                X_BASE = GP.X_LIST.X_BASE                                                               # Xベース転写
                TRN = GP.CONT.TRN                                                                       # TRNを転写
                BEGIN_INDEX = rowData[self.BEGIN_INDEX]                                                 # 開始インデックス
                END_INDEX = rowData[self.END_INDEX]                                                     # 終了インデックス
                BEGIN_INDEX = END_INDEX - N
                index = list(range(BEGIN_INDEX,END_INDEX+1))                                            #
                index = np.array(index,dtype='int')                                                     # ストリングをスプリットして指定された長さにカット
                LASER_ID = rowData[self.LASER_ID]                                                       # レーザーID取得
                PERIOD = rowData[self.PERIOD]                                                           # ピリオッド取得
                rdbData = self.PRB.periodBase[LASER_ID,PERIOD][0]                                       # CHPRAのデータを取得
                x_data = rdbData[self.PRB.TOTAL_SHOT:]                                                  # CHPRAのXデータを取得
                x_data = np.array([val.split(',') for val in x_data],dtype='O')[:,index]                # ストリングをスプリットしてインデックスデータを取得
                x_data[0:2] = np.array(x_data[0:2],dtype='int')                                         # ショットのタイプを'int'に変更
                x_data[2:] = np.array(x_data[2:],dtype='float32')                                       # ショット以外のタイプを'float32'に変換
                x_data = x_data.T                                                                       # x_dataを転置
                train = np.empty((len(x_data),TRN.LENGTH),dtype = 'O')                                  # trainデータをオブジェクトタイプで初期化
                train[:,TRN.LASER_ID:TRN.LABEL] = rowData[self.LASER_ID:self.HAPPEN_SHOT]               # LASER_ID,PERIOD,PERIOD_CLASS,VALIDをセット
                train[:,TRN.LABEL] =rowData[self.CAUSE]                                                 # ラベルをセット
                train[:,TRN.HAPPEN_SHOT:X_BASE] = x_data[:,0:2]                                         # 発生ショットをセット
                train[:,X_BASE:] = x_data[:,2:]                                                         # Xデータをセット
                trainList = list(train)
            return trainList                                                                            # トレインリストを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return []                                                                                   # トレインリストを返す

    #=======================================================================================================
    #   ファイルからフラットなリストに読み込む
    #=======================================================================================================
    def CsvFileToList(self, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            strPath = self.targetPath                                                                   # ファイルパス
            tableDesc = self.tableDesc                                                                  # テーブルデスクリプション
            dataList = emptyList(tableDesc.columnNr)                                                    # コンケート用の初期 NUMPY 配列を作成する
            with open(file=strPath,mode="r",encoding="utf-8") as file:                                  # "utf-8"でファイルをオープン
                strLine = file.readline()                                                               # headerを読み飛ばす
                strLine = file.readline()                                                               # 次の行からデータを読む
                while strLine != '':                                                                    # すべてのラインを実行
                    strLine = "".join(strLine.splitlines())                                             # 改行を削除
                    rowData = tableDesc.getRowData(strLine)                                             # DBデータをデスクリプションの定義に従って配列にセットする
                    dataList = np.concatenate([dataList, [rowData]])                                    # dataListに結合
                    strLine = file.readline()                                                           # 次の行からデータを読む
            return self.returnList(dataList)                                                            # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラー表示

    #---------------------------------------------------------------------------------------------------
    #   ファイルからフラットなリストをロード
    #---------------------------------------------------------------------------------------------------
    def loadListFromFile(self, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            strPath = self.targetPath                                                                   # ファイルパス
            self.flatBase = None                                                                        # ベースリストを初期化
            # ファイルが無かったら終了
            if os.path.exists(strPath):                                                                 # ファイルが有る時
                self.flatBase = self.CsvFileToList()                                                    # ファイルからフラットなリストに読み込む
            return self.returnList(self.flatBase)                                                       # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラー表示

    #---------------------------------------------------------------------------------------------------
    #   デスクトップサイズを返す
    #---------------------------------------------------------------------------------------------------
    def getDesktopSize(self):
        # 画面サイズを取得 (a.desktop()は QtWidgets.QDesktopWidget)
        desktop = QApplication.desktop()
        size = desktop.size()
        return size

    #---------------------------------------------------------------------------------------------------
    #   中央に表示
    #---------------------------------------------------------------------------------------------------
    def viewCenter(self):
        # 画面サイズを取得 (a.desktop()は QtWidgets.QDesktopWidget )
        desktop = QApplication.desktop()
        geometry = desktop.screenGeometry()
        framesize = self.frameSize()                                                                    # ウインドウサイズ(枠込)を取得
        # ウインドウの位置を指定
        self.move(geometry.width() / 2 - framesize.width() / 2, geometry.height() / 2 - framesize.height() / 2)

    #-------------------------------------------------------------------------------------------------------
    #   ベースリストからピリオッドデータを返す
    #-------------------------------------------------------------------------------------------------------
    def getLaserDicData(self, LASER_ID):
        try:
            if self.laserBase is not None:
                if LASER_ID in self.laserBase:
                    laserData = self.laserBase[LASER_ID]
                    return laserData
            return None

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #-------------------------------------------------------------------------------------------------------
    #   フラットベースからピリオッドデータを返す
    #-------------------------------------------------------------------------------------------------------
    def getFlatBaseData(self, LASER_ID):
        try:
            if self.flatBase is not None:                                                               # フラットベースが有る時
                laserData = self.flatBase[self.flatBase[:,self.LASER_ID] == LASER_ID]                   # レーザーデータ取得
                if len(laserData) > 0:                                                                  # レーザーデータが有る時
                    return laserData                                                                    # レーザーデータを返す
            return None                                                                                 # レーザーデータが無い時はNoneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   タイトルを返す
    #---------------------------------------------------------------------------------------------------
    def getMyTitle(self, train):
        try:
            TRN = GP.CONT.TRN                                                                           # TRNを転写
            PERIOD = train[TRN.PERIOD]                                                                  # ピリオッド取得
            LASER_ID = train[TRN.LASER_ID]                                                              # レーザーID取得
            title = str(LASER_ID) + "-" + str(PERIOD)                                                   # レーザーIDとピリオッド追加
            return title

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #    テーブルから指定したラベルリストのフラットなリストを読み込みフラットベースにセット
    #---------------------------------------------------------------------------------------------------
    def loadFlatListLabel(self, filterList, extractLabel, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            if filterList is not None:                                                                  # レーザーIDリストが有る時
                extractLabel = np.array(extractLabel, dtype='str')                                      # ストリングのnumpy配列に変換
                extractStr = "'" + "','".join(extractLabel) + "'"                                       # 抽出ストリングを作成
                query = self.makeObjectQuery(self)                                                      #  オブジェクトのフィールド名からセレクトクエリーを作成
                query += "WHERE BASE.CAUSE IN (" + extractStr + ")"                                     # クエリを作成
                self.flatBase = GP.SVR.DBSServer.makeLocFlatListFromQuery(self, query, filterList, p)   # フラットベースをセット
                return self.returnList(self.flatBase, p)                                                # 実行時間を表示してからデータを返す
            return self.returnNone(p)                                                                   # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    #---------------------------------------------------------------------------------------------------
    #   テーブルから指定したレーザーIDのデータを読み込む
    #---------------------------------------------------------------------------------------------------
    def getLaserData(self, laserId, p=None):
        try:
            query = self.makeObjectQuery(self)                                                          #  オブジェクトのフィールド名からセレクトクエリーを作成
            query.add(" WHERE BASE.LASER_ID = " + str(laserId))                                         # クエリ作成
            flatList = GP.SVR.DBSServer.getLocFlatListFromQuery(self, query, p)                         # フラットリストを取得
            return flatList                                                                             # フラットリストを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return None

    #---------------------------------------------------------------------------------------------------
    #   テーブルから指定したレーザーIDのデータを読み込む
    #---------------------------------------------------------------------------------------------------
    def getShotList(self, filterList, p=None):
        try:
            query = QueryClass()
            query.add("SELECT DISTINCT")                                                                # SELECT
            query.add("BASE.LASER_ID,")                                                                 # LASER_ID
            query.add("BASE.LOG_DATE_TIME,")                                                            # LOG_DATE_TIME
            query.add("CAST(BASE.TOTAL_SHOT AS UNSIGNED)")                                              # TOTAL_SHOT
            query.add("FROM " + self.TABLE_NAME + " BASE")                                              # FROM
            flatList = GP.SVR.DBSServer.getLocFilterFlatListFromQuery(self, query, filterList, p)       # フラットリストを取得
            return flatList                                                                             # フラットリストを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return None

    #---------------------------------------------------------------------------------------------------
    #   テーブルから指定したレーザーIDのデータを読み込む
    #---------------------------------------------------------------------------------------------------
    def getShotData2(self, laserId, p=None):
        try:
            query = QueryClass()
            query.add("SELECT DISTINCT")                                                                # SELECT
            query.add("LASER_ID,")                                                                      # LASER_ID
            query.add("CAST(TOTAL_SHOT AS UNSIGNED)")                                                   # TOTAL_SHOT
            query.add("FROM " + self.TABLE_NAME)                                                        # FROM
            query.add(" WHERE LASER_ID = " + str(laserId))                                              # クエリ作成
            flatList = GP.SVR.DBSServer.getLocFlatListFromQuery(self, query, p)                         # フラットリストを取得
            return flatList                                                                             # フラットリストを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return None

    #---------------------------------------------------------------------------------------------------
    #   テーブルからフラットリストを読み込みフラットベースにセットする
    #---------------------------------------------------------------------------------------------------
    def loadFlatBase(self, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            query = self.makeObjectQuery(self)                                                          #  オブジェクトのフィールド名からセレクトクエリーを作成
            filterList = self.MY_LASER_LIST                                                             # レーザーIDリスト
            if filterList is not None:                                                                  # レーザーIDリストが有る時
                self.flatBase = GP.SVR.DBSServer.getLocFilterFlatListFromQuery(self, query, filterList, p)       # レーザーベース辞書をセット
                if self.flatBase is not None:                                                           # レーザーベース辞書が有る時
                    return self.returnResult(True, p)                                                   # 実行時間を表示してからデータを返す
            return self.returnResult(False, p)                                                          # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    #---------------------------------------------------------------------------------------------------
    #   テーブルからレーザー単位でリストに読み込みlaserBaseにセットする
    #---------------------------------------------------------------------------------------------------
    def loadLaserDic(self, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            query = self.makeObjectQuery(self)                                                          #  オブジェクトのフィールド名からセレクトクエリーを作成
            filterList = self.MY_LASER_LIST                                                             # レーザーIDリスト
            if filterList is not None:                                                                  # レーザーIDリストが有る時
                self.laserBase = GP.SVR.DBSServer.getLocFilterLaserDicFromQuery(self, query, filterList, p)   # レーザーベース辞書をセット
                if self.laserBase is not None:                                                          # レーザーベース辞書が有る時
                    return self.returnResult(True, p)                                                   # 実行時間を表示してからデータを返す
            return self.returnResult(False, p)                                                          # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    #---------------------------------------------------------------------------------------------------
    #   テーブルから単一のピリオッド辞書を読み込む
    #---------------------------------------------------------------------------------------------------
    def loadPeriodDicOne(self, periodId, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            laserId, period = periodId                                                                  # ピリオッドIDを展開
            query = self.makeObjectQuery(self)                                                          #  オブジェクトのフィールド名からセレクトクエリーを作成
            query.add(" WHERE BASE.LASER_ID = " + str(laserId))                                         # レーザーID
            query.add(" AND BASE.PERIOD = " + str(period))                                              # ピリオッド
            self.periodBase = GP.SVR.DBSServer.getLocPeriodDicFromQuery(self, query, p)                 # ピリオッドベース辞書をセット
            return self.returnList(self.periodBase, p)                                                  # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    #---------------------------------------------------------------------------------------------------
    # テーブルからピリオッド辞書を読み込む
    #---------------------------------------------------------------------------------------------------
    def loadPeriodDic(self, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            query = self.makeObjectQuery(self)                                                          #  オブジェクトのフィールド名からセレクトクエリーを作成
            laserIdList = self.MY_LASER_LIST                                                            # レーザーIDリストを取得
            if laserIdList is not None:                                                                 # レーザーIDリストが有る時
                self.periodBase = GP.SVR.DBSServer.getFilterLocPeriodDicFromQuery(self, query, laserIdList, p)   # ピリオッドベース辞書をセット
            return self.returnList(self.periodBase, p)                                                  # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    #---------------------------------------------------------------------------------------------------
    # テーブルからピリオッド辞書を読み込む
    #---------------------------------------------------------------------------------------------------
    def loadPeriodDicList(self, laserIdList, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            query = self.makeObjectQuery(self)                                                          #  オブジェクトのフィールド名からセレクトクエリーを作成
            if laserIdList is not None and query is not None:                                           # レーザーIDリストが有る時
                self.periodBase = GP.SVR.DBSServer.getFilterLocPeriodDicFromQuery(self, query, laserIdList, p)   # ピリオッドベース辞書をセット
            return self.returnList(self.periodBase, p)                                                  # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    #---------------------------------------------------------------------------------------------------
    #   テーブルから排他的なピリオッド辞書を取得する
    #---------------------------------------------------------------------------------------------------
    def loadPeriodDicExtract(self, extractLabel, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            extractLabel = np.array(extractLabel, dtype='str')                                          # ストリングのnumpy配列に変換
            extractStr = "'" + "','".join(extractLabel) + "'"                                           # 抽出ストリングを作成
            query = self.makeObjectQuery(self)                                                          # オブジェクトのフィールド名からセレクトクエリーを作成
            query += "WHERE BASE.CAUSE IN (" + extractStr + ")"+GP.CRLF                                     # クエリを作成
            laserIdList = self.MY_LASER_LIST                                                            # レーザーIDリストを取得
            if laserIdList is not None:                                                                 # レーザーIDリストが有る時
                self.periodBase = GP.SVR.DBSServer.getFilterLocPeriodDicFromQuery(self, query, laserIdList, p)   # ピリオッドベース辞書をセット
            return self.returnList(self.periodBase, p)                                                  # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    #---------------------------------------------------------------------------------------------------
    #   トレインデータからXデータを正規化して返す
    #---------------------------------------------------------------------------------------------------
    def normalize(self, train, MINMAX):
        try:
            X_BASE = GP.X_LIST.X_BASE                                                                   # Xベース転写
            if len(train) > 0:                                                                          # データパックが有る時                                                                     # データパックが有る時
                min = MINMAX.MINVAL                                                                     # 列毎の最小値
                max = MINMAX.MAXVAL                                                                     # 列毎の最大値
                if min is not None and max is not None:
                    deff = max[X_BASE:] - min[X_BASE:]                                                  # 差分
                    deff = np.where(deff==0,1.0,deff)                                                   # 差分が0の時は1.0にする
                    normal = (train[:,X_BASE:] - min[X_BASE:])/ deff                                    # Xデータを正規化
                    return normal                                                                       # 正規化データを返す
            return None                                                                                 # Noneを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   ベース変数を削除してメモリーを解放する
    #---------------------------------------------------------------------------------------------------
    def releaseBase(self, p=None):
        try:
            if self.flatBase is not None:                                                               # フラットベースが有る時
                del self.flatBase                                                                       # フラットベースを削除
                self.flatBase = None                                                                    # フラットベースを初期化する

            if self.laserBase is not None:                                                              # レーザー辞書が有る時
                del self.laserBase                                                                      # レーザー辞書を削除
                self.laserBase = None                                                                   # レーザー辞書を初期化する

            if self.periodBase is not None:                                                             # ピリオッド辞書が有る時
                del self.periodBase                                                                     # ピリオッド辞書を削除
                self.periodBase = None                                                                  # ピリオッド辞書を初期化する
            gc.collect()                                                                                # メモリーを解放する
            emit(p)                                                                                     # 進捗を進める

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # エラー表示

#=======================================================================================================
#   クラス Qオブジェクトパッククラス
#=======================================================================================================
class QObjectPackClass():
    def __init__(self, qObject, method, vaType, no=0):                                                  # 初期化
        self.qObject = qObject                                                                          # Qオブジェクトを転写
        self.method = method                                                                            # メソッド名を転写
        self.varType = vaType                                                                           # 変数タイプを転写
        self.no = no                                                                                    # 番号を転写


