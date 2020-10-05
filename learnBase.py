import os
import math
import numpy as np
import matplotlib.pyplot as plt
from numpy import random
from sklearn.model_selection import train_test_split
from kerasImport import *
from staticImport import *
from analysisBase import AnalysisBaseClass
from qtBase import ProgressWindowClass
from PyQt5Import import *

#=======================================================================================================
#   LearnBaseClass クラス
#=======================================================================================================
class LearnBaseClass(AnalysisBaseClass):
    stopSignal = pyqtSignal()                                                                           # ストップシグナル
    def __init__(self, TABLE_NAME):                                                                     # 初期化
        AnalysisBaseClass.__init__(self, TABLE_NAME)                                                    # スーパークラスの初期化
        try:
            self.progress = ProgressWindowClass()                                                       # 進捗ダイアローグ生成
            self.trainX = None                                                                          # 訓練X初期化
            self.trainY = None                                                                          # 訓練Y初期化
            self.testX = None                                                                           # 評価X初期化
            self.testY = None                                                                           # 評価Y初期化
            self.stop = False;                                                                          # ストップフラグ初期化
            self.stopSignal.connect(self.STOP_SIGNAL)                                                   # ストップシグナルをストップメソッドと結合

        except Exception as e:                                                                          # 例外 
            self.printError(e)                                                                          # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   CH年齢学習時にすべてのオブジェクトのインスタンス変数をセットする
    #---------------------------------------------------------------------------------------------------
    def setClassVar(self, laserIdList, parameter):
        try:
            parameter.setClassVar(self)                                                                 # メンバーのパラメータデータをセット
            self.MY_LASER_LIST = laserIdList                                                            # レーザーIDリストを転写
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   訓練データセット
    #---------------------------------------------------------------------------------------------------
    def setSelfData(self, SAVE_DATA):
        try:
            self.trainX = SAVE_DATA.TRAIN_DATA.trainX                                                   # 訓練X
            self.trainY = SAVE_DATA.TRAIN_DATA.trainY                                                   # 訓練Y
            self.testX = SAVE_DATA.TEST_DATA.trainX                                                     # 評価X
            self.testY = SAVE_DATA.TEST_DATA.trainY                                                     # 評価Y
            if (self.trainX is not None and
                self.trainY is not None and
                self.testX is not None and
                self.testY is not None):                                                                # データパックがすべて有る時
                return True                                                                             # 結果を返す
            self.showNone()                                                                            # None表示
            return False                                                                                # 偽を返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # エラー表示
            return False

    #---------------------------------------------------------------------------------------------------
    #   学習
    #---------------------------------------------------------------------------------------------------
    def fit(self, exeEpochs, p=None):
        try:
            from keras import backend as K
            """
            print(K.backend())
            from keras.backend.tensorflow_backend import tf
            num_cores = 8
            num_CPU = 1
            num_GPU = 1
            config = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=num_cores,
                                    inter_op_parallelism_threads=num_cores,
                                    allow_soft_placement=True,
                                    device_count={'CPU': num_CPU,
                                                  'GPU': num_GPU}
                                    )
            session = tf.compat.v1.Session(config=config)
            K.set_session(session)
            #seed = 0
            #tf.session_with_seed(seed, disable_gpu=T, disable_parallel_cpu=F)
            """
            self.startNewLevel(exeEpochs, p)                                                            # 新しいレベルの進捗開始
            SAVE_MODEL = GP.CURPARTS.MODEL_COMB.SAVE_MODEL                                              # 保存モデルを転写
            history = SAVE_MODEL.HISTORY.history                                                        # historyの転写
            self.monitorCallBack.epoch = 0                                                              # コールバックのエポック初期化
            self.monitorCallBack.epochs = exeEpochs                                                     # コールバックのエポック数セット
            his = SAVE_MODEL.MODEL.fit(self.trainX, self.trainY,                                        # 訓練データ
                                    batch_size=self.BATCH_SIZE,                                         # ミニバッチサイズ
                                    epochs=exeEpochs,                                                   # エポック
                                    verbose=self.VERBOSE,                                               # 0:出力しない 1:プログレスバー 2:エポックごと
                                    validation_data=(self.testX, self.testY),                           # 評価データ
                                    callbacks=[self.monitorCallBack])                                   # コールバック
            history["score"] = SAVE_MODEL.SCORE                                                         # 正解率セット
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラーを表示

    #---------------------------------------------------------------------------------------------------
    #   ラベル毎のデータ数を平準化
    #   少ないときは乱数で分散させる
    #---------------------------------------------------------------------------------------------------
    def flattenEachLabel(self, mergeTrain, p=None):
        try:
            self.startNewLevel(len(mergeTrain), p)                                                      # 新しいレベルの進捗開始
            TRN = GP.CONT.TRN                                                                           # TRNを転写
            labelSamples = math.ceil(self.SAMPLES/len(mergeTrain)*2)                                    # レーザーラベル毎のデータ数
            trainList = []                                                                              # トレインリストを初期化
            trainDic = {}                                                                               # trainDicを初期化
            for label in GP.CONT.LABEL_LIST.LIST:                                                       # ラベルリストをすべて実行
                trainDic[label] = []                                                                    # ラベルリストを初期化
            for (LASER_ID,PERIOD), periodData in mergeTrain.items():                                    # マージデータをすべて実行
                for label in GP.CONT.LABEL_LIST.LIST:                                                   # ラベルリストをすべて実行
                    index0 = np.where(periodData[:,TRN.LABEL] == label)[0]                              # ラベルを持つインデックス
                    length = len(index0)                                                                # データ長
                    if length >= labelSamples:                                                          # Xデータ長がサンプル数以上の時
                        index = random.choice(index0, labelSamples, replace=False)                      # 重複無しでランダムサンプルしたインデックスをセット
                        train = periodData[index]                                                       # トレインデータを抽出
                        trainDic[label] += list(train)                                                  # ラベルリストに追加
                emit(p)                                                                                 # 進捗バーに進捗を送る
            SAMPLES = self.SAMPLES                                                                      # ラベル毎の総データ数
            for label in GP.CONT.LABEL_LIST.LIST:                                                       # ラベルリストをすべて実行
                labelData =  trainDic[label]
                length = len(labelData)
                index0 =  list(range(length))
                if length >= SAMPLES:
                    index = random.choice(index0, SAMPLES, replace=False)                               # ラベルリストの総数調整
                else:
                    index = random.choice(index0, SAMPLES, replace=True)                                # ラベルリストの総数調整
                labelTrain = np.array(labelData)                                                        # ラベルリストの総数調整
                labelTrain = labelTrain[index]                                                          # ラベルリストの総数調整
                trainList += list(labelTrain)                                                           # トレインリストに追加
            self.deleteObject(trainDic)                                                                 # 削除してメモリー解放
            trainList = np.array(trainList,'O')                                                         # リスト型のデータパックを返す
            return self.returnList(trainList, p)                                                        # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # 実行時間を表示してから結果を返す

    #---------------------------------------------------------------------------------------------------
    #   訓練データの上位のデータの抽出
    #---------------------------------------------------------------------------------------------------
    def extractTopData(self, train, predict, SAMPLE_RATIO, p=None):
        try:
            self.startNewLevel(GP.CONT.LABEL_LIST.length, p)                                            # 新しいレベルの進捗開始
            X_BASE = GP.X_LIST.X_BASE                                                                   # Xベース転写
            trainList = []                                                                              # トレインリスト初期化
            for labelNo,label in enumerate(GP.CONT.LABEL_LIST.LIST):                                    # ラベルリストをすべて実行
                print(label)                                                                            # ラベルを表示
                index = np.where(train[:,GP.CONT.TRN.LABEL] == label)[0]                                # 当該ラベルのインデックスを取得
                if len(index) > 0:                                                                      # インデックスが有る時
                    labelTrain = train[index]                                                           # 当該ラベルのトレインデータ
                    labelPredict = predict[index]                                                       # 当該ラベルの予測値
                    # 当該ラベル
                    labelPredict0 = labelPredict[:,X_BASE + labelNo]                                    # 当該ラベルの予測値
                    n = int(len(labelPredict0) * SAMPLE_RATIO)                                          # 上位のデータサンプル割合
                    sortIndex = np.argsort(labelPredict0)[::-1]                                         # 降順で並べた時のインデックス
                    indexList = list(sortIndex[:n])                                                     # 上位データを追加
                    indexList = np.unique(indexList)                                                    # インデックスリストをユニークにする
                    if len(indexList) > 0:                                                              # トレインデータが有る時
                        labelTrain = labelTrain[indexList]                                              # トレインデータを降順で並べる
                        trainList += list(labelTrain)                                                   # トレインリストに追加
                    self.deleteObject(indexList)                                                        # 削除してメモリー解放
                    self.deleteObject(labelPredict0)                                                    # 削除してメモリー解放
                    self.deleteObject(labelPredict)                                                     # 削除してメモリー解放
                    self.deleteObject(labelTrain)                                                       # 削除してメモリー解放
                self.deleteObject(index)                                                                # 削除してメモリー解放
                emit(p)
            trainList = np.array(trainList,'O')                                                         # NUMPY配列化
            return self.returnList(trainList, p)                                                        # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # 実行時間を表示してから結果を返す

    #---------------------------------------------------------------------------------------------------
    #   予測値の上位のデータの抽出(予測結果の前後のラベルのデータを加える)
    #---------------------------------------------------------------------------------------------------
    def getTopDataIndex(self, train, predict):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            X_BASE = GP.X_LIST.X_BASE                                                                   # Xベース転写
            trainList = []                                                                              # トレインリスト初期化
            labels = GP.CONT.LABEL_LIST.length                                                          # ラベル数
            average = np.zeros(labels,'float')
            for labelNo,label in enumerate(GP.CONT.LABEL_LIST.LIST):                                    # ラベルリストをすべて実行
                index = np.where(train[:,GP.CONT.TRN.LABEL] == label)[0]                                # 当該ラベルのインデックスを取得
                if len(index) > 0:                                                                      # インデックスが有る時
                    labelPredict = predict[index]                                                       # 当該ラベルの予測値
                    # 当該ラベル
                    labelPredict0 = labelPredict[:,X_BASE + labelNo]                                    # 当該ラベルの予測値
                    average[labelNo] = np.average(np.array(labelPredict0,'float'))
            index = np.argsort(average)[::-1]
            sortAverage = average[index]
            return self.returnList(index, p)                                                            # 実行時間を表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # 実行時間を表示してから結果を返す

    #---------------------------------------------------------------------------------------------------
    # 学習データ作成
    #---------------------------------------------------------------------------------------------------
    def makeTrainDataLevel1(self, SAMPLE_RATIO, p=None):
        try:
            self.startNewLevel(3, p)                                                                    # 新しいレベルの進捗開始
            MODEL_COMB = GP.CURPARTS.MODEL_COMB                                                         # MODEL_COMBを転写
            SAVE_MODEL = MODEL_COMB.SAVE_MODEL                                                          # 保存モデルを転写
            SAVE_DATA = MODEL_COMB.SAVE_DATA                                                            # 保存データを転写
            train = SAVE_DATA.SOURCE_DATA.flatBase                                                      # ソーストレインデータ
            if train is not None:                                                                       # トレインデータが有る時
                predict = self.getPredict(SAVE_MODEL.MODEL, train, p)                                   # 予測値取得
                if predict is not None:                                                                 # 予測値が有る時
                    extract = self.extractTopData(train, predict, SAMPLE_RATIO, p)                      # 予測値の上位のデータの抽出
                    res = SAVE_DATA.createTrainData(extract, p)                                         # 正常データと異常データ混合データから訓練データ作成
                    if res:                                                                             # データ作成が成功した時
                        res = self.setSelfData(SAVE_DATA)                                               # 訓練データをセットして結果を返す
                    self.deleteObject(extract)                                                          # 削除してメモリー解放
                    return self.returnResult(res, p)                                                    # 実行時間を表示してから結果を返す
            return self.returnResult(None, p)                                                           # 実行時間を表示してから結果を返す

        except Exception as e:                                                                          # 例外
            return self.returnError(e, p)                                                               # 実行時間を表示してから結果を返す

    #---------------------------------------------------------------------------------------------------
    # makeModelFunctional
    #---------------------------------------------------------------------------------------------------
    def makeModelFunctional(self, p=None):
        try:
            y_dim = len(GP.CONT.LABEL_LIST.LIST)                                                        # 出力次元 labelList数
            nodes = y_dim                                                                               # ノード数
            x_dim = GP.X_LIST.length                                                                    # 入力次元
            dropOut = self.DROPOUT                                                                      # ドロップアウト転写
            input1 = Input(shape=(x_dim,))                                                              # 入力層
            x1 = Dense(x_dim,kernel_initializer='random_uniform')(input1)                               # Dense
