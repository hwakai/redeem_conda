from PyQt5Import import *
from staticImport import *
from analysisBase import AnalysisBaseClass
from qtBase import GridClass
from classDef import *


# =======================================================================================================
#   クラス ローカルサーバー設定ビュークラス
# =======================================================================================================
class LocConfigViewClass(AnalysisBaseClass):
    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, parent, title):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, parent.TABLE_NAME)  # スーパークラスの初期化
            self.parentObject = parent  # 親クラスセット
            self.title = title  # タブのタイトル
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト生成
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            self.tabs = QTabWidget()  # タブウィジェット生成
            self.tabs.resize(300, 180)  # タブサイズ設定
            # タブ生成
            self.locRdmDBSTab = DBS_ConfigTabClass(  # ローカルREDEEM DBSサーバータブ生成
                GP.VIEW_TABLE_NAME.LOC_RDM_DBS,  # テーブル名
                "LOC RDM DBS",  # タイトル
                GP.CONF_LOG.LOC_RDM_DBS,  # タブログファイル名
                LocRdmDBSParameterClass.getInstance())  # パラメータ
            self.locRdmDBSDmyTab = DBS_ConfigTabClass(  # DUMMY REDEEM DBSサーバータブ生成
                GP.VIEW_TABLE_NAME.DMY_RDM_DBS,  # テーブル名
                "DMY_RDM_DBS",  # タイトル
                GP.CONF_LOG.DMY_RDM_DBS,  # タブログファイル名
                DmyRdmDBSParameterClass.getInstance())  # パラメータ
            # タブリストにタブを登録
            self.tabList = []  # 空のタブリスト生成
            self.tabList.append(self.locRdmDBSTab)  # ローカルREDEEM DBサーバータブ追加
            self.tabList.append(self.locRdmDBSDmyTab)  # ローカルREDEEM DBサーバータブ追加
            # タブをタブリストに追加
            for tab in self.tabList:  # タブリストをすべて実行
                self.tabs.addTab(tab, tab.title)  # タブをタブリストに追加

            # Add tabs to widget
            main = QVBoxLayout()  # 垂直レイアウト生成
            self.setLabelStyle2(main, self.title, "gray", "white", 50, "25pt")  # 表題ラベル
            main.addWidget(self.tabs)  # 垂直レイアウトにタブウィジェットを追加
            return main  # レイアウトを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトとメソッドの結合を解除
    # ---------------------------------------------------------------------------------------------------
    def disconnectButtons(self):
        try:
            for tab in self.tabList:  # タブリストをすべて実行
                tab.disconnectButtons()  # タブのオブジェクトとメソッドを結合

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス 方正サーバー設定ビュークラス
# =======================================================================================================
class FdrConfigViewClass(AnalysisBaseClass):
    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, parent, title):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, parent.TABLE_NAME)  # スーパークラスの初期化
            self.parentObject = parent  # 親クラスセット
            self.title = title  # タブのタイトル
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト生成
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            self.tabs = QTabWidget()  # タブウィジェット生成
            self.tabs.resize(300, 180)  # タブサイズ設定
            # タブ生成
            self.fdrRdmSSHTab = SSH_ConfigTabClass(  # 方正 REDEEM SSHサーバータブ生成
                GP.VIEW_TABLE_NAME.FDR_RDM_SSH,  # テーブル名
                "方正 RDM SSH",  # タイトル
                GP.CONF_LOG.FDR_RDM_SSH,  # タブログファイル名
                FdrRdmSSHParameterClass.getInstance())  # パラメータ
            self.fdrRdmDBSTab = DBS_ConfigTabClass(  # 方正 REDEEM DBS サーバータブ生成
                GP.VIEW_TABLE_NAME.FDR_RDM_DBS,  # テーブル名
                "方正 RDM DBS",  # タイトル
                GP.CONF_LOG.GPI_RDM_DBS,  # タブログファイル名
                FdrRdmDBSParameterClass.getInstance())  # パラメータ
            # タブリストにタブを登録
            self.tabList = []  # 空のタブリスト生成
            self.tabList.append(self.fdrRdmSSHTab)  # 方正 REDEEM SSHサーバータブ追加
            self.tabList.append(self.fdrRdmDBSTab)  # 方正 REDEEM DBサーバータブ追加
            # タブをタブリストに追加
            for tab in self.tabList:  # タブリストをすべて実行
                self.tabs.addTab(tab, tab.title)  # タブをタブリストに追加

            # Add tabs to widget
            main = QVBoxLayout()  # 垂直レイアウト生成
            self.setLabelStyle2(main, self.title, "gray", "white", 50, "25pt")  # 表題ラベル
            main.addWidget(self.tabs)  # 垂直レイアウトにタブウィジェットを追加
            return main  # レイアウトを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトとメソッドの結合を解除
    # ---------------------------------------------------------------------------------------------------
    def disconnectButtons(self):
        try:
            for tab in self.tabList:  # タブリストをすべて実行
                tab.disconnectButtons()  # タブのオブジェクトとメソッドを結合

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   クラス GPIサーバー設定ビュークラス
# =======================================================================================================
class GpiConfigViewClass(AnalysisBaseClass):
    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, parent, title):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, parent.TABLE_NAME)  # スーパークラスの初期化
            self.parentObject = parent  # 親クラスセット
            self.title = title  # タブのタイトル
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト生成
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            self.tabs = QTabWidget()  # タブウィジェット生成
            self.tabs.resize(300, 180)  # タブサイズ設定
            # タブ生成
            self.gpiRdmSSHTab = SSH_ConfigTabClass(  # GIGA REDEEM SSH 本番サーバータブ生成
                GP.VIEW_TABLE_NAME.GPI_RDM_SSH,  # テーブル名
                "GIGA RDM SSH 本番",  # タイトル
                GP.CONF_LOG.GPI_RDM_SSH,  # タブログファイル名
                GpiRdmSSHParameterClass.getInstance())  # パラメータ
            self.gpiRdmSSHTestTab = SSH_ConfigTabClass(  # GIGA REDEEM SSH 検証サーバータブ生成
                GP.VIEW_TABLE_NAME.GPI_RDM_SSH_TEST,  # テーブル名
                "GIGA RDM SSH 検証",  # タイトル
                GP.CONF_LOG.GPI_RDM_SSH_TEST,  # タブログファイル名
                GpiRdmSSHTestParameterClass.getInstance())  # パラメータ
            self.gpiRdmDBSTab = DBS_ConfigTabClass(  # GIGA REDEEM DBS本番サーバータブ生成
                GP.VIEW_TABLE_NAME.GPI_RDM_DBS,  # テーブル名
                "GIGA RDM DBS 本番",  # タイトル
                GP.CONF_LOG.GPI_RDM_DBS,  # タブログファイル名
                GpiRdmDBSParameterClass.getInstance())  # パラメータ
            # タブリストにタブを登録
            self.tabList = []  # 空のタブリスト生成
            self.tabList.append(self.gpiRdmSSHTab)  # GIGA REDEEM 本番サーバータブ追加
            self.tabList.append(self.gpiRdmSSHTestTab)  # GIGA REDEEM 検証サーバータブ追加
            self.tabList.append(self.gpiRdmDBSTab)  # GIGA REDEEM DBサーバータブ追加
            # タブをタブリストに追加
            for tab in self.tabList:  # タブリストをすべて実行
                self.tabs.addTab(tab, tab.title)  # タブをタブリストに追加

            # Add tabs to widget
            main = QVBoxLayout()  # 垂直レイアウト生成
            self.setLabelStyle2(main, self.title, "gray", "white", 50, "25pt")  # 表題ラベル
            main.addWidget(self.tabs)  # 垂直レイアウトにタブウィジェットを追加
            return main  # レイアウトを返す

        except Exception as e:  # 例外
            printError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトとメソッドの結合を解除
    # ---------------------------------------------------------------------------------------------------
    def disconnectButtons(self):
        try:
            for tab in self.tabList:  # タブリストをすべて実行
                tab.disconnectButtons()  # タブのオブジェクトとメソッドを結合

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示


