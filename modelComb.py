import os
import numpy as np
from numpy import random
import gc
from kerasImport import *
from staticImport import *
from sklearn.model_selection import train_test_split
from gpiBase import GpiBaseClass
from analysisBase import AnalysisBaseClass


# =======================================================================================================
#   クラス　HistoryClass
# =======================================================================================================
class HistoryClass():
    def __init__(self):  # 初期化
        self.history = {'acc': [], 'val_acc': [], 'loss': [], 'val_loss': [], 'epochs': 0, 'learnType': ''}  # ヒストリーを初期化

    # ---------------------------------------------------------------------------------------------------
    #   オリジナルタブのパラメーターをインスタンス変数に転写する
    # ---------------------------------------------------------------------------------------------------
    def appendHistory(self, his):
        try:
            self.history['acc'] += his.history['acc']  # acc配列をヒストリーに追加
            self.history['val_acc'] += his.history['val_acc']  # val_acc配列をヒストリーに追加
            self.history['loss'] += his.history['loss']  # loss配列をヒストリーに追加
            self.history['val_loss'] += his.history['val_loss']  # val_loss配列をヒストリーに追加

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return  # 終了

    # ---------------------------------------------------------------------------------------------------
    #   オリジナルタブのパラメーターをインスタンス変数に転写する
    # ---------------------------------------------------------------------------------------------------
    def initialize(self):
        try:
            self.history['acc'].clear()  # acc配列をクリア
            self.history['val_acc'].clear()  # val_acc配列をクリア
            self.history['loss'].clear()  # loss配列をクリア
            self.history['val_loss'].clear()  # val_loss配列をクリア
            self.history['epochs'] = 0  # epochsをクリア

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return  # 終了


