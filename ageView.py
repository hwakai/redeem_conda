import os
import math
import numpy as np
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from static import *
from PyQt5Import import *
from treeWidget import *
from analysisBase import *
from qtBase import ProgressWindowClass
from qtBase import GridClass
from qtBase import CheckWindowClass
from classDef import CommonParameterClass

from PIL import Image
from PIL import ImageQt
from commonBase import CommonBaseClass
from classDef import ParameterClass
from modelComb import *

#=======================================================================================================
#   クラス CH年齢バー
#=======================================================================================================
class AgeBarClass(AnalysisBaseClass):
    def __init__(self, PARTS, width, height, train, maxShot):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.SOURCE = PARTS.PARTS + "_" + PARTS.TYPE + str(PARTS.LEVEL)  # 子ディレクトリ名
            dpi = 100  # 1インチ当たりのピクセル数
            self.MY_SRC_Y_LIMIT = 1.1  # XデータY軸上限
            self.MY_AGE_Y_LIMIT = 1.1  # 年齢Y軸上限
            self.MY_VIEWS_PLOT = 2  # 年齢描画画面数（元データと予測値合計)を設定
            widthInch = width / dpi  # インチ幅
            baseHeight = 61  # グラフ高さが０の時の総高さ
            heigtInch = (baseHeight + height) / dpi  # グラフ高さを加えたインチ高さ
            self.figure = Figure(figsize=(10, heigtInch), dpi=dpi)
            self.figureCanvas = FigureCanvas(self.figure)
            self.figureCanvas.setParent(None)
            self.figureCanvas.setSizePolicy(  # サイズポリシー設定
                QSizePolicy.Expanding,  # 幅可変
                QSizePolicy.Expanding)  # 高さ可変
            self.layout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout.addWidget(self.figureCanvas)  # ビューレイアウトにグループボックスを追加
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.drawArgMaxBar(train, maxShot)  # 最大値バー描画
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   最大値バー描画
    # ---------------------------------------------------------------------------------------------------
    def drawArgMaxBar(self, train, maxShot):
        try:
            axes = self.figure.subplots(nrows=1, ncols=1)
            TRN = GP.CONT.TRN  # TRNを転写
            OUT_LIST = GP.CONT.OUT_LIST  # 出力リスト転写
            labels = OUT_LIST.length  # ラベル数
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            Y_LIMIT = 1.0  # グラフ高さ
            AGE_STEP = GP.AGE_STEP  # 年齢間隔
            axes.set_ylim([0, Y_LIMIT])  # Y軸レンジ
            target = train[0, TRN.TARGET]  # ターゲット
            REL_SHOT = train[:, TRN.REL_SHOT]  # 相対ショット
            train[:, TRN.REL_SHOT] = np.where(REL_SHOT < 0, 0, REL_SHOT)  # 0未満の時は0にする
            age = train[:, X_BASE]  # 年齢を抽出
            age = np.where(age >= (labels * AGE_STEP), (labels - 1) * AGE_STEP, age)  # ラベル数以上の年齢修正
            lastX = maxShot  # 最大ショット数
            for labelNo, label in enumerate(OUT_LIST.LIST):  # ラベルリストをすべて実行
                extract = train[(age[:] >= labelNo * AGE_STEP) & (age[:] < (labelNo + 1) * AGE_STEP)]  # ラベルのデータを抽出
                if len(extract) > 0:  # データが有る時
                    plotRange = extract[:, TRN.REL_SHOT]  # プロットレンジを相対ショット数にする
                    color = OUT_LIST.getColor(label)  # カラー取得
                    linestyle = "solid"  # ラインスタイルを実線にする
                    axes.vlines(x=plotRange, ymin=0, ymax=Y_LIMIT, linestyle=linestyle, color=color)  # ラインを引く
            axes.vlines(x=0, ymin=0, ymax=1, linestyle=linestyle, linewidths=1, color="black")  # 0にラインを引く
            axes.vlines(x=lastX, ymin=0, ymax=1, linestyle=linestyle, linewidths=1, color="black")  # 最大値にラインを引く
            axes.grid(True)  # グリッド描画
            self.figure.tight_layout()  # 余白をなくす
            self.axes = axes
            self.figure.savefig('foo.png')  # ファイルに保存

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None


# =======================================================================================================
#   クラス 切り出し年齢バー
# =======================================================================================================
class AgeCutBarClass(QLabel):
    def __init__(self, ageBar, bar):  # 初期化
        try:
            QLabel.__init__(self)  # スーパークラスの初期化
            dpi = 100  # 1インチ当たりのピクセル数
            self.setScaledContents(True)  # サイズを伸縮可能にする
            self.setMinimumSize(100, 10)
            self.setSizePolicy(  # サイズポリシー設定
                QSizePolicy.Expanding,  # 幅可変
                QSizePolicy.Fixed)  # 高さ固定
            self.setImage(ageBar.figureCanvas)  # キャンバスからimgArrayとpilImageとqImageとqPixmapをセット
            if bar == "BAR":
                cutPixmap = self.getBarPixMap()  # 領域を切り取ったピクセルマップを取得
            else:
                cutPixmap = self.getTickMarksPixMap()  # 領域を切り取ったピクセルマップを取得
            self.setPixmap(cutPixmap)  # ピクセルマップをセット

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   キャンバスからimgArrayとpilImageとqImageとqPixmapをセット
    # ---------------------------------------------------------------------------------------------------
    def setImage(self, canvas):
        try:
            self.imgArray = np.array(canvas.renderer.buffer_rgba())  # イメージ配列取得
            self.pilImage = Image.fromarray(self.imgArray)  # pillowのImageに変換
            self.qImage = ImageQt.ImageQt(
                self.pilImage)  # QImageに変換
            self.qPixmap = QPixmap.fromImage(self.qImage)  # QPixmapに変換

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   上部ラインを取得
    # ---------------------------------------------------------------------------------------------------
    def getUpperLine(self):
        try:
            height = self.imgArray.shape[0]  # 最大値ピクセルマップ高さ
            for row in range(height):  # 行を0からすべて実行
                data = self.imgArray[row]  # 行データ取得
                n = np.where((data[:, 0] == 0) & (data[:, 1] == 0) & (data[:, 2] == 0) & (data[:, 3] == 255))[
                    0]  # 黒点のインデックス
                if len(n) >= 100:  # 黒線の長さが100以上の時
                    break  # ループ終了
            return row  # 行番号を返す

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   下部ラインを取得
    # ---------------------------------------------------------------------------------------------------
    def getLowerLine(self):
        try:
            height = self.imgArray.shape[0]  # 最大値ピクセルマップ高さ
            for row in reversed(range(height)):  # 行を最終行からすべて実行
                data = self.imgArray[row]  # 行データ取得
                n = np.where((data[:, 0] == 0) & (data[:, 1] == 0) & (data[:, 2] == 0) & (data[:, 3] == 255))[
                    0]  # 黒点のインデックス
                if len(n) >= 100:  # 黒線の長さが100以上の時
                    break  # ループ終了
            return row  # 行番号を返す

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   左部ラインを取得
    # ---------------------------------------------------------------------------------------------------
    def getLeftLine(self):
        try:
            upperLine = self.getUpperLine()  # 上部ライン取得
            lowerLine = self.getLowerLine()  # 下部ライン取得
            width = self.imgArray.shape[1]  # 最大値ピクセルマップ幅
            for col in range(width):  # 列をを0からすべて実行
                data = self.imgArray[upperLine:lowerLine, col]  # 上部ラインと下部来の間の列データ取得
                if (data[:, 0:3] == 0).all():  # すべて黒色の時
                    break  # ループ終了
            return col  # 列番号を返す

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   右部ラインを取得
    # ---------------------------------------------------------------------------------------------------
    def getRightLine(self):
        try:
            upperLine = self.getUpperLine()  # 上部ライン取得
            lowerLine = self.getLowerLine()  # 下部ライン取得
            width = self.imgArray.shape[1]  # 最大値ピクセルマップ幅
            for col in reversed(range(width)):  # 列を最終列からすべて実行
                data = self.imgArray[upperLine:lowerLine, col]  # 列データ取得
                if (data[:, 0:3] == 0).all():  # すべて黒色の時
                    break  # ループ終了
            return col  # 列番号を返す

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   零点X座標を取得
    # ---------------------------------------------------------------------------------------------------
    def getZeroX(self):
        try:
            lowerLine = self.getLowerLine()  # 下部ライン取得
            leftLine = self.getLeftLine()  # 左部ライン取得
            width = self.imgArray.shape[1]  # 最大値ピクセルマップ幅
            for col in range(leftLine, width):  # 列をを左部ライン位置からすべて実行
                data = self.imgArray[lowerLine + 2, col]  # 列データ取得
                if (data[0:3] == 0).all():  # 黒色の時
                    break  # ループ終了
            return col  # 列番号を返す

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   空白下限を取得
    # ---------------------------------------------------------------------------------------------------
    def getLowerSpace(self):
        try:
            height = self.imgArray.shape[0]  # 最大値ピクセルマップ高さ
            for row in reversed(range(height)):  # 行を最終行からすべて実行
                if not (self.imgArray[row] == 255).all():  # 白色で無い時
                    break  # ループ終了
            return row  # 行番号を返す

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   領域を切り取ったピクセルマップを取得
    # ---------------------------------------------------------------------------------------------------
    def getBarPixMap(self):
        try:
            # 基礎データ取得
            upperLine = self.getUpperLine()  # 上部ライン取得
            lowerLine = self.getLowerLine()  # 下部ライン取得
            zeroX = self.getZeroX()  # 零点X座標を取得
            # 切り出し座標設定
            left = zeroX - 10  # 左辺設定
            top = upperLine  # 上辺設定
            right = self.getRightLine()  # 右辺設定
            bottom = lowerLine + 5  # 下辺設定
            # 切り出し領域設定
            rect = QRect(QPoint(left, top), QPoint(right, bottom))  # 切り出し矩形
            cutPixmap = self.qPixmap.copy(rect)  # 必要な領域を切り出す
            # グラフの左辺にラインを引く
            painter = QPainter(cutPixmap)  # ペインター生成
            pen = QPen(Qt.black, 1)  # ペン生成
            painter.setPen(pen)  # ペインターにペンをセット
            height = cutPixmap.height()  # 高さ
            painter.drawLine(0, 0, 0, height - 6)  # グラフの左辺にラインを引く
            painter.end()  # ペインター破棄
            return cutPixmap  # ピクセルマップを返す

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   領域を切り取ったピクセルマップを取得
    # ---------------------------------------------------------------------------------------------------
    def getTickMarksPixMap(self):
        try:
            # 基礎データ取得
            zeroX = self.getZeroX()  # 零点X座標を取得
            rightLine = self.getRightLine()  # 右部ライン取得
            lowerLine = self.getLowerLine()  # 下部ライン取得
            lowerSpace = self.getLowerSpace()  # 空白下限を取得
            # 切り出し座標設定
            left = zeroX - 10  # 左辺設定
            top = lowerLine + 1  # 上辺設定
            right = rightLine  # 右辺設定
            bottom = lowerSpace + 5  # 下辺設定
            # 切り出し領域設定
            rect = QRect(QPoint(left, top), QPoint(right, bottom))  # 切り出し矩形
            cutPixmap = self.qPixmap.copy(rect)  # 必要な領域を切り出す
            return cutPixmap  # ピクセルマップを返す

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示


