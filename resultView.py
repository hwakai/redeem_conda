import os
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from staticImport import *
from PyQt5Import import *
from qtBase import ProgressWindowClass
from analysisBase import AnalysisBaseClass
from ageLearn import AgeLearnClass
from evtLearn import EvtLearnClass
import matplotlib.pyplot as plt
from classDef import ParameterClass
from classDef import AgeLearnParameterClass
from classDef import EvtLearnParameterClass


# =======================================================================================================
#   クラス チャンバー年齢学習パラメータクラス
# =======================================================================================================
class ResultViewParameterClass(ParameterClass):
    def __init__(self, logPath):  # 初期化
        try:
            ParameterClass.__init__(self, logPath)  # スーパークラスの初期化
            ERROR = True  # 誤差表示フラグ
            INCORRECT = True  # 不正解表示フラグ
            CORRECT = True  # 正解表示フラグ
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != 'logPath') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
            self.loadData()  # パラメータをログファイルから読込
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# =======================================================================================================
#   クラス 学習結果ビュークラス
# =======================================================================================================
class ResultViewClass(AnalysisBaseClass):
    def __init__(self, title):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.title = title  # タイトル
            self.parameter = ResultViewParameterClass(GP.RESULT_LOG.AGE_RESULT)  # パラメータ
            self.progress = ProgressWindowClass()  # 進捗ダイアローグ生成
            self.canvas = None
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.connectButtons2()  # タブのオブジェクトとメソッドを結合
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.setWindowTitle(self.title)  # ウインドウのタイトル
            self.resize(800, 600)  # サイズをセット
            self.viewCenter()  # 中央に表示
            #            self.setWindowFlags(Qt.WindowStaysOnTopHint)                                               # 常に最前面に表示
            self.setWindowState(Qt.WindowMaximized)  # 表示を最大にする

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            mLayout = QVBoxLayout()  # メインレイアウト生成（垂直レイアウト）
            self.setLabelStyle2(mLayout, self.title, "gray", "white", 40, "20pt")  # 表題ラベル
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            self.setPredButton(hLayout, ["REDRAW", "再描画"])  # 再描画釦
            self.setCheckLayout(hLayout, {"ERROR": "誤差", "INCORRECT": "不正解", "CORRECT": "正解"})  # 表示グラフ選択フラグ
            self.setPredButton(hLayout, ['SAVE', "保存"])  # 保存
            self.setPredButton(hLayout, ['PRINT', "印刷"])  # 印刷
            self.setPredButton(hLayout, ['CLOSE', "閉じる"])  # ウインドウを閉じる
            mLayout.addLayout(hLayout)  # mLayoutに水平レイアウトを追加
            self.canvasLayout = QVBoxLayout()  # キャンバスレイアウト生成
            mLayout.addLayout(self.canvasLayout)  # mLayoutに生成したオブジェクトを追加
            mLayout.setAlignment(Qt.AlignTop)  # 上詰め
            return mLayout  # メインレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   レイアウトをクリア
    # ---------------------------------------------------------------------------------------------------
    def clearLayout(self, layout):
        try:
            for i in range(layout.count()):  # アイテムの数をすべて実行
                item = layout.itemAt(i)  # アイテムを取得
                if item.layout() is not None:  # アイテムがレイアウトの時
                    self.clearLayout(item.layout())  # 子レイアウトをクリア
                elif item.widget() is not None:  # アイテムがウイジェットの時
                    item.widget().deleteLater()  # ウイジェットを遅延削除
            while layout.itemAt(0) is not None:  # アイテムの数をすべて実行
                layout.removeItem(layout.itemAt(0))  # アイテムを取り除く

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   描画
    # ---------------------------------------------------------------------------------------------------
    def redraw(self):
        try:
            p = self.progress
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            self.clearLayout(self.canvasLayout)  # キャンバスレイアウクリア
            if self.canvas is not None:  # キャンバスが有る時
                self.deleteObject(self.canvas)  # メモリーを解放
            self.canvas = ResultCanvasClass(self, 10, 8)  # キャンバス生成
            self.parameter.setClassVar(self.canvas)  # パラメータの設定
            self.canvas.plotResult()  # キャンバス描画
            self.canvasLayout.addWidget(self.canvas)  # キャンバスレイアウトにキャンバスを追加
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外                                                                          # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ユニットディレクトリを取得する
    # ---------------------------------------------------------------------------------------------------
    def getUnitDir(self, pData):
        try:
            TRN = GP.CONT.TRN  # TRN転写
            LEARN_UNIT = GP.CONT.MAIN_PARAMETER.LEARN_UNIT  # 学習単位取得
            if LEARN_UNIT == GP.LEARN_UNIT.TYPE_CODE:  # 学習単位がタイプコードの時
                UNIT_DIR = pData[TRN.TYPE_CODE]  # ページリストのタイプコードをセット
            elif LEARN_UNIT == GP.LEARN_UNIT.TYPE_ID:  # 学習単位がタイプIDの時
                UNIT_DIR = pData[TRN.LASER_TYPE_ID]  # ページリストのタイプIDをセット
            elif LEARN_UNIT == GP.LEARN_UNIT.LASER_ID:  # 学習単位がレーザータイプ時
                UNIT_DIR = LEARN_UNIT  # 学習単位のレーザーIDをセット
            unitDir = "C:/Users/owner/Documents/GIGA_RESULT/" + UNIT_DIR + "/"  # ユニットディレクトリを作成
            if not os.path.exists(unitDir):  # ディレクトリの有無を確認
                os.makedirs(unitDir)  # 途中のディレクトリを含めてディレクトリを作成
            return unitDir  # ユニットディレクトリを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ***************************************************************************************************
    #   イベント処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   再描画
    # ---------------------------------------------------------------------------------------------------
    def REDRAW(self):
        try:
            self.redraw()  # 描画

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   クローズ処理
    # ---------------------------------------------------------------------------------------------------
    def CLOSE(self):
        try:
            self.close()  # ウインドウを閉じる

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   保存
    # ---------------------------------------------------------------------------------------------------
    def SAVE(self):
        try:
            MODEL_COMB = GP.CURPARTS.MODEL_COMB  # モデルコンボを転写
            SAVE_DATA = MODEL_COMB.SAVE_DATA  # 保存データを転写
            SRC = SAVE_DATA.TEST_DATA  # ソースデータ
            if SRC.flatBase is not None:  # フラットベースが有る時
                flatBase = SRC.flatBase  # フラットベースを転写
            unitDir = self.getUnitDir(SRC.flatBase[0])  # ユニットディレクトリを取得する
            start_dir = unitDir + "/learnResult.png"  # 初期ディレクトリ
            self.canvas.Save(start_dir)  # キャンバスを保存
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   印刷
    # ---------------------------------------------------------------------------------------------------
    def PRINT(self):
        try:
            return
            INCH = 1440
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
            hDC.StartDoc('TestPrint')
            hDC.StartPage()
            hDC.SetMapMode(win32con.MM_TWIPS)
            hDC.DrawText(sentence, (0, INCH * -1, INCH * 8, INCH * -2), win32con.DT_CENTER)
            hDC.EndPage()
            hDC.EndDoc()

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   クラス 年齢学習結果ビュークラス
# =======================================================================================================
class AgeResultViewClass(ResultViewClass):
    # ---------------------------------------------------------------------------------------------------
    # クラス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None

    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self):  # 初期化
        try:
            if AgeResultViewClass._singleton is None:  # シングルトンが無いとき
                title = "年齢学習結果"  # ビューのタイトル
                self.learnParam = AgeLearnParameterClass.getInstance()  # 学習パラメータ
                ResultViewClass.__init__(self, title)  # スーパークラスの初期化

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if AgeResultViewClass._singleton is None:  # シングルトンが無いとき
            AgeResultViewClass._singleton = AgeResultViewClass()  # インスタンスを生成してシングルトンにセット
        return AgeResultViewClass._singleton  # シングルトンがを返す