# =======================================================================================================
#   クラス モデルコンボクラス
# =======================================================================================================
class ModelCombClass(AnalysisBaseClass):
    def __init__(self, PARTS, LEVEL, LEARN_TYPE, TABLE_NAME):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.SAVE_MODEL = SaveModelClass(PARTS, LEVEL, LEARN_TYPE, TABLE_NAME)  # SAVE_DATAを生成
            self.SAVE_DATA = SaveDataClass(PARTS, LEVEL, LEARN_TYPE, TABLE_NAME)  # SAVE_DATAを生成

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   初期化
    # ---------------------------------------------------------------------------------------------------
    def initialize(self):
        try:
            self.SAVE_MODEL.initialize()  # SAVE_MODELを初期化する
            self.SAVE_DATA.initialize()  # SAVE_DATA削除

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   パラメータの設定
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self, laserIdList, parameter):
        try:
            self.SAVE_MODEL.setClassVar(laserIdList, parameter)  # SAVE_MODEL保存パスをセットする
            self.SAVE_DATA.setClassVar(laserIdList, parameter)  # SAVE_DATA保存パスをセットする

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習単位と学習単位名をセットして保存パスをセットする
    # ---------------------------------------------------------------------------------------------------
    def setLearnUnit(self, LEARN_UNIT, UNIT_NAME):
        try:
            self.SAVE_MODEL.setLearnUnit(LEARN_UNIT, UNIT_NAME)  # SAVE_MODEL保存パスをセットする
            self.SAVE_DATA.setLearnUnit(LEARN_UNIT, UNIT_NAME)  # SAVE_DATA保存パスをセットする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   モデルの読み込み
    # ---------------------------------------------------------------------------------------------------
    def loadModel(self, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if self.SAVE_MODEL.loadModel():  # SAVE_MODELを読み込に成功した時
                self.SAVE_DATA.loadData(p)  # 保存データをファイルから読み込む
                self.endLevel(p)                                                                            # 現レベルの終了
                return True  # 成功を返す
            self.endLevel(p)                                                                            # 現レベルの終了
            return False  # 失敗を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習データ保存
    # ---------------------------------------------------------------------------------------------------
    def saveModel(self, SRC_MODEL, p=None):
        try:
            self.startNewLevel(2, p)  # 新しいレベルの進捗開始
            self.SAVE_MODEL.saveModel(SRC_MODEL.SAVE_MODEL, p)  # モデルを保存
            self.SAVE_DATA.saveData(SRC_MODEL.SAVE_DATA, p)  # 訓練データを保存
            return self.returnResult(True, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # 例外を表示


# =======================================================================================================
#   クラス 保存ベースクラス
# =======================================================================================================
class SaveBaseClass(AnalysisBaseClass):
    def __init__(self, PARTS, LEVEL, LEARN_TYPE, TABLE_NAME):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.LEVEL = LEVEL  # 学習レベルをセット
            self.LEARN_TYPE = LEARN_TYPE  # 学習タイプをセット
            self.TABLE_NAME = TABLE_NAME  # テーブル名をセット
            self.SOURCE = PARTS + "_" + LEARN_TYPE + str(LEVEL)  # 子ディレクトリ名
            self.LEARN_UNIT = None  # 学習単位名をセット
            self.UNIT_NAME = None  # 学習単位名をセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   パラメータの設定
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self, laserIdList, parameter):
        try:
            parameter.setClassVar(self)  # メンバーのパラメータデータをセット
            self.MY_LASER_LIST = laserIdList  # レーザーIDリストを転写

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習単位名をセットする
    # ---------------------------------------------------------------------------------------------------
    def setUnitName(self, UNIT_NAME):
        try:
            self.UNIT_NAME = UNIT_NAME  # 学習単位名をセット
            self.PREFIX = UNIT_NAME + "_"  # テーブル名の前置名をセット

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習単位と学習単位名をセットして保存パスをセットする
    # ---------------------------------------------------------------------------------------------------
    def setLearnUnit(self, LEARN_UNIT, UNIT_NAME):
        try:
            self.LEARN_UNIT = LEARN_UNIT  # 学習単位名をセット
            self.setUnitName(UNIT_NAME)  # 学習単位名をセット
            # 学習タイプから学習結果の保存パスをセット
            uploadtDir = GP.UPLOADDIR  # 親ディレクトリ
            outputDir = uploadtDir + REDEEM + "/" + self.SOURCE + "/" + self.UNIT_NAME + "/"  # 保存ディレクトリパス
            if not os.path.exists(outputDir):  # ディレクトリの有無を確認
                os.makedirs(outputDir)  # 途中のディレクトリを含めてディレクトリを作成
            self.learnModelPath = outputDir + "Model_" + str(GP.AGE_STEP) + ".log"  # 学習モデルパス
            self.learnWeightPath = outputDir + "Weight_" + str(GP.AGE_STEP) + ".log"  # 学習モデル係数パス
            self.learnHistoryPath = outputDir + "History_" + str(GP.AGE_STEP) + ".log"  # 学習ヒストリーパス

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス 保存モデルクラス
# =======================================================================================================
class SaveModelClass(SaveBaseClass):
    def __init__(self, PARTS, LEVEL, LEARN_TYPE, TABLE_NAME):  # 初期化
        try:
            SaveBaseClass.__init__(self, PARTS, LEVEL, LEARN_TYPE, TABLE_NAME)  # スーパークラスの初期化
            self.MODEL = None  # モデル初期化
            self.HISTORY = None  # ヒストリー初期化
            self.SCORE = None  # スコア初期化
            self.HISTORY = HistoryClass()  # ヒストリー生成
            self.HISTORY.history['learnType'] = LEARN_TYPE  # 学習タイプセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   初期化
    # ---------------------------------------------------------------------------------------------------
    def initialize(self):
        try:
            self.HISTORY.initialize()  # ヒストリーを初期化する
            self.MODEL = None  # モデル初期化
            self.SCORE = None  # スコア初期化

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   モデルの読み込み
    # ---------------------------------------------------------------------------------------------------
    def loadModel(self, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            # 学習済みモデルの読み込み
            if os.path.exists(self.learnModelPath):  # ファイルが有る時
                self.MODEL = model_from_json(open(self.learnModelPath, 'r').read())  # モデルを読み込む
            if os.path.exists(self.learnWeightPath):  # ファイルが有る時
                self.MODEL.load_weights(self.learnWeightPath)  # モデルに係数を読み込む
            # HISTORYの読み込み
            if os.path.exists(self.learnHistoryPath):  # ファイルが有る時
                self.loadHistory(self.learnHistoryPath)  # ヒストリーの読み込み
                history = self.HISTORY.history  # history辞書転写
                self.SCORE = history['score']  # スコアインスタンス変数にセット
                self.SCORE = [history['loss'][-1], history['acc'][-1]]  # スコアインスタンス変数にセット
                self.LOSE = history['loss'][-1]  # ロスインスタンス変数にセット
                self.LEARNED_TYPE = history['learnType']  # 学習タイプインスタンス変数にセット
                self.EPOCHS = history['epochs']  # エポックスインスタンス変数にセット
                self.MODEL.compile(loss='categorical_crossentropy', optimizer='sgd',
                                   metrics=['accuracy'])  # モデルをコンパイルする
                self.endLevel(p)                                                                            # 現レベルの終了
                return True  # 成功を返す
            self.endLevel(p)                                                                            # 現レベルの終了
            return False  # 失敗を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    # Historyの保存
    # ---------------------------------------------------------------------------------------------------
    def saveHistory(self, SRC_MODEL):
        try:
            history = SRC_MODEL.HISTORY.history
            historyPath = self.learnHistoryPath
            acc = history['acc']
            val_acc = history['val_acc']
            loss = history['loss']
            val_loss = history['val_loss']
            score = history['score']
            epochs = history['epochs']
            learnType = GP.CURPARTS.TYPE

            acc_Str = ",".join(np.array(acc, dtype='str')) + "\n"
            val_acc_Str = ",".join(np.array(val_acc, dtype='str')) + "\n"
            loss_Str = ",".join(np.array(loss, dtype='str')) + "\n"
            val_loss_Str = ",".join(np.array(val_loss, dtype='str')) + "\n"
            score_Str = ",".join(np.array(score, dtype='str')) + "\n"
            epochs_Str = str(epochs) + "\n"
            learnType_Str = str(learnType) + "\n"
            strLines = acc_Str + val_acc_Str + loss_Str + val_loss_Str + score_Str + epochs_Str + learnType_Str
            dirName = os.path.dirname(historyPath)  # ディレクトリ名
            if not os.path.exists(dirName):  # ディレクトリの有無を確認
                os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
            with open(file=historyPath, mode="w", encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                f.writelines(strLines)

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # =========================================================
    # Historyの読み込み
    # =========================================================
    def loadHistory(self, historyPath):
        try:
            self.HISTORY.initialize()  # ヒストリー初期化
            history = self.HISTORY.history  # history辞書転写
            with open(file=historyPath, mode="r", encoding="utf-8") as file:  # "utf-8"でファイルをオープン
                acc_Str = "".join(file.readline().splitlines()).split(",")  # accストリング配列を読み込む
                val_acc_Str = "".join(file.readline().splitlines()).split(",")  # val_accストリング配列を読み込む
                loss_Str = "".join(file.readline().splitlines()).split(",")  # lossストリング配列を読み込む
                val_loss_Str = "".join(file.readline().splitlines()).split(",")  # VALロスストリング配列を読み込む
                score_Str = "".join(file.readline().splitlines()).split(",")  # スコアストリング配列を読み込む
                epochs_Str = file.readline().splitlines()  # epochsストリングを読み込む
                learnType_Str = file.readline().splitlines()  # learnTypeストリングを読み込む
            acc = [float(s) for s in acc_Str]  # acc配列を作成
            val_acc = [float(s) for s in val_acc_Str]  # val_acc配列を作成
            loss = [float(s) for s in loss_Str]  # loss配列を作成
            val_loss = [float(s) for s in val_loss_Str]  # VALロス配列を作成
            score = [float(s) for s in score_Str]  # スコア配列を作成
            epochs = int(epochs_Str[0])  # エポックスを作成
            learnType = learnType_Str[0]  # learnTypeを作成
            history['acc'] = acc  # acc配列をヒストリーにセット
            history['val_acc'] = val_acc  # val_acc配列をヒストリーにセット
            history['loss'] = loss  # loss配列をヒストリーにセット
            history['val_loss'] = val_loss  # val_loss配列をヒストリーにセット
            history['score'] = score  # score配列をヒストリーにセット
            history['epochs'] = epochs  # epochs配列をヒストリーにセット
            history['learnType'] = learnType  # learnType配列をヒストリーにセット
            return history  # ヒストリーを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   モデルの保存
    # ---------------------------------------------------------------------------------------------------
    def saveModel(self, SRC_MODEL, p=None):
        try:
            # モデルの保存
            dirName = os.path.dirname(self.learnModelPath)  # ディレクトリ名
            if not os.path.exists(dirName):  # ディレクトリの有無を確認
                os.makedirs(dirName)  # 途中のディレクトリを含めてディレクトリを作成
            with open(self.learnModelPath, "w", encoding="utf-8") as file:  # "utf-8"でファイルをオープン
                file.write(SRC_MODEL.MODEL.to_json())  # モデルを保存
            SRC_MODEL.MODEL.save_weights(self.learnWeightPath)  # モデルの係数を保存
            self.saveHistory(SRC_MODEL)  # HISTORYの保存
            emit(p)  # 進捗バーに進捗を送る

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス　SaveDataClass
# =======================================================================================================
class SaveDataClass(SaveBaseClass):
    def __init__(self, PARTS, LEVEL, LEARN_TYPE, TABLE_NAME):  # 初期化
        try:
            SaveBaseClass.__init__(self, PARTS, LEVEL, LEARN_TYPE, TABLE_NAME)  # スーパークラスの初期化
            self.MINMAX_DATA = MinmaxClass(TABLE_NAME)  # MINMAX_DATA生成
            self.SOURCE_DATA = TrainClass(TABLE_NAME)  # SOURCE_DATA生成
            self.TRAIN_DATA = TrainClass(TABLE_NAME)  # TRAIN_DATA生成
            self.TEST_DATA = TrainClass(TABLE_NAME)  # TEST_DATA生成

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            ppass

    # ---------------------------------------------------------------------------------------------------
    #   学習ターゲットパス
    # ---------------------------------------------------------------------------------------------------
    @property
    def targetPath(self):  # ターゲットパス
        tgtDir = GP.UPLOADDIR + self.DBSDIR + "/" + self.SOURCE + "/" + self.UNIT_NAME + "/"  # ターゲットディレクトリ作成
        strPath = tgtDir + self.TABLE_NAME + ".log"  # ターゲットパス作成
        return strPath  # ターゲットパスを返す

    # ---------------------------------------------------------------------------------------------------
    #   元データから訓練データと評価データを分離する
    # ---------------------------------------------------------------------------------------------------
    def separateTrainData(self, normal, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if normal is not None:
                train = []
                test = []
                for labelNo, label in enumerate(GP.CONT.LABEL_LIST.LIST):  # ラベルリストをすべて実行
                    index = np.where(normal[:, GP.CONT.TRN.LABEL] == label)[0]  # 当該ラベルのインデックスを取得
                    SAMPLES = len(index)
                    if SAMPLES > 0:  # インデックスが有る時
                        trainSAMPLES = int(SAMPLES * 0.8)
                        testSAMPLES = SAMPLES - trainSAMPLES
                        trainIndex = random.choice(index, trainSAMPLES, replace=False)  # 重複無しでランダムサンプルしたトレインインデックスをセット
                        testIndex = index[~np.in1d(index, trainIndex)]  # トレイン以外のインデックスをセット
                        labelTrain = normal[trainIndex]  # ラベルのトレインデータをセット
                        labelTest = normal[testIndex]  # ラベルのテストデータをセット
                        train += list(labelTrain)  # トレインリストに追加
                        test += list(labelTest)  # テストリストに追加
                train = np.array(train)  # numpy配列化
                trainSAMPLES = len(train)
                index = list(range(trainSAMPLES))
                train = train[random.choice(index, trainSAMPLES, replace=False)]  # 重複無しでランダムサンプルしたトレインデータをセット
                test = np.array(test)  # numpy配列化
                testSAMPLES = len(test)
                index = list(range(testSAMPLES))
                test = test[random.choice(index, testSAMPLES, replace=False)]  # 重複無しでランダムサンプルしたテストデータをセット
                return self.returnList2(train, test, p)  # トレインデータとテストデータを返す
            return self.returnNone2(p)  # Noneを返す

        except Exception as e:  # 例外
            return self.returnError2(e, p)  # エラーを表示してから(None,None)を返す

    # ---------------------------------------------------------------------------------------------------
    #   元データから訓練データと評価データを作成
    # ---------------------------------------------------------------------------------------------------
    def createTrainData(self, normal, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if normal is not None:  # 元データが有る時
                train, test = self.separateTrainData(normal, p)  # 元データから訓練データと評価データを作成
                self.SOURCE_DATA.flatBase = normal  # SOURCE_DATAのベースパックをセット
                self.TRAIN_DATA.flatBase = train  # TRAIN_DATAのフラットベースをセット
                self.TRAIN_DATA.setTrainData(GP.CONT.LABEL_LIST.NO_LIST)  # 訓練データをセットする
                self.TEST_DATA.flatBase = test  # TEST_DATAのフラットベースをセット
                self.TEST_DATA.setTrainData(GP.CONT.LABEL_LIST.NO_LIST)  # 訓練データをセットする
                return self.returnResult(True, p)  # 実行時間を表示してからデータを返す
            return self.returnResult(None, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してから(None,None)を返す

    # ---------------------------------------------------------------------------------------------------
    #   保存データをDBに保存
    # ---------------------------------------------------------------------------------------------------
    def saveData(self, SRC_DATA, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            SRC_DATA.TRAIN_DATA.setTrainType(GP.TRAIN_TYPE.TRAIN)  # TRAIN_DATAの訓練データタイプをTRAINにセット
            SRC_DATA.TEST_DATA.setTrainType(GP.TRAIN_TYPE.TEST)  # TEST_DATAの訓練データタイプをTESTにセット
            self.flatBase = np.concatenate([SRC_DATA.MINMAX_DATA.flatBase,
                                            SRC_DATA.TRAIN_DATA.flatBase,
                                            SRC_DATA.TEST_DATA.flatBase], axis=0)  # すべてコンケート
            GP.SVR.DBSServer.makeLocDBFromObject(self, GP.BASE_TYPE.F_BASE, p)  # フラットなリストをDBにセーブ
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e, p)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   保存データをDBから読み込む
    # ---------------------------------------------------------------------------------------------------
    def loadData(self, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            filterList = self.MY_LASER_LIST  # フィルターリスト
            self.flatBase = GP.SVR.DBSServer.getLocFlatListNoDistinct(self, p)  # DBからフラットなリストをロード
            if self.flatBase is not None:  # ベースリストが有る時
                MINVAL = self.flatBase[self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.MIN][0]  # ベースリストから最小値を取得
                MAXVAL = self.flatBase[self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.MAX][0]  # ベースリストから最大値を取得
                self.MINMAX_DATA.makeBase(MINVAL, MAXVAL)  # MINMAX_DATAフラットベース作成
                flatBase = self.flatBase[self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.TRAIN]  # ベースリストから訓練データを取得
                self.TRAIN_DATA.flatBase = flatBase  # 訓練データのフラットベースををセット
                flatBase = self.flatBase[self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.TEST]  # ベースリストから評価データを取得
                self.TEST_DATA.flatBase = flatBase  # 評価データのフラットベースををセット
                flatBase = self.flatBase[
                    (self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.TRAIN) |  # ベースリストからソースデータを取得
                    (self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.TEST)]  # ベースリストからソースデータを取得
                self.SOURCE_DATA.flatBase = flatBase  # ソースデータのフラットベースををセット
                self.TRAIN_DATA.setTrainData(GP.CONT.LABEL_LIST.NO_LIST)  # 訓練データをセットする
                self.TEST_DATA.setTrainData(GP.CONT.LABEL_LIST.NO_LIST)  # 訓練データをセットする
                return self.returnResult(True, p)  # 実行時間を表示してからデータを返す
            return self.returnResult(None, p)  # Noneを表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してから(None,None)を返す

    # ---------------------------------------------------------------------------------------------------
    #   メモリーの解放
    # ---------------------------------------------------------------------------------------------------
    def initialize(self, p=None):
        try:
            self.startNewLevel(4, p)  # 新しいレベルの進捗開始
            self.releaseBase()  # SAVE_DATA削除
            self.MINMAX_DATA.releaseBase(p)  # メモリーの解放
            self.SOURCE_DATA.releaseBase(p)  # メモリーの解放
            self.TRAIN_DATA.releaseBase(p)  # メモリーの解放
            self.TEST_DATA.releaseBase(p)  # メモリーの解放
            gc.collect()  # メモリーを解放する
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   新規に正規化
    # ---------------------------------------------------------------------------------------------------
    def normalizeNew(self, train, p=None):
        try:
            if len(train) > 0:
                TRN = GP.CONT.TRN  # TRNを転写
                X_BASE = GP.X_LIST.X_BASE  # Xベース転写
                min = train[0].copy()  # trainを最小値に転写
                min[X_BASE:] = 0.0  # 最小値の初期化
                max = min.copy()  # 最小値を最大値に複写
                min[X_BASE:] = np.nanmin(train[:, X_BASE:], axis=0)  # Xデータ列毎の最小値
                max[X_BASE:] = np.nanmax(train[:, X_BASE:], axis=0)  # Xデータ列毎の最大値
                deff = max[X_BASE:] - min[X_BASE:]  # 差分
                deff = np.where(deff == 0, 1.0, deff)  # 差分が0の時は1.0にする
                train[:, X_BASE:] = (train[:, X_BASE:] - min[X_BASE:]) / deff  # データパックのxを正規化
                self.MINMAX_DATA.makeBase(min, max)  # SAVE_DATA.MINMAX_DATAのフラットベース作成
            emit(p)  # 進捗バーに進捗を送る

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス　MinmaxClass
# =======================================================================================================
class MinmaxClass(GpiBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            GpiBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.flatBase = None  # フラットベースを初期化
            self.MINVAL = None  # 最小値を初期化
            self.MAXVAL = None  # 最大値を初期化

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   フラットベース作成
    # ---------------------------------------------------------------------------------------------------
    def makeBase(self, minVal, maxVal):
        try:
            minVal[self.TRAIN_TYPE] = GP.TRAIN_TYPE.MIN
            maxVal[self.TRAIN_TYPE] = GP.TRAIN_TYPE.MAX
            self.MINVAL = minVal  # ラベル毎の最小値をセット
            self.MAXVAL = maxVal  # ラベル毎の最大値をセット
            self.flatBase = np.concatenate([[minVal], [maxVal]])  # 最小値配列と最大値配列を結合

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   データコピー
    # ---------------------------------------------------------------------------------------------------
    def copyData(self, src):
        try:
            self.MINVAL = src.MINVAL  # 最小値をコピー
            self.MAXVAL = src.MAXVAL  # 最大値をコピー

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ベースリストと最大値最小値リストをファイルからロード
    # ---------------------------------------------------------------------------------------------------
    def loadDataFile(self):
        try:
            self.loadListFromFile()  # ファイルからフラットなリストをロード
            if self.flatBase is not None:  # ベースリストが有る時
                self.MINVAL = self.flatBase[self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.MIN][0]  # ベースリストから最小値を取得
                self.MAXVAL = self.flatBase[self.flatBase[:, self.TRAIN_TYPE] == GP.TRAIN_TYPE.MAX][0]  # ベースリストから最大値を取得
            else:  # ベースリストが無い時
                self.MINVAL = None  # 最小値を初期化
                self.MAXVAL = None  # 最大値を初期化

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ベース変数を削除してメモリーを解放する
    # ---------------------------------------------------------------------------------------------------
    def releaseBase(self, p=None):
        try:
            if self.flatBase is not None:  # フラットベースが有る時
                del self.flatBase  # メモリーの解放
                self.flatBase = None  # フラットベースを初期化する
            if self.MINVAL is not None:  # MINVAL有る時
                del self.MINVAL  # メモリーの解放
                self.MINVAL = None  # 最小値を初期化
            if self.MAXVAL is not None:  # MAXVAL有る時
                del self.MAXVAL  # メモリーの解放
                self.MAXVAL = None  # 最大値を初期化
            gc.collect()  # メモリーを解放する
            emit(p)  # 進捗を進める

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示


# =======================================================================================================
#   クラス　TrainClass
# =======================================================================================================
class TrainClass(GpiBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            GpiBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.flatBase = None  # ベースリストの初期化
            self.trainX = None  # 訓練Xデータ初期化
            self.trainY = None  # 訓練Yデータ初期化

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ベース変数を削除してメモリーを解放する
    # ---------------------------------------------------------------------------------------------------
    def releaseBase(self, p=None):
        try:
            if self.flatBase is not None:  # フラットベースが有る時
                del self.flatBase  # フラットベースを削除
                self.flatBase = None  # フラットベースを初期化する
            if self.trainX is not None:  # 訓練Xデータが有る時
                del self.trainX  # 訓練Xデータのメモリーを解放する
                self.trainX = None  # 訓練Xデータを初期化する
            if self.trainY is not None:  # 訓練Yデータが有る時
                del self.trainY  # 訓練Yデータのメモリーを解放する
                self.trainY = None  # 訓練Yデータを初期化する
            gc.collect()  # メモリーを解放する
            emit(p)  # 進捗を進める

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   trainXを抽出してtrainYにkeras形式のラベルをセットする
    # ---------------------------------------------------------------------------------------------------
    def setTrainData(self, labelNoList):
        try:
            if self.flatBase is not None and len(self.flatBase) > 0:  # フラットベースが有る時
                train = self.flatBase  # 訓練
                self.trainX = np.array(train[:, GP.X_LIST.X_BASE:],'float')  # 訓練Xデータをセットする
                n_label = len(labelNoList)  # ラベル数
                if train is None:  # trainが無いとき
                    keras_y = np.array([], dtype='O').reshape((0, n_label))  # 空のkeras形式のラベルをセット
                else:  # trainが有る時
                    if len(train) == 0:  # trainが無いとき
                        keras_y = np.array([], dtype='O').reshape((0, n_label))  # 空のkeras形式のラベルをセット
                    else:  # trainが有るとき
                        labelNo = [labelNoList[label] for label in train[:, self.LABEL]]  # ラベル番号を取得
                        keras_y = np.array(to_categorical(labelNo, n_label), dtype='int')  # ラベル番号をKERASの形式に変換
                self.trainY = keras_y  # keras形式のラベルをtrainYにセットする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   訓練データタイプセット
    # ---------------------------------------------------------------------------------------------------
    def setTrainType(self, trainType):
        try:
            if self.flatBase is not None:  # フラットベースが有る時
                self.flatBase[:, self.TRAIN_TYPE] = trainType  # 訓練データタイプセット

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   保存データをDBから読み込む
    # ---------------------------------------------------------------------------------------------------
    def loadData(self, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            self.flatBase = GP.SVR.DBSServer.getLocFlatList(self, p)  # DBからフラットなリストをロード
            return self.returnResult(self.flatBase is not None, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してから(None,None)を返す

