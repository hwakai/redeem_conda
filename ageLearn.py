import numpy as np
import math
from numpy import random
import multiprocessing
from kerasImport import *
from static import *
from learnBase import LearnBaseClass
from learnBase import MonitorCallBack
from qtBase import ProgressWindowClass
from classDef import AgeLearnParameterClass
from comb import CombClass
from PyQt5Import import *

#=======================================================================================================
#   クラス　AgeLearnClass
#=======================================================================================================
class AgeLearnClass():
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None                                                                                   # シングルトン初期化

    #---------------------------------------------------------------------------------------------------
    #   初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if AgeLearnClass._singleton is None:                                                        # クラス変数の_singletonの有無を確認
                # オブジェクト生成
                CH_LEARN  = AgeLearnBaseClass(GP.PCONT.CH.AGE.LEARN_CONF.LTYPE0)                        # CH学習クラスの生成
                LN_LEARN  = AgeLearnBaseClass(GP.PCONT.LN.AGE.LEARN_CONF.LTYPE0)                        # LN学習クラスの生成
                PPM_LEARN = AgeLearnBaseClass(GP.PCONT.PPM.AGE.LEARN_CONF.LTYPE0)                       # PPM学習クラスの生成
                MM_LEARN  = AgeLearnBaseClass(GP.PCONT.MM.AGE.LEARN_CONF.LTYPE0)                        # MM学習クラスの生成
                # オブジェクトのインスタンス変数のセット
                self.nameList = [name for name in locals().keys()
                                if (name != 'self') and
                                    (name != '__pydevd_ret_val_dict')]                                  # ローカル変数名リストを作成
                self.objectList = []                                                                    # オブジェクトリスト初期化
                for objectName in self.nameList:                                                        # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)                                     # オブジェクトのインスタンス変数のセット
                    exec("self.objectList += [self." + objectName + "]")                                # オブジェクトリストに追加
                pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if AgeLearnClass._singleton is None:                                                            # クラス変数の_singletonの有無を確認
            AgeLearnClass._singleton = AgeLearnClass()                                                  # クラスを生成して_singletonにセット
        return AgeLearnClass._singleton                                                                 # _singletonを返す