# =======================================================================================================
#   スーパークラス 設定タブ
# =======================================================================================================
class ConfigTabClass(AnalysisBaseClass):
    def __init__(self, TABLE_NAME, title, strPath, parameter):  # 初期化
        try:
            AnalysisBaseClass.__init__(self, None)  # スーパークラスの初期化
            self.title = title  # タブのタイトル
            self.strPath = strPath  # パラメータ保存パス
            self.parameter = parameter  # パラメータ
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.setSizePolicy(  # サイズポリシー設定
                QSizePolicy.Expanding,  # 幅可変
                QSizePolicy.Expanding)  # 高さ可変
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.connectButtons2()  # タブのオブジェクトとメソッドを結合

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass


# =======================================================================================================
#   クラス SSH設定タブクラス
# =======================================================================================================
class SSH_ConfigTabClass(ConfigTabClass):
    def __init__(self, TABLE_NAME, title, strPath, parameter):  # 初期化
        try:
            ConfigTabClass.__init__(self, TABLE_NAME, title, strPath, parameter)  # スーパークラスの初期化

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            mLayout = QVBoxLayout()  # メインレイアウト生成（垂直レイアウト）
            self.setLabelStyle(mLayout, self.title, "gray", "white", Qt.AlignCenter)  # 表題ラベル
            grid = GridClass(self, 10, 10)  # グリッドレイアウト生成
            mLayout.addLayout(grid)  # layoutにグリッドレイアウトを追加
            grid.addLineEdit(self, "str", "SSH_ADDRESS", "SSH アドレス")  # SSH アドレス
            grid.addLineEdit(self, "int", "SSH_PORT", "SSH ポート番号")  # SSH ポート
            grid.addLineEdit(self, "str", "SSH_USER", "SSH ユーザー")  # SSH ユーザー
            grid.addLineEdit(self, "str", "SSH_PASS", "SSH パスワード")  # SSH パスワード
            grid.addLineEdit(self, "str", "SSH_PKEY_PATH", "SSH PKEY_PATH")  # SSH PKEY_PATH
            grid.addLineEdit(self, "str", "MYSQL_HOST", "MYSQL ホスト名")  # MYSQL アドレス
            grid.addLineEdit(self, "int", "MYSQL_PORT", "MYSQL ポート番号")  # MYSQL ポート
            grid.addLineEdit(self, "str", "MYSQL_USER", "MYSQL ユーザー")  # MYSQL ユーザー
            grid.addLineEdit(self, "str", "MYSQL_PASS", "MYSQL パスワード")  # MYSQL パスワード
            grid.addLineEdit(self, "str", "MYSQL_DB", "MYSQL DB")  # MYSQL DB名
            grid.addLineEdit(self, "str", "LOCAL_ADDRESS", "MYSQL ローカルバインドアドレス")  # MYSQL LOCAL BIND アドレス
            grid.addLineEdit(self, "int", "LOCAL_PORT", "MYSQL ローカルバインドポート番号")  # MYSQL LOCAL BIND ポート
            mLayout.setAlignment(Qt.AlignTop)  # 上詰め
            return mLayout  # メインレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す