# =======================================================================================================
#   クラス イベント学習結果ビュークラス
# =======================================================================================================
class EvtResultViewClass(ResultViewClass):
    # ---------------------------------------------------------------------------------------------------
    # クラス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None

    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self):  # 初期化
        try:
            if EvtResultViewClass._singleton is None:  # シングルトンが無いとき
                title = "イベント学習結果"  # ビューのタイトル
                self.learnParam = EvtLearnParameterClass.getInstance()  # 学習パラメータ
                ResultViewClass.__init__(self, title)  # スーパークラスの初期化

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if EvtResultViewClass._singleton is None:  # シングルトンが無いとき
            EvtResultViewClass._singleton = EvtResultViewClass()  # インスタンスを生成してシングルトンにセット
        return EvtResultViewClass._singleton  # シングルトンがを返す


# =======================================================================================================
#   クラス 学習結果キャンバスクラス
# =======================================================================================================
class ResultCanvasClass(AnalysisBaseClass):
    def __init__(self, parent, width, height, dpi=100):
        try:
            AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.learnParam = parent.learnParam
            self.TRAIN_Y_LIMIT = 1.1  # Yリミット
            self.figure = Figure(figsize=(width, height), dpi=dpi)
            self.figureCanvas = FigureCanvas(self.figure)
            self.figureCanvas.setParent(parent)
            self.figureCanvas.setSizePolicy(  # サイズポリシー設定
                QSizePolicy.Expanding,  # 幅可変
                QSizePolicy.Expanding)  # 高さ可変
            self.layout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout.addWidget(self.figureCanvas)  # ビューレイアウトにグループボックスを追加
            self.setLayout(self.layout)  # レイアウトを自分にセット
            pass

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習結果タイトルを返す
    # ---------------------------------------------------------------------------------------------------
    def getResultTitle(self, learnParam):
        try:
            CURPARTS = GP.CURPARTS  # コンテナを転写
            SAVE_MODEL = CURPARTS.MODEL_COMB.SAVE_MODEL  # 保存モデルを転写
            title = ""  # タイトル初期化
            title += " PARTS=" + str(CURPARTS.PARTS)  # 学習部品追加
            title += " TYPE=" + str(CURPARTS.TYPE)  # 学習タイプ追加
            title += " LEVEL=" + str(SAVE_MODEL.LEVEL)  # レベル追加
            title += " SCORE=" + str(round(SAVE_MODEL.SCORE[1], 3))  # スコア追加
            title += " LOSE=" + str(round(SAVE_MODEL.LOSE, 3))  # ロス追加
            title += " HL=" + str(learnParam.HIDDEN_LAYERS)  # 隠れ層数追加
            title += " DROP=" + str(learnParam.DROPOUT)  # ドロップアウト追加
            title += " INIT_EPOCHS=" + str(learnParam.INIT_EPOCHS)  # エポック追加
            title += " CUT_EPOCHS=" + str(learnParam.CUT_EPOCHS)  # エポック追加
            title += " BATCH_SIZE=" + str(learnParam.BATCH_SIZE)  # バッチサイズ追加
            title += " SAMPLES=" + str(learnParam.SAMPLES)  # ラベル毎のデータ数追加
            title += " RATIO_0=" + str(learnParam.SAMPLE_RATIO_0)  # 初回上位のデータサンプル割合追加
            title += " RATIO_N=" + str(learnParam.SAMPLE_RATIO_N)  # 次回以後上位のデータサンプル割合追加
            return title  # 基準ショット追加

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   plotResult
    # ---------------------------------------------------------------------------------------------------
    def plotResult(self):
        try:
            MODEL_COMB = GP.CURPARTS.MODEL_COMB  # モデルコンボを転写
            SAVE_DATA = MODEL_COMB.SAVE_DATA  # 保存データを転写
            SAVE_MODEL = MODEL_COMB.SAVE_MODEL  # 保存モデルを転写
            MODEL_COMB.loadModel()  # 学習済みモデルの読み込み
            SRC = SAVE_DATA.TEST_DATA  # ソースデータ
            if SRC.flatBase is not None:  # フラットベースが有る時
                flatBase = SRC.flatBase  # フラットベースを転写
                LASER_ID = flatBase[0, GP.CONT.TRN.LASER_ID]  # レーザーID
                predict = self.getPredict(SAVE_MODEL.MODEL, flatBase)  # テストデータの予測値取得
                views = 0  # ディスプレイ上の描画画面数
                if self.ERROR:  views += 1  # 誤差プロットの時描画画面数+1
                if self.INCORRECT:  views += 1  # 不正解のプロットの時描画画面数+1
                if self.CORRECT:  views += 1  # 正解のプロットの時描画画面数+1
                axes = self.figure.subplots(nrows=views, ncols=1)  # アキス配列を取得
                self.figure.subplots_adjust(wspace=0.3, hspace=0.6, left=0.05, right=0.85)  # ラベル表示位置調整
                if self.INCORRECT or self.CORRECT:  # 不正解か正解プロットの時
                    self.plotLabel(axes[views - 1], LASER_ID)  # ラベルをプロット
                view = 0  # 描画画面番号
                if self.ERROR:  # 誤差プロットの時
                    if views == 1:  # 描画画面数が1の時
                        self.plotLose(axes)  # 誤差のプロット
                    else:
                        self.plotLose(axes[view])  # 誤差のプロット
                    view += 1  # 描画画面数+1
                if self.INCORRECT:  # 不正解のプロットの時
                    if views == 1:  # 描画画面数が1の時
                        self.plotTestIncorrect(predict, axes, False)  # 不正解データのプロット
                    else:
                        self.plotTestIncorrect(predict, axes[view], False)  # 不正解データのプロット
                    view += 1  # 描画画面数+1
                if self.CORRECT:  # 正解のプロットの時
                    if views == 1:  # 描画画面数が1の時
                        self.plotTestCorrect(predict, axes, False)  # 正解データのプロット
                    else:
                        self.plotTestCorrect(predict, axes[view], False)  # 正解データのプロット
                    view += 1  # 描画画面数+1
                self.deleteObject(predict)  # メモリー解放
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ラベルをプロット
    # ---------------------------------------------------------------------------------------------------
    def plotLabel(self, axes, LASER_ID):
        try:
            OUT_LIST = GP.CONT.OUT_LIST  # 出力リスト転写
            plotRange = range(1)  # プロットレンジ
            for i, label in enumerate(OUT_LIST.LIST):  # ラベルリストをすべて実行
                color = OUT_LIST.COLOR_LIST[i]  # カラー取得
                drawLabel = self.getDescLabel(LASER_ID, label)  # 説明文付きのエラーラベルを取得
                axes.scatter(plotRange, [0], marker='.', label=drawLabel, color=color, s=40)  # ラベル有りでプロット
            axes.legend(fontsize=10, bbox_to_anchor=(1.0, 0.0), loc='lower left', markerscale=40)  # 配置

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    # 誤差のプロット
    # ---------------------------------------------------------------------------------------------------
    def plotLose(self, axes):
        try:
            history = GP.CURPARTS.MODEL_COMB.SAVE_MODEL.HISTORY  # ヒストリーを転写
            loss = history.history['loss']  # ロスを取得
            val_loss = history.history['val_loss']  # val_lossを取得
            acc = history.history['acc']  # acc取得
            nb_epoch = len(loss)  # エポック数
            self.EPOCHS = nb_epoch  # エポック数
            axes.plot(range(nb_epoch), loss, marker='.', label='loss', color='blue')  # ロスをプロット
            axes.plot(range(nb_epoch), val_loss, marker='.', label='val_loss', color='orange')  # val_lossをプロット
            axes.plot(range(nb_epoch), acc, marker='.', label='acc', color='red')  # accをプロット
            axes.legend(loc='best', fontsize=10)  # 配置
            axes.grid(True)  # グリッド描画
            axes.set_xlabel('epoch')  # X軸ラベル
            axes.set_ylabel('loss')  # Y軸ラベル
            axes.set_title(self.getResultTitle(self.learnParam))  # タイトルに学習タブパラメータを描画
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   テストデータの予測正解値のプロット
    # ---------------------------------------------------------------------------------------------------
    def plotTestCorrect(self, predict, axes, labelFlag=True):
        try:
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            if len(predict) == 0:  # ソースデータパックが無いとき
                return  # 終了
            LABEL_LIST = GP.CONT.LABEL_LIST  # 出力ラベルリストの転写
            plotRangeList = self.makePlotRange(predict)  # ラベル毎のプロットレンジセット
            # プロット
            for i, label in enumerate(LABEL_LIST.LIST):  # ラベルリストをすべて実行
                labelPredict = predict[predict[:, GP.CONT.TRN.LABEL] == label]  # ラベルのYデータ
                color = LABEL_LIST.getColor(label)  # ラベルのカラーを取得
                if len(labelPredict) > 0:  # データパックの有無を確認
                    plotRange = plotRangeList[i]  # 正解プロットのレンジ
                    correct = labelPredict[:, X_BASE + i]  # ラベルのXデータ
                    correct = correct.reshape(-1, 1)  # ラベルのXデータ
                    correct = np.concatenate([labelPredict[:, :X_BASE], correct], axis=1)  # トレイン形式の予測値データを作成
                    self.plotData(axes, correct, plotRange, label, labelFlag, color,
                                  GP.PLOT_MODE.SCATTER)  # ラベル値とデータのプロット

            # ラベルの境界線の描画
            self.plotBoundary(plotRangeList, 1.1, axes)  # ラベルの境界線の描画
            # 描画パラメータセット
            axes.legend(fontsize=10, bbox_to_anchor=(1.00, -0.03), loc='lower left')  # 配置
            axes.grid(True)  # グリッド描画
            axes.set_xlabel('CORRECT DATA (rel shot/target(%))')  # X軸ラベル
            axes.set_ylabel('predict')  # Y軸ラベル
            axes.set_ylim([0, self.TRAIN_Y_LIMIT])  # Y軸レンジ
            axes.set_title(self.getResultTitle(self.learnParam))  # タイトルに学習タブパラメータを描画
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   テストデータの予測不正解値のプロット
    # ---------------------------------------------------------------------------------------------------
    def plotTestIncorrect(self, predict, axes, labelFlag=True):
        try:
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            if len(predict) == 0:  # ソースデータパックが無いとき
                return  # 終了
            LABEL_LIST = GP.CONT.LABEL_LIST  # 出力ラベルリストの転写
            plotRangeList = self.makePlotRange(predict)  # ラベル毎のプロットレンジセット
            # プロット
            for i, label in enumerate(LABEL_LIST.LIST):  # ラベルリストをすべて実行
                labelPredict = predict[predict[:, GP.CONT.TRN.LABEL] == label]  # ラベルのXデータ
                if len(labelPredict) > 0:  # ラベルリストが有る時
                    for j, myLabel in enumerate(LABEL_LIST.LIST):  # ラベルリストをすべて実行
                        if j != i:  # ラベルが異なる時
                            plotRange = plotRangeList[i]  # 不正解プロットのレンジ
                            color = LABEL_LIST.getColor(myLabel)  # ラベルのカラーを取得
                            incorrect = labelPredict[:, X_BASE + j]  # ラベルのXデータ
                            incorrect = incorrect.reshape(-1, 1)  # ラベルのXデータ
                            incorrect = np.concatenate([labelPredict[:, :X_BASE], incorrect],
                                                       axis=1)  # トレイン形式の予測値データを作成
                            self.plotData(axes, incorrect, plotRange, label, False, color,
                                          GP.PLOT_MODE.SCATTER)  # ラベル値とデータのプロット
            # ラベルの境界線の描画
            self.plotBoundary(plotRangeList, self.TRAIN_Y_LIMIT, axes)  # ラベルの境界線の描画
            # 描画パラメータセット
            axes.legend(fontsize=10, bbox_to_anchor=(1.0, 0.0), loc='lower left')  # 配置
            axes.grid(True)  # グリッド描画
            axes.set_xlabel('INCORRECT DATA (rel shot/target(%))')  # X軸ラベル
            axes.set_ylabel('predict')  # Y軸ラベル
            axes.set_ylim([0, self.TRAIN_Y_LIMIT])  # Y軸レンジ
            axes.set_title(self.getResultTitle(self.learnParam))  # タイトルに学習タブパラメータを描画
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ラベルの境界線の描画
    # ---------------------------------------------------------------------------------------------------
    def plotBoundary(self, plotRangeList, Y_LIMIT, axes):
        try:
            # ラベルの境界線の描画
            dx = plotRangeList[-1].stop / 1000  # 文字のXオフセット
            for i, label in enumerate(GP.CONT.LABEL_LIST.LIST):  # ラベルリストをすべて実行
                plotRange = plotRangeList[i]  # プロットレンジ取得
                if plotRange.stop > plotRange.start:  # プロットレンジの最後が最初より大きいとき
                    linestyle = "-"  # ラインスタイルを実線にする
                    color = "#ff0000"  # カラーを赤にする
                    x = plotRange.start  # xをプロットレンジの最初から10ずらす
                    axes.axvline(x=x, linestyle=linestyle, color=color)  # 開始のラインを引く
                    axes.axvline(x=plotRange.stop, linestyle=linestyle, color=color)  # 終了のラインを引く
                    if 'R_' in label:  # ラベルに'R_'が有る時
                        label = label.replace('R_', '')  # 'R_'を削除
                        color = "red"  # 文字を赤色にする
                    else:  # ラベルに'R_'が無い時
                        color = "black"  # 文字を黒色にする
                    if GP.CONT.LABEL_LIST.length > 30:  # ラベル数が一定数以上の時
                        label = label[0:5]  # 5文字に制限
                    y = Y_LIMIT - 0.07  # y位置をY_LIMITより0.07下にする
                    axes.text(x + dx, y, label, ha='left', va='bottom', fontsize=7, color=color)  # テキスト描画
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ラベル毎のプロットレンジセット
    # ---------------------------------------------------------------------------------------------------
    def makePlotRange(self, flatList):
        try:
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            plotRangeList = []  # プロットレンジリスト初期化
            x = 0  # ｘを初期化
            for label in GP.CONT.LABEL_LIST.LIST:  # ラベルリストをすべて実行
                labelList = flatList[flatList[:, GP.CONT.TRN.LABEL] == label]  # ラベルのデータパックを取得
                length = len(labelList)  # データ数
                plotRangeList.append(range(x, x + length))  # プロットレンジリストにセット
                x = x + length  # ｘを更新
            return plotRangeList  # プロットレンジリストを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   クラス 学習結果モニタービュークラス