#=======================================================================================================
#   クラス AgeLearnBaseClass
#=======================================================================================================
class AgeLearnBaseClass(LearnBaseClass):
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        try:
            LearnBaseClass.__init__(self, TABLE_NAME)                                                   # スーパークラスの初期化
            self.parameter = AgeLearnParameterClass.getInstance()                                       # パラメータをセット
            self.treeWidget = GP.TREE.AGE_LEARN                                                         # ツリーウイジェット

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                           # エラー表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   学習
    #---------------------------------------------------------------------------------------------------
    def learn(self, LEVEL, monitorView):
        try:
            p = self.progress                                                                           # 進捗バー
            self.startNewLevel(self.CUT_TRIALS*2 + 2, p)                                                # 新しいレベルの進捗開始
            totalEpochs = self.INIT_EPOCHS + self.CUT_EPOCHS * self.CUT_TRIALS                          # 総エポック数計算
            CURPARTS = GP.CURPARTS                                                                      # コンテナ転写
            CURPARTS.MODEL_COMB = CURPARTS.MODEL_COMB_LIST[LEVEL]                                       # モデルコンボを転写
            MODEL_COMB = CURPARTS.MODEL_COMB_LIST[LEVEL]                                                # モデルコンボを転写
            SAVE_MODEL = MODEL_COMB.SAVE_MODEL                                                          # 保存モデルを転写
            SAVE_DATA = MODEL_COMB.SAVE_DATA                                                            # 保存モデルを転写
            MODEL_COMB.initialize()                                                                     # モデルコンボ初期化
            if SAVE_DATA.loadData():                                                                    # 訓練データの読込
                self.setSelfData(SAVE_DATA)                                                             # 自身の訓練データをセットして結果を返す
                SAVE_MODEL.MODEL = self.makeModelFunctional()                                           # モデルの新規作成
                SAVE_MODEL.MODEL._make_predict_function()                                                # predictを速くする
                SAVE_MODEL.HISTORY.history['epochs'] = self.INIT_EPOCHS                                 # 初期エポック結果保存用
                monitorView.initialize(totalEpochs)                                                     # 初期設定
                self.MY_CANVAS = monitorView.canvas                                                     # キャンバスを転写
                self.monitorCallBack = MonitorCallBack(self, p)                                         # モニターコールバック
                self.fit(self.INIT_EPOCHS, p)                                                           # 初期学習
                CURPARTS.MODEL_COMB_LIST[LEVEL+1].SAVE_DATA.MINMAX_DATA = SAVE_DATA.MINMAX_DATA         # MINMAX_DATAの転写
                CURPARTS.MODEL_COMB_LIST[LEVEL+1].saveModel(MODEL_COMB, p)                              # モデルの保存
                if self.stop == True:                                                                   # ストップフラグがセットされている時
                    return
                CURPARTS.MODEL_COMB_LIST[LEVEL+2].SAVE_DATA.MINMAX_DATA = SAVE_DATA.MINMAX_DATA         # MINMAX_DATAの転写
                for i in range(self.CUT_TRIALS):                                                        # カットトライアル回数実行
                    if i==0:                                                                            # 初回の時
                        SAMPLE_RATIO = self.SAMPLE_RATIO_0                                              # 上位のデータサンプル割合
                    else:                                                                               # 次回以後
                        SAMPLE_RATIO = self.SAMPLE_RATIO_N                                              # 次回以後のデータサンプル割合
                    if self.makeTrainDataLevel1(SAMPLE_RATIO, p):                                       # 上位のデータの抽出に成功した時
                        self.fit(self.CUT_EPOCHS, p)                                                    # 学習
                        SAVE_MODEL.HISTORY.history['epochs'] += self.CUT_EPOCHS                         # 総エポックを設定
                        if self.stop == True:                                                           # ストップフラグがセットされている時
                            CURPARTS.MODEL_COMB_LIST[LEVEL+2].saveModel(MODEL_COMB, p)                  # モデルの保存
                            CURPARTS.MODEL_COMB_LIST[LEVEL+2].initialize()                              # メモリーの解放
                            break
                CURPARTS.MODEL_COMB_LIST[LEVEL+2].saveModel(MODEL_COMB, p)                              # モデルの保存
                CURPARTS.MODEL_COMB_LIST[LEVEL+2].initialize()                                          # メモリーの解放
                MODEL_COMB.initialize()                                                                 # メモリーの解放
                self.endLevel(p)                                                                        # 現レベルの終了
                return                                                                                  # 終了
            self.showNone(p)                                                                            # None表示
            return                                                                                      # データが無かったら終了

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                        # エラー表示
            return

    #---------------------------------------------------------------------------------------------------
    #   追加学習
    #---------------------------------------------------------------------------------------------------
    def addLearn(self, LEVEL, monitorView):
        try:
            p = self.progress                                                                           # 進捗バー
            self.startNewLevel(self.CUT_TRIALS*2 + 1, p)                                                # 新しいレベルの進捗開始
            CURPARTS = GP.CURPARTS                                                                      # コンテナ転写
            CURPARTS.MODEL_COMB = CURPARTS.MODEL_COMB_LIST[LEVEL+2]                                     # モデルコンボを転写
            MODEL_COMB = CURPARTS.MODEL_COMB                                                            # モデルコンボを転写
            SAVE_MODEL = MODEL_COMB.SAVE_MODEL                                                          # 保存モデルを転写
            SAVE_DATA = MODEL_COMB.SAVE_DATA                                                            # 保存データを転写
            MODEL_COMB.initialize()                                                                     # モデルコンボ初期化
            if MODEL_COMB.loadModel():                                                                  # 訓練データの読込
                self.setSelfData(SAVE_DATA)                                                             # 自身の訓練データをセットして結果を返す
                exeEpochs = self.CUT_EPOCHS * self.CUT_TRIALS                                           # 実行エポック数再計算
                totalEpochs = SAVE_MODEL.HISTORY.history['epochs'] + exeEpochs                          # 総エポック数
                SAVE_MODEL.HISTORY.history['epochs'] = SAVE_MODEL.HISTORY.history['epochs']             # エポックを再設定
                monitorView.initialize(totalEpochs)                                                     # 初期設定
                self.MY_CANVAS = monitorView.canvas                                                     # キャンバスを転写
                self.MY_CANVAS .monitorLoseInitialize(SAVE_MODEL.HISTORY)                               # ロスモニター初期描画表示
                self.monitorCallBack = MonitorCallBack(self, p)                                         # モニターコールバック
                for i in range(self.CUT_TRIALS):                                                        # カットトライアル回数実行
                    SAMPLE_RATIO = self.SAMPLE_RATIO_N                                                  # 次回以後のデータサンプル割合
                    if self.makeTrainDataLevel1(SAMPLE_RATIO, p):                                       # 上位のデータの抽出に成功した時
                        self.fit(self.CUT_EPOCHS, p)                                                    # 学習
                        if self.stop == True:                                                           # ストップフラグがセットされている時
                            break
                        SAVE_MODEL.HISTORY.history['epochs'] += self.CUT_EPOCHS                         # 総エポックを設定
                if self.SAVE_FLAG:                                                                      # モデル保存フラグが真の時
                    MODEL_COMB.saveModel(MODEL_COMB, p)                                                 # モデルの保存
                    MODEL_COMB.initialize()                                                             # メモリーの解放
                MODEL_COMB.initialize()                                                                 # モデルコンボ初期化
                self.endLevel(p)                                                                        # 現レベルの終了
                return                                                                                  # 終了
            self.showNone(p)                                                                            # None表示
            return                                                                                      # データが無かったら終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示
            return

    #---------------------------------------------------------------------------------------------------
    #   初期学習の後のカットモデルだけ追加学習
    #---------------------------------------------------------------------------------------------------
    def learnCutModel(self, LEVEL, monitorView):
        try:
            p = self.progress                                                                           # 進捗バー
            self.startNewLevel(self.CUT_TRIALS*2 + 1, p)                                                # 新しいレベルの進捗開始
            CURPARTS = GP.CURPARTS                                                                      # コンテナ転写
            CURPARTS.MODEL_COMB = CURPARTS.MODEL_COMB_LIST[LEVEL+1]                                     # モデルコンボを転写
            MODEL_COMB = CURPARTS.MODEL_COMB                                                            # モデルコンボを転写
            SAVE_MODEL = MODEL_COMB.SAVE_MODEL                                                          # 保存モデルを転写
            SAVE_DATA = MODEL_COMB.SAVE_DATA                                                            # 保存データを転写
            MODEL_COMB.initialize()                                                                     # モデルコンボ初期化
            if MODEL_COMB.loadModel():                                                                  # 訓練データの読込
                self.setSelfData(SAVE_DATA)                                                             # 自身の訓練データをセットして結果を返す
                exeEpochs = self.CUT_EPOCHS * self.CUT_TRIALS                                                 # 実行エポック数
                totalEpochs = SAVE_MODEL.HISTORY.history['epochs'] + exeEpochs                          # 総エポック数
                SAVE_MODEL.HISTORY.history['epochs'] = SAVE_MODEL.HISTORY.history['epochs']             # エポックを再設定
                monitorView.initialize(totalEpochs)                                                     # 初期設定
                self.MY_CANVAS = monitorView.canvas                                                     # キャンバスを転写
                self.MY_CANVAS .monitorLoseInitialize(SAVE_MODEL.HISTORY)                               # ロスモニター初期描画表示
                self.monitorCallBack = MonitorCallBack(self, p)                                         # モニターコールバック
                for i in range(self.CUT_TRIALS):                                                        # トライアル回数実行
                    if i==0:                                                                            # 初回の時
                        SAMPLE_RATIO = self.SAMPLE_RATIO_0                                              # 上位のデータサンプル割合
                    else:                                                                               # 次回以後
                        SAMPLE_RATIO = self.SAMPLE_RATIO_N                                              # 次回以後のデータサンプル割合
                    if self.makeTrainDataLevel1(SAMPLE_RATIO, p):                                       # 上位のデータの抽出に成功した時
                        self.fit(self.CUT_EPOCHS, p)                                                    # 学習
                        if self.stop == True:                                                           # ストップフラグがセットされている時
                            break                                                                       # 中断する
                        SAVE_MODEL.HISTORY.history['epochs'] += self.CUT_EPOCHS                         # 総エポックを設定
                if self.SAVE_FLAG:                                                                      # モデル保存フラグが真の時
                    CURPARTS.MODEL_COMB_LIST[LEVEL+2].saveModel(MODEL_COMB, p)                          # モデルの保存
                    CURPARTS.MODEL_COMB_LIST[LEVEL+2].initialize()                                      # メモリーの解放
                MODEL_COMB.initialize()                                                                 # モデルコンボ初期化
                self.endLevel(p)                                                                        # 現レベルの終了
                return                                                                                  # 終了
            self.showNone(p)                                                                            # None表示
            return                                                                                      # データが無かったら終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示
            return


    #---------------------------------------------------------------------------------------------------
    #   学習データ生成
    #---------------------------------------------------------------------------------------------------
    def makeLearnData(self):
        try:
            p = self.progress                                                                           # 進捗バー
            self.startNewLevel(5, p)                                                                    # 新しいレベルの進捗開始
            CURPARTS = GP.CURPARTS                                                                      # コンテナ転写
            CURPARTS.MODEL_COMB = CURPARTS.MODEL_COMB_LIST[0]                                           # モデルコンボを転写
            SAVE_DATA = CURPARTS.MODEL_COMB.SAVE_DATA                                                   # 保存データを転写
            SAVE_DATA.initialize()                                                                      # 保存データ初期化
            merageData = self.getMerageData(p)                                                          # 全てのデータをマージしたフラットリストを取得する
            if merageData is not None:                                                                  # マージデータが有る時
                SAVE_DATA.normalizeNew(merageData, p)                                                   # マージデータの正規化
                if SAVE_DATA.createTrainData(merageData, p):                                            # 正常データと異常データ混合データから訓練データ作成
                    self.deleteObject(merageData)                                                       # 削除してメモリー解放
                    if self.setSelfData(SAVE_DATA):                                                     # 訓練データをセットして結果を返す
                        SAVE_DATA.saveData(SAVE_DATA, p)                                                # 訓練データを保存
                        SAVE_DATA.initialize()                                                          # メモリーの解放
                        self.endLevel(p)                                                                # 現レベルの終了
                        return                                                                          # 終了
                self.deleteObject(merageData)                                                           # 削除してメモリー解放
            self.showNone(p)                                                                            # None表示
            return                                                                                      # データが無かったら終了

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    #---------------------------------------------------------------------------------------------------
    #   マージデータを作成
    #---------------------------------------------------------------------------------------------------
    def getMerageData(self, p=None):
        try:
            self.startNewLevel(3, p)                                                                    # 新しいレベルの進捗開始
            CURPARTS = GP.CURPARTS                                                                      # コンテナを転写
            LABEL = CURPARTS.LABEL                                                                      # ラベルクラスを転写
            JBB = CURPARTS.JBB                                                                          # JBBを転写
            PRB = CURPARTS.PRB                                                                          # PRBを転写
            if self.USE_ABNORMAL:                                                                       # 異常値使用の時
                labelList = [LABEL.REG,LABEL.ACC]                                                       # 定期交換部品と異常終了部品
            else:                                                                                       # 異常値を使用しない時
                labelList = [LABEL.REG]                                                                 # 定期交換部品
            res = False                                                                                 # 結果フラグ初期化
            extractList = JBB.extractExcList(self.MY_LASER_LIST, labelList, p)                          # 指定したラベルリストを含むピリオッドリストを抽出する
            if extractList is not None:                                                                 # 抽出リストが有る時
                dataList = PRB.getCauseList(extractList, labelList, p)                                  # 指定した原因のフラットリストを取得
                if dataList is not None and  len(dataList) > 0:                                         # データリストが有る時
                    merageData = PRB.mergeDataAge(dataList, p)                                          # 全てのデータをマージしたフラットリストを取得する
                    self.deleteObject(dataList)                                                         # 削除してメモリー解放
                self.deleteObject(extractList)                                                          # 削除してメモリー解放
            return self.returnList(merageData, p)                                                       # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す

    #---------------------------------------------------------------------------------------------------
    #   後期学習データ生成
    #---------------------------------------------------------------------------------------------------
    def makeLearnDataAfter(self, LEVEL):
        try:
            p = self.progress                                                                           # 進捗バー
            self.startNewLevel(4, p)                                                                    # 新しいレベルの進捗開始
            CURPARTS = GP.CURPARTS                                                                      # コンテナ転写
            CURPARTS.MODEL_COMB = CURPARTS.MODEL_COMB_LIST[LEVEL]                                       # コンテナ転写
            SAVE_DATA = CURPARTS.MODEL_COMB.SAVE_DATA                                                   # 保存データを転写
            SAVE_MODEL = CURPARTS.MODEL_COMB_LIST[LEVEL-1].SAVE_MODEL                                   # 保存モデルを転写
            CURPARTS.MODEL_COMB.SAVE_MODEL = SAVE_MODEL                                                 # 保存モデルを転写
            SAVE_DATA0 = CURPARTS.MODEL_COMB_LIST[0].SAVE_DATA                                          # モデルコンボを転写
            if SAVE_DATA0.loadData(p):                                                                  # 訓練データの読込
                if SAVE_MODEL.loadModel(p):                                                             # 訓練データの読込
                    merageData = self.getMerageDataAfter(p)                                             # 全てのデータをマージしたフラットリストを取得する
                    if merageData is not None:                                                          # マージデータが有る時
                        SAVE_DATA.normalizeNew(merageData, p)                                           # マージデータの正規化
                        if SAVE_DATA.createTrainData(merageData, p):                                    # 正常データと異常データ混合データから訓練データ作成
                            self.deleteObject(merageData)                                               # 削除してメモリー解放
                            if self.setSelfData(SAVE_DATA):                                             # 訓練データをセットして結果を返す
                                SAVE_DATA.saveData(SAVE_DATA, p)                                        # 訓練データを保存
                                SAVE_DATA.initialize()                                                  # メモリーの解放
                                self.endLevel(p)                                                        # 現レベルの終了
                                return                                                                  # 終了
                        self.deleteObject(merageData)                                                   # 削除してメモリー解放
            self.showNone(p)                                                                            # None表示
            return                                                                                      # データが無かったら終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示
            return

    #---------------------------------------------------------------------------------------------------
    #   マージデータを作成
    #---------------------------------------------------------------------------------------------------
    def getMerageDataAfter(self, p=None):
        try:
            self.startNewLevel(3, p)                                                                    # 新しいレベルの進捗開始
            CURPARTS = GP.CURPARTS                                                                      # コンテナを転写
            SAVE_MODEL = CURPARTS.MODEL_COMB.SAVE_MODEL                                                 # SAVE_MODELを転写
            MINMAX_DATA = CURPARTS.MODEL_COMB_LIST[0].SAVE_DATA.MINMAX_DATA                             # MINMAX_DATAを転写
            LABEL = CURPARTS.LABEL                                                                      # ラベルクラスを転写
            JBB = CURPARTS.JBB                                                                          # JBBを転写
            PRB = CURPARTS.PRB                                                                          # PRBを転写
            if self.USE_ABNORMAL:                                                                       # 異常値使用の時
                labelList = [LABEL.REG,LABEL.ACC]                                                       # 定期交換部品と異常終了部品
            else:                                                                                       # 異常値を使用しない時
                labelList = [LABEL.REG]                                                                 # 定期交換部品
            res = False                                                                                 # 結果フラグ初期化
            extractList = JBB.extractExcList(self.MY_LASER_LIST, labelList, p)                          # 指定したラベルリストを含むピリオッドリストを抽出する
            if extractList is not None:                                                                 # 抽出リストが有る時
                dataList = PRB.getCauseList(extractList, labelList, p)                                  # 指定した原因のフラットリストを取得
                if dataList is not None and  len(dataList) > 0:                                         # データリストが有る時
                    merageData = PRB.mergeDataAgeAfter(dataList, SAVE_MODEL, MINMAX_DATA, p)            # 全てのデータをマージしたフラットリストを取得する
                    self.deleteObject(dataList)                                                         # 削除してメモリー解放
                self.deleteObject(extractList)                                                          # 削除してメモリー解放
            return self.returnList(merageData, p)                                                       # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # エラーを表示してからNoneを返す