# =======================================================================================================
#   クラス DB設定タブクラス
# =======================================================================================================
class DBS_ConfigTabClass(ConfigTabClass):
    def __init__(self, TABLE_NAME, title, strPath, parameter):  # 初期化
        try:
            ConfigTabClass.__init__(self, TABLE_NAME, title, strPath, parameter)  # スーパークラスの初期化

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            mLayout = QVBoxLayout()  # メインレイアウト生成（垂直レイアウト）
            self.setLabelStyle(mLayout, self.title, "gray", "white", Qt.AlignCenter)  # 表題ラベル
            grid = GridClass(self, 10, 10)  # グリッドレイアウト生成
            grid.addLineEdit(self, "str", "MYSQL_HOST", "MYSQL ホスト名")  # MYSQL アドレス
            grid.addLineEdit(self, "int", "MYSQL_PORT", "MYSQL ポート番号")  # MYSQL ポート
            grid.addLineEdit(self, "str", "MYSQL_USER", "MYSQL ユーザー")  # MYSQL ユーザー
            grid.addLineEdit(self, "str", "MYSQL_PASS", "MYSQL パスワード")  # MYSQL パスワード
            grid.addLineEdit(self, "str", "MYSQL_DB", "MYSQL DB")  # MYSQL DB名
            mLayout.addLayout(grid)  # layoutにグリッドレイアウトを追加
            mLayout.setAlignment(Qt.AlignTop)  # 上詰め
            return mLayout  # メインレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す