# =======================================================================================================
class MonitorViewClass(AnalysisBaseClass):
    def __init__(self, title, parameter):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.title = title  # タイトル
            self.parameter = parameter
            self.progress = ProgressWindowClass()  # 進捗ダイアローグ生成
            self.canvas = None
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.connectButtonsMethod()  # タブのオブジェクトとメソッドを結合
            self.setWindowTitle(self.title)  # ウインドウのタイトル
            self.resize(800, 600)  # サイズをセット
            self.viewCenter()  # 中央に表示
            #            self.setWindowFlags(Qt.WindowStaysOnTopHint)                                               # 常に最前面に表示
            self.setWindowState(Qt.WindowMaximized)  # 表示を最大にする

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            mLayout = QVBoxLayout()  # メインレイアウト生成（垂直レイアウト）
            self.setLabelStyle2(mLayout, self.title, "gray", "white", 40, "20pt")  # 表題ラベル
            hLayout = QHBoxLayout()  # 水平レイアウト生成
            self.setExeButton(hLayout, ["STOP", "学習中断"])  # 学習中断釦
            self.setPredButton(hLayout, ['CLOSE', "閉じる"])  # ウインドウを閉じる
            mLayout.addLayout(hLayout)  # mLayoutに水平レイアウトを追加
            self.canvasLayout = QVBoxLayout()  # キャンバスレイアウト生成
            mLayout.addLayout(self.canvasLayout)  # mLayoutに生成したオブジェクトを追加
            mLayout.setAlignment(Qt.AlignTop)  # 上詰め
            return mLayout  # メインレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   レイアウトをクリア
    # ---------------------------------------------------------------------------------------------------
    def clearLayout(self, layout):
        try:
            for i in range(layout.count()):  # アイテムの数をすべて実行
                item = layout.itemAt(i)  # アイテムを取得
                if item.layout() is not None:  # アイテムがレイアウトの時
                    self.clearLayout(item.layout())  # 子レイアウトをクリア
                elif item.widget() is not None:  # アイテムがウイジェットの時
                    item.widget().deleteLater()  # ウイジェットを遅延削除
            while layout.itemAt(0) is not None:  # アイテムの数をすべて実行
                layout.removeItem(layout.itemAt(0))  # アイテムを取り除く

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   初期設定
    # ---------------------------------------------------------------------------------------------------
    def initialize(self, epochs):
        try:
            self.clearLayout(self.canvasLayout)  # キャンバスレイアウクリア
            if self.canvas is not None:  # キャンバスが有る時
                self.deleteObject(self.canvas)  # メモリーを解放
            self.canvas = MonitorCanvasClass(self, 10, 8)  # キャンバス生成
            self.parameter.setClassVar(self.canvas)  # パラメーターをキャンバスに転写する
            self.canvas.plotFrame(epochs)  # キャンバス描画
            self.canvasLayout.addWidget(self.canvas)  # キャンバスレイアウトにキャンバストを追加
            self.show()  # 表示
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ***************************************************************************************************
    #   イベント処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   クローズ処理
    # ---------------------------------------------------------------------------------------------------
    def CLOSE(self):
        try:
            self.close()  # ウインドウを閉じる

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   学習中断釦
    # ---------------------------------------------------------------------------------------------------
    def STOP(self):
        try:
            if GP.CURPARTS.LEARN is not None:  # 学習クラスが有る時
                GP.CURPARTS.LEARN.stopSignal.emit()  # 学習クラスにストップシグナルを送る

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass


