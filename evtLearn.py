import numpy as np
from numpy import random
import multiprocessing
from static import *
from kerasImport import *
from staticImport import *
from learnBase import LearnBaseClass
from classDef import EvtLearnParameterClass

from comb import CombClass


# =======================================================================================================
#   クラス　EvtLearnClass
# =======================================================================================================
class EvtLearnClass():
    # ---------------------------------------------------------------------------------------------------
    #   クラス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None  # シングルトン初期化

    # ---------------------------------------------------------------------------------------------------
    #   初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self):  # 初期化
        try:
            if EvtLearnClass._singleton is None:  # クラス変数の_singletonの有無を確認
                # オブジェクト生成
                CH_LEARN = EvtLearnBaseClass(GP.PCONT.CH.EVT)  # CH学習クラスの生成

                # オブジェクトのインスタンス変数のセット
                self.nameList = [name for name in locals().keys()
                                 if (name != 'self') and
                                 (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
                self.objectList = []  # オブジェクトリスト初期化
                for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                    exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
                    exec("self.objectList += [self." + objectName + "]")  # オブジェクトリストに追加
                pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if EvtLearnClass._singleton is None:  # クラス変数の_singletonの有無を確認
            EvtLearnClass._singleton = EvtLearnClass()  # クラスを生成して_singletonにセット
        return EvtLearnClass._singleton  # _singletonを返す


# =======================================================================================================
#   クラス EvtLearnBaseClass
# =======================================================================================================
class EvtLearnBaseClass(LearnBaseClass):
    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, PARTSCONT):  # 初期化
        try:
            LearnBaseClass.__init__(self, PARTSCONT.LEARN_CONF.LTYPE0)  # スーパークラスの初期化
            GP.PCONT.CH.setTypes(GP.LEARN_TYPE.EVT)  # タイプとレベルセット
            self.parameter = EvtLearnParameterClass.getInstance()  # パラメータをセット
            self.treeWidget = GP.TREE.EVT_LEARN  # ツリーウイジェット

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習
    # ---------------------------------------------------------------------------------------------------
    def learn(self, monitorView):
        try:
            p = self.progress
            self.startNewLevel(5, p)                                                                    # 新しいレベルの進捗開始
            self.MY_VIEW = monitorView
            self.MY_CANVAS = monitorView.canvas
            if self.makeTrainData(p):                                                                   # 訓練データの作成
                self.MODEL = self.makeModelFunctional(p)                                                # モデルの新規作成
                self.HISTORY = self.fit(p)                                                              # 学習
                self.saveModel(p)                                                                       # モデルの保存
                self.SAVE_DATA.releaseBase(p)                                                           # メモリーの解放
                self.deleteObject(self.HISTORY)                                                         # メモリーの解放
                self.endLevel(p)                                                                        # 現レベルの終了
                return                                                                                  # 終了
            self.showNone(p)                                                                            # None表示してからデータを返す

        except Exception as e:                                                                          # 例外 
            self.showError(e, p)                                                                        # エラー表示
            return

    # ------------------------------------------------------------
    #   学習データ作成
    # ------------------------------------------------------------
    def makeTrainData(self, p=None):
        try:
            self.startNewLevel(4, p)  # 新しいレベルの進捗開始
            SAVE_DATA = GP.CURPARTS.MODEL_COMB.SAVE_DATA
            train = self.mergeData(p)  # 定期交換時のデータパックを作成する
            train = GP.CURPARTS.PRB.mergeDataAge(dataList, p)  # 全てのデータをマージしたフラットリストを取得する
            if train is not None:  # データパックが有る時
                flatten = self.flattenEachLabel(train)  # ラベル毎のデータ数を平準化
                if len(flatten) > 0:
                    SAVE_DATA.normalizeNew(flatten, p)  # 正規化
                    res = SAVE_DATA.createTrainData(flatten, p)  # 正常データと異常データ混合データから訓練データ作成
                    self.deleteObject(flatten)  # 削除してメモリー解放
                    return self.returnResult(res, p)  # 実行時間を表示してからデータを返す
            return self.returnResult(False, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnResultError(e, p)  # エラーを表示してからFalseを返す

    # ---------------------------------------------------------------------------------------------------
    #   全てのデータをマージしたトレインリストを取得する
    # ---------------------------------------------------------------------------------------------------
    def mergeData(self, p=None):
        try:
            self.startNewLevel(4, p)  # 新しいレベルの進捗開始
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            JBB = GP.CURPARTS.JBB  # JBBを転写
            ERB = GP.CURPARTS.ERB  # ERBを転写
            PRB = GP.CURPARTS.PRB  # PRBを転写
            PRB.loadPeriodDic(p)  # CHPRAのピリオッド辞書を読み込む
            trainList = []  # トレインリスト初期化
            excList = [GP.PCONT.CH.LABEL.REG, GP.PCONT.LN.LABEL.REG]  # 排他的なラベルリスト作成
            train = JBB.extractExcList(self.MY_LASER_LIST, GP.PCONT.CH.LABEL.REG,
                                       p)  # ピリオッド内で排他的なデータのレーザーID＆ピリオッドリストを抽出する
            trainList += list(train)
            incList = list(set(GP.PEX_LIST.LIST) - set(excList))  # 非排他的なラベルリスト作成
            train = JBB.extractIncPack(incList, self.ABN_LEN, p)  # ピリオッド内で非排他的なデータパックをを抽出する
            trainList += train
            train = ERB.extractIncPack(GP.GR_ERR_LIST.LIST, self.ABN_LEN, p)  # ピリオッド内で非排他的なデータパックをを抽出する
            trainList += train
            trainList = np.array(trainList, 'O')  # NUMPY配列化
            return self.returnList(trainList, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す