#            x1 = Dense(x_dim,kernel_initializer='random_normal')(input1)                               # Dense
            x1 = BatchNormalization()(x1)                                                               # BatchNormalization
            x1 = Dropout(dropOut)(x1)                                                                   # ドロップアウト
            x1 = Activation('relu')(x1)                                                                 # Activation relu
            for i in range(int(self.HIDDEN_LAYERS)):                                                    # 隠れ層数すべて実行
#                x1 = Dense(int(nodes+x_dim))(x1)                                                       # 出力層を加える
                x1 = Dense(int(nodes))(x1)                                                              # 出力層を加える
                x1 = BatchNormalization()(x1)                                                           # BatchNormalization
                x1 = Dropout(dropOut)(x1)
                x1 = Activation('relu')(x1)                                                             # Activation relu
            output = Dense(nodes)(x1)                                                                   # 出力層を加える
            output = BatchNormalization()(output)                                                       # BatchNormalization
            output = Activation('softmax')(output)                                                      # softmax関数を加える
            model = Model(inputs=input1, outputs=output)                                                # モデル生成
            model.compile(loss='categorical_crossentropy',optimizer='sgd',metrics=['accuracy'])         # モデルコンパイル

            # モデルを可視化する。
            plot_model(model, to_file='model1.png',show_shapes = False)                                 # 概要モデルをプロット
            plot_model(model, to_file='model2.png',show_shapes = True)                                  # 詳細モデルをプロット
            emit(p)                                                                                     # 進捗バーに進捗を送る
            return model                                                                                # モデルを返す

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示
            return None                                                                                 # Noneを返す

    #---------------------------------------------------------------------------------------------------
    #   ストップシグナル
    #---------------------------------------------------------------------------------------------------
    def STOP_SIGNAL(self):
        try:
            self.stop = True;                                                                           # ストップフラグをセットする

        except Exception as e:                                                                          # 例外
            self.showError(e)                                                                          # 例外を表示

