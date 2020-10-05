import platform
import datetime
import numpy as np
import matplotlib.pyplot as plt
import inspect
import math
from PyQt5Import import *

# ---------------------------------------------------------------------------------------------------
#   グロバル変数
# ---------------------------------------------------------------------------------------------------
REDEEM = "redeem"


# ---------------------------------------------------------------------------------------------------
#   コンケート用の初期 NUMPY 配列を返す
# ---------------------------------------------------------------------------------------------------
def emptyList(fields):
    concatList = np.array([], dtype='O').reshape((0, fields))  # オブジェクトタイプの空NUMPY配列を作成
    return concatList  # コンケート用の初期 NUMPY 配列を返す


# ---------------------------------------------------------------------------------------------------
#   オブジェクトが存在するか否かを返す
# ---------------------------------------------------------------------------------------------------
def exist(object):
    if object is not None:
        return True
    else:
        return False


# ---------------------------------------------------------------------------------------------------
#   クラス名を返す
# ---------------------------------------------------------------------------------------------------
def getClassName(object):
    try:
        return object.__class__.__name__  # クラス名を返す

    except Exception as e:  # 例外
        printError(e)  # エラー表示
        return None  # Noneを返す


# ---------------------------------------------------------------------------------------------------
#   プログレスウインドウのstartNewLevelを呼ぶ
# ---------------------------------------------------------------------------------------------------
def startNewLevel(levels, p=None):
    if p is not None:
        curframe = inspect.currentframe()  # カレントのフレーム取得
        calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
        functionName = calframe[1][3]  # 呼び出し元の関数名
        text = functionName + " "  # テキストに関数名セット
        text += "しばらくお待ちください。"  # テキストにコメント追加
        p.startNewLevel(levels, text)  # プログレスウインドウのstartNewLevelを呼ぶ


# ---------------------------------------------------------------------------------------------------
#   プログレスウインドウのemitを呼ぶ
# ---------------------------------------------------------------------------------------------------
def emit(p, n=1):
    if p is not None:
        p.emit(n)


# ---------------------------------------------------------------------------------------------------
#   プログレスウインドウのendLevelを呼ぶ
# ---------------------------------------------------------------------------------------------------
def endLevel(p):
    if p is not None:
        p.endLevel()

# ---------------------------------------------------------------------------------------------------
#         エラー表示
# ---------------------------------------------------------------------------------------------------
def printError(e):
    curframe = inspect.currentframe()  # カレントのフレーム取得
    calframe = inspect.getouterframes(curframe, 4)  # 呼び出し元のフレーム取得
    title = calframe[1][3]  # 呼び出し元の関数名
    print("Exception", e.args)  # 例外を表示
    print(title + " Error")  # タイトルを表示
    return

# =======================================================================================================
#   クラス　trainデータとxデータとラベルをKERASの形式に変換したもののパッククラス
# =======================================================================================================
class LabelBaseClass():
    def __init__(self):  # 初期化
        pass

    # ---------------------------------------------------------------------------------------------------
    #   property
    # ---------------------------------------------------------------------------------------------------
    @property
    def length(self):  # データ長
        return len(self.LIST)  # ラベルリストの長さを返す

    # ---------------------------------------------------------------------------------------------------
    #   ラベルカラー取得
    # ---------------------------------------------------------------------------------------------------
    def getColor(self, label):
        try:
            if label in self.LIST:  # ラベルがリストに有る時
                no = self.NO_LIST[label]  # ラベル番号を取得
                color = self.COLOR_LIST[no]  # カラーを取得
                return color  # カラーを返す
            else:  # ラベルがラベルリストに無い時
                return '#000000'  # 黒色を返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

    # ---------------------------------------------------------------------------------------------------
    # ラベル番号リスト作成
    # ---------------------------------------------------------------------------------------------------
    def getLabelNoList(self):
        try:
            labelNoList = {}  # ラベル番号リスト初期化
            for i, LABEL in enumerate(self.LIST):  # LABEL_LISTを繰り返す
                labelNoList[LABEL] = i  # ラベル番号リストに通し番号をセット
            return labelNoList  # ラベル番号リストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

    # ---------------------------------------------------------------------------------------------------
    #   QT用ラベルカラーリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeQtColorList(self):
        try:
            colorList = []
            for i, color in enumerate(self.COLOR_LIST):  # COLOR_LISTを繰り返す
                color = [hex(math.floor(c * 255)) for c in color]
                color = [str(c)[2:].upper().zfill(2) for c in color]
                color = "#" + "".join(color)
                colorList.append(color)  # カラーリストに追加
            return colorList  # カラーリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

    # ---------------------------------------------------------------------------------------------------
    #   ラベルカラーリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeTab20ColorList(self):
        try:
            cmap = plt.get_cmap("tab20")  # tab20を選択
            colorList = list(cmap.colors)  # カラーリストを生成
            colorList = colorList + colorList + colorList + colorList + colorList + colorList  # カラーリストを生成
            n = len(self.LIST)  # 要素数
            colorList = colorList[0:n]  # カラーリストを生成
            return np.array(colorList)  # カラーリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

    # ---------------------------------------------------------------------------------------------------
    #   プレフィックスを付ける
    # ---------------------------------------------------------------------------------------------------
    def addPrefix(self, prefix, PEX_LIST):
        try:
            labelList = prefix + PEX_LIST  # オリジナル部品リストの頭に'R_'を付ける
            return labelList  # ラベルリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None


# =======================================================================================================
#   クラス　オリジナル交換部品ラベルクラス
# =======================================================================================================
class OrgPexLabelClass(LabelBaseClass):
    def __init__(self):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.LIST = self.makeLabelList()  # ラベルリスト設定
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定

    # ---------------------------------------------------------------------------------------------------
    #   ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self):
        try:
            labelList = []
            #            labelList.append('Auto')
            labelList.append('CH')
            labelList.append('CHG')
            labelList.append('ENERGY')
            labelList.append('HG')
            labelList.append('HV')
            labelList.append('INV')
            labelList.append('LN')
            labelList.append('MAIN')
            labelList.append('MM')
            labelList.append('PPM')
            #            labelList.append('UTILITY')
            labelList.append('WAVE')
            labelList.append('WINDOWS')

            labelList = np.array(labelList, 'O')
            return labelList

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None


# ---------------------------------------------------------------------------------------------------
#   SR_PARTS_EXCHANGE_TRNの部品名を変換する
# ---------------------------------------------------------------------------------------------------
class PartsNameClass():
    PARTS_NAME_MST = {}
    PARTS_NAME_MST["CH"] = "CH"
    PARTS_NAME_MST["CHG"] = "CHG"
    PARTS_NAME_MST["ENERGY CTRL."] = "ENERGY"
    PARTS_NAME_MST["FM"] = "FM"
    PARTS_NAME_MST["HG LAMP"] = "HG"
    PARTS_NAME_MST["HV CTRL."] = "HV"
    PARTS_NAME_MST["INV. CIRCUIT"] = "INV"
    PARTS_NAME_MST["Line Narrow Modu"] = "LN"
    PARTS_NAME_MST["LN"] = "LN"
    PARTS_NAME_MST["MAIN CTRL."] = "MAIN"
    PARTS_NAME_MST["MM"] = "MM"
    PARTS_NAME_MST["PPM"] = "PPM"
    #    PARTS_NAME_MST["UTILITY CTRL."] = "UTILITY"
    PARTS_NAME_MST["WAVE CTRL."] = "WAVE"
    PARTS_NAME_MST["WINDOW"] = "WINDOW"

    # ---------------------------------------------------------------------------------------------------
    #   有効部品名を取得
    # ---------------------------------------------------------------------------------------------------
    def getValidPartsName(self, name):
        try:
            if name in self.PARTS_NAME_MST:
                return self.PARTS_NAME_MST[name]
            return None

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   クラス　定期交換部品リスト設定
# =======================================================================================================
class RegPexLabelClass(LabelBaseClass):
    def __init__(self, ORG_PEX_LIST):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.LIST = self.addPrefix('R_', ORG_PEX_LIST.LIST)  # ラベルリスト設定
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定


# =======================================================================================================
#   クラス　異常交換部品ラベルクラス
# =======================================================================================================
class AbnPexLabelClas(LabelBaseClass):
    def __init__(self, ORG_PEX_LIST):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.LIST = self.addPrefix('A_', ORG_PEX_LIST.LIST)  # ラベルリスト設定
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定


