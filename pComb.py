import datetime
import math
import numpy as np
import os
import csv
from sshtunnel import SSHTunnelForwarder
# from numba.decorators import jit
from staticImport import *
from PyQt5Import import *
from classDef import *
from qtBase import ProgressWindowClass
from comb import CombBaseClass
from commonBase import CommonBaseClass
from comb import CombClass
from origin import OriginClass
from gpiBase import *
from numpy import random


# =======================================================================================================
#   クラス　PCombClass
# =======================================================================================================
class PCombClass():
    # ---------------------------------------------------------------------------------------------------
    #   クラス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None  # シングルトン初期化

    # ---------------------------------------------------------------------------------------------------
    #   初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self):  # 初期化
        try:
            if PCombClass._singleton is None:  # クラス変数の_singletonの有無を確認
                # オブジェクト生成
                CH = PartsCombClass(GP.PCONT.CH)  # CH生成
                LN = PartsCombClass(GP.PCONT.LN)  # LN生成
                PPM = PartsCombClass(GP.PCONT.PPM)  # PPM生成
                MM = PartsCombClass(GP.PCONT.MM)  # MM生成
                # オブジェクトのインスタンス変数のセット
                self.nameList = [name for name in locals().keys()
                                 if (name != 'self') and
                                 (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
                self.objectList = []  # オブジェクトリスト初期化
                for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
                    exec("self.objectList += [self." + objectName + "]")  # オブジェクトリストに追加
                # すべてのオブジェクトのインスタンス変数をセットする
                #                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                #                    for name in self.nameList:                                                          # オブジェクト名リストをすべて実行
                #                        exec("self." + objectName + "." + name + " = self." + name)                     # オブジェクトをインスタンス変数に転写する
                pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if PCombClass._singleton is None:  # クラス変数の_singletonの有無を確認
            PCombClass._singleton = PCombClass()  # クラスを生成して_singletonにセット
        return PCombClass._singleton  # _singletonを返す

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトリストを返す
    # ---------------------------------------------------------------------------------------------------
    def getObjectList(self, DBSDIR, TABLE_NAME):
        try:
            objectList = []  # オブジェクトリスト
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self.object = self." + objectName)  # オブジェクトを転写する
                if (DBSDIR == self.object.DBSDIR):  # 選択されたテーブル名がオブジェクトのテーブル名かALLの時
                    if (TABLE_NAME == self.object.TABLE_NAME) or (
                            TABLE_NAME == GP.ALL):  # 選択されたテーブル名がオブジェクトのテーブル名かALLの時
                        objectList += [self.object]  # オブジェクトリストに追加
            return objectList  # オブジェクトリスト を返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   すべてのオブジェクトのインスタンス変数をセットする
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self, laserIdList, parameter):
        try:
            parameter.setClassVar(self)  # メンバーのパラメータデータをセット
            self.MY_LASER_LIST = laserIdList  # レーザーIDリストを転写
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self.object = self." + objectName)  # オブジェクトを転写する
                parameter.setClassVar(self.object)  # メンバーのパラメータデータをセット
                self.object.MY_LASER_LIST = laserIdList  # メンバーのレーザーIDリストを転写
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# =======================================================================================================
#   クラス　PartsPartsBaseClass
# =======================================================================================================
class PartsPartsBaseClass(CombBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        CombBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化

    # ---------------------------------------------------------------------------------------------------
    # チャンバー交換期間情報DBを作成
    # ---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(6, p)  # 新しいレベルの進捗開始
            RPB = GP.CONT.RPB  # RPBの転写
            PEX = GP.CONT.PEX  # PEXを転写
            if PEX.loadLaserDic(p):  # PEXレーザー辞書読込に成功した時
                if RPB.loadLaserDic(p):  # RPBレーザー辞書読込に成功した時
                    if self.makeCsvFile(GP.CURPARTS.LABEL.ORG, self.MY_LASER_LIST, p):  # CSVファイルの作成に成功した時
                        GP.SVR.DBSServer.makeLocDBFromObjectFile(self, p)  # オブジェクトファイルからローカルDBを作成
                    RPB.releaseBase(p)  # メモリーの解放
                PEX.releaseBase(p)  # メモリーの解放
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e, p)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   部品交換期間ベースを作成
    # ---------------------------------------------------------------------------------------------------
    def makeCsvFile(self, partsName, filterList, p=None):
        try:
            self.startNewLevel(len(filterList), p)  # 新しいレベルの進捗開始
            PEX = GP.CONT.PEX  # PEXを転写
            RPB = GP.CONT.RPB  # RPBの転写
            MODULE_ID = GP.CURPARTS.LABEL.ORG  # モジュールID
            written = False  # 書き込み完了フラグを初期化
            logPath = self.targetPath  # ファイルパス
            if logPath is not None:
                dirName = os.path.dirname(logPath)  # ディレクトリ名
                if not os.path.exists(dirName):  # ディレクトリの有無を確認
                    os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
                block = self.getFileBlock(self)  # ファイルブロック長を取得
                blockList = []  # ブロックリスト初期化
                with open(file=logPath, mode="w", encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                    writer = csv.writer(f, delimiter="\t", lineterminator='\n')  # テーブルデスクリプションを書き込む
                    writer.writerow(self.tableDesc.colName)  # CSVライター設定
                    for LASER_ID in filterList:  # レーザーIDリストをすべて実行
                        periods = 1  # ピリオッド数の初期値を１にする
                        TARGET = RPB.getTarget(LASER_ID, MODULE_ID)  # ターゲット取得
                        if LASER_ID in PEX.laserBase:  # レーザーIDがPEXレーザーベースに有る時
                            PEX_laserData = PEX.laserBase[LASER_ID]  # PEXピリオッドリストを取得
                            LASER_TYPE_ID = PEX_laserData[0, PEX.LASER_TYPE_ID]  # レーザータイプIDを取得
                            TYPE_CODE = PEX_laserData[0, PEX.TYPE_CODE]  # レーザータイプIDを取得
                            partsList = PEX_laserData[PEX_laserData[:, PEX.PARTS_NAME] == partsName]  # PEXのパーツリストを取得
                            PEX_DATA, periodEndDateList = PEX.remakePexList(partsName, partsList)  # 部品交換リストを再作成する
                            periods = len(PEX_DATA) + 1  # 最終ピリオッドを加える
                            pData = np.empty((periods, self.LENGTH), dtype='O')  # ピリオッドデータをオブジェクトタイプで初期化
                            pData[:, self.LASER_ID] = LASER_ID  # レーザーIDセット
                            pData[:, self.LASER_TYPE_ID] = LASER_TYPE_ID  # レーザータイプIDセット
                            pData[:, self.TYPE_CODE] = TYPE_CODE  # タイプコードセット
                            pData[:, self.PERIOD] = np.array([np.arange(periods)])  # ピリオッドセット
                            pData[:, self.TARGET] = TARGET  # ピリオッドセット
                            pData[0, self.PERIOD_BEGIN_DATE_TIME] = GP.MIN_DATE  # 最初の行にピリオッド開始日時セット
                            pData[:, self.PERIOD_END_DATE_TIME] = periodEndDateList  # ピリオッド終了日時セット
                            pData[-1, self.PERIOD_CLASS] = '99'  # 最終行にピリオッドクラスセット
                            if periods > 1:  # ピリオッド数が2以上の時
                                pData[1:, self.PERIOD_BEGIN_DATE_TIME] = PEX_DATA[:,
                                                                         PEX.HAPPEN_DATE]  # 二番目以降の行にピリオッド開始日時セット
                                pData[:-1, self.PERIOD_CLASS] = PEX_DATA[:, PEX.CLASS]  # 最終行の前の行までピリオッドクラスセット
                            blockList += list(pData)  # ブロックリストに追加
                            if len(blockList) >= block:  # ブロックリストにデータリストを加える
                                writer.writerows(blockList)  # レーザーIDデータ書き込み
                                written = True  # 書き込み完了フラグを真にする
                                blockList.clear()  # ブロックリストをクリア
                            self.deleteObject(pData)  # メモリーを解放
                            emit(p)  # 進捗バーにシグナルを送る
                    if len(blockList) > 0:  # ブロックリストが有る時
                        writer.writerows(blockList)  # データリストをまとめて書き込み
                        written = True  # 書き込み完了フラグを真にする
                        self.deleteObject(blockList)  # メモリーをクリア
            return self.returnResult(written, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnResultError(e, p)  # エラーを表示してからFalseを返す

    # ---------------------------------------------------------------------------------------------------
    #   srcListにチャンバー交換期間を加えた辞書リストを作成する。
    # ---------------------------------------------------------------------------------------------------
    def extractPeriodShot(self, srcList, IDX, minLen, p=None):
        try:
            self.startNewLevel(len(self.flatBase), p)  # 新しいレベルの進捗開始
            laserDic = {}  # レーザー辞書を初期化
            for periodData in self.flatBase:  # レーザーベース辞書のすべてのレーザーを実行
                LASER_ID = periodData[self.LASER_ID]  # レーザーID取得
                PERIOD = periodData[self.PERIOD]  # ピリオッド取得
                if LASER_ID in srcList:  # ソースリストをすべて実行
                    srcData = srcList[LASER_ID]  # ソースレーザーデータを取得
                    begin = periodData[self.PERIOD_BEGIN_DATE_TIME]  # ピリオッド開始ショット
                    end = periodData[self.PERIOD_END_DATE_TIME]  # ピリオッド終了ショット開始
                    extract = srcData[(srcData[:, IDX] >= begin) & (srcData[:, IDX] <= end)]  # ピリオッド内のデータを取得
                    if len(extract) >= minLen:  # インデックス長が最小長以上の時
                        laserDic[LASER_ID, PERIOD] = extract  # ピリオッド辞書リストに登録
                emit(p)  # 進捗バーにシグナルを送る
            return self.returnList(laserDic, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す


# =======================================================================================================
#   スーパークラス ChPeriodBaseClass
# =======================================================================================================
class PartsPeriodBaseClass(CommonBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        CommonBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化

    # ---------------------------------------------------------------------------------------------------
    #   チャンバー交換期間を加えたPLOTとWPLOTの合成DBを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(2, p)  # 新しいレベルの進捗開始
            if self.makeCsvFile(p):  # COMB_PLOT_WPLOTに部品交換期間を加えたファイルを作成する
                GP.SVR.DBSServer.makeLocDBFromObjectFile(self, p)  # オブジェクトファイルからローカルDBを作成
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e, p)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   COMB_PLOT_WPLOTに部品交換期間を加えたファイルを作成する 実行時間 = 315.794346秒
    # ---------------------------------------------------------------------------------------------------
    def makeCsvFile(self, p=None):
        try:
            PTB = GP.CURPARTS.PTB  # PTBを転写
            PWB = GP.CONT.PWB  # PWBを転写
            IDX = 1  # PWB総ショット数インデックス
            LABEL = GP.CURPARTS.LABEL
            GP.SERVER.LOC_RDM_DBS
            DBSServer = GP.SVR.DBSServer  # DBサーバー
            laserIdList = GP.SVR.DBSServer.getLocLaserIdList(PWB, p)  # PWBのレーザーIDリストを取得
            laserIdList = laserIdList[np.in1d(laserIdList, self.MY_LASER_LIST)]  # 取得可能なレーザーIDリスト
            PTB_laserIdList = PTB.getLaserIdList(GP.BASE_TYPE.F_BASE)  # PTBのレーザーIDリストを取得
            laserIdList = laserIdList[np.in1d(laserIdList, PTB_laserIdList)]  # PTBのレーザーIDリストに有るものを抽出
            self.startNewLevel(len(laserIdList), p)  # 新しいレベルの進捗開始
            written = False  # 書き込み完了フラグを初期化
            logPath = self.targetPath  # ファイルパス
            dirName = os.path.dirname(logPath)  # ディレクトリ名
            if not os.path.exists(dirName):  # ディレクトリの有無を確認
                os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
            block = self.getFileBlock(self)  # ファイルブロック長を取得
            blockList = []  # ブロックリスト初期化
            with open(file=logPath, mode="w", encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                writer = csv.writer(f, delimiter="\t", lineterminator='\n')  # テーブルデスクリプションを書き込む
                writer.writerow(self.tableDesc.colName)  # CSVライター設定
                laserList = []  # レーザーリスト初期化
                for LASER_ID in laserIdList:  # レーザーリストをすべて実行
                    pwbList = PWB.getShotList([LASER_ID])  # コンブプロットベースのレーザーデータ取得
                    laserList.clear()  # レーザーリスト初期化
                    PTB_laserList = PTB.flatBase[PTB.flatBase[:, PTB.LASER_ID] == LASER_ID]  # PTBレーザーリストを取得
                    pData = np.empty((len(PTB_laserList), self.LENGTH), dtype='O')  # ピリオッドデータをオブジェクトタイプで初期化
                    pData[:, :self.TYPE_CODE + 1] = PTB_laserList[:, :PTB.TYPE_CODE + 1]  # レーザータイプコードまでをセット
                    pData[:, self.PERIOD] = PTB_laserList[:, PTB.PERIOD]  # ピリオッドセット
                    pData[:, self.PERIOD_CLASS] = PTB_laserList[:, PTB.PERIOD_CLASS]  # ピリオッドクラスセット
                    pData[:, self.VALID] = 1  # 有効フラグをセット
                    pData[:, self.CLASS] = PTB_laserList[:, PTB.PERIOD_CLASS]  # クラスセット
                    pData[:, self.TARGET] = PTB_laserList[:, PTB.TARGET]  # ターゲットセット
                    pData[:, self.BEGIN_DATE_TIME] = PTB_laserList[:, PTB.PERIOD_BEGIN_DATE_TIME]  # 開始日時
                    pData[:, self.END_DATE_TIME] = PTB_laserList[:, PTB.PERIOD_END_DATE_TIME]  # 終了日時
                    pData[:, self.CAUSE] = np.where(pData[:, self.PERIOD_CLASS] == '00', LABEL.REG, LABEL.ACC)  # 発生原因
                    pData[:, self.CAUSE] = np.where(pData[:, self.PERIOD_CLASS] == '99', LABEL.PDG,
                                                    pData[:, self.CAUSE])  # 発生原因
                    pData[:, self.ELEMENTS] = 0  # 要素数
                    for periodData in pData:  # PTBピリオッドベース辞書をすべて実行
                        PERIOD = periodData[self.PERIOD]
                        # 有効データフラグを設定する
                        begin = periodData[self.BEGIN_DATE_TIME]  # ピリオッド開始ショット
                        end = periodData[self.END_DATE_TIME]  # ピリオッド終了ショット開始
                        pwbData = pwbList[(pwbList[:, 1] >= begin) & (pwbList[:, 1] < end)]  # ピリオッド内のPWBデータを取得
                        ELEMENTS = len(pwbData)  # 要素数
                        pData[PERIOD, self.ELEMENTS] = ELEMENTS  # 要素数
                        if ELEMENTS == 0:  # PWBデータがない時
                            pData[PERIOD, self.VALID] = 0  # 無効にする
                            pData[PERIOD, self.BEGIN_DATE] = GP.INVALID_SHOT  # 開始日時
                            pData[PERIOD, self.BEGIN_SHOT] = -1  # 開始ショット
                            pData[PERIOD, self.END_DATE] = GP.INVALID_SHOT  # 終了日時
                            pData[PERIOD, self.END_SHOT] = -1  # 終了ショット
                        elif ELEMENTS <= self.MINLEN:  # インデックス長が最小長以下の時
                            pData[PERIOD, self.VALID] = 0  # 無効にする
                            pData[PERIOD, self.BEGIN_DATE] = pwbData[0, 1]  # 開始日時
                            if PERIOD == 0:
                                pData[PERIOD, self.BEGIN_SHOT] = 0  # 開始ショット
                            else:
                                pData[PERIOD, self.BEGIN_SHOT] = pwbData[0, 2]  # 開始ショット
                            pData[PERIOD, self.END_DATE] = pwbData[-1, 1]  # 終了日時
                            pData[PERIOD, self.END_SHOT] = pwbData[-1, 2]  # 終了ショット
                        else:  # インデックス長が最小長以上の時
                            pData[PERIOD, self.BEGIN_DATE] = pwbData[0, 1]  # 開始日時
                            if PERIOD == 0:
                                pData[PERIOD, self.BEGIN_SHOT] = 0  # 開始ショット
                            else:
                                pData[PERIOD, self.BEGIN_SHOT] = pwbData[0, 2]  # 開始ショット
                            pData[PERIOD, self.END_DATE] = pwbData[-1, 1]  # 終了日時
                            pData[PERIOD, self.END_SHOT] = pwbData[-1, 2]  # 終了ショット
                            BEGIN_DATE = pData[PERIOD, self.BEGIN_DATE]  # PWBデータ内開始日時
                            BEGIN_DATE_TIME = pData[PERIOD, self.BEGIN_DATE_TIME]  # PEX交換日時
                            days = (BEGIN_DATE - BEGIN_DATE_TIME).days  # 経過日数
                            if BEGIN_DATE_TIME != GP.MIN_DATE and days > 30:  # 開始日時とデータが有る開始日時の差が３０日以上の時
                                pData[PERIOD, self.VALID] = 0  # 無効にする
                            END_DATE = pData[PERIOD, self.END_DATE]  # PWBデータ内終了日時
                            END_DATE_TIME = pData[PERIOD, self.END_DATE_TIME]  # PEX交換日時
                            days = (END_DATE_TIME - END_DATE).days  # 経過日数
                            if END_DATE_TIME != GP.MAX_DATE and days > 30:  # 終了日時とデータが有る終了日時の差が３０日以上の時
                                pData[PERIOD, self.VALID] = 0  # 無効にする
                            relShot = pwbData[:, 2] - pwbData[0, 2]  # 相対ショット
                            if np.any(relShot < 0):  # 相対ショットにマイナスが有る時
                                pData[PERIOD, self.VALID] = 0  # 無効にする
                                print(str(LASER_ID) + " INVALID MINUS INDEX")  # プリント
                        print(str(LASER_ID) + "-" + str(PERIOD))  # レーザーIDを表示
                    laserList += list(pData)  # レーザーリストに追加
                    self.deleteObject(pData)  # メモリークリア
                    if len(laserList) > 0:  # レーザーリストが有る時
                        blockList += list(laserList)  # レーザーリストをブロックリストに追加
                        if len(blockList) >= block:  # ブロックリスト長がブロックを超えた時
                            writer.writerows(blockList)  # レーザーIDデータ書き込み
                            written = True  # 書き込み完了フラグを真にする
                            blockList.clear()  # ブロックリストをクリア
                    laserList.clear()  # レーザーリストをクリア
                    self.deleteObject(pwbList)  # メモリークリア
                    emit(p)  # 進捗バーにシグナルを送る
                if len(blockList) > 0:  # ブロックリストが有る時
                    writer.writerows(blockList)  # データリストをまとめて書き込み
                    written = True  # 書き込み完了フラグを真にする
                    self.deleteObject(blockList)  # メモリーをクリア
                    self.deleteObject(laserList)  # メモリーをクリア
            return self.returnResult(written, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   全てのデータをマージしたフラットリストを取得する
    # ---------------------------------------------------------------------------------------------------
    def mergeDataAge(self, dataList, p=None):
        try:
            PWB = GP.CONT.PWB  # PWBを転写
            TRN = GP.CONT.TRN  # TRNを転写
            length = GP.CONT.LABEL_LIST.length  # ラベルクラスを転写
            dataList = dataList[dataList[:, self.VALID] == 1]
            laserIdList = np.unique(dataList[:, self.LASER_ID])  # レーザーリスト取得
            periodList = np.unique(np.array(dataList[:, [self.LASER_ID, self.PERIOD]], 'int'), axis=0)  # ピリオッドリスト取得
            rows = len(laserIdList)  # レーザーID数
            block = self.getLaserBlock(self)  # ファイルブロック長を取得
            blocks = math.ceil(rows / block)  # ブロック数
            labelSamples = math.ceil(self.SAMPLES / len(periodList) * 1.2)  # レーザーラベル毎のデータ数
            labelDic = {}  # labelDicを初期化
            for label in GP.CONT.LABEL_LIST.LIST:  # ラベルリストをすべて実行
                labelDic[label] = []  # ラベルリストを初期化
            self.startNewLevel(blocks * 2, p)  # 新しいレベルの進捗開始
            for i in range(blocks):  # ブロックをすべて実行
                blockList = laserIdList[block * i:(block) * (i + 1)]  # ブロックリスト作成
                PWBList = GP.SVR.DBSServer.getLocFilterFlatList(PWB, blockList, p)  # PWB取得
                length = len(PWBList)  # トレインデータ長
                self.startNewLevel(len(blockList), p)  # 新しいレベルの進捗開始
                for LASER_ID in blockList:  # ブロックリストをすべて実行
                    laserData = dataList[dataList[:, self.LASER_ID] == LASER_ID]  # PRBのLASER_ID行データ
                    PWBData = PWBList[PWBList[:, PWB.LASER_ID] == LASER_ID]  # LASER_IDのPWBデータ
                    self.startNewLevel(len(laserData), p)  # 新しいレベルの進捗開始
                    for periodData in laserData:  # レーザーデータをすべて実行
                        train = self.makeTrain(periodData, PWBData)  # 行データとPWBからトレインデータを取得
                        train = self.makeAgeTrainListMax(train, p)  # 行データから年齢分析用トレインリストの作成
                        PERIOD = periodData[self.PERIOD]  # ピリオッド取得
                        for label in GP.CONT.LABEL_LIST.LIST:  # ラベルリストをすべて実行
                            index0 = np.where(train[:, TRN.LABEL] == label)[0]  # ラベルを持つインデックス
                            length = len(index0)  # データ長
                            if length >= labelSamples:  # Xデータ長がサンプル数以上の時
                                index = random.choice(index0, labelSamples, replace=False)  # 重複無しでランダムサンプルしたインデックスをセット
                                labelDic[label] += list(train[index])  # ラベルリストに追加
                            elif length > 0:  # Xデータが有るがサンプル数未満の時
                                labelDic[label] += list(train[index0])  # ラベルリストに追加
                        print(str(LASER_ID) + "-" + str(PERIOD))  # レーザーIDプリント
                        self.deleteObject(train)  # 削除してメモリー解放
                    self.deleteObject(PWBData)  # 削除してメモリー解放
                    self.deleteObject(laserData)  # 削除してメモリー解放
                    self.endLevel(p)  # 現レベルの終了
                self.deleteObject(PWBList)  # 削除してメモリー解放
                self.endLevel(p)  # 現レベルの終了
            trainList = self.trimTrainList(labelDic, self.SAMPLES, p)  # トレインリストをすべてサンプル数に調整する
            self.deleteObject(labelDic)  # 削除してメモリー解放
            return self.returnList(trainList, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   トレインリストをすべてサンプル数に調整する
    # ---------------------------------------------------------------------------------------------------
    def trimTrainList(self, labelDic, SAMPLES, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            trainList = []  # トレインリストを初期化
            for label, labelData in labelDic.items():  # ラベルリストをすべて実行
                labelData = labelDic[label]  # ラベルデータを抽出
                length = len(labelData)  # ラベルデータ長
                index0 = list(range(length))  # インデクス作成
                if length >= SAMPLES:  # サンプル数以上の時
                    index = random.choice(index0, SAMPLES, replace=False)  # ラベルリストの総数調整
                elif length > 0:  # ラベルデータは有るがサンプル数未満の時
                    index = random.choice(index0, SAMPLES, replace=True)  # ラベルリストの総数調整
                labelTrain = np.array(labelData)  # ラベルリストの総数調整
                labelTrain = labelTrain[index]  # ラベルリストの総数調整
                trainList += list(labelTrain)  # トレインリストに追加
            trainList = np.array(trainList, 'O')  # リスト型のデータパックを返す
            return self.returnList(trainList, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            self.showError(e, p)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   全てのデータをマージしたフラットリストを取得する
    # ---------------------------------------------------------------------------------------------------
    def mergeDataAgeAfter(self, dataList, SAVE_MODEL, MINMAX_DATA, p=None):
        try:
            PWB = GP.CONT.PWB  # PWBを転写
            TRN = GP.CONT.TRN  # TRNを転写
            length = GP.CONT.LABEL_LIST.length  # ラベルクラスを転写
            laserIdList = np.unique(dataList[:, self.LASER_ID])  # レーザーリスト取得
            periodList = np.unique(np.array(dataList[:, [self.LASER_ID, self.PERIOD]], 'int'), axis=0)  # ピリオッドリスト取得
            rows = len(laserIdList)  # レーザーID数
            block = self.getLaserBlock(self)  # ファイルブロック長を取得
            blocks = math.ceil(rows / block)  # ブロック数
            labelSamples = math.ceil(self.SAMPLES / len(periodList) * 1.2)  # レーザーラベル毎のデータ数
            labelDic = {}  # labelDicを初期化
            for label in GP.CONT.LABEL_LIST.LIST: labelDic[label] = []  # ラベルリストを初期化
            LAST_SAMPLE = 50  # 最後のサンプル数
            self.startNewLevel(blocks * 2, p)  # 新しいレベルの進捗開始
            for i in range(blocks):  # ブロックをすべて実行
                blockList = laserIdList[block * i:(block) * (i + 1)]  # ブロックリスト作成
                PWBList = GP.SVR.DBSServer.getLocFilterFlatList(PWB, blockList, p)  # PWB取得
                length = len(PWBList)  # トレインデータ長
                self.startNewLevel(len(blockList), p)  # 新しいレベルの進捗開始
                for LASER_ID in blockList:  # ブロックリストをすべて実行
                    laserData = dataList[dataList[:, self.LASER_ID] == LASER_ID]  # PRBのLASER_ID行データ
                    PWBData = PWBList[PWBList[:, PWB.LASER_ID] == LASER_ID]  # LASER_IDのPWBデータ
                    self.startNewLevel(len(laserData), p)  # 新しいレベルの進捗開始
                    for periodData in laserData:  # レーザーデータをすべて実行
                        PERIOD = periodData[self.PERIOD]  # ピリオッド取得
                        train = self.makeTrain(periodData, PWBData)  # 行データとPWBからトレインデータを取得
                        self.setAgeLabel(train, SAVE_MODEL, MINMAX_DATA)  # 最後のデータの予測年齢を使ってトレインデータのラベルをセット
                        for label in GP.CONT.LABEL_LIST.LIST:  # ラベルリストをすべて実行
                            index0 = np.where(train[:, TRN.LABEL] == label)[0]  # ラベルを持つインデックス
                            length = len(index0)  # データ長
                            if length >= labelSamples:  # Xデータ長がサンプル数以上の時
                                index = random.choice(index0, labelSamples, replace=False)  # 重複無しでランダムサンプルしたインデックスをセット
                                labelDic[label] += list(train[index])  # ラベルリストに追加
                            elif length > 0:  # Xデータ長がサンプル数以上の時
                                labelDic[label] += list(train[index0])  # ラベルリストにあるだけ追加
                        print(str(LASER_ID) + "-" + str(PERIOD))  # レーザーIDプリント
                        self.deleteObject(train)  # 削除してメモリー解放
                    self.deleteObject(PWBData)  # 削除してメモリー解放
                    self.deleteObject(laserData)  # 削除してメモリー解放
                    self.endLevel(p)  # 現レベルの終了
                self.deleteObject(PWBList)  # 削除してメモリー解放
                self.endLevel(p)  # 現レベルの終了
            trainList = self.trimTrainList(labelDic, self.SAMPLES, p)  # トレインリストをすべてサンプル数に調整する
            self.deleteObject(labelDic)  # 削除してメモリー解放
            return self.returnList(trainList, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   最後のデータの予測年齢を使ってトレインデータのラベルをセットする
    # ---------------------------------------------------------------------------------------------------
    def setAgeLabel(self, train, SAVE_MODEL, MINMAX_DATA):
        try:
            TRN = GP.CONT.TRN  # TRNを転写
            AGE_STEP = GP.AGE_STEP  # 年齢刻み転写
            MAX_AGE = GP.MAX_AGE  # 最大年齢転写
            LAST_SAMPLE = 50  # 最後のサンプル数
            lastTrain = train[-LAST_SAMPLE:]  # 最後のデータ
            normal = self.normalize(lastTrain, MINMAX_DATA)  # トレインデータからXデータを正規化して返す
            predict = SAVE_MODEL.MODEL.predict(normal)  # 予測値
            expect = self.getExpect2(predict)  # 期待値を取得
            maxShot = lastTrain[-1, TRN.REL_SHOT]  # 最大ショット取得
            lastExpect = np.sort(expect)  # 昇順でソート
            rangeMax0 = lastExpect[-10:].mean()  # 大きいものから十個の平均
            rangeMax = math.ceil(rangeMax0 / AGE_STEP) * AGE_STEP + AGE_STEP  # AGE_STEP刻みで切り上げ
            if rangeMax > MAX_AGE: rangeMax = MAX_AGE  # 最大年齢に調整
            age0 = train[:, TRN.REL_SHOT] / (maxShot + 1) * rangeMax  # AGE_STEP刻みの割合に変換
            age = np.array(age0 / AGE_STEP, dtype='int') * AGE_STEP  # AGE_STEP刻みの割合に変換
            train[:, TRN.LABEL] = np.array(age, dtype='str')  # ラベルをセット

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   行データから年齢分析用トレインリストの作成
    # ---------------------------------------------------------------------------------------------------
    def makeAgeTrainListMax(self, train, p=None):
        try:
            # GP.AGE_STEP刻みでラベルをセット
            TRN = GP.CONT.TRN  # TRNを転写
            maxShot = train[-1, TRN.REL_SHOT]  # 最大ショット取得
            rangeMax = GP.CONT.LABEL_LIST.LAST_AGE  # 最大年齢レンジ
            age = np.array(train[:, TRN.REL_SHOT] / maxShot * 100 / GP.AGE_STEP,
                           dtype='int') * GP.AGE_STEP  # AGE_STEP刻みの割合に変換
            age = np.where(age > rangeMax, rangeMax, age)
            train[:, TRN.LABEL] = np.array(age, dtype='str')  # ラベルをセット
            emit(p)  # 進捗バーにシグナルを送る
            return train  # データパックにtrain0をマージ

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   指定した原因のフラットリストを作成して返す
    # ---------------------------------------------------------------------------------------------------
    def getCauseList(self, periodList, causeList, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if GP.SVR.DBSServer.existsLocTable(self):  # テーブルが有る時
                channel, cursor = GP.SVR.DBSServer.openLocServer()  # ローカルサーバーをオープンしてcursorを取得
                query = self.makeObjectQuery(self)  # オブジェクトのフィールド名からセレクトクエリーを作成
                whereQuery = self.makeFilterPeriodQuery(periodList)  # WHEREクエリー作成
                query = query.insertWhereQuery(whereQuery)  # WHEREクエリー挿入
                query.add("AND (")  # 原因一致
                for cause in causeList:
                    query.add("BASE.CAUSE = " + "'" + cause + "'")  # 原因一致
                    if cause != causeList[-1]:  # 最後の要素で無い時
                        query.add("OR")  # 原因一致
                query.add(")")  # 原因一致
                query.add("AND BASE.VALID = 1")  # 有効
                query.execute(cursor)  # クエリを実行する
                rowData = cursor.fetchall()  # すべて読み込む
                emit(p)  # 進捗バーにシグナルを送る
                channel.close()  # DBクローズ
                rowData = np.array(rowData, 'O')  # ベースリストを確認返す
                return self.returnList(rowData, p)  # 実行時間を表示してからデータを返す
            return self.returnNone(p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ノードリストに対応するPRBのリストを抽出する
    # ---------------------------------------------------------------------------------------------------
    def makePRANodeList(self, nodeList, p=None):
        try:
            self.startNewLevel(1, p)  # 計測開始時間セット
            if len(nodeList) > 0:  # チェックリストが有る時
                channel, cursor = GP.SVR.DBSServer.openLocServer()  # DBをオープンしてcursorを取得
                periodList = []  # ピリオッドリスト初期化
                for node in nodeList:  # ノードリストをすべて実行
                    periodData = self.getNodeList(cursor, node)  # 指定されたタイプコードとタイプIDのリストを返す
                    if periodData is not None:  # ピリオッドデータ有る時
                        periodList += list(periodData)  # ピリオッドリストにピリオッドデータを追加
                channel.close()  # DBクローズ
                periodList = np.array(periodList, 'O')  # ピリオッドリストを返す
                return self.returnList(periodList, p)  # 実行時間を表示してからデータを返す
            return self.returnNone(p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   指定されたノードのリストを返す
    # ---------------------------------------------------------------------------------------------------
    def getNodeList(self, cursor, node):
        try:
            LTR = GP.CONT.LTR  # レーザーツリークラスの転写
            treeNode = node[LTR.TREE_NODE]  # ツリーノード
            typeCode = node[LTR.TYPE_CODE]  # タイプコード
            typeId = node[LTR.TYPE_ID]  # タイプID
            laserId = node[LTR.LASER_ID]  # レーザーID
            period = node[LTR.PERIOD]  # ピリオッド
            typeCodeStr = "'" + str(typeCode) + "'"
            typeIdStr = "'" + str(typeId) + "'"
            laserIdStr = str(laserId)
            periodStr = str(period)
            query = self.makeObjectQuery(self)  # オブジェクトのフィールド名からセレクトクエリーを作成
            query.add(" WHERE BASE.TYPE_CODE = " + typeCodeStr)  # タイプコードかつ
            query.add(" AND BASE.LASER_TYPE_ID = " + typeIdStr)  # タイプIDかつ
            query.add(" AND BASE.LASER_ID = " + laserIdStr)  # レーザーIDかつ
            query.add(" AND BASE.PERIOD = " + periodStr)  # ピリオッドかつ
            query.add(" AND BASE.VALID = 1")  # 有効なものを抽出
            query.execute(cursor)  # クエリを実行する
            rowData = cursor.fetchall()  # すべて読み込む
            rowData = np.array(rowData, dtype='O')  # すべて読み込む
            if len(rowData) > 0:  # データが有る時
                return rowData  # データを返す
            self.showNone()  # None表示
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ページリストからPWBリストを作成する
    # ---------------------------------------------------------------------------------------------------
    def getTrainDic(self, pageList, p=None):
        try:
            self.startNewLevel(len(pageList), p)  # 新しいレベルの進捗開始
            PWB = GP.CONT.PWB  # PWBを転写
            TRN = GP.CONT.TRN  # TRNを転写
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if pageList is not None:  # ページリストが有る時
                laserIdList = pageList[:, self.LASER_ID]  # レーザーIDリスト取得
                laserIdList = np.unique(laserIdList)  # レーザーIDリストをユニークにする
                PWBList = GP.SVR.DBSServer.getLocFilterFlatList(PWB, laserIdList, p)  # PWB取得
                trainDic = {}  # train辞書を初期化
                for periodData in pageList:  # ページリスをすべて実行
                    LASER_ID = periodData[self.LASER_ID]  # レーザーID取得
                    PERIOD = periodData[self.PERIOD]  # ピリオッド取得
                    PWBData = PWBList[PWBList[:, PWB.LASER_ID] == LASER_ID]  # LASER_IDのPWBデータ
                    train = self.makeTrain(periodData, PWBData)  # 行データとPWBからトレインデータを取得
                    if train is not None:
                        trainDic[LASER_ID, PERIOD] = train  # トレイン辞書に追加
                    emit(p)  # 進捗バーにシグナルを送る
                return self.returnList(trainDic, p)  # 実行時間を表示してからデータを返す
            return self.returnNone(p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ページリストから区間平均値リストを作成する
    # ---------------------------------------------------------------------------------------------------
    def getIntervalMeanList(self, PARTS, trainDic, RED_SPAN, p=None):
        try:
            self.startNewLevel(len(trainDic), p)  # 新しいレベルの進捗開始
            TRN = GP.CONT.TRN  # TRNを転写
            PWB = GP.CONT.PWB  # PWBを転写
            MODEL_DIC = PARTS.MODEL_DIC  # モデルを転写
            if trainDic is not None and MODEL_DIC is not None:  # トレイン辞書が有る時
                meanDic = {}  # 期待値辞書を初期化
                maxShot = 0  # 最大ショットを初期化
                for (LASER_ID, PERIOD), train in trainDic.items():  # トレインリスをすべて実行
                    maxShot = max(maxShot, train[-1, TRN.REL_SHOT])  # 最大ショットを更新
                    reduce, predict = self.getPredictOne(PARTS, train, RED_SPAN, p)  # 予測値を取得
                    if predict is not None:  # 予測値が有る時
                        meanDic[LASER_ID, PERIOD] = predict  # 期待値辞書に追加
                    emit(p)  # 進捗バーにシグナルを送る
                return self.returnList2(meanDic, maxShot, p)  # 正規化した間引きデータと予測データを返す
            return self.returnNone2(p)  # エラーを表示してからNoneを返す

        except Exception as e:  # 例外
            return self.returnError2(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   予測値を取得
    # ---------------------------------------------------------------------------------------------------
    def getPredictOne(self, PARTS, train, RED_SPAN, p=None):
        try:
            TRN = GP.CONT.TRN  # TRNを転写
            MODEL_DIC = PARTS.MODEL_DIC  # モデル辞書の転写
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if train is not None:  # ピリオッドデータが有る時
                MODEL_COMB = TRN.getModelComb(PARTS, train[0])  # モデルコンボを取得する
                MODEL = MODEL_COMB.SAVE_MODEL.MODEL  # モデルを転写
                if MODEL is not None:
                    # 訓練データの間引きしたデータを作成(元データ表示用)
                    reduce = self.reducePredictData(train, RED_SPAN)  # データを削減する
                    reduceNnormal = self.normalize(reduce, MODEL_COMB.SAVE_DATA.MINMAX_DATA)  # ピリオッドデータを正規化
                    if reduceNnormal is not None:
                        reduce = np.concatenate([reduce[:, :X_BASE], reduceNnormal], axis=1)  # 正規化した間引きデータを作成
                        # 予測値の期待値データを作成
                        normal = self.normalize(train, MODEL_COMB.SAVE_DATA.MINMAX_DATA)  # ピリオッドデータを正規化
                        prdData = MODEL.predict(normal)  # モデルから予測値取得
                        expect = self.getExpect(prdData)  # 期待値を取得
                        meanPredict = self.getIntervalMeanExpect(train, expect, RED_SPAN)  # 期待値を区間平均する
                        return self.returnList2(reduce, meanPredict, p)  # 正規化した間引きデータと予測データを返す
            return self.returnNone2(p)  # エラーを表示してからNoneを返す

        except Exception as e:  # 例外
            return self.returnError2(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   抽出フラットリストからトレインピリオッド辞書を作成する
    # ---------------------------------------------------------------------------------------------------
    def makeTrainData(self, periodData, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            PWB = GP.CONT.PWB  # PWBを転写
            train = None  # トレインデータ初期化
            if periodData is not None:  # ピリオッド辞書が有る時
                LASER_ID = periodData[self.LASER_ID]
                PWBList = GP.SVR.DBSServer.getLocFilterFlatList(PWB, [LASER_ID], p)  # PWB取得
                length = len(PWBList)  # トレインデータ長
                train = self.makeTrain(periodData, PWBList)  # 行データとPWBからトレインデータを取得
                self.deleteObject(PWBList)  # 削除してメモリー解放
                train = np.array(train, 'O')  # NUMPY配列化
            return self.returnList(train, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #  ピリオッドデータとPWBデータからトレインデータを作成して返す
    # ---------------------------------------------------------------------------------------------------
    def makeTrain(self, periodData, PWBData):
        try:
            PWB = GP.CONT.PWB  # PWBを転写
            TRN = GP.CONT.TRN  # TRNを転写
            PERIOD = periodData[self.PERIOD]  # ピリオッド開始日時
            begin = periodData[self.BEGIN_DATE_TIME]  # ピリオッド開始日時
            end = periodData[self.END_DATE_TIME]  # ピリオッド終了日時
            periodPWB = PWBData[
                (PWBData[:, PWB.LOG_DATE_TIME] >= begin) & (PWBData[:, PWB.LOG_DATE_TIME] < end)]  # 開始日時から終了日時までのデータ取得
            if len(periodPWB) > 0:  # ピリオッドデータが有る時
                if PERIOD == 0:
                    beginShot = 0  # ピリオッド0の時は最初のショット数は0
                else:
                    beginShot = periodPWB[0, PWB.TOTAL_SHOT]  # 最初のショット数
                X_BASE = GP.X_LIST.X_BASE  # トレインデータXベース転写
                train = np.empty((len(periodPWB), TRN.LENGTH), dtype='O')  # trainデータをオブジェクトタイプで初期化
                train[:, 1:TRN.TARGET + 1] = periodData[
                                             :self.TARGET + 1]  # LASER_ID,LASER_TYPE_ID,TYPE_CODE,PERIOD,PERIOD_CLASS,VALID,TARGETをセット
                train[:, TRN.LABEL] = periodData[self.CAUSE]  # LABELを仮セット
                train[:, TRN.LOG_DATE_TIME] = periodPWB[:, PWB.LOG_DATE_TIME]  # LOG_DATE_TIMEをセット
                train[:, TRN.HAPPEN_SHOT] = periodPWB[:, PWB.TOTAL_SHOT]  # HAPPEN_SHOTをセット
                train[:, TRN.REL_SHOT] = periodPWB[:, PWB.TOTAL_SHOT] - beginShot  # REL_SHOTをセット
                train[:, X_BASE:] = periodPWB[:, PWB.WL_ERROR:]  # Xデータをセット
                self.deleteObject(periodPWB)  # 削除してメモリー解放
                return train  # trainを返す
            self.showNone()  # None表示
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   予想値データを削減する
    # ---------------------------------------------------------------------------------------------------
    def reducePredictData(self, train, RED_SPAN):
        try:
            TRN = GP.CONT.TRN  # TRNを転写する
            spans = math.ceil(len(train) / RED_SPAN)  # 区間数
            reduce = np.array([train[i * RED_SPAN] for i in range(spans)])  # 間引き配列を作成
            return reduce  # 間引きデータを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   与えられた日付けが属するピリオッドを返す
    # ---------------------------------------------------------------------------------------------------
    def getDatePeriod(self, LASER_ID, happenDate):
        try:
            flatBase = self.flatBase
            laserData = flatBase[flatBase[:, self.LASER_ID] == LASER_ID]
            validList = np.full(len(happenDate), False, 'bool')  # 結果リストを初期化
            retList = np.zeros(len(happenDate), 'int')  # 結果リストを初期化
            for i in range(len(happenDate)):  # 発生日時リストをすべて実行
                pData = laserData[(happenDate[i] > laserData[:, self.BEGIN_DATE_TIME]) &
                                  (happenDate[i] <= laserData[:, self.END_DATE_TIME])]  # 該当するピリオッドデータ取得
                if len(pData) > 0:  # 該当するピリオッドデータが有る時
                    retList[i] = pData[0, self.PERIOD]  # 結果リストにピリオッドをセット
                    validList[i] = pData[0, self.VALID]  # 有効フラグをセット
                else:
                    a = 0
            return retList, validList  # 結果リストを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None, None  # Noneを返す


# =======================================================================================================
#   スーパークラス PartsJobBaseClass
# =======================================================================================================
class PartsJobBaseClass(CommonBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        CommonBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化

    # ---------------------------------------------------------------------------------------------------
    # チャンバー交換期間番号を持ったDBを作成
    # ---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(6, p)                                                                    # 新しいレベルの進捗開始
            PEX = GP.CONT.PEX                                                                           # PEXの転写
            PRB = GP.CURPARTS.PRB                                                                       # PRBの転写
            if PEX.loadLaserDic(p):                                                                     # PEXレーザー辞書読込に成功した時
                if PRB.loadFlatBase(p):
                    if self.makeCsvFile(p):                                                             # COMB_PLOT_WPLOTに部品交換期間を加えたファイルを作成する
                        GP.SVR.DBSServer.makeLocDBFromObjectFile(self, p)                               # オブジェクトファイルからローカルDBを作成
                    PRB.releaseBase(p)                                                                  # メモリーの解放
                PEX.releaseBase(p)                                                                      # メモリーの解放
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   部品交換リストに部品毎の交換期間を加える
    # ---------------------------------------------------------------------------------------------------
    def makeCsvFile(self, p=None):
        try:
            self.startNewLevel(len(GP.CONT.PEX.laserBase), p)                                           # 新しいレベルの進捗開始
            PEX = GP.CONT.PEX                                                                           # PEXを転写
            PWB = GP.CONT.PWB                                                                           # PWBを転写
            PTB = GP.CURPARTS.PTB                                                                       # PTBの転写
            PRB = GP.CURPARTS.PRB                                                                       # PRBを転写
            periodDic = {}                                                                              # ピリオッド辞書を初期化
            written = False                                                                             # 書き込み完了フラグを初期化
            strPath = self.targetPath                                                                   # ファイルパス
            dirName = os.path.dirname(strPath)                                                          # ディレクトリ名
            if not os.path.exists(dirName):                                                             # ディレクトリの有無を確認
                os.makedirs(dirName)                                                                    # 途中のディレクトリを含めてディレクトリを作成
            block = self.getFileBlock(self)                                                             # ファイルブロック長を取得
            blockList = []                                                                              # ブロックリスト初期化
            with open(file=strPath, mode="w", encoding="utf-8") as f:                                   # "utf-8"でファイルをオープン
                writer = csv.writer(f, delimiter="\t", lineterminator='\n')                             # テーブルデスクリプションを書き込む
                writer.writerow(self.tableDesc.colName)                                                 # CSVライター設定
                for LASER_ID, PEX_PeriodList in PEX.laserBase.items():                                  # PEXレーザーベース辞書をすべて実行
                    prbList = PRB.flatBase[PRB.flatBase[:, PRB.LASER_ID] == LASER_ID]
                    pwbList = PWB.getShotList([LASER_ID])                                               # コンブプロットベースのレーザーデータ取得
                    for partsName in GP.ORG_PEX_LIST.LIST:                                              # 交換部品リストをすべて実行
                        parts = str(partsName)                                                          # 部品名
                        partsList = PEX_PeriodList[PEX_PeriodList[:, PEX.PARTS_NAME] == parts]          # 部品のリスト
                        partsPeriods = len(partsList) + 1                                               # 部品ピリオッドの行数
                        pData = np.empty((partsPeriods, self.LENGTH), dtype='O')                        # ピリオッドデータをオブジェクトタイプで初期化
                        pData[:, self.LASER_ID] = LASER_ID                                              # レーザーIDセット
                        pData[:, self.LASER_TYPE_ID] = PEX_PeriodList[0, PEX.LASER_TYPE_ID]             # レーザータイプIDセット
                        pData[:, self.TYPE_CODE] = PEX_PeriodList[0, PEX.TYPE_CODE]                     # タイプコードセット
                        pData[:, self.PARTS_PERIOD] = np.array([np.arange(partsPeriods)])               # 部品ピリオッドセット
                        pData[0, self.PARTS_PERIOD_BEGIN] = GP.MIN_DATE                                 # ピリオッド最初の部品ピリオッド開始ショット
                        pData[-1, self.PARTS_PERIOD_END] = GP.MAX_DATE                                  # ピリオッド最後の部品ピリオッド終了ショット
                        pData[-1, self.HAPPEN_DATE] = GP.MAX_DATE                                       # ピリオッド最後の発生ショット
                        pData[-1, self.JOB_NO] = None                                                   # ピリオッド最後のジョブ番号
                        pData[-1, self.CLASS] = '99'                                                    # ピリオッド最後のクラス
                        pData[-1, self.PARTS_NAME] = partsName                                          # ピリオッド最後の部品名
                        if partsPeriods > 1:                                                            # 部品ピリオッドの行数が２以上の時
                            pData[:-1, self.HAPPEN_DATE] = partsList[:, PEX.HAPPEN_DATE]                # ピリオッド最後の一つ前までの発生ショット
                            pData[1:, self.PARTS_PERIOD_BEGIN] = partsList[:,
                                                                 PEX.HAPPEN_DATE]                       # ピリオッド二番目以後の部品ピリオッド開始ショット
                            pData[:-1, self.PARTS_PERIOD_END] = partsList[:,
                                                                PEX.HAPPEN_DATE]                        # ピリオッド最後の一つ前までの部品ピリオッド終了ショット
                            pData[:-1, self.JOB_NO:] = partsList[:, PEX.JOB_NO:PEX.SUBJECT]             # ピリオッド最後の一つ前までのジョブ番号以後のデータ
                        # ベースピリオッドのセット
                        happenDateList = np.concatenate(
                            [partsList[:, PEX.HAPPEN_DATE], [GP.MAX_PRE_DATE]])                         # 与えられたショットが属するピリオッド
                        periodList, validList = PRB.getDatePeriod(LASER_ID, happenDateList)             # 与えられた日付けが属するピリオッド
                        pData[:, self.PERIOD] = periodList  # ピリオッドをセット
                        for i, PERIOD in enumerate(periodList):
                            if validList[i]:  # ピリオッドクラスが無い時
                                PERIOD_CLASS = PTB.getField(GP.BASE_TYPE.F_BASE, LASER_ID, PERIOD, PTB.PERIOD_CLASS)
                                if PERIOD_CLASS is not None:
                                    pData[i, self.PERIOD_CLASS] = PERIOD_CLASS[0]                       # ピリオッドクラスセット
                                    # 定期交換部品のラベルに'R_'を加える
                                    if pData[i, self.CLASS] == '00':                                    # クラスが定期交換'00'のインデックス取得
                                        pData[i, self.PARTS_NAME] = "R_" + pData[
                                            i, self.PARTS_NAME]                                         # 定期交換の部品名の頭に'R_'を追加する
                                                                                                        # 最終ピリオッドの交換部品のラベルに'R_'を加える
                                    elif pData[i, self.CLASS] == '99':                                  # クラスが定期交換'99'のインデックス取得
                                        pData[i, self.PARTS_NAME] = "P_" + pData[
                                            i, self.PARTS_NAME]                                         # 最終ピリオッドの部品名の頭に'P_'を追加する
                                    else:                                                               # クラスが定期交換'99'のインデックス取得
                                        pData[i, self.PARTS_NAME] = "A_" + pData[
                                            i, self.PARTS_NAME]                                         # 最終ピリオッドの部品名の頭に'P_'を追加する
                                    prbData = prbList[prbList[:, PRB.PERIOD] == PERIOD][0]              # ピリオッド内のPWBデータを取得
                                    beginShot = prbData[PRB.BEGIN_SHOT]
                                    HAPPEN_DATE = pData[i, self.HAPPEN_DATE]
                                    pwbData = pwbList[(pwbList[:, 1] <= HAPPEN_DATE)]                   # ピリオッド内のPWBデータを取得
                                    if len(pwbData) > 0:
                                        pData[i, self.HAPPEN_SHOT] = pwbData[-1, 2] - beginShot         # ピリオッドクラスセット
                                        blockList += [list(pData[i])]                                   # ピリオッドリストにピリオッドデータを追加
                                    else:
                                        a = 0

                    if len(blockList) >= block:                                                         # ブロックリストがブロック長以上になった時
                        writer.writerows(blockList)                                                     # ブロックリストを書き込み
                        written = True                                                                  # 書き込み完了フラグを真にする
                        blockList.clear()                                                               # ブロックリストをクリア
                    emit(p)                                                                             # 進捗バーにシグナルを送る
                if len(blockList) > 0:                                                                  # ブロックリストにまだデータが残っている時
                    writer.writerows(blockList)                                                         # ブロックリストをまとめて書き込み
                    written = True                                                                      # 書き込み完了フラグを真にする
                    self.deleteObject(blockList)                                                        # メモリーをクリア
            return self.returnResult(written, p)                                                        # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnResultError(e, p)                                                         # エラーを表示してからFalseを返す

    # ---------------------------------------------------------------------------------------------------
    #   指定したラベルリストを含むピリオッドリストを抽出する
    # ---------------------------------------------------------------------------------------------------
    def extractIncList(self, filterList, labelList, p=None):
        try:
            LABEL = GP.CURPARTS.LABEL  # ラベルクラスを転写
            flatList = GP.SVR.DBSServer.getLocFilterFlatList(self, filterList, p)  # フラットリストを読み込む
            if flatList is not None:  # jobが有る時
                incList = flatList[np.in1d(flatList[:, self.PARTS_NAME], labelList)]  # ラベルリストを含むリスト
                if len(incList) > 0:  # 抽出リストが有る時
                    emit(p)  # 進捗を進める
                    return incList  # 抽出リストを返す
            emit(p)  # 進捗を進める
            self.showNone()  # Noneを表示
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ピリオッド内で排他的なデータのレーザーID＆ピリオッドリストを抽出する
    # ---------------------------------------------------------------------------------------------------
    def extractExcList(self, filterList, label, p=None):
        try:
            LABEL = GP.CURPARTS.LABEL  # ラベルクラスを転写
            self.flatBase = GP.SVR.DBSServer.getLocFilterFlatList(self, filterList, p)  # フラットリベースをセット
            if self.flatBase is not None:  # jobが有る時
                flatBase = self.flatBase  # フラットベースの転写
                labelList = flatBase[np.in1d(flatBase[:, self.PARTS_NAME], label)]  # ラベルが有るリスト
                exList = flatBase[~np.in1d(flatBase[:, self.PARTS_NAME], label) &  # 指定ラベル以外かつ
                                  (flatBase[:, self.PARTS_NAME] == LABEL.ACC)]  # 'ACC'が有るインデックスを取得
                exIndex = exList[:, self.LASER_ID] * 100 + exList[:, self.PERIOD]  # LASER_IDとPERIODを結合した排他イデックスを作る
                labelIndex = labelList[:, self.LASER_ID] * 100 + labelList[:,
                                                                 self.PERIOD]  # LASER_IDとPERIODを結合したラベルインデックスを作る
                extractList = labelList[~np.in1d(labelIndex, exIndex)]  # ラベルインデックスから排他インデックスを除いた抽出リスト作成
                if len(extractList) > 0:  # 抽出リストが有る時
                    emit(p)  # 進捗を進める
                    return extractList  # 抽出リストを返す
            emit(p)  # 進捗を進める
            self.showNone(p)  # Noneを表示
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ピリオッド内で非排他的なデータパックをを抽出する
    # ---------------------------------------------------------------------------------------------------
    def extractIncPack(self, extractList, abnLen, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            trainList = []
            dataList = emptyList(self.LENGTH)  # 空のコンケート可能なデータリストを作成する
            self.loadFlatListLabel(self.MY_LASER_LIST, extractList, p)  # フラットリストを取得
            if self.flatBase is not None:  # jobが有る時
                for label in extractList:  # ラベルリストをすべて実行
                    extract = self.flatBase[self.flatBase[:, self.PARTS_NAME] == label]  # labelが有るインデックス
                    dataList = np.concatenate([dataList, extract])  # データリストに追加
            if len(dataList) > 0:  # データリストが有る時
                for rowData in dataList:  # データリストのすべてのレーザーを実行
                    train = self.getDataPackByRow2(rowData, abnLen)  # 行データの読み込み
                    trainList += list(train)
            return self.returnList(trainList, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示


# =======================================================================================================
#   クラス GasBaseClass
# =======================================================================================================
class PartsGasBaseClass(CommonBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        CommonBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化

    # ---------------------------------------------------------------------------------------------------
    # チャンバー交換期間番号とガス交換期間番号を持ったDBを作成
    # ---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            PTB = GP.CURPARTS.PTB  # PTBの転写
            GFP = GP.CONT.GFP  # GFPを転写
            self.startNewLevel(6, p)  # 新しいレベルの進捗開始
            if GFP.loadLaserDic(p):  # GFPレーザー辞書に成功した時
                GFP.periodBase = PTB.extractPeriodShot(GFP.laserBase, GFP.START_DATE_TIME, 0,
                                                       p)  # チャンバー交換期間を加えたレーザー辞書を作成する
                if self.makeCsvFile(p):  # CSVファイルを作成する
                    GP.SVR.DBSServer.makeLocDBFromObjectFile(self, p)  # オブジェクトファイルからローカルDBを作成
                    GFP.periodBase = PTB.extractPeriodShot(GFP.laserBase, GFP.START_DATE_TIME, 0,
                                                           p)  # チャンバー交換期間を加えたレーザー辞書を作成する
                GFP.releaseBase(p)  # メモリーの解放
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   CSVファイルを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeCsvFile(self, p=None):
        try:
            GFP = GP.CONT.GFP  # GFPを転写
            self.startNewLevel(len(GFP.periodBase), p)  # 新しいレベルの進捗開始
            written = False  # 書き込み完了フラグを初期化
            strPath = self.targetPath  # ファイルパス
            dirName = os.path.dirname(strPath)  # ディレクトリ名
            if not os.path.exists(dirName):  # ディレクトリの有無を確認
                os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
            block = self.getFileBlock(self)  # ファイルブロック長を取得
            blockList = []  # ブロックリスト初期化
            with open(file=strPath, mode="w", encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                writer = csv.writer(f, delimiter="\t", lineterminator='\n')  # テーブルデスクリプションを書き込む
                writer.writerow(self.tableDesc.colName)  # CSVライター設定
                for (LASER_ID, PERIOD), GFP_pData in GFP.periodBase.items():  # GFPピリオッド辞書をすべて実行
                    length = len(GFP_pData)  # GFPピリオッドデータ長を取得
                    pData = np.empty((length, self.LENGTH), dtype='O')  # ピリオッドデータをオブジェクトタイプで初期化
                    pData[:, self.LASER_ID] = LASER_ID  # レーザーIDセット
                    pData[:, self.PERIOD] = PERIOD  # ピリオッドセット
                    pData[:, self.HAPPEN_SHOT] = GFP_pData[:, GFP.END_SHOT]  # 発生ショットにGFPピリオッドデータの終了ショットをセット
                    pData[:, self.INTERVAL_NO] = np.array([range(length)])  # インターバル番号をセット
                    pData[:, self.START_DATE_TIME:] = GFP_pData[:,
                                                      GFP.START_DATE_TIME:]  # 開始日時にGFPピリオッドデータの開始日時をセット
                    blockList += list(pData)  # ブロックリストに追加
                    if len(blockList) >= block:  # ブロックリスト長がブロックを超えた時
                        writer.writerows(blockList)  # レーザーIDデータ書き込み
                        written = True  # 書き込み完了フラグを真にする
                        blockList.clear()  # ブロックリストをクリア
                    self.deleteObject(pData)  # メモリークリア
                    emit(p)  # 進捗バーにシグナルを送る
                if len(blockList) > 0:  # ブロックリストが有る時
                    writer.writerows(blockList)  # データリストをまとめて書き込み
                    written = True  # 書き込み完了フラグを真にする
                    self.deleteObject(blockList)  # メモリーをクリア
            return self.returnResult(written, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # 例外を表示


# =======================================================================================================
#   スーパークラス PartsErrorBaseClass
# =======================================================================================================
class PartsErrorBaseClass(CommonBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        CommonBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化

    # ---------------------------------------------------------------------------------------------------
    # レーザーID単位でクエリーを実行してDBに挿入する。CSVファイもを作る
    # ---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(4, p)  # 新しいレベルの進捗開始
            PRB = GP.CURPARTS.PRB  # PRBの転写
            laserIdList = self.MY_LASER_LIST  # レーザーIDリストを取得
            if laserIdList is not None:  # レーザーリストが有る時
                if PRB.loadFlatBase(p):
                    baseQuery = self.makeQueryErrBase()  # ベースクエリ作成
                    if self.makeCsvFile(baseQuery, laserIdList, p):  # CSVファイルの作成に成功した時
                        GP.SVR.DBSServer.makeLocDBFromObjectFile(self, p)  # オブジェクトファイルからローカルDBを作成
                    PRB.releaseBase(p)  # メモリーの解放
                self.endLevel(p)  # 現レベルの終了
                return
            self.showNone(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e, p)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   DBからフィルターをかけたCSVファイルを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeCsvFile(self, baseQuery, filterList, p=None):
        try:
            PRB = GP.CURPARTS.PRB  # PRBの転写
            DBSServer = GP.SVR.DBSServer  # DBSサーバー転写
            strPath = self.targetPath  # ファイルパス
            rows = len(filterList)  # レーザーID数
            fileBlock = self.getFileBlock(self)  # レーザーブロック長を取得
            block = self.getLaserBlock(self)  # ファイルブロック長を取得
            blocks = math.ceil(rows / block)  # ブロック数
            self.startNewLevel(blocks, p)  # 新しいレベルの進捗開始
            channel, cursor = DBSServer.openLocServer()  # DBをオープンする
            GROUP_DIC = GP.GR_ERR_LIST.GROUP_DIC  # グループ化用の書き換え辞書
            # CSV を作成
            written = False  # 書き込みフラグを初期化
            blockList = []  # ブロックリスト初期化
            with open(file=strPath, mode="w", encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                writer = csv.writer(f, delimiter="\t", lineterminator='\n')  # CSVライター設定
                writer.writerow(self.tableDesc.colName)  # テーブルデスクリプションを書き込む
                filterList = np.array(filterList)  # numpy配列化
                for i in range(blocks):  # ブロックをすべて実行
                    partList = filterList[block * i:(block) * (i + 1)]  # 部分フィルタ作成
                    whereQuery = self.makeFilterQuery(partList)  # フィルタクエリ作成
                    query = baseQuery.insertWhereQuery(whereQuery)  # WHEREクエリー挿入
                    query.execute(cursor)  # クエリを実行する
                    dataList = cursor.fetchall()  # すべて読み込む
                    extract = [row for row in dataList if row[self.ERROR_CODE] in GROUP_DIC]  # グループコードに有るものを抽出
                    if len(extract) > 0:  # 抽出データが有る時
                        extract = np.array(extract, 'O')  # numpy配列化
                        grCode = [GROUP_DIC[row[self.ERROR_CODE]] for row in extract]  # グループコードに有るものを抽出
                        extract[:, self.ERROR_CODE] = grCode  # グループコードに置き換え
                        for i, data in enumerate(extract):  # 抽出データをすべて実行
                            LASER_ID = data[self.LASER_ID]  # レーザーID転写
                            PERIOD = data[self.PERIOD]  # ピリオッド転写
                            prbData = PRB.flatBase[
                                (PRB.flatBase[:, PRB.LASER_ID] == LASER_ID) & (PRB.flatBase[:, PRB.PERIOD] == PERIOD)][
                                0]  # ピリオッドデータ取得
                            beginShot = prbData[PRB.BEGIN_SHOT]  # 開始ショット
                            extract[i, self.HAPPEN_SHOT] -= beginShot  # 相対ショット化
                            blockList += list(extract)  # ブロックリストに抽出データを追加
                            if len(blockList) > fileBlock:  # ブロックリストがブロック長以上になった時
                                writer.writerows(blockList)  # ブロックリストを書き込み
                                written = True  # 書き込み完了フラグを真にする
                                blockList.clear()  # ブロックリストをクリア
                    self.deleteObject(dataList)  # メモリーを解放
                    emit(p)  # 進捗バーにシグナルを送る
                if len(blockList) > 0:  # ブロックリストにまだデータが残っている時
                    writer.writerows(blockList)  # ブロックリストをまとめて書き込み
                    written = True  # 書き込み完了フラグを真にする
                    self.deleteObject(blockList)  # メモリーをクリア
            channel.close()  # DBをクローズ
            return self.returnResult(written, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnResultError(e, p)  # エラーを表示してからFalseを返す

    # ---------------------------------------------------------------------------------------------------
    #   ERRORにピリオッドを加えたクエリを作成
    # ---------------------------------------------------------------------------------------------------
    def makeQueryErrBase(self):
        try:
            query = QueryClass()  # クエリを生成
            query.add("SELECT DISTINCT")
            query.add("BASE.LASER_ID as LASER_ID,")
            query.add("PTB.LASER_TYPE_ID as LASER_TYPE_ID,")
            query.add("PTB.TYPE_CODE as TYPE_CODE,")
            query.add("PTB.PERIOD as PERIOD,")
            query.add("PTB.PERIOD_CLASS as PERIOD_CLASS,")
            query.add("BASE.LOG_DATE_TIME as HAPPEN_DATE,")
            query.add("BASE.TOTAL_SHOT as HAPPEN_SHOT,")
            query.add("CASE WHEN BASE.LASER_ID >= 10000 AND BASE.LASER_ID <= 20000")
            query.add(
                "THEN CONCAT('E', CASE WHEN BASE.ERROR_CODE >= 4440 AND BASE.ERROR_CODE <= 4499 THEN BASE.ERROR_CODE - 3000 ELSE BASE.ERROR_CODE END)")
            query.add("ELSE CONCAT('E', BASE.ERROR_CODE)")
            query.add("END as ERROR_CODE")
            query.add("FROM ERROR BASE")
            query.add("JOIN")
            query.add(
                "(SELECT LASER_ID,LASER_TYPE_ID,TYPE_CODE, PERIOD,PERIOD_BEGIN_DATE_TIME,PERIOD_END_DATE_TIME,PERIOD_CLASS")
            query.add("FROM " + GP.CURPARTS.PTB.TABLE_NAME + ")")
            query.add("PTB")
            query.add("on PTB.LASER_ID = BASE.LASER_ID")
            query.add(
                "and BASE.LOG_DATE_TIME >= PTB.PERIOD_BEGIN_DATE_TIME AND BASE.LOG_DATE_TIME < PTB.PERIOD_END_DATE_TIME")
            return query  # クエリーを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   スーパークラス　PartsCombClass
# =======================================================================================================
class PartsCombClass():
    def __init__(self, PARTSCONT):  # 初期化
        try:
            # オブジェクト生成
            PTB = PartsPartsBaseClass(PARTSCONT.PCOMB_CONF.PTB)  # PTB生成
            PRB = PartsPeriodBaseClass(PARTSCONT.PCOMB_CONF.PRB)  # PRB生成
            JBB = PartsJobBaseClass(PARTSCONT.PCOMB_CONF.JBB)  # JBB生成
            ERB = PartsErrorBaseClass(PARTSCONT.PCOMB_CONF.ERB)  # ERB生成
            GSB = PartsGasBaseClass(PARTSCONT.PCOMB_CONF.GSB)  # GSB生成
            # オブジェクトのインスタンス変数のセット
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != 'PARTSCONT') and  # ローカル変数名リストを作成
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            self.objectList = []  # オブジェクトリスト初期化
            self.tableList = []  # テーブル名リスト初期化
            self.objectDic = {}  # オブジェクト辞書初期化
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
                exec("self.objectList += [self." + objectName + "]")  # オブジェクトリストに追加
                exec("self.tableList += [self." + objectName + ".TABLE_NAME]")  # テーブル名リストに追加
                exec("self.objectDic[self." + objectName + ".TABLE_NAME] = self." + objectName)  # オブジェクト辞書に追加
            # すべてのオブジェクトのインスタンス変数をセットする
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                for name in self.nameList:  # オブジェクト名リストをすべて実行
                    exec("self." + objectName + "." + name + " = self." + name)  # オブジェクトをインスタンス変数に転写する
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   すべてのオブジェクトのインスタンス変数をセットする
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self, laserIdList, parameter):
        try:
            parameter.setClassVar(self)  # メンバーのパラメータデータをセット
            self.MY_LASER_LIST = laserIdList  # レーザーIDリストを転写
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self.object = self." + objectName)  # オブジェクトを転写する
                parameter.setClassVar(self.object)  # メンバーのパラメータデータをセット
                self.object.MY_LASER_LIST = laserIdList  # メンバーのレーザーIDリストを転写
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトリストを返す
    # ---------------------------------------------------------------------------------------------------
    def getObjectList(self, DBSDIR, TABLE_NAME):
        try:
            objectList = []  # オブジェクトリスト
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self.object = self." + objectName)  # オブジェクトを転写する
                if (DBSDIR == self.object.DBSDIR):  # 選択されたテーブル名がオブジェクトのテーブル名かALLの時
                    if (TABLE_NAME == self.object.TABLE_NAME) or (
                            TABLE_NAME == GP.ALL):  # 選択されたテーブル名がオブジェクトのテーブル名かALLの時
                        objectList += [self.object]  # オブジェクトリストに追加
            return objectList  # オブジェクトリスト を返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示