#=======================================================================================================
#   クラス　モニターコールバッククラス
#=======================================================================================================
class MonitorCallBack(callbacks.Callback):
    def __init__(self, parent, p):                                                                      # 初期化
        try:
            self.parent = parent                                                                        # ペアレントをセット
            self.canvas = parent.MY_CANVAS                                                              # キャンバス
            self.VERBOSE = parent.VERBOSE                                                               # VERBOSE転写
            self.p = p                                                                                  # プログレス
            self.last_loss = 10                                                                         # 直前ロス初期化
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

    #---------------------------------------------------------------------------------------------------
    # epoch完了時 (進捗表示)
    #---------------------------------------------------------------------------------------------------
    def on_epoch_end(self, epoch, logs={}):
        try:
            SAVE_MODEL = GP.CURPARTS.MODEL_COMB.SAVE_MODEL                                              # SAVE_MODELを転写
            history = SAVE_MODEL.HISTORY.history                                                        # ヒストリーを転写
            # ロス
            acc = logs.get('acc') if logs.get('acc') else 0.0                                 # accuracy
            val_acc = logs.get('val_acc') if logs.get('val_acc') else 0.0                     # val_accuracy
            loss = logs.get('loss') if logs.get('loss') else 0.0                                        # loss
            val_loss = logs.get('val_loss') if logs.get('val_loss') else 0.0                            # val_loss
            history['acc']      += [acc]                                                                # acc配列をヒストリーに追加
            history['val_acc']  += [val_acc]                                                            # val_acc配列をヒストリーに追加
            history['loss']     += [loss]                                                               # loss配列をヒストリーに追加
            history['val_loss'] += [val_loss]                                                           # val_loss配列をヒストリーに追加
            SAVE_MODEL.SCORE = [val_loss, val_acc]                                                      # スコアセット
            self.epoch += 1                                                                             # エポックを加算
            if self.VERBOSE == 0:                                                                       # VRBOSEが0の時
                print(str(self.epoch) + '/' + str(self.epochs))                                         # エポック表示
            # ロスモニター描画
            n = 1
            if len(history['acc']) % n == 0:
                self.canvas.monitorLose(history, n)                                                     # ロスモニター描画
            # ストップ
            """
            if loss > self.last_loss + 1.02:                                                            # ロスが前回より一定値以上の時
                self.model.stop_training = True                                                         # ストップ
                history['acc']      = history['acc'][0:-3]                                              # acc配列の最後から三つを取り除く
                history['val_acc']  = history['val_acc'][0:-3]                                          # val_acc配列の最後から三つを取り除く
                history['loss']     = history['loss'][0:-3]                                             # loss配列の最後から三つを取り除く
                history['val_loss'] = history['val_loss'][0:-3]                                         # val_loss配列の最後から三つを取り除く
                loss = history['loss'][0:-1]                                                            # 最終ロス更新
            """
            # ストップフラグによるストップ
            if self.parent.stop == True:                                                                # ストップフラグがセットされている時
                self.model.stop_training = True                                                         # ストップ
            self.last_loss = loss                                                                       # 最終ロス更新
            emit(self.p)                                                                                # 進捗バーに進捗を送る
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示
            pass

#=======================================================================================================
#   StopCallBack クラス
#=======================================================================================================
class StopCallBack(callbacks.Callback):
    def __init__(self):                                                                                 # 初期化
        try:
            self.last_loss = 10
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    # epoch完了時 (進捗表示)
    def on_epoch_end(self, epoch, logs={}):
        loss = logs.get('loss') if logs.get('loss') else 0.0
        if loss > self.last_loss + 0.02:
            self.model.stop_training = True
        self.last_loss = loss
        pass