# =======================================================================================================
#   クラス　使用中交換部品ラベルクラス
# =======================================================================================================
class PdgPexLabelClass(LabelBaseClass):
    def __init__(self, ORG_PEX_LIST):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.LIST = self.addPrefix('P_', ORG_PEX_LIST.LIST)  # ラベルリスト設定
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定


# =======================================================================================================
#   クラス　部品交換ラベルクラス
# =======================================================================================================
class PexLabelClass(LabelBaseClass):
    def __init__(self, REG_PEX_LIST, ABN_PEX_LIST, PDG_PEX_LIST):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.LIST = np.concatenate([REG_PEX_LIST.LIST, ABN_PEX_LIST.LIST, PDG_PEX_LIST.LIST])  # ラベルリスト設定
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定


# =======================================================================================================
#   クラス　エラーラベルクラス
# =======================================================================================================
class ErrorLabelClass(LabelBaseClass):
    def __init__(self):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.LIST = self.makeLabelList()  # ラベルリスト設定
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定

    # ---------------------------------------------------------------------------------------------------
    #   ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self):
        try:
            labelList = []
            labelList.append("E1441")  # 初期計測中にM/Mのファインラインセンサの応答がなかった。
            labelList.append("E1443")  # ファインラインセンサのフリーランバックグランド光量が規定値を越えた。
            labelList.append("E1453")  # コースバックグランドラインセンサバックグランドレベルの上限異常
            labelList.append("E1463")  # ファイン水銀光量の上限異常
            labelList.append("E1464")  # ファイン水銀光量の下限異常
            labelList.append("E1466")  # ファイン水銀光フリンジピーク検出不能
            labelList.append("E1467")  # ファイン水銀光フリンジピーク検出数が不正
            labelList.append("E1469")  # ファイン水銀光フリンジ定数が規定範囲外
            labelList.append("E1473")  # コース水銀光量の上限異常
            labelList.append("E1474")  # コース水銀光量の下限異常
            labelList.append("E1476")  # コース水銀光フリンジピーク検出不能
            labelList.append("E1481")  # ファインエキシマ光ラインセンサ異常
            labelList.append("E1483")  # ファインエキシマ光量の上限異常
            labelList.append("E1484")  # ファインエキシマ光量の下限異常
            labelList.append("E1486")  # ファインエキシマ光フリンジピーク検出不能
            labelList.append('E1488')  # ファインエキシマ光フリンジのしきい値境界検出不能
            labelList.append("E1491")  # コースエキシマ光ラインセンサ異常
            labelList.append("E1494")  # コースエキシマ光量の下限異常
            labelList.append("E1496")  # コースエキシマ光フリンジピーク検出不能
            labelList = np.array(labelList)
            return labelList

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None


# =======================================================================================================
#   クラス　エラーグループラベルクラス
# =======================================================================================================
class GrErrLabelClass(LabelBaseClass):
    def __init__(self):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.LIST = self.makeLabelList()  # ラベルリスト設定
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定
        self.GROUP_DIC = self.makeReplaceDic()  # グループ化用の書き換え辞書作成
        pass

    # ---------------------------------------------------------------------------------------------------
    #   エラーコードのグループ化用の書き換え辞書作成
    # ---------------------------------------------------------------------------------------------------
    def makeReplaceDic(self):
        try:
            replaceList = {}
            replaceList['E1441'] = 'E0001'  # 初期計測中にM/Mのファインラインセンサの応答がなかった。
            replaceList['E1443'] = 'E0001'  # ファインラインセンサのフリーランバックグランド光量が規定値を越えた。
            replaceList['E1453'] = 'E0011'  # コースバックグランドラインセンサバックグランドレベルの上限異常
            replaceList['E1463'] = 'E0001'  # ファイン水銀光量の上限異常
            replaceList['E1464'] = 'E0001'  # ファイン水銀光量の下限異常
            replaceList['E1466'] = 'E0001'  # ファイン水銀光フリンジピーク検出不能
            replaceList['E1467'] = 'E0001'  # ファイン水銀光フリンジピーク検出数が不正
            replaceList['E1469'] = 'E0001'  # ファイン水銀光フリンジ定数が規定範囲外
            replaceList['E1473'] = 'E0011'  # コース水銀光量の上限異常
            replaceList['E1474'] = 'E0011'  # コース水銀光量の下限異常
            replaceList['E1476'] = 'E0011'  # コース水銀光フリンジピーク検出不能
            replaceList['E1481'] = 'E0001'  # ファインエキシマ光ラインセンサ異常
            replaceList['E1483'] = 'E0001'  # ファインエキシマ光量の上限異常
            replaceList['E1484'] = 'E0001'  # ファインエキシマ光量の下限異常
            replaceList['E1486'] = 'E0001'  # ファインエキシマ光フリンジピーク検出不能
            replaceList['E1488'] = 'E0001'  # ファインエキシマ光フリンジのしきい値境界検出不能
            replaceList['E1491'] = 'E0011'  # コースエキシマ光ラインセンサ異常
            #        replaceList['E1493'] = 'E0011'                                                              # コースエキシマ光量の上限異常
            replaceList['E1494'] = 'E0011'  # コースエキシマ光量の下限異常
            replaceList['E1496'] = 'E0011'  # コースエキシマ光フリンジピーク検出不能
            return replaceList  # 書き換え辞書を返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

    # ---------------------------------------------------------------------------------------------------
    # ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self):
        try:
            labelList = []  # グループリスト初期化
            labelList.append('E0001')  # ファイン異常
            labelList.append('E0011')  # コース異常
            return labelList  # グループリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None


# =======================================================================================================
#   クラス　trainデータとxデータとラベルをKERASの形式に変換したもののパッククラス
# =======================================================================================================
class AllLabelClass(LabelBaseClass):
    def __init__(self, PEX_LIST, PDG_PEX_LIST, GR_ERR_LIST,
                 AGE_LIST):  # 初期化                                                                     # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.PEX_LIST = PEX_LIST  # 部品交換部品リスト
        self.PDG_PEX_LIST = PDG_PEX_LIST  # 使用中交換部品リスト
        self.GR_ERR_LIST = GR_ERR_LIST  # グループエラーリスト
        self.AGE_LIST = AGE_LIST  # 年齢学習リスト
        self.LIST = self.makeLabelList()  # ラベルリスト設定
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定

    # ---------------------------------------------------------------------------------------------------
    #   ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self):
        try:
            labelList = np.empty((0,))  # コンケート用の初期 NUMPY 配列を作成する
            labelList = np.concatenate([labelList, self.PEX_LIST.LIST])  # 部品交換部品リストアペンド
            labelList = np.concatenate([labelList, self.PDG_PEX_LIST.LIST])  # 使用中交換部品リストアペンド
            labelList = np.concatenate([labelList, self.GR_ERR_LIST.LIST])  # グループエラーリストアペンド
            labelList = np.concatenate([labelList, self.AGE_LIST.LIST])  # 年齢学習リストアペンド
            return labelList  # ラベルリスト

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None


# =======================================================================================================
#   クラス　イベントラベルクラス
# =======================================================================================================
class EvtLabelClass(LabelBaseClass):
    def __init__(self, PEX_LIST, GR_ERR_LIST):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.PEX_LIST = PEX_LIST  # 部品交換部品リスト
        self.GR_ERR_LIST = GR_ERR_LIST  # エラーリスト
        self.LIST = self.makeLabelList()  # ラベルリスト設定
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定

    # ---------------------------------------------------------------------------------------------------
    #   ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self):
        try:
            labelList = np.empty((0,))  # コンケート用の初期 NUMPY 配列を作成する
            labelList = np.concatenate([labelList, self.PEX_LIST.LIST])  # 部品交換部品リストアペンド
            labelList = np.concatenate([labelList, self.GR_ERR_LIST.LIST])  # エラーリストアペンド
            return labelList  # ラベルリスト

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None


# =======================================================================================================
#   クラス　グループイベントラベルクラス
# =======================================================================================================
class GrEvtLabelClass(LabelBaseClass):
    def __init__(self, PEX_LIST, GR_ERR_LIST):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.PEX_LIST = PEX_LIST  # 部品交換部品リスト
        self.GR_ERR_LIST = GR_ERR_LIST  # グループエラーリスト
        self.LIST = self.makeLabelList()  # ラベルリスト設定
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定

    # ---------------------------------------------------------------------------------------------------
    #   ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self):
        try:
            labelList = np.empty((0,))  # コンケート用の初期 NUMPY 配列を作成する
            labelList = np.concatenate([labelList, self.PEX_LIST.LIST])  # 部品交換部品リストアペンド
            labelList = np.concatenate([labelList, self.GR_ERR_LIST.LIST])  # グループエラーリストアペンド
            return labelList  # ラベルリスト

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None