# =======================================================================================================
#   クラス 学習結果モニターキャンバスクラス
# =======================================================================================================
class MonitorCanvasClass(AnalysisBaseClass):
    def __init__(self, parent, width, height, dpi=100):
        try:
            AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.figure = Figure(figsize=(width, height), dpi=dpi)
            self.figureCanvas = FigureCanvas(self.figure)
            self.figureCanvas.setParent(parent)
            self.figureCanvas.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
            self.layout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout.addWidget(self.figureCanvas)  # ビューレイアウトにグループボックスを追加
            self.setLayout(self.layout)  # レイアウトを自分にセット
            pass

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習結果タイトルを返す
    # ---------------------------------------------------------------------------------------------------
    def getResultTitle(self):
        try:
            CURPARTS = GP.CURPARTS  # コンテナを転写
            SAVE_MODEL = CURPARTS.MODEL_COMB.SAVE_MODEL  # 保存モデルを転写
            title = ""  # タイトル初期化
            title += " PARTS=" + str(CURPARTS.PARTS)  # 学習部品追加
            title += " TYPE=" + str(CURPARTS.TYPE)  # 学習タイプ追加
            title += " LEVEL=" + str(SAVE_MODEL.LEVEL)  # レベル追加
            title += " HL=" + str(self.HIDDEN_LAYERS)  # 隠れ層数追加
            title += " DROP=" + str(self.DROPOUT)  # ドロップアウト追加
            title += " EPOCHS=" + str(self.EPOCHS)  # エポック追加
            title += " CUT_EPOCHS=" + str(self.CUT_EPOCHS)  # エポック追加
            title += " BATCH_SIZE=" + str(self.BATCH_SIZE)  # バッチサイズ追加
            title += " SAMPLES=" + str(self.SAMPLES)  # ラベル毎のデータ数追加
            title += " RATIO_0=" + str(self.SAMPLE_RATIO_0)  # 初回上位のデータサンプル割合追加
            title += " RATIO_N=" + str(self.SAMPLE_RATIO_N)  # 次回以後上位のデータサンプル割合追加
            return title  # 基準ショット追加

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   サブプロットを初期設定
    # ---------------------------------------------------------------------------------------------------
    def initializeSubPlots(self):
        try:
            self.viewCount = 0  # 描画画面カウントリセット
            self.axes = self.figure.subplots(nrows=1, ncols=1)  # 単一アキスを取得
            self.figure.subplots_adjust(wspace=0.3, hspace=0.6, left=0.05, right=0.85)  # ラベル表示位置調整
            return self.axes  # figとaxesを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   フレームのプロット
    # ---------------------------------------------------------------------------------------------------
    def plotFrame(self, epochs):
        try:
            self.EPOCHS = epochs  # エポックスセット
            axes = self.initializeSubPlots()  # サブプロットを初期設定
            axes.plot([0], 0, marker='.', label='loss', color='blue')  # ロスをプロット
            axes.plot([0], 0, marker='.', label='val_loss', color='orange')  # val_lossをプロット
            axes.plot([0], 0, marker='.', label='acc', color='red')  # accをプロット
            axes.legend(loc='best', fontsize=10)  # 配置
            axes.grid(True)  # グリッド描画
            axes.set_xlabel('epoch')  # X軸ラベル
            axes.set_ylabel('loss')  # Y軸ラベル
            axes.set_xlim([0, epochs - 1])  # X軸レンジ
            axes.set_ylim([0, 3.5])  # Y軸レンジ
            axes.set_title(self.getResultTitle())  # タイトルに学習タブパラメータを描画
            self.figureCanvas.draw()
            self.updateView()  # ビューを更新する
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ロスのモニター
    # ---------------------------------------------------------------------------------------------------
    def monitorLose(self, history, n):
        try:
            axes = self.axes
            loss = history['loss']  # ロスを取得
            val_loss = history['val_loss']  # val_lossを取得
            acc = history['acc']  # ロスを取得
            nb_epoch = len(loss)  # エポック数

            if nb_epoch > n:
                n += 1
            loss = loss[-n:]  # ロスを取得
            val_loss = val_loss[-n:]  # val_lossを取得
            acc = acc[-n:]  # accを取得
            axes.plot(range(nb_epoch - n, nb_epoch), loss, marker='.', color='blue')  # ロスをプロット
            axes.plot(range(nb_epoch - n, nb_epoch), val_loss, marker='.', color='orange')  # val_lossをプロット
            axes.plot(range(nb_epoch - n, nb_epoch), acc, marker='.', color='red')  # accをプロット
            self.figureCanvas.draw()
            self.updateView()  # ビューを更新する

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ロスの初期描画表示
    # ---------------------------------------------------------------------------------------------------
    def monitorLoseInitialize(self, history):
        try:
            axes = self.axes
            loss = history.history['loss']  # ロスを取得
            val_loss = history.history['val_loss']  # val_lossを取得
            acc = history.history['acc']  # ロスを取得
            nb_epoch = len(loss)  # エポック数
            if nb_epoch > 0:
                axes.plot(range(nb_epoch), loss, marker='.', color='blue')  # ロスをプロット
                axes.plot(range(nb_epoch), val_loss, marker='.', color='orange')  # val_lossをプロット
                axes.plot(range(nb_epoch), acc, marker='.', color='red')  # accをプロット
                self.figureCanvas.draw()
            self.updateView()  # ビューを更新する

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass


