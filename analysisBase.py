import os
import numpy as np
from functools import partial
from PyQt5Import import *
from kerasImport import *
from static import *
from commonBase import QObjectPackClass
from commonBase import CommonBaseClass
from comb import CombClass
from qtBase import QtBaseClass
from gpiBase import LaserTreeClass
import pathlib
from classDef import ParameterClass


# =======================================================================================================
#   クラス AnalysisBaseClass 分析ベースクラス
# =======================================================================================================
class AnalysisBaseClass(QtBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            QtBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            self.HISTORY = None  # 学習履歴初期化
            self.SCORE = None  # スコア初期化
            self.LOSE = None  # ロス初期化
            self.predict_data = None  # 予測値初期化
            self.predictMax = None  # 予測値最大値初期化
            self.merged = None  # Xデータを初期化
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ***************************************************************************************************
    #   基本処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   ビューを更新する
    # ---------------------------------------------------------------------------------------------------
    def updateView(self):
        try:
            QApplication.processEvents()  # プロセスイベントを呼んで制御をイベントループに返す
            size = self.size()  # 現在のサイズ
            self.resize(size.width(), size.height() + 1)  # サイズをセット
            self.resize(size.width(), size.height())  # サイズをセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   トレイン形式の予測値データを返す
    # ---------------------------------------------------------------------------------------------------
    def getPredict(self, MODEL, flatList, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            predict = MODEL.predict(np.array(flatList[:, X_BASE:],'float'))  # 予測値取得
            predict = np.concatenate([flatList[:, :X_BASE], predict], axis=1)  # トレイン形式の予測値データを作成
            return self.returnList(predict, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   ラベル値とデータのプロット
    # ---------------------------------------------------------------------------------------------------
    def plotData(self, axes, predict, plotRange, label, labelFlag, color, plotMode):
        try:
            X_BASE = GP.X_LIST.X_BASE  # Xベース転写
            drawLabel = self.getDescLabel(predict[0, GP.CONT.TRN.LASER_ID], label)  # 説明文付きのエラーラベルを取得
            if plotMode == GP.PLOT_MODE.PLOT:  # 予測値表示形式がPLOTの時
                if labelFlag:  # ラベル表示の時
                    axes.plot(plotRange, predict[:, X_BASE:], marker='.', label=drawLabel, color=color)  # ラベル有りでプロット
                else:  # ラベル非表示の時
                    axes.plot(plotRange, predict[:, X_BASE:], marker='.', color=color)  # ラベル無しでプロット
            elif plotMode == GP.PLOT_MODE.SCATTER:  # 予測値表示形式がSCATTERの時
                if labelFlag:  # ラベル表示の時
                    axes.scatter(plotRange, predict[:, X_BASE:], marker='.', label=drawLabel, color=color)  # ラベル有りでプロット
                else:  # ラベル非表示の時
                    axes.scatter(plotRange, predict[:, X_BASE:], marker='.', color=color)  # ラベル無しでプロット
            else:
                pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   タイトルを返す
    # ---------------------------------------------------------------------------------------------------
    def getTitle(self, PARTS, train):
        try:
            title = self.getMyTitle(train[0])
            #            title += " PARTS=" + str(PARTS.PARTS)                                                       # 学習タイプ追加
            #            title += " TYPE=" + str(PARTS.TYPE)                                                         # 学習タイプ追加
            #            title += " LEVEL=" + str(PARTS.LEVEL)                                                       # フィルターレベル追加
            title += " BEGIN=" + str(train[0, GP.CONT.TRN.LOG_DATE_TIME])  # 開始日時ル追加
            title += " END=" + str(train[-1, GP.CONT.TRN.LOG_DATE_TIME])  # 終了日時追加
            return title  # タイトルを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   サブプロットを初期設定
    # ---------------------------------------------------------------------------------------------------
    def initializeSubPlots(self, LASER_ID):
        try:
            if self.views == 1:  # 描画数が１の時
                self.viewCount = 0  # 描画画面カウントリセット
                self.axes = self.figure.subplots(nrows=self.views, ncols=1)  # 単一アキスを取得
                self.figure.subplots_adjust(wspace=0.3, hspace=0.6, left=0.05, right=0.85)  # ラベル表示位置調整
                return self.axes  # figとaxesを返す
            else:  # 描画数が２以上の時
                if self.viewCount % self.views == 0:  # 新しい画面にするか確認
                    self.viewCount = 0  # 描画画面カウントリセット
                    self.axes = self.figure.subplots(nrows=self.views, ncols=1)  # アキス配列を取得
                    self.figure.subplots_adjust(wspace=0.3, hspace=0.6, left=0.05, right=0.85)  # ラベル表示位置調整
                return self.axes[self.viewCount]  # axesを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   凡例だけをプロット
    # ---------------------------------------------------------------------------------------------------
    def plotLabel(self, axes, LASER_ID):
        try:
            OUT_LIST = GP.CONT.OUT_LIST  # 出力リスト転写
            Y_FLAG = self.yCheckWindow.flagList  # Yフラグ
            plotRange = range(1)  # プロットレンジ
            for i, label in enumerate(OUT_LIST.LIST):  # ラベルリストをすべて実行
                labelNo = OUT_LIST.NO_LIST[label]  # 表示用のラベル番号を取得
                if Y_FLAG[labelNo]:  # チェックされているか確認
                    color = OUT_LIST.COLOR_LIST[i]  # カラー取得
                    drawLabel = self.getDescLabel(LASER_ID, label)  # 説明文付きのエラーラベルを取得
                    axes.scatter(plotRange, [0], marker='.', label=drawLabel, color=color, s=40)  # ラベル有りでプロット
            axes.legend(fontsize=10, bbox_to_anchor=(1.0, 0.0), loc='lower left', markerscale=40)  # 配置

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #  発生日時から発生時相対ショット数計算
    # ---------------------------------------------------------------------------------------------------
    def getHappenShot(self, happenDate, train):
        try:
            TRN = GP.CONT.TRN  # TRNを転写
            endDate = train[train[:, TRN.LOG_DATE_TIME] <= happenDate]  # 開始日時
            if len(endDate) > 0:
                endShot = endDate[-1, TRN.REL_SHOT]  # 終了ショット
                return endShot  # 発生時相対ショット数を返す
            return None  # 発生時相対ショット数を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #  発生日時から発生時相対ショット数計算
    # ---------------------------------------------------------------------------------------------------
    def getHappenShot2(self, happenDate, train):
        try:
            TRN = GP.CONT.TRN  # TRNを転写
            beginDate = train[0, TRN.LOG_DATE_TIME]  # 開始日時
            endDate = train[-1, TRN.LOG_DATE_TIME]  # 終了日時
            beginShot = train[0, TRN.HAPPEN_SHOT]  # 開始ショット
            endShot = train[-1, TRN.HAPPEN_SHOT]  # 終了ショット
            span = (endShot - beginShot)  # 表示スパン
            relSec = (happenDate - beginDate).total_seconds()  # 相対時間
            spanSec = (endDate - beginDate).total_seconds()  # スパン時間
            happenShot = (span * relSec / spanSec)  # 発生時ショット数を比例配分で計算する
            return int(happenShot)  # 発生時相対ショット数を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   チャンバーステータス表示釦設定
    # ---------------------------------------------------------------------------------------------------
    def setChStatusButton(self, grid, row, col, LABEL, label):
        try:
            background = None  # バックグラウンドカラー　
            if label == LABEL.ACC:  # タイトルがCHの時
                title = "異常交換"  # タイトルを"異常交換"
                background = "red"  # バックグラウンドカラー　
            elif label == LABEL.REG:  # タイトルがREGの時
                title = "定期交換"  # タイトルを"定期交換"
                background = "blue"  # バックグラウンドカラー　
            elif label == LABEL.PDG:  # タイトルがPDGの時
                title = "稼働中"  # タイトルを"稼働中"
                background = "green"  # バックグラウンドカラー　
            color = "white"  # 文字カラー
            #            title = '{:.<8}'.format(title)
            if background is not None:  # バックグラウンドカラーが有る時
                method = 'CH_STATUS_' + str(row)  # 釦のメソッド名
                object = QPushButton(title)  # プッシュボタンを生成してオブジェクトにセット
                object.setFixedSize(GP.BAR_SIZE)  # プッシュボタンサイズ設定
                object.setStyleSheet("background:" + background + "; color:" + color + ";");  # オブジェクトのスタイルを設定する
                grid.addWidget(object, row, col)  # gridに生成したオブジェクトを追加
                exec("self.pushButton_" + method + " = object")  # メソッド名を付けたプッシュボタンにオブジェクトをセット
                return object  # 生成したオブジェクトを返す
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   LNテータス表示釦設定
    # ---------------------------------------------------------------------------------------------------
    def setLnStatusButton(self, grid, row, col, title):
        try:
            background = "black"  # バックグラウンドカラー　
            color = "white"  # 文字カラー
            #            title = '{:.<8}'.format(title)
            if background is not None:  # バックグラウンドカラーが有る時
                method = 'LN_STATUS_' + str(row)  # 釦のメソッド名
                object = QPushButton(title)  # プッシュボタンを生成してオブジェクトにセット
                object.setFixedSize(GP.BAR_SIZE)  # プッシュボタンサイズ設定
                object.setStyleSheet("background:" + background + "; color:" + color + ";");  # オブジェクトのスタイルを設定する
                grid.addWidget(object, row, col)  # gridに生成したオブジェクトを追加
                exec("self.pushButton_" + method + " = object")  # メソッド名を付けたプッシュボタンにオブジェクトをセット
                return object  # 生成したオブジェクトを返す
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   レーザー選択釦設定
    # ---------------------------------------------------------------------------------------------------
    def setLaserSelButton(self, grid, row, col, title):
        try:
            method = 'LASER_SEL'  # 釦のメソッド名
            objectName = method + '_' + str(row)  # 釦の名前
            #            background = "lightblue"                                                                   # バックグラウンドカラー　
            background = "lightblue"  # バックグラウンドカラー　
            color = "black"  # 文字カラー
            object = QPushButton(title)  # プッシュボタンを生成してオブジェクトにセット
            object.setFixedSize(GP.BAR_SIZE)  # プッシュボタンサイズ設定
            object.setStyleSheet("background:" + background + "; color:" + color + ";");  # オブジェクトのスタイルを設定する
            grid.addWidget(object, row, col)  # gridに生成したオブジェクトを追加
            pack = QObjectPackClass(object, method, 'bool', row)  # Qオブジェクトパックを生成
            self.pushButtonList.append(pack)  # プッシュボタンメソッドリストにオブジェクトパックをアペンド
            exec("self.pushButton_" + objectName + " = object")  # メソッド名を付けたプッシュボタンにオブジェクトをセット
            return object  # 生成したオブジェクトを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ページスライダーレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setPageSliderLayout(self, layout):
        try:
            slider = QSlider(Qt.Horizontal)
            layout.addWidget(slider)  # hLayoutに生成したオブジェクトを追加
            slider.setFocusPolicy(Qt.NoFocus)
            slider.setStyleSheet("background:gray; color:blue");  # オブジェクトのスタイルを設定する
            # スライダーが動くとchangeValue関数が呼び出される
            self.pageSliderLabel = self.setLabel(layout, '1頁')  # ラベルを生成
            slider.valueChanged.connect(self.pageValueChanged)  # コネクト
            slider.sliderReleased.connect(self.pageSliderReleased)  # コネクト
            self.pageSlider = slider

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   間引きスライダーレイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def setRedSliderLayout(self, layout):
        try:
            method = 'RED_SPAN'  # メソッド名
            slider = QSlider(Qt.Horizontal)
            layout.addWidget(slider)  # hLayoutに生成したオブジェクトを追加
            slider.setFocusPolicy(Qt.NoFocus)
            slider.setStyleSheet("background:gray; color:blue");  # オブジェクトのスタイルを設定する
            # スライダーが動くとchangeValue関数が呼び出される
            self.redSliderLabel = self.setLabel(layout, str(0))  # ラベルを生成
            slider.setRange(10, 500)  # スライダーレンジセット
            slider.setSingleStep(10)  # スライダーバリューセット
            slider.valueChanged.connect(self.redValueChanged)  # コネクト
            slider.sliderReleased.connect(self.redSliderReleased)  # コネクト
            self.redSlider = slider  # 間引きスラダーセット
            pack = QObjectPackClass(slider, method, 'int')  # Qオブジェクトパックを生成
            self.sliderList.append(pack)  # スライダーリストにオブジェクトパックをアペンド

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   保存
    # ---------------------------------------------------------------------------------------------------
    def Save(self, start_dir):
        try:
            configDialog = QFileDialog()
            filter_str = "*.png"
            fd = configDialog.getSaveFileName(self,
                                              "Save As...",
                                              start_dir, filter_str)
            pixmap = self.grab(QRect(QPoint(0, 0), QSize(-1, -1)))  # キャンバスを保存
            pixmap.save(fd[0])
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   学習名を返す
    # ---------------------------------------------------------------------------------------------------
    def getLearnName(self, LTYPE, TYPE, LEVEL):
        try:
            if LEVEL == 0:
                TABLE_NAME = LTYPE.LEARN_CONF.LTYPE0
            elif LEVEL == 1:
                TABLE_NAME = LTYPE.LEARN_CONF.LTYPE1
            elif LEVEL == 2:
                TABLE_NAME = LTYPE.LEARN_CONF.LTYPE2
            elif LEVEL == 3:
                TABLE_NAME = LTYPE.LEARN_CONF.LTYPE3
            elif LEVEL == 4:
                TABLE_NAME = LTYPE.LEARN_CONF.LTYPE4
            else:
                TABLE_NAME = LTYPE.LEARN_CONF.LTYPE5
            return TABLE_NAME

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   主部品のチェックボックスを隠す
    # ---------------------------------------------------------------------------------------------------
    def hideMainPartsCheckBox(self):
        try:
            PARTS_LIST = GP.MIXCONT.PARTS_LIST  # 部品コンテナリスト転写
            MAIN_PARTS = GP.MIXCONT.MAIN_PARTS  # 主部品を取得
            for PARTS in PARTS_LIST:  # 部品コンテナリストをすべて実行
                exec("self.checkBox = " + "self.checkBox_SHOW_" + PARTS.PARTS)  # チェックボックスを取得
                if PARTS == MAIN_PARTS:  # 主部品の時
                    self.checkBox.setChecked(True)  # チェック状態にする
                    self.checkBox.setVisible(False)  # 隠す
                else:  # 主部品でない時
                    self.checkBox.setVisible(True)  # 表示する隠す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