# =======================================================================================================
#   クラス　年齢ラベルクラス
# =======================================================================================================
class AgeLabelClass(LabelBaseClass):
    def __init__(self, maxAge, step):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.maxAge = maxAge  # 最大値
        self.step = step  # ステップ
        self.LIST = self.makeLabelList()  # ラベルリスト設定
        self.LAST_AGE = int(self.LIST[-1])  # 最終年齢
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定

    # ---------------------------------------------------------------------------------------------------
    #   ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self):
        try:
            labelList = []  # 異常交換部品リストと定期交換部品リストをアペンド
            for i in range(0, self.maxAge, self.step):  # 0からmaxValueまで実行
                labelList += [str(i)]  # ストリング化し追加
            labelList = np.array(labelList)  # numpy配列化
            return labelList  # ラベルリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

    # ---------------------------------------------------------------------------------------------------
    #   ラベルカラーリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeColorList(self):
        try:
            colorList = []
            n = len(self.LIST)
            greenAge = str(int(40 / self.step) * self.step)
            green = self.NO_LIST[greenAge]
            yellowAge = str(int(70 / self.step) * self.step)
            yellow = self.NO_LIST[yellowAge]
            redAge = self.LIST[-1]
            red = self.NO_LIST[redAge]
            for i, LABEL in enumerate(self.LIST):  # LISTを繰り返す
                if i <= green:  # 40以下の時は緑色
                    r = (i / green) * 0.5
                    g = 1.0
                    b = (i / green) * 0.5
                elif i <= yellow:  # 70以下の時は黄色
                    r = 0.95
                    g = 0.95
                    b = ((yellow - i) / (yellow - green)) * 0.8
                elif i <= red:  # 100以下の時は赤色
                    r = 1.0
                    g = ((red - i) / (red - yellow)) * 0.9
                    b = ((red - i) / (red - yellow)) * 0.9
                else:
                    r = (n - 1 - i) / (n - red)  # 100超の時は濃赤色
                    g = 0.0
                    b = 0.0
                colorList.append([r, g, b])  # カラーリストに追加
            return colorList  # カラーリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None


# =======================================================================================================
#   クラス　LN年齢ラベルクラス
# =======================================================================================================
class LnmLabelClass(LabelBaseClass):
    def __init__(self, maxAge, step):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.maxAge = maxAge  # 最大値
        self.step = step  # ステップ
        self.LIST = self.makeLabelList()  # ラベルリスト設定
        self.LAST_LNM = int(self.LIST[-1])  # 最終年齢
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定

    # ---------------------------------------------------------------------------------------------------
    #   ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self):
        try:
            labelList = []  # 異常交換部品リストと定期交換部品リストをアペンド
            for i in range(0, self.maxAge, self.step):  # 0からmaxValueまで実行
                labelList += [str(i)]  # ストリング化し追加
            labelList = np.array(labelList)  # numpy配列化
            return labelList  # ラベルリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None

    # ---------------------------------------------------------------------------------------------------
    #   ラベルカラーリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeColorList(self):
        try:
            colorList = []
            n = len(self.LIST)
            greenAge = str(int(40 / self.step) * self.step)
            green = self.NO_LIST[greenAge]
            yellowAge = str(int(70 / self.step) * self.step)
            yellow = self.NO_LIST[yellowAge]
            redAge = str(int(100 / self.step) * self.step)
            red = self.NO_LIST[redAge]
            for i, LABEL in enumerate(self.LIST):  # LISTを繰り返す
                if i <= green:  # 40以下の時は緑色
                    r = (i / green) * 0.5
                    g = 1.0
                    b = (i / green) * 0.5
                elif i <= yellow:  # 70以下の時は黄色
                    r = 0.95
                    g = 0.95
                    b = ((yellow - i) / (yellow - green)) * 0.8
                elif i <= red:  # 100以下の時は赤色
                    r = 1.0
                    g = ((red - i) / (red - yellow)) * 0.9
                    b = ((red - i) / (red - yellow)) * 0.9
                else:
                    r = (n - 1 - i) / (n - red)  # 100超の時は濃赤色
                    g = 0.0
                    b = 0.0
                colorList.append([r, g, b])  # カラーリストに追加
            return colorList  # カラーリストを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None


# =======================================================================================================
#   クラス　trainデータとxデータとラベルをKERASの形式に変換したもののパッククラス
# =======================================================================================================
class X_LabelClass(LabelBaseClass):
    def __init__(self, UPLOADDIR):  # 初期化
        LabelBaseClass.__init__(self)  # スーパークラスの初期化
        self.UPLOADDIR = UPLOADDIR  # 保存ディレクトリ
        self.LIST = self.makeLabelList("WL_ERROR")  # TRAINデータ内のXデータ開始番号とリストをセット
        self.NO_LIST = self.getLabelNoList()  # 番号リスト設定
        self.COLOR_LIST = self.makeTab20ColorList()  # カラーリスト設定
        self.QT_COLOR_LIST = self.makeQtColorList()  # QT用カラーリスト設定

    # ---------------------------------------------------------------------------------------------------
    #   ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeLabelList(self, COLUMN_NAME):
        try:
            TABLE_NAME = "COMB_TRAIN"  # 取り出すDescription
            strPath = self.UPLOADDIR + REDEEM + "/combDesc.log"  # Description File Pass
            # データの読み込み
            with open(file=strPath, encoding="utf-8") as f:  # "utf-8"でファイルをオープン
                colName = []  # コラム名を初期化
                for strLine in f:  # ファイルをすべて行単位で読み込む
                    strLine = "".join(strLine.splitlines())  # 改行を削除
                    arrLine = strLine.split("\t")  # strLineをタブで区切りarrLineに格納
                    if arrLine[0] == TABLE_NAME:  # テーブル名と一致するとき
                        colName.append(arrLine[1])  # コラム名リストにアペンド
                colName = np.array(colName)  # コラム名をnumpy配列化
                index = np.where(colName == COLUMN_NAME)[0]  # ターゲットに対する相対ショット割合のインデックス取得
                self.X_BASE = None  # Xデータ開始番号を初期化
                if len(index) > 0:  # インデックスが有る時
                    self.X_BASE = index[0]  # Xデータ開始番号をセット
                    colName = colName[self.X_BASE:]  # Xデータを抽出
                    return np.array(colName)  # コラム名リストをnumpy配列にして返す
                return None  # Noneを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示


# -------------------------------------------------------------------------------------------------------
#   更新タブログクラス
# -------------------------------------------------------------------------------------------------------
class UpdateTabLogClass():
    directory = "updateTab/"  # ディレクトリ
    RDM = directory + "redeemUpdate.log"  # REDEEM更新タブ
    DATA_TRANS = directory + "dataTrans.log"  # データ移行タブ


# -------------------------------------------------------------------------------------------------------
#   設定タブログクラス
# -------------------------------------------------------------------------------------------------------
class ConfigTabLogClass():
    directory = "configTab/"  # ディレクトリ
    SERVER_SELECT = directory + "serverSelect.log"  # サーバー選択タブ
    FDR_RDM_SSH = directory + "founderRedeemSSH.log"  # 方正 REDEEM SSHサーバータブ
    FDR_RDM_DBS = directory + "founderRedeemDBS.log"  # 方正 REDEEM DBサーバータブ
    GPI_RDM_SSH_TEST = directory + "gpiRedeemSSHTest.log"  # GIGA REDEEM SSH 検証サーバータブ
    GPI_RDM_SSH = directory + "gpiRedeemSSH.log"  # GIGA REDEEM SSH 本番サーバータブ
    GPI_RDM_DBS = directory + "gpiRedeemDBS.log"  # GIGA REDEEM DBサーバータブ
    DMY_RDM_DBS = directory + "dummyRedeemDBS.log"  # DUMMY REDEEM DBサーバータブ
    LOC_RDM_DBS = directory + "localRedeemDBS.log"  # ローカル REDEEM DBサーバータブ


# -------------------------------------------------------------------------------------------------------
#   分析設定ビューログクラス
# -------------------------------------------------------------------------------------------------------
class AnalysisConfigViewLogClass():
    directory = "analysisConfigView/"  # ディレクトリ
    COMMON = directory + "common.log"  # 共通パラメータタブファイル名
    COMB = directory + "comb.log"  # 中間処理ビューファイル名
    PCOMB = directory + "pcomb.log"  # 部品中間処理ビューファイル名