# =======================================================================================================
#   スーパークラス 年齢テーブルビューパラメータクラス
# =======================================================================================================
class AgeTableViewParameterClass(ParameterClass):
    def __init__(self, logPath):  # 初期化
        try:
            ParameterClass.__init__(self, logPath)  # スーパークラスの初期化
            SHOW_CH = True  # CH表示
            SHOW_LN = True  # LN表示
            SHOW_PPM = True  # PPM表示
            SHOW_MM = True  # MM表示
            MAX_PAGE_LASERS = 20  # 一頁の最大レーザー数
            RED_SPAN = 20  # 間引き幅
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != 'logPath') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
            self.loadData()  # ログファイルのデータを読み込む

        except Exception as e:  # 例外
            printError(e)  # 例外を表示


# =======================================================================================================
#   クラス 年齢一覧ビュー
# =======================================================================================================
class AgeTableViewClass(AnalysisBaseClass):
    # ---------------------------------------------------------------------------------------------------
    #   クラス変数
    # ---------------------------------------------------------------------------------------------------
    _singleton = None

    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self):  # 初期化
        try:
            if AgeTableViewClass._singleton is None:  # シングルトンが無いとき
                AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
                #                self.title = GP.MIXCONT.MAIN_PARTS.PARTS + "年齢分析結果一覧表"                          # タイトル
                self.title = "年齢分析結果一覧表"  # タイトル
                self.parameter = AgeTableViewParameterClass(GP.MAIN_LOG.AGE_TABLE_VIEW)  # パラメータ
                self.progress = ProgressWindowClass()  # 進捗ダイアローグ生成
                self.canvas = None  # キャンバス初期化
                self.page = 0  # 現ページ初期化
                self.resize(1000, 600)
                self.layout = self.createLayout()  # レイアウト生成
                self.setLayout(self.layout)  # レイアウトを自分にセット
                self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
                self.redSliderLabel.setText(str(self.RED_SPAN))  # スライダーラベルをセット
                self.connectButtons3()
                self.treeWidget = GP.TREE.AGE_RESULT  # ツリー設定
                pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    # シングルトン呼び出し
    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if AgeTableViewClass._singleton is None:  # シングルトンが無いとき
            AgeTableViewClass._singleton = AgeTableViewClass()  # インスタンスを生成してシングルトンにセット
        return AgeTableViewClass._singleton  # シングルトンがを返す

    # ---------------------------------------------------------------------------------------------------
    #   パラメータの設定
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self):
        try:
            self.parameter.setClassVar(self)  # パラメータ
            if self.canvas is not None:  # キャンバスが有る時
                self.canvas.clearPredictView()  # 予測値ビューが開いていたらクリア
            self.clearLayout(self.canvasLayout)  # キャンバスレイアウクリア
            self.canvas = AgeTableCanvasClass(self.MAX_PAGE_LASERS)  # テーブルキャンバス生成
            self.canvasLayout.addWidget(self.canvas)
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトを関数呼び出しメソッドと結合
    # ---------------------------------------------------------------------------------------------------
    def connectButtonsMethod(self):
        try:
            # パラメータ保存メソッドと結合
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                pack.qObject.currentTextChanged.connect(self.saveMethod)  # コンボボックスをパラメータ保存メソッドと結合
            # パラメータ保存メソッドと結合
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                exec("pack.qObject.currentTextChanged.connect(self." + pack.method + ")")  # コンボボックスを関数呼び出しメソッドと結合
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                exec("pack.qObject.clicked.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            for pack in self.lineEditList:  # ラインエディットリストをすべて実行
                exec("pack.qObject.textEdited.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            for pack in self.pushButtonList:  # プッシュボタンリストをすべて実行
                exec("pack.qObject.clicked.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            self.connected = True  # コネクト済にする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            # ビューレイアウト
            viewLayout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            viewLayout.setAlignment(Qt.AlignTop)  # 上詰め
            self.setLabelStyle2(viewLayout, self.title, "gray", "white", 40, "20pt")  # 表題ラベル
            buttonLayout = QHBoxLayout()  # ボタンレイアウト生成（水平レイアウト）
            self.setPredButton(buttonLayout, ["REDRAW", "再描画"])  # 再描画釦
            self.setPageSliderLayout(buttonLayout)  # ページスライダーレイアウト設定
            self.setRedSliderLayout(buttonLayout)  # 間引きスライダーレイアウト設定
            self.setCheckGroup(buttonLayout, {"SHOW_CH": "CH", "SHOW_LN": "LN", "SHOW_PPM": "PPM", "SHOW_MM": "MM"},
                               '表示部品選択')  # 表示部品選択フラグ
            self.setPredButton(buttonLayout, ['SAVE', "保存"])  # 保存
            self.setPredButton(buttonLayout, ['SAVE_PREDICT', "頁グラフ保存"])  # 頁グラフ全保存
            self.setIntCombo(buttonLayout, ["MAX_PAGE_LASERS", "頁最大レーザー数"], self.flatRange(1, 100))  # 一頁の最大レーザー数
            viewLayout.addLayout(buttonLayout)  # ビューレイアウトにボタンレイアウトを加える
            # ビュー本体レイアウト
            self.canvasLayout = QVBoxLayout()  # キャンバスレイアウト生成
            self.canvasLayout.setAlignment(Qt.AlignTop)  # 上詰め
            viewLayout.addLayout(self.canvasLayout)  # メインレイアウトにキャンバスレイアウトを追加
            return viewLayout  # ビューレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #    最大年齢テーブル表示
    # ---------------------------------------------------------------------------------------------------
    def showMaxArgTable(self):
        try:
            p = self.progress  # プログレスバー転写
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            self.title = GP.MIXCONT.MAIN_PARTS.PARTS + "年齢分析結果一覧表"  # タイトル
            PARTS_LIST = GP.MIXCONT.PARTS_LIST  # 部品コンテナリスト転写
            checkedList = self.treeWidget.getCheckedList()  # チェックされているリストを抽出
            if checkedList is not None:  # 抽出リストが有る時
                self.extractBase = GP.MIXCONT.MAIN_PARTS.PRB.makePRANodeList(checkedList)  # チェックされているPRBのリストを抽出
                if self.extractBase is not None:  # 抽出リストが有る時
                    length = len(self.extractBase)  # 訓練ピリオッドベース長
                    self.pages = math.ceil(length / self.MAX_PAGE_LASERS)  # ページ数をセット
                    self.page = 0  # ページをセット
                    self.pageSlider.setRange(1, self.pages)  # スライダーバリューセット
                    self.pageSliderLabel.setText(str(1) + "/" + str(self.pages) + "頁")  # ラベルをセット
                    self.showPageView(self.page, p)  # 頁のビューを表示
            self.endLevel(p)                                                                            # 現レベルの終了
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   頁のビューを表示
    # ---------------------------------------------------------------------------------------------------
    def showPageView(self, page, p=None):
        try:
            PARTS_LIST = GP.MIXCONT.PARTS_LIST  # 部品コンテナリスト転写
            self.parameter.setClassVar(self.canvas)
            maxLasers = self.MAX_PAGE_LASERS  # ページレーザー数
            self.pageList = self.extractBase[maxLasers * page:maxLasers * (page + 1)]  # ページリスト作成
            self.setAccBaseList(self.pageList)  # アクシデントライン描画用リストセット
            MAIN_PARTS = GP.MIXCONT.MAIN_PARTS  # 主部品を取得
            self.hideMainPartsCheckBox()  # 主部品のチェックボックスを隠す
            trainDic = MAIN_PARTS.PRB.getTrainDic(self.pageList)  # 主部品のトレイン辞書を作成する
            MAIN_PARTS.trainDic = trainDic  # 主部品のトレイン辞書をセット
            self.startNewLevel(len(PARTS_LIST) * 2, p)  # 新しいレベルの進捗開始
            if trainDic is not None:  # トレイン辞書が有る時
                for PARTS in PARTS_LIST:
                    mean = PARTS.PRB.getIntervalMeanList(PARTS, trainDic, self.RED_SPAN, p)  # 主部品のトレイン辞書から期待値平均辞書を生成
                    PARTS.meanDic, PARTS.maxShot = mean  # 期待値平均辞書と最大ショットをセット
                self.canvas.showPageView(self.pageList, p)  # キャンバスの頁のビューを表示
                self.deleteObject(trainDic)
                for PARTS in PARTS_LIST:
                    self.deleteObject(PARTS.meanDic)
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   アクシデントライン描画用ベースリストセット
    # ---------------------------------------------------------------------------------------------------
    def setAccBaseList(self, pageList, p=None):
        try:
            PRB = GP.MIXCONT.MAIN_PARTS.PRB
            self.startNewLevel(len(GP.MIXCONT.PARTS_LIST) * 3, p)  # 新しいレベルの進捗開始
            laserIdList = pageList[:, PRB.LASER_ID]  # レーザーIDリスト抽出
            laserIdList = np.unique(laserIdList)  # レーザーIDリストをユニークにする
            for PARTS in GP.MIXCONT.PARTS_LIST:  # 部品コンテナリストをすべて実行
                PARTS.JBB.loadPeriodDicList(laserIdList, p)  # JBBのピリオッド辞書を読み込む
                PARTS.ERB.loadPeriodDicList(laserIdList, p)  # ERBのピリオッド辞書を読み込む
                PARTS.GSB.loadPeriodDicList(laserIdList, p)  # GSBのピリオッド辞書を読み込む
            self.endLevel(p)                                                                            # 現レベルの終了
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

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
    #   ユニットディレクトリを取得する
    # ---------------------------------------------------------------------------------------------------
    def getUnitDir(self, pData):
        try:
            PRB = GP.MIXCONT.PARTS_LIST[0].PRB
            LEARN_UNIT = GP.CONT.MAIN_PARAMETER.LEARN_UNIT  # 学習単位取得
            if LEARN_UNIT == GP.LEARN_UNIT.TYPE_CODE:  # 学習単位がタイプコードの時
                UNIT_DIR = pData[PRB.TYPE_CODE]  # ページリストのタイプコードをセット
            elif LEARN_UNIT == GP.LEARN_UNIT.TYPE_ID:  # 学習単位がタイプIDの時
                UNIT_DIR = pData[PRB.LASER_TYPE_ID]  # ページリストのタイプIDをセット
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
    #   一頁の最大レーザー数
    # ---------------------------------------------------------------------------------------------------
    def MAX_PAGE_LASERS_EVENT(self):
        try:
            #            self.pageSlider.setRange(1,self.pages)                                                      # スライダーバリューセット
            #            self.pageSlider.setValue(1)                                                                 # スライダーバリューセット
            #            self.pageSliderLabel.setText(str(1)+ "/" + str(self.pages) + "頁")                          # ラベルをセット
            self.showMaxArgTable()  # 最大年齢テーブル表示
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   表示単位変更イベント
    # ---------------------------------------------------------------------------------------------------
    def DRAW_UNIT_EVENT(self):
        try:
            self.showMaxArgTable()  # 最大年齢テーブル表示

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   頁スライダー変更時の処理
    # ---------------------------------------------------------------------------------------------------
    def pageValueChanged(self):
        try:
            value = self.pageSlider.value()  # スライダーの値を取得
            self.pageSliderLabel.setText(str(value) + "/" + str(self.pages) + "頁")  # ラベルをセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   頁スライダリリース時の処理
    # ---------------------------------------------------------------------------------------------------
    def pageSliderReleased(self):
        try:
            p = self.progress  # プログレスバー転写
            self.page = self.pageSlider.value() - 1  # スライダーの値を取得
            self.showPageView(self.page, p)  # 頁のビューを表示

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   間引きスライダー変更時の処理
    # ---------------------------------------------------------------------------------------------------
    def redValueChanged(self):
        try:
            value = int(self.redSlider.value() / 10) * 10  # スライダーの値を取得
            self.redSlider.setValue(value)  # スライダーバリューセット
            self.redSliderLabel.setText(str(value))  # ラベルをセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   間引きスライダリリース時の処理
    # ---------------------------------------------------------------------------------------------------
    def redSliderReleased(self):
        try:
            p = self.progress  # プログレスバー転写
            self.RED_SPAN = self.redSlider.value()  # スライダーの値を取得
            self.canvas.RED_SPAN = self.RED_SPAN  # canvasのRED_SPANをセット
            self.saveParam()  # オブジェクトのデータをパラメータとファイルにセット
            self.showPageView(self.page, p)  # 最大値リスト作成
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   保存
    # ---------------------------------------------------------------------------------------------------
    def SAVE(self):
        try:
            unitDir = self.getUnitDir(self.pageList[0])  # ユニットディレクトリを取得する
            start_dir = unitDir + "/page" + str(self.page) + ".png"  # 初期ディレクトリ
            self.canvas.Save(start_dir)  # キャンバスを保存
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ページの予測グラフ保存
    # ---------------------------------------------------------------------------------------------------
    def SAVE_PREDICT(self):
        try:
            PRB = GP.MIXCONT.MAIN_PARTS.PRB
            p = self.progress  # プログレスバー転写
            self.startNewLevel(len(self.pageList), p)  # 新しいレベルの進捗開始
            unitDir = self.getUnitDir(self.pageList[0])  # ユニットディレクトリを取得する
            for i, rowData in enumerate(self.pageList):  # ページリストをすべて実行
                periodId = [rowData[PRB.LASER_ID], rowData[PRB.PERIOD]]  # ピリオッドID生成
                self.train = PRB.makeTrainData(rowData)  # トレインデータ作成
                if self.train is not None:  # トレインデータが有る時
                    predictView = AgePredictViewClass(self.train, i)  # 予測値ビューを生成
                    predictView.show()  # 予測値ビューを見せる
                    QApplication.processEvents()  # プロセスイベントを呼んで制御をイベントループに返す
                    predictView.SAVE2(unitDir)  # 予測値ビューを見せる
                    predictView.close()  # 予測値ビューを閉じる
                emit(p)
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   再描画
    # ---------------------------------------------------------------------------------------------------
    def REDRAW(self):
        try:
            p = self.progress  # プログレスバー転写
            self.showPageView(self.page, p)  # 頁のビューを表示
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   AgeTableCanvasClass クラス
# =======================================================================================================
class AgeTableCanvasClass(AnalysisBaseClass):
    def __init__(self, MAX_PAGE_LASERS):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.MAX_PAGE_LASERS = MAX_PAGE_LASERS
            self.progress = ProgressWindowClass()  # 進捗ダイアローグ生成
            self.page = 0  # 現ページ初期化
            self.resize(1000, 600)  # リサイズ
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.connectButtonsMethod()  # タブのオブジェクトとメソッドを結合
            self.predictViewList = [None] * self.MAX_PAGE_LASERS  # 表示中の予測値ビューリスト

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            # ビューレイアウト
            viewLayout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            viewLayout.setAlignment(Qt.AlignTop)  # 上詰め
            self.grid = GridClass(self, 10, 0)  # グリッドレイアウト生成
            viewLayout.addLayout(self.grid)  # ビューレイアウトにグループボックスを追加
            return viewLayout  # ビューレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   頁のビューを表示
    # ---------------------------------------------------------------------------------------------------
    def showPageView(self, pageList, p=None):
        try:
            self.pageList = pageList
            self.startNewLevel(2, p)  # 新しいレベルの進捗開始
            self.clearPredictView(p)  # 予測値ビューのクローズ処理
            self.predictViewList = [None] * self.MAX_PAGE_LASERS  # キャンバスの予測値ビューリストを再設定
            self.disconnectButtons()  # オブジェクトとメソッドの結合解除してからリストをクリアする
            self.grid.clear()  # グリッドレイアウトクリア
            self.setMaxArgBar(p)  # 期待値バー設定
            self.connectLaserSelButton()  # タブのオブジェクトとメソッドを結合
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   最大値バー設定
    # ---------------------------------------------------------------------------------------------------
    def setMaxArgBar(self, p=None):
        try:
            common = CommonParameterClass.getInstance()  # 年齢パラメーターをクラス変数に転写する
            TRN = GP.CONT.TRN  # TRNを転写
            frameSize = self.frameSize()  # フレームサイズ
            width = 1000  # フレーム幅 PIXEL
            height = frameSize.height()  # フレーム高さ PIXEL
            dpi = 100  # 1インチ当たりのピクセル数
            oneHeight = 20  # レーザー毎のグラフ本体の高さ(ピクセル)
            PARTS_LIST = GP.MIXCONT.PARTS_LIST  # 部品コンテナリスト転写
            MAIN_PARTS = GP.MIXCONT.MAIN_PARTS  # 主部品転写
            self.pushButtonList.clear  # プッシュボタンリストを初期化
            self.periodList = []  # ピリオッドリスト初期化
            ageBarList = []  # 年齢バーリスト初期化
            row = 0
            mainMeanDic = MAIN_PARTS.meanDic  # 主部品転写
            maxShot = MAIN_PARTS.maxShot  # 最大ショット転写
            if maxShot is not None:
                self.startNewLevel(len(mainMeanDic), p)  # 新しいレベルの進捗開始
                for (LASER_ID, PERIOD), mean in mainMeanDic.items():  # 期待値辞書をすべて実行
                    # 主部品設定
                    self.periodList.append([LASER_ID, PERIOD])  # ピリオッドリストに追加
                    # レーザーボタン設定
                    title = str(LASER_ID) + '-' + str(PERIOD)  # ボタンタイトル
                    self.setLaserSelButton(self.grid, row, 0, title)  # レーザー選択釦設定
                    # ステータス表示釦設定
                    label = mean[0, TRN.LABEL]  # ラベル
                    self.setChStatusButton(self.grid, row, 1, MAIN_PARTS.LABEL, label)  # レーザーステータス表示釦設定
                    # 最大値バー設定
                    ageBar = AgeBarClass(MAIN_PARTS, width, oneHeight, mean, maxShot)  # 年齢バー生成
                    ageBarList.append(ageBar)  # 年齢バーリストに追加
                    self.ageCutBar = AgeCutBarClass(ageBar, "BAR")  # カット年齢バー生成
                    self.grid.addWidget(self.ageCutBar, row, 2)  # グリッド(row,0)に最大値バーをセット
                    row += 1
                    # ステータス表示釦設定
                    for PARTS in PARTS_LIST:  # 部品リストをすべて実行
                        if (PARTS != MAIN_PARTS and  # 主部品でない時かつ
                                PARTS.meanDic is not None and  # 期待値平均データパックが有る時かつ
                                (PARTS.PARTS == GP.PARTS.CH and self.SHOW_CH or  # CHかつCH表示の時または
                                 PARTS.PARTS == GP.PARTS.LN and self.SHOW_LN or  # LNかつLN表示の時または
                                 PARTS.PARTS == GP.PARTS.PPM and self.SHOW_PPM or  # PPMかつPPM表示の時または
                                 PARTS.PARTS == GP.PARTS.MM and self.SHOW_MM)):  # MMかつMM表示の時
                            mean = PARTS.meanDic.get((LASER_ID, PERIOD))  # 期待値平均データ取得
                            if mean is not None:  # 期待値平均データが有る時
                                self.periodList.append([LASER_ID, PERIOD])  # ピリオッドリストに追加
                                # ステータス表示釦設定
                                self.setLnStatusButton(self.grid, row, 1, PARTS.PARTS)  # レーザーステータス表示釦設定
                                # 最大値バー設定
                                ageBar = AgeBarClass(PARTS, width, oneHeight, mean, maxShot)  # 年齢バー生成
                                ageBarList.append(ageBar)  # 年齢バーリストに追加
                                self.ageCutBar = AgeCutBarClass(ageBar, "BAR")  # カット年齢バー生成
                                self.grid.addWidget(self.ageCutBar, row, 2)  # グリッド(row,0)に最大値バーをセット
                                row += 1
                    # グリッド(row,0)に目盛りをセット
                    self.ageCutBar = AgeCutBarClass(ageBarList[0], "TICK_MARKS")  # 目盛りバーラベル生成
                    self.grid.addWidget(self.ageCutBar, row, 2)  # グリッド(row,1)に目盛りをセット
                    emit(p)  # 進捗バーにシグナルを送る
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   予測値ビューのクローズ処理
    # ---------------------------------------------------------------------------------------------------
    def clearPredictView(self, p=None):
        try:
            length = len(self.predictViewList)  # 予測値ビューの現在の長さ
            self.startNewLevel(length, p)  # 新しいレベルの進捗開始
            for i in range(length):  # 表示最大レーザー数を実行
                if self.predictViewList[i] is not None:  # 表示中の予測値ビューが有る時
                    self.predictViewList[i].close()  # 表示中の予測値ビューを閉じる
                    self.predictViewList[i] = None  # 表示中の予測値ビューを閉じる
                emit(p)  # 進捗バーにシグナルを送る
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ***************************************************************************************************
    #   イベント処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   レーザー選択ボタンクリック
    # ---------------------------------------------------------------------------------------------------
    def LASER_SEL(self, i):
        try:
            MAIN_PARTS = GP.MIXCONT.MAIN_PARTS  # メイン部品転写
            PRB = MAIN_PARTS.PRB  # PRB転写
            periodId = self.periodList[i]  # ピリオッド取得
            laser = np.where(
                (self.pageList[:, [PRB.LASER_ID, PRB.PERIOD]] == periodId).all(axis=1))  # ページリストのインデックスリスト取得
            if len(laser) > 0:  # インデックスリストが有る時
                laser = laser[0][0]  # インデックス取得
                if self.predictViewList[laser] is None:  # 表示中の予測値ビューが無い時
                    train = MAIN_PARTS.trainDic.get(tuple(periodId))  # トレインデータ取得
                    self.predictViewList[laser] = AgePredictViewClass(train, laser)  # 予測値ビューを生成
                    self.predictViewList[laser].show()  # 予測値ビューを表示
                else:  # 表示中の予測値ビューが有る時
                    if self.predictViewList[laser].isVisible():  # 予測値ビューがビジブルな時
                        self.predictViewList[laser].close()  # 予測値ビューを隠す
                    else:
                        self.predictViewList[laser].show()  # 予測値ビューを見せる
            return

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   クラス 年齢予測値パラメータクラス
# =======================================================================================================
class AgePredictViewParameterClass(ParameterClass):
    def __init__(self, logPath):  # 初期化
        try:
            ParameterClass.__init__(self, logPath)  # スーパークラスの初期化
            ACCERR = True  # 異常発生ライン選択（ERROR）
            ACCPEX = True  # 異常発生ライン選択（PEX）
            ACCGAS = True  # 異常発生ライン選択（ACCGAS）
            VIEW_SRC = True  # 元データ表示
            VIEW_AGE = True  # 年齢表示
            SHOW_CH = True  # CH表示
            SHOW_LN = True  # LN表示
            SHOW_PPM = True  # PPM表示
            SHOW_MM = True  # MM表示
            RED_SPAN = 20  # 平均区間幅
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != 'logPath') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
            self.loadData()  # タブパラメータをファイルから読み込み

        except Exception as e:  # 例外
            printError(e)  # 例外を表示


# =======================================================================================================
#   スーパークラス 年齢予測値ビュークラス
# =======================================================================================================
class AgePredictViewClass(AnalysisBaseClass):
    def __init__(self, train, viewNo):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.parameter = AgePredictViewParameterClass(GP.MAIN_LOG.AGE_PREDICT_VIEW)  # パラメータ
            common = CommonParameterClass.getInstance()  # 年齢パラメーターをクラス変数に転写する
            self.title = GP.MIXCONT.MAIN_PARTS.PARTS + "年齢分析結果"  # ビューのタイトル
            self.setWindowTitle(self.title)  # ウインドウのタイトル
            self.progress = ProgressWindowClass()  # 進捗ダイアローグ生成
            self.resize(800, 600)  # サイズをセット
            self.setWindowState(Qt.WindowMaximized)  # 表示を最大にする
            self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 常に最前面に表示
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.redSliderLabel.setText(str(self.RED_SPAN))  # スライダーラベルをセット

            self.train = train  # レーザーID
            self.viewNo = viewNo  # ビュー番号
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.connectButtons3()  # タブのオブジェクトとメソッドを結合
            self.canvas = AgePredictCanvasClass(self, 10, 8)  # キャンバス描画
            self.canvasLayout.addWidget(self.canvas)  # キャンバスレイアウトにキャンバストを追加
            self.viewCenter()  # 中央に表示
            self.redraw()  # キャンバスを描画
            self.show()  # キャンバスを描画

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
            self.setPredButton(hLayout, ["redraw", "再描画"])  # 再描画釦
            self.setRedSliderLayout(hLayout)  # 間引きスライダーレイアウト設定
            self.setCheckGroup(hLayout, {"ACCERR": "エラー", "ACCPEX": "交換", "ACCGAS": "ガス"}, 'イベント選択')  # イベント選択フラグ
            self.setCheckGroup(hLayout, {"VIEW_SRC": "入力", "VIEW_AGE": "年齢"}, 'グラフ選択')  # グラフ選択フラグ
            self.setCheckGroup(hLayout, {"SHOW_CH": "CH", "SHOW_LN": "LN", "SHOW_PPM": "PPM", "SHOW_MM": "MM"},
                               '表示部品選択')  # 表示部品選択フラグ
            self.setPredButton(hLayout, ["X_CHECK", "入力表示"])  # 表示Xデータ選択釦
            self.setPredButton(hLayout, ["AGE_CHECK", "年齢選択"])  # 表示年齢選択釦
            self.setPredButton(hLayout, ['SAVE', "保存"])  # 保存
            self.setPredButton(hLayout, ['CLOSE', "閉じる"])  # ウインドウを閉じる
            mLayout.addLayout(hLayout)  # mLayoutに水平レイアウトを追加
            #  予測値レイアウト作成
            self.canvasLayout = QVBoxLayout()  # キャンバスレイアウト生成
            mLayout.addLayout(self.canvasLayout)  # メインレイアウトにキャンバスレイアウトを追加
            mLayout.setAlignment(Qt.AlignTop)  # 上詰め
            return mLayout  # メインレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   再描画
    # ---------------------------------------------------------------------------------------------------
    def redraw(self):
        try:
            p = self.progress  # プログレス転写
            PRB = GP.MIXCONT.MAIN_PARTS.PRB  # PRBを転写
            PARTS_LIST = GP.MIXCONT.PARTS_LIST  # 部品コンテナリスト転写
            self.startNewLevel(len(PARTS_LIST), p)  # 新しいレベルの進捗開始
            self.hideMainPartsCheckBox()  # 主部品のチェックボックスを隠す
            for PARTS in PARTS_LIST:  # 部品リストをすべて実行
                reduce, meanPredict = PRB.getPredictOne(PARTS, self.train, self.RED_SPAN, p)  # 予測値を取得
                PARTS.reduce = reduce  # 区間平均値リストに追加
                PARTS.mean = meanPredict  # 区間平均値リストに追加
            if PARTS_LIST[0].reduce is not None and PARTS_LIST[0].mean is not None:  # CHの間引きリストと区間平均値リストが有る時
                self.parameter.setClassVar(self.canvas)  # パラメータセット
                self.canvas.redraw(self.train)  # キャンバス描画
                self.updateView()  # ビューを更新する
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ユニットディレクトリを取得する
    # ---------------------------------------------------------------------------------------------------
    def getUnitDirTrn(self, trnData):
        try:
            TRN = GP.CONT.TRN  # TRNを転写
            LEARN_UNIT = GP.CONT.MAIN_PARAMETER.LEARN_UNIT  # 学習単位取得
            if LEARN_UNIT == GP.LEARN_UNIT.TYPE_CODE:  # 学習単位がタイプコードの時
                UNIT_DIR = trnData[TRN.TYPE_CODE]  # ページリストのタイプコードをセット
            elif LEARN_UNIT == GP.LEARN_UNIT.TYPE_ID:  # 学習単位がタイプIDの時
                UNIT_DIR = trnData[TRN.LASER_TYPE_ID]  # ページリストのタイプIDをセット
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
    #   表示単位変更イベント
    # ---------------------------------------------------------------------------------------------------
    def DRAW_UNIT_EVENT(self):
        self.redraw()  # キャンバスを描画

    # ---------------------------------------------------------------------------------------------------
    #   Xデータプロットモード変更時時処理
    # ---------------------------------------------------------------------------------------------------
    def SRC_PLOT_MODE_EVENT(self):
        self.redraw()  # キャンバスを描画

    # ---------------------------------------------------------------------------------------------------
    #    年齢プロットモード変更時時処理
    # ---------------------------------------------------------------------------------------------------
    def AGE_PLOT_MODE_EVENT(self):
        self.redraw()  # キャンバスを描画

    # ---------------------------------------------------------------------------------------------------
    #   X_DATAクリック時処理
    # ---------------------------------------------------------------------------------------------------
    def X_CHECK(self):
        if self.canvas.xCheckWindow.isVisible():  # Xチェックボックスウインドウが表示されている時
            self.canvas.xCheckWindow.close()  # Xチェックボックスウインドウを非表示
        else:  # Xチェックボックスウインドウが表示されていない時
            self.canvas.xCheckWindow.show()  # Xチェックボックスウインドウを表示

    # ---------------------------------------------------------------------------------------------------
    #   AGE_CHECKクリック時処理
    # ---------------------------------------------------------------------------------------------------
    def AGE_CHECK(self):
        if self.canvas.yCheckWindow.isVisible():  # Yチェックボックスウインドウが表示されている時
            self.canvas.yCheckWindow.close()  # Yチェックボックスウインドウを非表示
        else:
            self.canvas.yCheckWindow.show()  # Yチェックボックスウインドウを表示

    # ---------------------------------------------------------------------------------------------------
    #   レイアウトをクリア
    # ---------------------------------------------------------------------------------------------------
    def clearLayout(self, layout):
        try:
            while layout.itemAt(0) is not None:  # アイテムの数をすべて実行
                layout.removeItem(layout.itemAt(0))  # アイテムを取り除く

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   レイアウトをクリア
    # ---------------------------------------------------------------------------------------------------
    def clearGroupBox(self, groupBox):
        try:
            groupBox.widget().deleteLater()  # ウイジェットを遅延削除
            groupBox.removeItem(groupBox.widget())  # アイテムを取り除く

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   間引きスライダー変更時の処理
    # ---------------------------------------------------------------------------------------------------
    def redValueChanged(self):
        try:
            value = int(self.redSlider.value() / 10) * 10  # スライダーの値を取得
            self.redSlider.setValue(value)  # スライダーバリューセット
            self.redSliderLabel.setText(str(value))  # ラベルをセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   スライダリリース時の処理
    # ---------------------------------------------------------------------------------------------------
    def redSliderReleased(self):
        try:
            self.saveParam()  # オブジェクトのデータをパラメータとファイルにセット
            self.redraw()

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   チェックウインドウをすべて閉じる
    # ---------------------------------------------------------------------------------------------------
    def closeCheckWindows(self):
        try:
            self.canvas.xCheckWindow.close()  # Xチェックウインドウを表示
            self.canvas.yCheckWindow.close()  # Yチェックウインドウを表示

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
    #   クローズ処理
    # ---------------------------------------------------------------------------------------------------
    def closeEvent(self, e):
        try:
            self.closeCheckWindows()  # チェックウインドウをすべて閉じる
            return

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ダイアローグ有りで保存
    # ---------------------------------------------------------------------------------------------------
    def SAVE(self):
        try:
            TRN = GP.CONT.TRN  # TRNを転写
            begin = self.train[0, TRN.LOG_DATE_TIME]  # 開始日時追加
            begin = str(begin.date())
            end = self.train[-1, TRN.LOG_DATE_TIME]  # 終了日時追加
            end = str(end.date())
            unitDir = self.getUnitDirTrn(self.train[0])  # ユニットディレクトリを取得する
            LASER_ID = self.train[0, TRN.LASER_ID]
            PERIOD = self.train[0, TRN.PERIOD]
            startName = str(LASER_ID) + "_" + str(PERIOD) + "_[" + begin + "]" + "-[" + end + "]"  # ファイル名をセット
            start_dir = unitDir + startName + ".png"  # 初期パスをセット
            self.canvas.Save(start_dir)  # キャンバスを保存
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ダイアローグなしで直接保存
    # ---------------------------------------------------------------------------------------------------
    def SAVE2(self, unitDir):
        try:
            TRN = GP.CONT.TRN  # TRNを転写
            begin = self.train[0, TRN.LOG_DATE_TIME]  # 開始日時追加
            begin = str(begin.date())
            end = self.train[-1, TRN.LOG_DATE_TIME]  # 終了日時追加
            end = str(end.date())
            start_dir = "C:/Users/owner/Documents/"  # 初期ディレクトリ
            LASER_ID = self.train[0, TRN.LASER_ID]
            PERIOD = self.train[0, TRN.PERIOD]
            startName = str(LASER_ID) + "_" + str(PERIOD) + "_[" + begin + "]" + "-[" + end + "]"
            start_dir = unitDir + startName + ".png"
            pixmap = self.canvas.grab(QRect(QPoint(0, 0), QSize(-1, -1)))  # キャンバスを保存
            pixmap.save(start_dir)
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   ChAgePredictCanvasClass クラス
# =======================================================================================================
class AgePredictCanvasClass(AnalysisBaseClass):
    def __init__(self, parent, width, height, dpi=100):
        try:
            AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.xCheckWindow = XCheckWindowClass()  # Xチェックボックスウインドウを生成
            self.yCheckWindow = YCheckWindowClass()  # Yチェックボックスウインドウを生成
            self.figure = Figure(figsize=(width, height), dpi=dpi)
            self.figureCanvas = FigureCanvas(self.figure)
            self.figureCanvas.setParent(self)
            self.figureCanvas.setSizePolicy(  # サイズポリシー設定
                QSizePolicy.Expanding,  # 幅可変
                QSizePolicy.Expanding)  # 高さ可変
            self.setClassVar()  # パラメータの設定
            self.layout = QVBoxLayout()  # ビューレイアウト生成（垂直レイアウト）
            self.layout.addWidget(self.figureCanvas)  # ビューレイアウトにグループボックスを追加
            self.setLayout(self.layout)  # レイアウトを自分にセット

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   パラメータの設定
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self):
        try:
            # ユーザーパラメータから転写
            #            self.parameter.setClassVar(self)                                                            # 年齢パラメーターをインスタンス変数に転写する
            self.MY_SRC_Y_LIMIT = 1.1  # XデータY軸上限
            self.MY_AGE_Y_LIMIT = 1.1  # 年齢Y軸上限
            self.MY_LIFE_Y_LIMIT = 100  # 年齢Y軸上限
            self.MY_VIEWS_PLOT = 2  # 年齢描画画面数（元データと予測値合計)を設定

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   予測値をプロット
    # ---------------------------------------------------------------------------------------------------
    def redraw(self, train):
        try:
            PARTS_LIST = GP.MIXCONT.PARTS_LIST  # 部品コンテナリスト転写
            MAIN_PARTS = GP.MIXCONT.MAIN_PARTS  # 部品コンテナリスト転写
            OUT_LIST = GP.CONT.OUT_LIST  # 出力リスト転写
            self.figure.clf()  # フィガークリア
            LASER_ID = MAIN_PARTS.reduce[GP.CONT.TRN.LASER_ID]  # レーザーID
            PERIOD = MAIN_PARTS.reduce[GP.CONT.TRN.PERIOD]  # ピリオッド
            self.views = 0  # 描画画面数
            if self.VIEW_SRC:  # Xデータを表示の時
                self.views += 1  # 描画画面数
            if self.VIEW_AGE:  # Xデータを表示の時
                self.views += 1  # 描画画面数
            self.viewCount = 0  # 描画画面カウントリセット
            # Xデータを表示
            if self.VIEW_SRC:  # Xデータを表示の時
                axes = self.initializeSubPlots(LASER_ID)  # サブプロットを初期設定
                reduce = MAIN_PARTS.reduce
                if reduce is not None:
                    Y_LIMIT = self.MY_SRC_Y_LIMIT  # Y_LIMITを転写
                    self.plotAccLine(axes, PARTS_LIST[0], train, Y_LIMIT)  # 異常発生ライン描画
                    self.plotSrcData(axes, PARTS_LIST[0], reduce, Y_LIMIT, True)  # 元データを表示
                self.viewCount += 1  # 描画画面カウントを加算
            # 年齢を表示
            if self.VIEW_AGE:  # 年齢表示の時
                colorList = ['black', 'orange', 'blue', 'violet']
                axes = self.initializeSubPlots(LASER_ID)  # サブプロットを初期設定
                Y_LIMIT = self.MY_LIFE_Y_LIMIT  # Y_LIMITを転写
                self.plotAccLine(axes, MAIN_PARTS, train, Y_LIMIT)  # 異常発生ライン描画
                for i, PARTS in enumerate(PARTS_LIST):
                    color = colorList[i]
                    if PARTS.mean is not None:
                        if (PARTS.PARTS == GP.PARTS.CH and self.SHOW_CH or
                                PARTS.PARTS == GP.PARTS.LN and self.SHOW_LN or
                                PARTS.PARTS == GP.PARTS.PPM and self.SHOW_PPM or
                                PARTS.PARTS == GP.PARTS.MM and self.SHOW_MM):
                            self.plotLifeData(axes, PARTS, train, PARTS.mean, Y_LIMIT, color, True)  # 寿命のプロット
                self.viewCount += 1  # 描画画面カウントを加算
                pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   入力データのプロット
    # ---------------------------------------------------------------------------------------------------
    def plotSrcData(self, axes, PARTS, source, LASER_ID, Y_LIMIT, labelFlag=False):
        try:
            TRN = GP.CONT.TRN  # TRNを転写
            X_FLAG = self.xCheckWindow.flagList  # Xフラグ
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            X_INDEX = GP.X_LIST.LIST  # Xインデックス転写
            target = source[0, TRN.TARGET]  # ターゲット
            plotRange = source[:, TRN.REL_SHOT]  # プロットレンジ
            plotMode = GP.PLOT_MODE.PLOT  # プロットモード
            for i, label in enumerate(X_INDEX):  # 予測値Xデータをすべて実行
                if X_FLAG[i]:  # Xデータがチェックされているか確認
                    color = GP.X_LIST.getColor(label)  # 当該ラベルのカラー取得
                    labelTrain = np.concatenate([source[:, :X_BASE], source[:, X_BASE + i:X_BASE + i + 1]],
                                                axis=1)  # トレインデータを作成
                    self.plotData(axes, labelTrain, plotRange, label, labelFlag, color, plotMode)  # ラベル値とデータのプロット
            axes.legend(loc='upper left', fontsize=10, bbox_to_anchor=(1.05, 1.0), markerscale=3)  # 配置
            axes.grid(True)  # グリッド描画
            axes.set_xlabel('shots')  # X軸ラベル
            axes.set_ylabel('X_DATA')  # Y軸ラベル
            axes.set_ylim([0, Y_LIMIT])  # Y軸レンジ
            axes.set_title(self.getTitle(PARTS, source))  # タイトル描画
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   予測のプロット
    # ---------------------------------------------------------------------------------------------------
    def plotPrdData(self, axes, PARTS, predict, Y_LIMIT, Y_FLAG_LIST, labelFlag=False):
        try:
            TRN = GP.CONT.TRN  # TRNを転写
            OUT_LIST = GP.CONT.OUT_LIST  # 出力リスト転写
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            Y_FLAG = self.yCheckWindow.flagList  # Yフラグ
            plotRange = predict[:, TRN.REL_SHOT]  # プロットレンジ
            plotMode = GP.PLOT_MODE.PLOT  # プロットモード
            drawn = False  # 描画済フラグをリセット
            for i, label in enumerate(OUT_LIST.LIST):  # ラベルリストをすべて実行
                labelNo = Y_FLAG_LIST.NO_LIST[label]  # 表示Yフラグ用のラベル番号を取得
                if Y_FLAG[labelNo]:  # チェックされているか確認
                    color = OUT_LIST.getColor(label)  # カラー取得
                    labelTrain = np.concatenate([predict[:, :X_BASE], predict[:, X_BASE + i:X_BASE + i + 1]],
                                                axis=1)  # トレインデータを作成
                    self.plotData(axes, labelTrain, plotRange, label, labelFlag, color, plotMode)  # ラベル値とデータのプロット
                    drawn = True  # 描画済フラグをセット
            if drawn:  # 描画されている時
                axes.legend(fontsize=10, bbox_to_anchor=(1.0, 0.0), loc='lower left', markerscale=3)  # 配置
                axes.grid(True)  # グリッド描画
                axes.set_xlabel('M shots')  # X軸ラベル
                axes.set_ylabel('predict')  # Y軸ラベル
                axes.set_ylim([0, Y_LIMIT])  # Y軸レンジ
                axes.set_title(self.getTitle(PARTS, predict))  # タイトル描画
                pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   寿命のプロット
    # ---------------------------------------------------------------------------------------------------
    def plotLifeData(self, axes, PARTS, train, predict, Y_LIMIT, color, labelFlag=False):
        try:
            TRN = GP.CONT.TRN  # TRNを転写
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            plotRange = predict[:, TRN.REL_SHOT]  # プロットレンジ
            plotMode = GP.PLOT_MODE.PLOT  # プロットモード
            pt = predict[:, X_BASE:]  # Xデータ
            drawn = False  # 描画済フラグをリセット
            text = 'LIFE'  # テキスト
            maxX = predict[-1, TRN.REL_SHOT]
            deltaX = int(maxX * 0.01)
            maxLife = GP.MAX_AGE - GP.AGE_STEP  # 寿命
            axes.text(-deltaX, maxLife + 1.1, text, ha='right', va='bottom', fontsize=12,
                      backgroundcolor='white')  # テキスト描画
            linestyle = "solid"  # ラインスタイルを実線にする
            axes.axhline(y=GP.MAX_AGE - GP.AGE_STEP, linestyle=linestyle, color='violet', alpha=1.0)  # 最大年齢線プロット
            self.plotData(axes, predict, plotRange, PARTS.PARTS, labelFlag, color, plotMode)  # ラベル値とデータのプロット
            drawn = True  # 描画済フラグをセット
            if drawn:  # 描画されている時
                axes.legend(fontsize=10, bbox_to_anchor=(1.0, 0.0), loc='lower left', markerscale=3)  # 配置
                axes.grid(True)  # グリッド描画
                axes.set_xlabel('M shots')  # X軸ラベル
                axes.set_ylabel('predict age')  # Y軸ラベル
                axes.set_ylim([0, Y_LIMIT])  # Y軸レンジ
                axes.set_title(self.getTitle(PARTS, train))  # タイトル描画

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   異常発生ライン描画
    # ---------------------------------------------------------------------------------------------------
    def plotAccLine(self, axes, PARTS, train, Y_LIMIT):
        try:
            JBB = PARTS.JBB  # JBBを転写
            ERB = PARTS.ERB  # ERBを転写
            GSB = PARTS.GSB  # GSBを転写
            TRN = GP.CONT.TRN  # TRNを転写
            LABEL = PARTS.LABEL  # ラベルを転写
            LASER_ID = train[0, TRN.LASER_ID]  # レーザーID
            PERIOD = train[0, TRN.PERIOD]  # ピリオッド
            target = train[0, TRN.TARGET]  # ターゲット
            maxX = train[-1, TRN.REL_SHOT]  # ターゲット
            jobList = JBB.getPeriodData(GP.BASE_TYPE.P_BASE, LASER_ID, PERIOD)  # JBBベースリストからピリオッドデータを取得
            errList = ERB.getPeriodData(GP.BASE_TYPE.P_BASE, LASER_ID, PERIOD)  # ERBベースリストからピリオッドデータを取得
            periodLength = len(train)  # 予測値長さ
            dx = maxX * 0.002 * GP.AGE_STEP  # 表示時のXオフセット量
            # TARGET
            if target is not None:  # ターゲットが有る時
                x = target  # x
                Y = Y_LIMIT - 3.5  # テキストY位置
                color = "Green"  # ラベルのカラー取得
                linestyle = "solid"  # ラインスタイルを点線にする
                axes.axvline(x=x, linestyle=linestyle, color=color, alpha=1.0)  # ラインを引く
                text = 'TARGET'  # テキスト
                axes.text(x + dx, Y, text, ha='left', va='bottom', fontsize=10, backgroundcolor='white')  # テキスト描画
            # GAS_FILL
            if self.ACCGAS:  # ACCGAS選択の時
                gasList = GSB.getPeriodData(GP.BASE_TYPE.P_BASE, LASER_ID, PERIOD)  # ERBベースリストからピリオッドデータを取得
                if gasList is not None:  # ガスリストが有る時
                    for rowData in gasList:  # エラーリストをすべて実行
                        HAPPEN_DATE = rowData[GSB.END_DATE_TIME]  # ガス交換日時
                        color = "skyblue"  # ラベルのカラー取得
                        x = self.getHappenShot(HAPPEN_DATE, train)
                        if x is not None:
                            linestyle = "dotted"  # ラインスタイルを点線にする
                            axes.axvline(x=x, linestyle=linestyle, color=color, alpha=1.0)  # ラインを引く
            # ERROR
            if self.ACCERR:  # ERROR選択の時
                if errList is not None:  # エラーリストが有る時
                    deltaText = 0  # テキストYオフセットリセット
                    lastX = -10000  # 直前のテキストXリセット
                    happenList = errList[:, ERB.HAPPEN_SHOT]
                    codeList = np.array(happenList, 'str') + errList[:, ERB.ERROR_CODE]
                    codeList = np.unique(codeList)
                    errorList = []
                    for code in codeList:
                        happen = int(code[0:-5])
                        error = code[-5:]
                        codeLst = errList[
                            (errList[:, ERB.HAPPEN_SHOT] == happen) & (errList[:, ERB.ERROR_CODE] == error)]
                        errorList += [list(codeLst[0])]
                    for rowData in errorList:  # エラーリストをすべて実行
                        HAPPEN_DATE = rowData[ERB.HAPPEN_DATE]  # エラー発生日時
                        x = self.getHappenShot(HAPPEN_DATE, train)
                        if x is not None:
                            ERROR_CODE = rowData[ERB.ERROR_CODE]  # ERROR_CODE
                            if ERROR_CODE in GP.GR_ERR_LIST.LIST:  # ERROR_CODEがエラーリストに有る時
                                color = GP.EVT_LIST.getColor(ERROR_CODE)  # ラベルのカラー取得
                                linestyle = "dotted"  # ラインスタイルを点線にする
                                axes.axvline(x=x, linestyle=linestyle, color=color, alpha=1.0)  # ラインを引く
                                text = ERROR_CODE
                                if ERROR_CODE == 'E0001':
                                    text = "fine abnormal"
                                elif ERROR_CODE == 'E0011':
                                    text = "coarse abnormal"
                                if x - lastX > maxX * 0.05:
                                    deltaText = 0  # テキストYオフセットセット
                                    Y = Y_LIMIT - 3.5  # テキストY位置
                                else:
                                    deltaText += 3.5  # テキストYオフセットセット
                                    if deltaText >= 90: deltaText = 0  # 文字オフセットが90以上の時は0にする
                                Y = Y_LIMIT - 3.5 - deltaText  # テキストY位置
                                axes.text(x + dx, Y, text, ha='left', va='bottom', fontsize=10,
                                          backgroundcolor='white')  # テキスト描画
                                lastX = x
            # 部品交換
            if self.ACCPEX:  # PEX選択の時
                if jobList is not None:  # ジョブリストが有る時
                    deltaText = 0  # テキストYオフセットリセット
                    lastX = -10000  # 直前のテキストXリセット
                    for rowData in jobList:  # ジョブリストをすべて実行
                        HAPPEN_DATE = rowData[JBB.HAPPEN_DATE]  # ジョブ発生日時
                        PARTS_NAME = rowData[JBB.PARTS_NAME]  # 部品名
                        CLASS = rowData[JBB.CLASS]  # 部品クラス
                        x = self.getHappenShot(HAPPEN_DATE, train)
                        if x is not None:
                            if CLASS != '99':
                                color = GP.PEX_LIST.getColor(PARTS_NAME)  # ラベルのカラー設定
                                if PARTS_NAME in GP.PEX_LIST.LIST:  # 部品交換リストに有る時
                                    if CLASS == '04':
                                        linestyle = "solid"  # 部品クラスが'04'の時はラインスタイルを実線にする
                                        classText = "install"
                                    elif CLASS == '08':
                                        color = 'red'  # ラベルのカラー設定
                                        linestyle = "solid"  # 部品クラスが'08'の時はラインスタイルを実線にする
                                        classText = "abnormal replacement"
                                    elif CLASS == '09':
                                        color = 'red'  # ラベルのカラー設定
                                        linestyle = "solid"  # 部品クラスが'09'の時はラインスタイルを実線にする
                                        classText = "abnormal replacement"
                                    elif CLASS == '10':
                                        color = 'red'  # ラベルのカラー設定
                                        linestyle = "solid"  # 部品クラスが'10'の時はラインスタイルを実線にする
                                        classText = "abnormal replacement"
                                    elif CLASS == '11':
                                        color = 'red'  # ラベルのカラー設定
                                        linestyle = "solid"  # 部品クラスが'11'の時はラインスタイルを実線にする
                                        classText = "abnormal replacement"
                                    elif CLASS == '12':
                                        color = 'red'  # ラベルのカラー設定
                                        linestyle = "solid"  # 部品クラスが'12'の時はラインスタイルを実線にする
                                        classText = "abnormal replacement"
                                    elif CLASS == '00':
                                        linestyle = "solid"  # 部品クラスが'00'の時はラインスタイルを点線にする
                                        classText = "regular replacement"
                                    else:
                                        linestyle = "dotted"  # その他の時はラインスタイルを点線にする
                                        classText = "others"
                                    axes.axvline(x=x, linestyle=linestyle, color=color, alpha=1.0, lw=2)  # ラインを引く
                                    if x - lastX > maxX * 0.05:
                                        deltaText = 0  # テキストYオフセットセット
                                        Y = Y_LIMIT - 3.5  # テキストY位置
                                    else:
                                        deltaText += 3.5  # テキストYオフセットセット
                                        if deltaText >= 90: deltaText = 0  # 文字オフセットが90以上の時は0にする
                                    Y = Y_LIMIT - 3.5 - deltaText  # テキストY位置
                                    PARTS_NAME = PARTS_NAME.replace('R_', '')
                                    PARTS_NAME = PARTS_NAME.replace('A_', '')
                                    PARTS_NAME = PARTS_NAME.replace('P_', '')
                                    text = PARTS_NAME + ' ' + classText  # テキスト
                                    axes.text(x + dx, Y, text, ha='left', va='bottom', fontsize=10,
                                              backgroundcolor='white')  # テキスト描画
                                    lastX = x
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass


# =======================================================================================================
#   クラス Xチェックウインドウ
# =======================================================================================================
class XCheckWindowClass(CheckWindowClass):
    def __init__(self):  # 初期化
        try:
            title = "X_DATA 選択"  # タイトル
            listPack = GP.X_LIST  # チェックデータリスト設定
            crList = [0, listPack.length]  # Xデータ段落設定リスト設定(リストの項目の値毎に段落替え)
            CheckWindowClass.__init__(self, title, None, listPack, crList)  # スーパークラスの初期化
            size = QSize(260, 500)  # ウインドウサイズ
            self.resize(size)  # ウインドウサイズ設定
            deskTopSize = self.getDesktopSize()  # デスクトップサイズ
            self.move(deskTopSize.width() - 34 - size.width(), 120)  # ウインドウ位置設定
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass


# =======================================================================================================
#   クラス Yチェックウインドウ
# =======================================================================================================
class YCheckWindowClass(CheckWindowClass):
    def __init__(self):  # 初期化
        try:
            title = "AGE 選択"  # タイトル
            listPack = GP.AGE_LIST  # チェックデータリスト設定
            n1 = int(listPack.length / 2)  # 一番目の段落の項目番号（n0から）
            n2 = listPack.length  # 二番目の段落の項目番号（n1から）
            crList = [0, n1, n2]  # 段落設定リスト設定(リストの項目の値毎に段落替え)
            CheckWindowClass.__init__(self, title, None, listPack, crList)  # スーパークラスの初期化
            size = QSize(260, 500)  # ウインドウサイズ
            self.resize(size)  # ウインドウサイズ設定
            deskTopSize = self.getDesktopSize()  # デスクトップサイズ
            self.move(deskTopSize.width() - 34 - size.width(), 120)  # ウインドウ位置設定
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