# -------------------------------------------------------------------------------------------------------
#   学習ビューログクラス
# -------------------------------------------------------------------------------------------------------
class LearnViewLogClass():
    directory = "learnView/"  # ディレクトリ
    AGE_LEARN = directory + "ageLearn.log"  # 年齢学習
    EVT_LEARN = directory + "evtLearn.log"  # イベント学習
    Y_FLAG = directory + "Y_FLAG.log"  # Y_FLAG選択タブ


# -------------------------------------------------------------------------------------------------------
#   学習結果ビューログクラス
# -------------------------------------------------------------------------------------------------------
class LearnResultViewLogClass():
    directory = "learnView/"  # ディレクトリ
    AGE_RESULT = directory + "ageResult.log"  # 年齢学習結果
    EVT_RESULT = directory + "evtResult.log"  # イベント学習結果


# -------------------------------------------------------------------------------------------------------
#   メインウインドウログクラス
# -------------------------------------------------------------------------------------------------------
class MainWindowLogClass():
    directory = "mainView/"  # ディレクトリ
    MAIN = directory + "main.log"  # 共通パラメータタブファイル名
    AGE_TABLE_VIEW = directory + "ageTableView.log"  # AGEテーブルビューファイル名
    AGE_PREDICT_VIEW = directory + "agePredictView.log"  # AGEテーブルビューファイル名


# -------------------------------------------------------------------------------------------------------
#   ツリーパラメータログクラス
# -------------------------------------------------------------------------------------------------------
class TreeWidgetLogClass():
    directory = "treeWidget/"  # ディレクトリ
    RDM_UPDATE = directory + "rdmUpdate.log"  # REDEEMアップデートツリーファイル名
    COMMON = directory + "common.log"  # 共通ツリーファイル名
    ORIGIN = directory + "origin.log"  # オリジンツリーファイル名
    AGE_RESULT = directory + "ageResult.log"  # 年齢学習結果ツリーファイル名
    COMB = directory + "comb.log"  # COMBツリーファイル名
    AGE_LEARN = directory + "ageLearn.log"  # 年齢学習ツリーファイル名
    EVT_LEARN = directory + "evtLearn.log"  # イベント学習ツリーファイル名
    DATA_TRANS = directory + "dataTrans.log"  # データ移行ツリーファイル名


# -------------------------------------------------------------------------------------------------------
#   ビューテーブル名クラス
# -------------------------------------------------------------------------------------------------------
class ViewTableNameClass():
    UPDATE = "UPDATE_VIEW"  # 更新ビューテーブル名
    RDM_UPDATE = "RDM_UPDATE_VIEW"  # REDEEM更新ビューテーブル名
    DATA_TRANS = "DATA_TRANS_VIEW"  # DATA_TRANS更新ビューテーブル名
    COMMON = "COMMON_VIEW"  # 共通ビューテーブル名
    LOC_RDM_DBS = "LOC_RDM_DBS"  # ローカルREDEEM DBSサーバータブテーブル名
    DMY_RDM_DBS = "DMY_RDM_DBS"  # ダミーREDEEM DBSサーバータブテーブル名
    FDR_RDM_SSH = "FDR_RDM_SSH"  # 方正 REDEEM SSHサーバータブテーブル名
    FDR_RDM_DBS = "FDR_RDM_DBS"  # 方正 REDEEM DBSサーバータブテーブル名
    GPI_RDM_SSH = "GPI_RDM_SSH"  # GPI REDEEM SSHサーバータブテーブル名
    GPI_RDM_SSH_TEST = "GPI_RDM_SSH_TEST"  # GPI REDEEM DBS 検証サーバータブテーブル名
    GPI_RDM_DBS = "GPI_RDM_DBS"  # GPI REDEEM SSHサーバータブテーブル名
    ORIGIN = "ORIGIN_VIEW"  # オリジンビューテーブル名
    MAIN = "MAIN_VIEW"  # メインビューテーブル名
    COMB = "COMB_VIEW"  # COMBツリーテーブル名
    CH_AGE_LEARN = "CH_AGE_LEARN_VIEW"  # CH年齢学習ビューテーブル名
    LN_AGE_LEARN = "LN_AGE_LEARN_VIEW"  # LN年齢学習ビューテーブル名
    PPM_AGE_LEARN = "PPM_AGE_LEARN_VIEW"  # PPM年齢学習ビューテーブル名
    MM_AGE_LEARN = "MM_AGE_LEARN_VIEW"  # MM年齢学習ビューテーブル名
    CH_EVT_LEARN = "CH_EVT_LEARN_VIEW"  # CHイベント学習ビューテーブル名


# -------------------------------------------------------------------------------------------------------
#   データソースタイプクラス
# -------------------------------------------------------------------------------------------------------
class DataSourceTypeClass():
    def __init__(self):  # 初期化
        try:
            ORIGIN = "ORIGIN"  # ORIGINタイプ
            COMB = "COMB"  # COMBタイプ
            PCOMB = "PCOMB"  # PCOMBタイプ

            # オブジェクトのインスタンス変数のセットとテーブル名リスト作成
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#   ツリーノードクラス
# -------------------------------------------------------------------------------------------------------
class TreeNodeClass():
    ROOT = "root"  # ルート
    TREE_NODE = "treeNode"  # ツリーノード
    TYPE_CODE = "typeCode"  # タイプコード
    TYPE_ID = "typeId"  # レーザータイプID
    LASER_ID = "laserId"  # レーザーID
    PERIOD = "period"  # ピリオッド


# -------------------------------------------------------------------------------------------------------
#   学習単位クラス
# -------------------------------------------------------------------------------------------------------
class LearnUnitClass():
    TYPE_CODE = "typeCode"  # タイプコード
    TYPE_ID = "typeId"  # レーザータイプID
    LASER_ID = "laserId"  # レーザーID


# -------------------------------------------------------------------------------------------------------
#   ベースタイプクラス
# -------------------------------------------------------------------------------------------------------
class BaseTypeClass():
    F_BASE = 0  # フラットベース
    L_BASE = 1  # レーザー辞書
    P_BASE = 2  # ピリオッド辞書


# -------------------------------------------------------------------------------------------------------
#   学習タイプクラス
# -------------------------------------------------------------------------------------------------------
class LearnTypeClass():
    AGE = "AGE"  # 年齢
    EVT = "EVT"  # イベント


# -------------------------------------------------------------------------------------------------------
#   プロットモードクラス
# -------------------------------------------------------------------------------------------------------
class PlotModeClass():
    PLOT = "PLOT"  # 表示形式(折線)
    SCATTER = "SCATTER"  # 表示形式(散布図)


# -------------------------------------------------------------------------------------------------------
#   年齢基準クラス
# -------------------------------------------------------------------------------------------------------
class AgeBaseClass():
    MAX = "MAX"  # 最大値
    TARGET = "TARGET"  # ターゲット


# -------------------------------------------------------------------------------------------------------
#   サーバータイプクラス
# -------------------------------------------------------------------------------------------------------
class ServerTypeClass():
    DBS = "DBS"  # DBサーバータイプ
    SSH = "SSH"  # SSHサーバータイプ


# -------------------------------------------------------------------------------------------------------
#   訓練データクラス
# -------------------------------------------------------------------------------------------------------
class TrainTypeClass():
    MIN = 0  # MINタイプMIN
    MAX = 1  # MAXタイプ
    TRAIN = 2  # TRAINタイプ
    TEST = 3  # TESTタイプ
    MERGE = 4  # MERGEタイプ


# -------------------------------------------------------------------------------------------------------
#   ツリータイプクラス
# -------------------------------------------------------------------------------------------------------
class TreeTypeClass():
    MASTER = "MASTER"  # マスター
    SLAVE = "SLAVE"  # スレーブ


# -------------------------------------------------------------------------------------------------------
#   サーバー属性クラス
# -------------------------------------------------------------------------------------------------------
class ServerAttributeClass():
    def __init__(self):  # 初期化
        try:
            FDR_RDM_SSH = "FDR_RDM_SSH"  # 方正 REDEEM SSHサーバー
            FDR_RDM_DBS = "FDR_RDM_DBS"  # 方正 REDEEM DBサーバータブ
            GPI_RDM_SSH = "GPI_RDM_SSH"  # GIGA REDEEM SSH 本番サーバータブ
            GPI_RDM_SSH_TEST = "GPI_RDM_SSH_TEST"  # GIGA REDEEM SSH 検証サーバータブ
            GPI_RDM_DBS = "GPI_RDM_DBS"  # GIGA REDEEM DBサーバータブ
            DMY_RDM_DBS = "DMY_RDM_DBS"  # DUMMY REDEEM DBサーバータブ
            LOC_RDM_DBS = "LOC_RDM_DBS"  # ローカル REDEEM DBサーバータブ
            # オブジェクトのインスタンス変数のセット
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for name in self.nameList:  # サーバー名リストをすべて実行
                exec("self." + name + " = " + name)  # オブジェクトのインスタンス変数のセット

            # ベース辞書作成
            SERVER_TYPE = ServerTypeClass()  # サーバータイプクラス
            self.BASE = {}  # ベース辞書
            self.BASE[FDR_RDM_SSH] = [REDEEM, True, SERVER_TYPE.DBS, 20, 20]  # 方正 REDEEM SSHサーバー
            self.BASE[FDR_RDM_DBS] = [REDEEM, True, SERVER_TYPE.DBS, 20, 20]  # 方正 REDEEM DBサーバータブ
            self.BASE[GPI_RDM_SSH] = [REDEEM, False, SERVER_TYPE.SSH, 20, 20]  # GIGA REDEEM SSH 本番サーバータブ
            self.BASE[GPI_RDM_SSH_TEST] = [REDEEM, False, SERVER_TYPE.SSH, 20, 20]  # GIGA REDEEM SSH 検証サーバータブ
            self.BASE[GPI_RDM_DBS] = [REDEEM, False, SERVER_TYPE.DBS, 20, 20]  # GIGA REDEEM DBサーバータブ
            self.BASE[DMY_RDM_DBS] = [REDEEM, True, SERVER_TYPE.DBS, 20, 20]  # DUMMY REDEEM DBサーバータブ
            self.BASE[LOC_RDM_DBS] = [REDEEM, True, SERVER_TYPE.DBS, 20, 20]  # ローカル REDEEM DBサーバータブ

            # 辞書を作成
            self.DBSDIR = {}  # DBディレクトリ辞書初期化
            self.WRITE_ENABLE = {}  # 書き込み可否辞書初期化
            self.TYPE = {}  # サーバータイプ辞書初期化
            self.FILE_BLOCK = {}  # 一回に読み書きするファイルブロック長初期化
            self.LASER_BLOCK = {}  # レーザーブロック長（レーザーID数）初期化
            for name in self.nameList:  # サーバー名リストをすべて実行
                self.DBSDIR[name] = self.BASE[name][0]  # DBディレクトリを追加
                self.WRITE_ENABLE[name] = self.BASE[name][1]  # 書き込み可否を追加
                self.TYPE[name] = self.BASE[name][2]  # サーバータイプを追加
                self.FILE_BLOCK[name] = self.BASE[name][3]  # ファイルブロック長を追加
                self.LASER_BLOCK[name] = self.BASE[name][4]  # レーザーブロック長を追加
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   書き込みサーバー名リストを返す
    # ---------------------------------------------------------------------------------------------------
    def dstList(self):
        try:
            nameList = []  # サーバー名リスト初期化
            for name in self.nameList:  # サーバー名リストをすべて実行
                if (name == self.LOC_RDM_DBS or  # サーバー名がLOC_RDM_DBSの時
                        name == self.DMY_RDM_DBS or  # サーバー名がDMY_RDM_DBSの時
                        name == self.FDR_RDM_DBS or  # サーバー名がFDR_RDM_DBSの時
                        name == self.FDR_RDM_SSH):  # サーバー名がFDR_RDM_DBSの時
                    nameList += [name]  # サーバー名リストに加える
            return nameList

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   REDEEMサーバー名リストを返す
    # ---------------------------------------------------------------------------------------------------
    def redeemList(self):
        try:
            nameList = []  # サーバー名リスト初期化
            for name in self.nameList:  # サーバー名リストをすべて実行
                if name != self.LOC_RDM_DBS:  # サーバー名がローカルサーバーで無い時
                    if self.DBSDIR[name] == REDEEM:  # DBディレクトリがREDEEMの時
                        nameList += [name]  # サーバー名リストに加える
            return nameList

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#  スーパークラス　ベース設定クラス
# -------------------------------------------------------------------------------------------------------
class BaseConfClass():
    def __init__(self):  # 初期化
        try:
            self.BASE = {}  # ベース辞書
            self.tableNameList = []  # テーブル名リスト
            self.DBSDIR = {}  # ローカルDB名辞書初期化
            self.SOURCE = {}  # サブディレクトリ名辞書初期化
            self.DESC_NAME = {}  # テーブル定義名辞書初期化
            self.DESC_FILE_NAME = {}  # テーブル定義ファイル名辞書初期化
            self.DATE_FIELD = {}  # 日付フィールド辞書初期化
            self.FILE_BLOCK = {}  # ファイルブロック長初期化
            self.LASER_BLOCK = {}  # レーザーブロック長初期化

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   辞書を作成
    # ---------------------------------------------------------------------------------------------------
    def makeDictionalys(self):
        try:
            for name in self.tableNameList:  # テーブル名リストをすべて実行
                self.DBSDIR[name] = self.BASE[name][0]  # DBディレクトリ名を追加
                self.SOURCE[name] = self.BASE[name][1]  # サブディレクトリ名を追加
                self.DESC_NAME[name] = self.BASE[name][2]  # テーブル定義名を追加
                self.DESC_FILE_NAME[name] = self.BASE[name][3]  # テーブル定義ファイル名を追加
                self.DATE_FIELD[name] = self.BASE[name][4]  # 日付フィールドを追加
                self.FILE_BLOCK[name] = self.BASE[name][5]  # ファイルブロック長を追加
                self.LASER_BLOCK[name] = self.BASE[name][6]  # レーザーブロック長を追加
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#   ORIGINテーブル設定クラス
# -------------------------------------------------------------------------------------------------------
class OriginConfClass(BaseConfClass):
    def __init__(self):  # 初期化
        try:
            BaseConfClass.__init__(self)  # スーパークラス初期化
            LSM = "LASER_MST"  # LSM
            LTM = "LASER_TYPE_MST"  # LTM
            MDM = "MODULE_MST"  # MDM
            PRE = "PRD_ERROR"  # PRE
            RFLM = "REPLACEMENT_FORECAST_LASER_MST"  # RFLM
            RFM = "REPLACEMENT_FORECAST_MST"  # RFM
            ERR = "ERROR"  # ERR
            GSF = "GASFIL"  # GSF
            PLOT = "PLOT"  # PLOT
            WPLOT = "WPLOT"  # WPLOT
            SRM = "SR_MAIN"  # SRM
            SRPEX = "SR_PARTS_EXCHANGE_TRN"  # SRPEX

            # オブジェクトのインスタンス変数のセットとテーブル名リスト作成
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
                exec("self.tableNameList += [self." + objectName + "]")  # オブジェクトをテーブル名リストに追加

            # ベース辞書作成
            SOURCE = "ORIGIN"  # サブディレクトリ名
            DESC = "originDesc.log"  # テーブル定義ファイル名
            self.BASE[LSM] = [REDEEM, SOURCE, "LASER_MST", DESC, "INSTALL_DATE", 200, 200]  # LSM
            self.BASE[LTM] = [REDEEM, SOURCE, "LASER_TYPE_MST", DESC, "", 200, 200]  # LTM
            self.BASE[MDM] = [REDEEM, SOURCE, "MODULE_MST", DESC, "", 200, 200]  # MDM
            self.BASE[PRE] = [REDEEM, SOURCE, "PRD_ERROR", DESC, "", 200, 200]  # PRE
            self.BASE[RFLM] = [REDEEM, SOURCE, "REPLACEMENT_FORECAST_LASER_MST", DESC, "", 400, 200]  # RFLM
            self.BASE[RFM] = [REDEEM, SOURCE, "REPLACEMENT_FORECAST_MST", DESC, "", 400, 200]  # RFM
            self.BASE[ERR] = [REDEEM, SOURCE, "ERROR", DESC, "LOG_DATE_TIME", 100000, 100]  # ERR
            self.BASE[GSF] = [REDEEM, SOURCE, "GASFIL", DESC, "LOG_DATE_TIME", 10000, 200]  # GSF
            self.BASE[PLOT] = [REDEEM, SOURCE, "PLOT", DESC, "LOG_DATE_TIME", 100000, 50]  # PLOT
            self.BASE[WPLOT] = [REDEEM, SOURCE, "WPLOT", DESC, "LOG_DATE_TIME", 100000, 50]  # WPLOT
            self.BASE[SRM] = [REDEEM, SOURCE, "SR_MAIN", DESC, "END_WORK", 100000, 50]  # SRM
            self.BASE[SRPEX] = [REDEEM, SOURCE, "SR_PARTS_EXCHANGE_TRN", DESC, "INSTALLED_DATE", 100000, 50]  # SRPEX
            self.makeDictionalys()  # 辞書作成

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#   COMBテーブル設定クラス
# -------------------------------------------------------------------------------------------------------
class CombConfClass(BaseConfClass):
    def __init__(self):  # 初期化
        try:
            BaseConfClass.__init__(self)  # スーパークラス初期化
            PEX = "COMB_PARTS_EXCHANGE"  # PEX
            PWB = "COMB_PLOT_WPLOT"  # PWB
            ERM = "COMB_ERR_MST"  # ERM
            GFP = "COMB_GASFIL_PERIOD"  # GFP
            RPB = "COMB_RPL_BASE"  # RPB
            LST = "COMB_LASER_TYPE"  # LST
            TRN = "TRN"  # TRN

            # オブジェクトのインスタンス変数のセットとテーブル名リスト作成
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
                exec("self.tableNameList += [self." + objectName + "]")  # オブジェクトをテーブル名リストに追加

            # ベース辞書作成
            DBSDIR = REDEEM  # DBディレクトリ名
            SOURCE = "COMB"  # サブディレクトリ名
            DESC = "combDesc.log"  # テーブル定義ファイル名
            self.BASE[LST] = [DBSDIR, SOURCE, "COMB_LASER_TYPE", DESC, "", 200, 200]  # LST
            self.BASE[ERM] = [DBSDIR, SOURCE, "COMB_ERR_MST", DESC, "", 20000, 100]  # ERM
            self.BASE[RPB] = [DBSDIR, SOURCE, "COMB_RPL_BASE", DESC, "", 400, 100]  # RPB
            self.BASE[PWB] = [DBSDIR, SOURCE, "COMB_PLOT_WPLOT", DESC, "LOG_DATE_TIME", 100000, 10]  # PWB
            self.BASE[PEX] = [DBSDIR, SOURCE, "COMB_PARTS_EXCHANGE", DESC, "HAPPEN_DATE", 10000, 10]  # PEX
            self.BASE[GFP] = [DBSDIR, SOURCE, "COMB_GASFIL_PERIOD", DESC, "END_DATE_TIME", 10000, 200]  # GFP
            self.BASE[TRN] = [DBSDIR, SOURCE, "COMB_TRAIN", DESC, "", 200, 200]  # TRN
            self.makeDictionalys()  # 辞書作成

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#   TREEテーブル設定クラス
# -------------------------------------------------------------------------------------------------------
class TreeConfClass(BaseConfClass):
    def __init__(self):  # 初期化
        try:
            BaseConfClass.__init__(self)  # スーパークラス初期化
            LASER = "LASER_TREE"  # フィールド番号取得用レーザーツリー名
            RDMUD = "RDM_UPDATE_TREE"  # REDEEM更新ツリー名
            COMMON = "COMMON_TREE"  # 共通ツリー名
            ORIGIN = "ORIGIN_TREE"  # オリジンツリー名
            COMB = "COMB_TREE"  # COMBツリー名
            DATATR = "DATA_TRANS_TREE"  # データ移行寿命学習ツリー名
            PCOMB = "PCOMB_TREE"  # 部品COMBツリー名
            AGE_LEARN = "AGE_LEARN_TREE"  # 年齢学習ツリー名
            EVT_LEARN = "EVT_LEARN_TREE"  # イベント学習ツリー名
            AGE_RESULT = "AGE_RESULT_TREE"  # 年齢学習結果ツリー名

            # オブジェクトのインスタンス変数のセットとテーブル名リスト作成
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
                exec("self.tableNameList += [self." + objectName + "]")  # オブジェクトをテーブル名リストに追加

            # 辞書を作成
            DBSDIR = REDEEM  # DBディレクトリ名
            SOURCE = "TREE"  # サブディレクトリ名
            DESC_NAME = "LASER_TREE"  # テーブル名
            DESC = "combDesc.log"  # テーブル定義ファイル名
            DATE_FIELD = ""  # 日付フィールド名
            UPLOAD = 10000  # アップロードブロック長
            DOWNLOAD = 100  # ダウンロードブロック長
            self.BASE[LASER] = [DBSDIR, SOURCE, DESC_NAME, DESC, DATE_FIELD, UPLOAD, DOWNLOAD]  # LASER_TREE
            self.BASE[RDMUD] = [DBSDIR, None, DESC_NAME, DESC, DATE_FIELD, None, None]  # RDMUD_TREE
            self.BASE[COMMON] = [DBSDIR, None, DESC_NAME, DESC, DATE_FIELD, None, None]  # COMMON_TREE
            self.BASE[ORIGIN] = [DBSDIR, None, DESC_NAME, DESC, DATE_FIELD, None, None]  # ORIGIN_TREE
            self.BASE[COMB] = [DBSDIR, None, DESC_NAME, DESC, DATE_FIELD, None, None]  # COMB_TREE
            self.BASE[DATATR] = [DBSDIR, None, DESC_NAME, DESC, DATE_FIELD, None, None]  # DATATR_TREE
            self.BASE[PCOMB] = [DBSDIR, None, DESC_NAME, DESC, DATE_FIELD, None, None]  # PCOMB_TREE
            self.BASE[AGE_LEARN] = [DBSDIR, None, DESC_NAME, DESC, DATE_FIELD, None, None]  # 年齢学習ツリー
            self.BASE[EVT_LEARN] = [DBSDIR, None, DESC_NAME, DESC, DATE_FIELD, None, None]  # イベント学習ツリー
            self.BASE[AGE_RESULT] = [DBSDIR, None, DESC_NAME, DESC, DATE_FIELD, None, None]  # 年齢学習結果ツリー
            self.makeDictionalys()  # 辞書作成

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#   コンテナクラス
# -------------------------------------------------------------------------------------------------------
class ContainerClass():
    def __init__(self):  # 初期化
        try:
            self.ORIGIN_CONF = OriginConfClass()  # テーブル設定クラス
            self.COMB_CONF = CombConfClass()  # テーブル設定クラス
            self.TREE_CONF = TreeConfClass()  # テーブル設定クラス
            self.ORIGIN = None  # ORIGIN
            self.COMB = None  # COMB
            self.LTR = None  # LTR
            self.dataTransTab = None  # データ移行タブ

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   COMB設定
    # ---------------------------------------------------------------------------------------------------
    def setCOMB(self, ORIGIN, COMB):
        try:
            self.ORIGIN = ORIGIN  # OriginClassセット
            self.COMB = COMB  # ChCombClassセット
            for name in ORIGIN.nameList:  # テーブル名リストをすべて実行
                exec("GP.CONT." + name + " = ORIGIN." + name)  # テーブルの名前リストを転写
            for name in self.COMB.nameList:  # テーブル名リストをすべて実行
                exec("GP.CONT." + name + " = COMB." + name)  # テーブルの名前リストを転写

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return

    # ---------------------------------------------------------------------------------------------------
    #   出力ラベルリストをセット
    # ---------------------------------------------------------------------------------------------------
    def setLabelList(self, LEARN_TYPE):
        try:
            if LEARN_TYPE == GP.LEARN_TYPE.EVT:  # 学習タイプがGP.EVTの時
                self.LABEL_LIST = GP.EVT_LIST  # ラベルリストをセット
                self.OUT_LIST = GP.GR_EVT_LIST  # 出力ラベルリストをセット
                self.OUT_ERR_LIST = GP.GR_ERR_LIST  # 出力エラーラベルリストをセット
            elif LEARN_TYPE == GP.LEARN_TYPE.AGE:  # 学習タイプがGP.LEARN_TYPE.AGEの時
                self.LABEL_LIST = GP.AGE_LIST  # ラベルリストをセット
                self.OUT_LIST = GP.AGE_LIST  # 出力ラベルリストをセット
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# -------------------------------------------------------------------------------------------------------
#   ラベルクラス
# -------------------------------------------------------------------------------------------------------
class LabelClass():
    def __init__(self, parts):  # 初期化
        self.ORG = parts  # オリジナル部品名
        self.REG = 'R_' + parts  # 定期交換
        self.ACC = 'A_' + parts  # 異常交換
        self.PDG = 'P_' + parts  # 稼働中


# -------------------------------------------------------------------------------------------------------
#   部品ベーステーブル設定クラス
# -------------------------------------------------------------------------------------------------------
class PartsBaseConfClass(BaseConfClass):
    def __init__(self, parts):  # 初期化
        try:
            BaseConfClass.__init__(self)  # スーパークラス初期化
            PTB = parts + "_PARTS_BASE"  # PTB
            PRB = parts + "_PERIOD_BASE"  # PRB
            JBB = parts + "_JOB_BASE"  # JBB
            ERB = parts + "_ERR_BASE"  # ERB
            GSB = parts + "_GAS_BASE"  # GSB

            # オブジェクトのインスタンス変数のセットとテーブル名リスト作成
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != 'parts') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
                exec("self.tableNameList += [self." + objectName + "]")  # オブジェクトをテーブル名リストに追加

            # ベース辞書作成
            DBSDIR = REDEEM  # DBディレクトリ名
            SOURCE = "PCOMB"  # サブディレクトリ名
            DESC = "combDesc.log"  # テーブル定義ファイル名
            self.BASE[PTB] = [DBSDIR, SOURCE, "COMB_PARTS_BASE", DESC, "PERIOD_END_DATE_TIME", 1000, 20]  # PTB
            self.BASE[PRB] = [DBSDIR, SOURCE, "COMB_PERIOD_BASE", DESC, "HAPPEN_SHOT", 1000, 5]  # PRB
            self.BASE[JBB] = [DBSDIR, SOURCE, "COMB_JOB_BASE", DESC, "HAPPEN_SHOT", 1000, 20]  # JBB
            self.BASE[ERB] = [DBSDIR, SOURCE, "COMB_ERR_BASE", DESC, "HAPPEN_SHOT", 100000, 20]  # ERB
            self.BASE[GSB] = [DBSDIR, SOURCE, "COMB_GAS_BASE", DESC, "HAPPEN_SHOT", 10000, 20]  # GSB
            self.makeDictionalys()  # 辞書作成

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#   学習テーブル設定クラス
# -------------------------------------------------------------------------------------------------------
class LearnConfClass(BaseConfClass):
    def __init__(self, parts, learnType):  # 初期化
        try:
            BaseConfClass.__init__(self)  # スーパークラス初期化
            for i in range(6):
                exec("LTYPE" + str(i) + " = '" + parts + '_' + learnType + str(i) + "'")

            # オブジェクトのインスタンス変数のセットとテーブル名リスト作成
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != 'parts') and
                             (name != 'i') and
                             (name != 'learnType') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            self.tableNameList = []  # テーブル名リスト
            self.objectList = []  # オブジェクトリスト初期化
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
                exec("self.objectList += [self." + objectName + "]")  # オブジェクトリストに追加
                exec("self.tableNameList += [self." + objectName + "]")  # オブジェクトをテーブル名リストに追加

            # ベース辞書作成
            DBSDIR = REDEEM  # DBディレクトリ名
            DESC = "combDesc.log"  # テーブル定義ファイル名
            # SaveDataClass
            for object in self.objectList:
                self.BASE[object] = [DBSDIR, object, "COMB_TRAIN", DESC, "HAPPEN_SHOT", 10000, 20]  # LTYPE0
            self.makeDictionalys()  # 辞書作成

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#   学習コンテナクラス
# -------------------------------------------------------------------------------------------------------
class LearnContainerClass():
    def __init__(self, parts, learnType):  # 初期化
        try:
            self.LEARN_CLASS = None  # 学習クラス
            self.MODEL_COMB = None  # MODEL_COMB
            self.LEARN_CONF = LearnConfClass(parts, learnType)  # 学習テーブル設定クラス
            self.length = len(self.LEARN_CONF.nameList)  # モデルコンボ数
            self.MODEL_COMB_LIST = [None] * self.length  # MODEL_COMB_LIST
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   学習単位と学習単位名をセット
    # ---------------------------------------------------------------------------------------------------
    def setLearnUnit(self, LEARN_UNIT, UNIT_NAME):
        try:
            for i in range(self.length):
                self.MODEL_COMB_LIST[i].setLearnUnit(LEARN_UNIT, UNIT_NAME)  # 学習単位と学習単位名をセット

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   学習パラメーターを更新する
    # ---------------------------------------------------------------------------------------------------
    def setClassVar(self, laserIdList, parameter):
        try:
            self.LEARN_CLASS.setClassVar(laserIdList, parameter)  # 学習パラメーターを更新する

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す


# -------------------------------------------------------------------------------------------------------
#   部品クラス
# -------------------------------------------------------------------------------------------------------
class PartsClass():
    def __init__(self):  # 初期化
        try:
            CH = 'CH'  # チャンバー
            LN = "LN"  # LN
            PPM = 'PPM'  # PPM
            MM = "MM"  # MM
            MIX = "MIX"  # MIX
            # オブジェクトのインスタンス変数のセット
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#   部品コンテナクラス
# -------------------------------------------------------------------------------------------------------
class PContainerClass():
    def __init__(self):  # 初期化
        try:
            PARTS = PartsClass()  # 部品クラス
            CH = PartsContainerClass(PARTS.CH)  # CHコンテナクラス
            LN = PartsContainerClass(PARTS.LN)  # LNコンテナクラス
            PPM = PartsContainerClass(PARTS.PPM)  # PPMコンテナクラス
            MM = PartsContainerClass(PARTS.MM)  # MMコンテナクラス
            self.PCOMB = None  # PCombClass
            # オブジェクトのインスタンス変数のセット
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != 'PARTS') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            self.objectList = []  # オブジェクトリスト初期化
            self.objectDic = {}  # オブジェクトリスト初期化
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
                exec("self.objectList += [self." + objectName + "]")  # オブジェクトリストに追加
                exec("self.objectDic[self." + objectName + ".PARTS] = self." + objectName)  # オブジェクト辞書に追加
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   PCOMB設定
    # ---------------------------------------------------------------------------------------------------
    def setPCOMB(self, PCOMB):
        try:
            self.PCOMB = PCOMB  # ChCombClass取得
            self.CH.PCOMB = PCOMB.CH  # PCOMBにCHをセット
            for name in PCOMB.CH.nameList:  # テーブル名リストをすべて実行
                exec("self.CH." + name + " = PCOMB.CH." + name)  # テーブルの名前リストを転写
            self.LN.PCOMB = PCOMB.LN  # PCOMBにLNをセット
            for name in PCOMB.LN.nameList:  # テーブル名リストをすべて実行
                exec("self.LN." + name + " = PCOMB.LN." + name)  # テーブルの名前リストを転写
            self.PPM.PCOMB = PCOMB.PPM  # PCOMBにPPMをセット
            for name in PCOMB.PPM.nameList:  # テーブル名リストをすべて実行
                exec("self.PPM." + name + " = PCOMB.PPM." + name)  # テーブルの名前リストを転写
            self.MM.PCOMB = PCOMB.MM  # PCOMBにMMをセット
            for name in PCOMB.MM.nameList:  # テーブル名リストをすべて実行
                exec("self.MM." + name + " = PCOMB.MM." + name)  # テーブルの名前リストを転写
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return


# -------------------------------------------------------------------------------------------------------
#   学習部品コンテナクラス
# -------------------------------------------------------------------------------------------------------
class PartsContainerClass():
    def __init__(self, parts):  # 初期化
        try:
            self.PARTS = parts  # 学習部品クラス
            self.LABEL = LabelClass(parts)  # ラベルクラス
            self.PCOMB_CONF = PartsBaseConfClass(parts)  # テーブル設定クラス
            self.AGE = LearnContainerClass(parts, "AGE")  # AGEコンテナー
            self.EVT = LearnContainerClass(parts, "EVT")  # EVTコンテナー
            self.PCOMB = None  # PCOMB
            self.LEVEL = None  # レベルI
            self.TYPE = None  # 学習タイプ
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   タイプセット
    # ---------------------------------------------------------------------------------------------------
    def setTypes(self, TYPE):
        try:
            self.TYPE = TYPE  # 学習タイプセット

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   タイプセット
    # ---------------------------------------------------------------------------------------------------
    def getConfTable(self, TABLE_NAME):
        try:
            if TABLE_NAME in self.PCOMB_CONF.tableNameList:  # テーブル名がPCOMB_CONFに有る時
                TABLE = self.PCOMB_CONF  # TABLEをテーブルをセット
            elif TABLE_NAME in self.AGE.LEARN_CONF.tableNameList:  # テーブル名がAGE.LEARN_CONFに有る時
                TABLE = self.AGE.LEARN_CONF  # AGE.LEARN_CONFをテーブルをセット
            elif TABLE_NAME in self.EVT.LEARN_CONF.tableNameList:  # テーブル名がLEARN_CONFに有る時
                TABLE = self.EVT.LEARN_CONF  # EVT.LEARN_CONFをテーブルをセット
            else:
                TABLE = None  # Noneをテーブルにセット
            return TABLE

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す


# -------------------------------------------------------------------------------------------------------
#   混合学習部品コンテナクラス
# -------------------------------------------------------------------------------------------------------
class MixPartsContainerClass():
    def __init__(self, parts, partsList):  # 初期化
        try:
            self.PARTS = parts  # 学習部品クラス
            self.PARTS_LIST = partsList  # 学習部品クラスリスト
            self.MAIN_PARTS = None  # 主部品コンテナ
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   property
    # ---------------------------------------------------------------------------------------------------
    @property
    def LABEL(self):  # データ長
        return self.PARTS_LIST[0].LABEL  # ラベルリストの長さを返す

    # ---------------------------------------------------------------------------------------------------
    #   学習部品コンテナセット
    # ---------------------------------------------------------------------------------------------------
    def setPartsContainer(self, parts, partsList):
        try:
            self.PARTS = parts  # 学習部品クラス
            self.PARTS_LIST = partsList  # 学習部品コンテナリスト

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   PCOMB設定
    # ---------------------------------------------------------------------------------------------------
    def setPCOMB(self, PCOMB):
        try:
            self.PCOMB = PCOMB.CH  # PCOMBにCHをセット
            for name in PCOMB.CH.nameList:  # テーブル名リストをすべて実行
                exec("self." + name + " = PCOMB.CH." + name)  # テーブルの名前リストを転写
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            return


# -------------------------------------------------------------------------------------------------------
#   サーバーコンテナクラス
# -------------------------------------------------------------------------------------------------------
class ServerContainerClass():
    def __init__(self):  # 初期化
        try:
            self.FILEServer = None  # FILEサーバークラス
            self.DBSServer = None  # DBSサーバークラス
            self.SSHServer = None  # SSHサーバークラス
            self.parameter = {}  # サーバーパラメータ辞書初期化
            self.SOURCE_CLASS = {}  # ソースクラス辞書初期化
            pass

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass


# -------------------------------------------------------------------------------------------------------
#   グローバル変数
# -------------------------------------------------------------------------------------------------------
class GP():
    if platform.system() == "Windows":
        CRLF = "\r\n" # windows
        SEP_CRLF = "'\\r\\n'" # windows
        UPLOADDIR = "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Uploads6/"  # 保存ディレクトリ
    elif platform.system() == "Darwin":
        CRLF = "\n" # macOS
        SEP_CRLF = "'\\n'" # macOS
        UPLOADDIR = "/Users/wakai/Documents/Uploads/Uploads6/"  # 保存ディレクトリ
    else:
        CRLF = "\n" # unix
        SEP_CRLF = "'\\n'"  # unix
        UPLOADDIR = "/Users/wakai/Documents/Uploads/Uploads6/"  # 保存ディレクトリ
    ALL = "ALL"  # すべて選択
    MAX_SHOT = 99999999  # 最大ショット
    INVALID_SHOT = -1  # 無効ショット
    MIN_DATE = datetime.datetime(1980, 1, 1, 0, 0, 0)  # 最小日時
    MAX_DATE = datetime.datetime(2100, 1, 1, 0, 0, 0)  # 最大日時
    INVALID_DATE = datetime.datetime(2200, 1, 1, 0, 0, 0)  # 無効日時
    MAX_PRE_DATE = datetime.datetime(2099, 12, 31, 0, 0, 0)  # 最大日時前日
    MAX_AGE = 100  # CH年齢学習最大値
    MAX_LNM = 140  # LN年齢学習最大値
    AGE_STEP = 5  # 年齢学習ステップ
    LNM_STEP = 5  # 年齢学習ステップ
    TREE_VIEW_WIDTH = 350  # ツリービュー幅
    TREE_WIDTH = TREE_VIEW_WIDTH + 30  # ツリーウイジェット幅
    TREE_WIDGET_WIDTH = TREE_WIDTH  # 共通ツリービューメニュー幅
    AGE_SEL = 48  # 年齢選択釦最大幅
    MENU_WIDTH = TREE_WIDGET_WIDTH  # メニュー幅
    PRED_BUTTON_WIDTH = 120  # 予測ニュープッシュ釦幅
    BAR_SIZE = QSize(100, 24)
    FETCH_BLOCK = 10000  # DB読込ブロック長

    PARTS = PartsClass()  # 部品クラス
    CONT = ContainerClass()  # CONTコンテナクラス
    PCONT = PContainerClass()  # PCONTコンテナクラス
    MIXCONT = MixPartsContainerClass(PARTS.MIX, PCONT.objectList)  # MIXコンテナクラス

    SVR = ServerContainerClass()  # サーバーコンテナクラス
    DATA_SOURCE = DataSourceTypeClass()  # データソースクラス
    VIEW_TABLE_NAME = ViewTableNameClass()  # ビュー（タブ）テーブル名
    MAIN_LOG = MainWindowLogClass()  # 分析設定ビューログクラス
    UPDATE_LOG = UpdateTabLogClass()  # 更新ビューログクラス
    ANAL_LOG = AnalysisConfigViewLogClass()  # 分析設定ビューログクラス
    CONF_LOG = ConfigTabLogClass()  # 設定タブログクラス
    LEARN_LOG = LearnViewLogClass()  # 学習ビューログクラス
    RESULT_LOG = LearnResultViewLogClass()  # 学習結果ログクラス
    TREE_LOG = TreeWidgetLogClass()  # ツリーウイジェットログクラス
    NODE = TreeNodeClass()  # ツリーノードクラス
    BASE_TYPE = BaseTypeClass()  # ベースタイプクラス
    LEARN_TYPE = LearnTypeClass()  # 学習タイプクラス
    PLOT_MODE = PlotModeClass()  # プロットモードクラス
    AGE_BASE = AgeBaseClass()  # 年齢基準クラス
    SERVER = ServerAttributeClass()  # サーバー属性クラス
    SERVER_TYPE = ServerTypeClass()  # サーバータイプクラス
    ORG_PEX_LIST = OrgPexLabelClass()  # オリジナル部品リスト設定
    REG_PEX_LIST = RegPexLabelClass(ORG_PEX_LIST)  # 定期交換部品リスト設定
    ABN_PEX_LIST = AbnPexLabelClas(ORG_PEX_LIST)  # 異常交換部品リスト設定
    PDG_PEX_LIST = PdgPexLabelClass(ORG_PEX_LIST)  # 使用中交換部品リスト設定
    PEX_LIST = PexLabelClass(REG_PEX_LIST, ABN_PEX_LIST, PDG_PEX_LIST)  # 部品交換リスト設定
    ERR_LIST = ErrorLabelClass()  # エラーラベルリスト設定
    GR_ERR_LIST = GrErrLabelClass()  # エラーグループリスト設定
    AGE_LIST = AgeLabelClass(MAX_AGE, AGE_STEP)  # 年齢学習ラベルリスト設定
    LNM_LIST = LnmLabelClass(MAX_LNM, LNM_STEP)  # 年齢学習ラベルリスト設定
    EVT_LIST = EvtLabelClass(PEX_LIST, GR_ERR_LIST)  # イベントラベルリスト設定
    GR_EVT_LIST = GrEvtLabelClass(PEX_LIST, GR_ERR_LIST)  # グループマージラベルリスト設定
    X_LIST = X_LabelClass(UPLOADDIR)  # Xデータラベルリスト設定
    ALL_LIST = AllLabelClass(PEX_LIST, PDG_PEX_LIST, GR_ERR_LIST, AGE_LIST)  # 全ラベルリスト設定
    LEARN_UNIT = LearnUnitClass()  # 学習単位
    TRAIN_TYPE = TrainTypeClass()  # 訓練データタイプ
    TREE_TYPE = TreeTypeClass()  # ツリータイプ
    PARTS_NAME = PartsNameClass()

    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self):  # 初期化
        pass


