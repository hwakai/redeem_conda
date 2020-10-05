import numpy as np
from PyQt5Import import *
from static import *
from qtBase import QtBaseClass
from qtBase import ProgressWindowClass
from comb import CombClass
from commonBase import CommonBaseClass
from classDef import ParameterClass
from gpiBase import QueryClass
from gpiBase import GpiBaseClass


# =======================================================================================================
#   クラス　TreeClass
# =======================================================================================================
class TreeClass(GpiBaseClass):
    def __init__(self, TABLE_NAME):  # 初期化
        try:
            GpiBaseClass.__init__(self, TABLE_NAME)  # スーパークラスの初期化
            # オブジェクト生成
            DATA_TR = MasterTreeWidgetClass("データ移行ツリー", GP.CONT.TREE_CONF.DATATR)  # DATA_TRマスターツリーウイジェットの取得
            COMMON = MasterTreeWidgetClass("機種選択ツリー", GP.CONT.TREE_CONF.COMMON)  # COMMONマスターツリーウイジェットの取得
            PCOMB = MasterTreeWidgetClass("機種選択ツリー", GP.CONT.TREE_CONF.PCOMB)  # PCOMBツリーウイジェット
            RDM_UD = MasterTreeWidgetClass("REDEEM更新ツリー", GP.CONT.TREE_CONF.RDMUD)  # RDM_UDツリーウイジェット
            COMB = MasterTreeWidgetClass("機種選択ツリー", GP.CONT.TREE_CONF.COMB)  # COMBツリー ウイジェット生成
            AGE_LEARN = MasterTreeWidgetClass("機種選択ツリー", GP.CONT.TREE_CONF.AGE_LEARN)  # AGE_LEARNツリーウイジェット
            EVT_LEARN = MasterTreeWidgetClass("機種選択ツリー", GP.CONT.TREE_CONF.EVT_LEARN)  # CH_EVTツリーウイジェット
            AGE_RESULT = ResultTreeWidgetClass("機種選択ツリー", GP.CONT.TREE_CONF.AGE_RESULT, COMMON)  # AGE_RESULTツリーウイジェット
            # オブジェクトのインスタンス変数のセット
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != 'TABLE_NAME') and
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

            self.progress = ProgressWindowClass()  # 進捗ダイアローグ生成
            self.loadData(self.progress)  # 保存データをDBから読み込む
            pass

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   DBに保存
    # ---------------------------------------------------------------------------------------------------
    def saveData(self, p=None):
        try:
            self.startNewLevel(len(self.objectList) + 1, p)  # 新しいレベルの進捗開始
            self.flatBase = []
            for object in self.objectList:  # オブジェクト名リストをすべて実行
                if object.flatBase is not None and len(object.flatBase) > 0:  # オブジェクトのフラットベースが有る時
                    object.flatBase[:, self.TREE_NAME] = object.TABLE_NAME  # TREE_NAMEをセット
                    self.flatBase += list(object.flatBase)  # すべてコンケート
                emit(p)
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
            self.startNewLevel(len(self.objectList) + 2, p)  # 新しいレベルの進捗開始
            self.flatBase = GP.SVR.DBSServer.getLocFlatList(self, p)  # ファイルからフラットなリストをロード
            LST = GP.CONT.LST  # LSTを転写
            lstFlatBase = None  # LSTフラットベースを初期化
            if GP.SVR.DBSServer.existsLocTable(LST):  # LSTが有る時
                query = self.makeObjectQuery(LST)  # オブジェクトのフィールド名からセレクトクエリーを作成
                if self.flatBase is not None:  # フラットベースが有る時
                    for object in self.objectList:  # オブジェクト名リストをすべて実行
                        object.flatBase = self.flatBase[
                            self.flatBase[:, self.TREE_NAME] == object.TABLE_NAME]  # ベースリストから最小値を取得
                        if object.treeType == GP.TREE_TYPE.MASTER:  # ツリータイプがマスターの時
                            if len(object.flatBase) == 0:  # オブジェクトのフラットベースが無い時
                                if lstFlatBase is None:
                                    lstFlatBase = GP.SVR.DBSServer.makeLocFlatListFromQuery(LST, query,
                                                                                            p)  # LSTのフラットベースをすべて読み込む
                                object.makeBase(lstFlatBase, p)  # オブジェクトのベース作成
                            object.makeCheckTree()  # オブジェクトのベース作成
                        else:  # ツリータイプがスレーブの時
                            if len(object.flatBase) == 0:  # オブジェクトのフラットベースが無い時
                                object.makeBase(p)  # オブジェクトのベース作成
                            object.makeCheckTree()  # オブジェクトのベース作成
                else:  # フラットベースが無い時
                    for object in self.objectList:  # オブジェクト名リストをすべて実行
                        if object.treeType == GP.TREE_TYPE.MASTER:  # ツリータイプがマスターの時
                            if lstFlatBase is None:  # LSTフラットベースが無い時
                                lstFlatBase = GP.SVR.DBSServer.makeLocFlatListFromQuery(LST, query,
                                                                                        p)  # LSTのフラットベースをすべて読み込む
                            object.makeBase(lstFlatBase, p)  # オブジェクトのベース作成
                            object.makeCheckTree()  # オブジェクトのベース作成
                        else:  # ツリータイプがスレーブの時
                            object.makeBase(p)  # オブジェクトのベース作成
                            object.makeCheckTree()  # オブジェクトのベース作成
                self.deleteObject(lstFlatBase)  # オブジェクトを削除してメモリーを解放する
                self.saveData(p)  # 保存データをDBに書き込む
            self.endLevel(p)  # 現レベルの終了
            return

        except Exception as e:  # 例外
            self.showError(e, p)  # 例外を表示
            pass


# =======================================================================================================
#   クラス　ツリービュークラス
# =======================================================================================================
class TreeViewClass(QTreeView):
    # ---------------------------------------------------------------------------------------------------
    # 初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, parent):
        try:
            QTreeView.__init__(self, parent)  # スーパークラスの初期化
            self.parentObect = parent  # 親クラスを転写する
            self.model = QStandardItemModel(self)  # モデルを生成
            self.setModel(self.model)  # モデルをセット
            self.setFixedWidth(GP.TREE_VIEW_WIDTH)  # 固定幅にする
            self.resize(200, 400)
            self.setSizePolicy(  # サイズポリシー設定
                QSizePolicy.Expanding,  # 幅固定
                QSizePolicy.Expanding)  # 高さ拡張
            self.clicked.connect(self.itemClicked)  # クリックイベント接続
            pass

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ***************************************************************************************************
    #   イベント処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   アイテムクリックイベント処理
    # ---------------------------------------------------------------------------------------------------
    def itemClicked(self, index):
        try:
            QApplication.processEvents()  # プロセスイベントを呼んで制御をイベントループに返す
            item = self.model.itemFromIndex(index)  # インデックスからアイテムを取得
            checkState = item.checkState()  # チェックステート取得
            data = item.data(Qt.ToolTipRole)  # クリックされたアイテムのデータ
            data[self.parentObect.CHECK_STATE] = checkState  # チェックステートのセット
            item.setData(data, Qt.ToolTipRole)  # データの更新
            self.parentObect.treeSignal.emit(data)

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示
            pass


# =======================================================================================================
#   クラス ベースツリーウイジェットクラス
# =======================================================================================================
class BaseTreeWidgetClass(QtBaseClass):
    # ---------------------------------------------------------------------------------------------------
    #   クラス変数
    # ---------------------------------------------------------------------------------------------------
    treeSignal = pyqtSignal(type([]))  # ツリービュークリック時シグナル

    def __init__(self, title, TABLE_NAME):  # 初期化
        try:
            QtBaseClass.__init__(self, TABLE_NAME)  # スーパークラス初期化
            self.title = title  # タイトルセット
            self.slaveList = []  # スレーブーリスト初期化
            self.masterBase = None  # マスターベースを初期化
            self.flatBase = None  # フラットベースを初期化
            self.checkedBase = None  # チェック済ベースを初期化（フラットリスト）
            self.laserIdList = None  # レーザーIDリストを初期化（フラットリスト）
            self.trainPeriodBase = None  # トレインピリオッドベース辞書
            self.extractBase = None  # チェックされているPRBのリスト
            self.progress = ProgressWindowClass()  # プログレスクラス
            self.myTreeView = TreeViewClass(self)  # ツリービュー作成
            self.model = self.myTreeView.model  # モデル転写
            self.treeSignal.connect(self.treeItemClicked)  # ツリービュークリック時処理
            self.setFixedWidth(GP.TREE_WIDTH)  # 固定幅にする
            self.setSizePolicy(  # サイズポリシー設定
                QSizePolicy.Fixed,  # 幅固定
                QSizePolicy.Expanding)  # 高さ拡張
            self.setFixedWidth(GP.TREE_WIDGET_WIDTH)  # 固定サイズに設定
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   オブジェクトとメソッドを結合
    # ---------------------------------------------------------------------------------------------------
    def connectTreeButtons(self, saveMethod):
        try:
            # パラメータ保存メソッドと結合
            for pack in self.comboBoxList:  # コンボボックスリストをすべて実行
                pack.qObject.currentTextChanged.connect(self.saveParam)  # コンボボックスをパラメータ保存メソッドと結合
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                pack.qObject.clicked.connect(self.saveParam)  # チェックボックスをパラメータ保存メソッドと結合
            for pack in self.lineEditList:  # ラインエディットリストをすべて実行
                pack.qObject.textEdited.connect(self.saveParam)  # ラインエディットをパラメータ保存メソッドと結合
            # 関数呼び出しメソッドと結合
            for pack in self.checkBoxList:  # チェックボックスリストをすべて実行
                exec("pack.qObject.clicked.connect(self." + pack.method + "_EVENT)")  # プッシュボタンを関数呼び出しメソッドと結合
            for pack in self.pushButtonList:  # プッシュボタンリストをすべて実行
                exec("pack.qObject.clicked.connect(self." + pack.method + ")")  # プッシュボタンを関数呼び出しメソッドと結合
            self.connected = True  # コネクト済にする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ツリーテーブルからフラットなリストを読み込む
    # ---------------------------------------------------------------------------------------------------
    def loadTreeBase(self, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            query = self.makeObjectQuery(self)  # オブジェクトのフィールド名からセレクトクエリーを作成
            query.add("ORDER BY BASE.TYPE_CODE,BASE.TYPE_ID,BASE.LASER_ID")  # クエリ作成
            self.flatBase = GP.SVR.DBSServer.getLocFlatListFromQuery(self, query, p)  # すべてのレーザーを読み込みフラットベースをセット
            return self.returnList(self.flatBase, p)  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   子のチェックステートを与えられたチェックステートにセット(再帰メソッド)
    # ---------------------------------------------------------------------------------------------------
    def setChildCheckState(self, flatList, node, checkState):
        try:
            self.setCheckState(flatList, node, checkState)  # 自ノードのチェックステートセット
            children = self.getChildren(flatList, node)  # 子リスト取得
            for child in children:  # 子リストをすべて実行
                self.setChildCheckState(flatList, child, checkState)  # 孫ノードのチェックステートセット
            pass
        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   指定したノードのトリステートを設定してチェックステートを返す(再帰メソッド)
    # ---------------------------------------------------------------------------------------------------
    def setNodeTriState(self, flatList, node, endNode):
        try:
            if node[self.TREE_NODE] == endNode[self.TREE_NODE]:
                return node[self.CHECK_STATE]
            else:
                children = self.getChildren(flatList, node)  # 子リスト取得
                length = len(children)  # 子供の数
                if length == 0:  # 子供の数が0の時
                    checkState = node[self.CHECK_STATE]  # チェックステートを自分のステートにセット
                else:  # 子供が有る時
                    checkedNr = 0  # チェックされている数
                    partialNr = 0  # 部分チェックされている数
                    for child in children:  # 子リストをすべて実行
                        childState = self.setNodeTriState(flatList, child, endNode)  # 子ノードのトリステートを設定
                        if childState == Qt.Checked:  # 子ノードのステートがチェックの時
                            checkedNr += 1  # チェック数を加算
                        elif childState == Qt.PartiallyChecked:  # パーシャルの時
                            partialNr += 1  # パーシャル数を加算
                    if checkedNr + partialNr == 0:  # チェック数が0の時
                        checkState = Qt.Unchecked  # チェックステートをアンチェックにする
                    elif checkedNr == length:  # 全部チェックの時
                        checkState = Qt.Checked  # チェックステートををアンチェックにする
                    else:  # 一部チェックの時
                        checkState = Qt.PartiallyChecked  # チェックステートをパーシャルにする
                    self.setCheckState(flatList, node, checkState)  # ノードのチェックステートをセット
                return checkState  # ノードのチェックステートを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   指定したノードのトリステートを設定する
    # ---------------------------------------------------------------------------------------------------
    def setNodeTriStateOne(self, node):
        try:
            flatList = self.flatBase
            children = self.getChildren(flatList, node)  # 子リスト取得
            length = len(children)  # 子供の数
            if length == 0:  # 子供の数が0の時
                checkState = Qt.Unchecked  # チェックステートアンチェックドにセット
            else:  # 子供が有る時
                checkedNr = 0  # チェックされている数
                partialNr = 0  # 部分チェックされている数
                for child in children:  # 子リストをすべて実行
                    childState = child[self.CHECK_STATE]  # 子ノードのチェックステートを取得
                    if childState == Qt.Checked:  # 子ノードのチェックステートがチェックの時
                        checkedNr += 1  # チェック数を加算
                    elif childState == Qt.PartiallyChecked:  # パーシャルの時
                        partialNr += 1  # パーシャル数を加算
                if checkedNr + partialNr == 0:  # チェック数が0の時
                    checkState = Qt.Unchecked  # チェックステートをアンチェックにする
                elif checkedNr == length:  # 全部チェックの時
                    checkState = Qt.Checked  # チェックステートををアンチェックにする
                else:  # 一部チェックの時
                    checkState = Qt.PartiallyChecked  # チェックステートをパーシャルにする
                self.setCheckState(flatList, node, checkState)  # ノードのチェックステートをセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ノードのフィールド番号を返す
    # ---------------------------------------------------------------------------------------------------
    def getFieldNo(self, node):
        try:
            if node[self.TREE_NODE] == GP.NODE.ROOT:  # ツリーノードがルートの時
                fieldNo = self.TREE_NODE  # ツリーノードのフィールド番号をセット
            elif node[self.TREE_NODE] == GP.NODE.TYPE_CODE:  # ツリーノードがタイプコードの時
                fieldNo = self.TYPE_CODE  # タイプコードのフィールド番号をセット
            elif node[self.TREE_NODE] == GP.NODE.TYPE_ID:  # ツリーノードがタイプIDの時
                fieldNo = self.TYPE_ID  # タイプIDのフィールド番号をセット
            elif node[self.TREE_NODE] == GP.NODE.LASER_ID:  # ツリーノードがレーザーIDの時
                fieldNo = self.LASER_ID  # レーザーIDのフィールド番号をセット
            elif node[self.TREE_NODE] == GP.NODE.PERIOD:  # ツリーノードがピリオッドの時
                fieldNo = self.PERIOD  # ピリオッドのフィールド番号をセット
            return fieldNo  # フィールド番号を返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ツリーノードの名前を返す
    # ---------------------------------------------------------------------------------------------------
    def getNodeName(self, node):
        try:
            if node[self.TREE_NODE] == GP.NODE.ROOT:  # ツリーノードがルートの時
                name = GP.NODE.ROOT  # GPのルート名を取得
            elif node[self.TREE_NODE] == GP.NODE.TYPE_CODE:  # ツリーノードがタイプコードの時
                name = node[self.TYPE_CODE]  # タイプコード名を取得
            elif node[self.TREE_NODE] == GP.NODE.TYPE_ID:  # ツリーノードがタイプIDの時
                name = node[self.TYPE_ID]  # タイプID名を取得
            elif node[self.TREE_NODE] == GP.NODE.LASER_ID:  # ツリーノードがレーザーIDの時
                name = str(node[self.LASER_ID])  # レーザーID番号を取得
            elif node[self.TREE_NODE] == GP.NODE.PERIOD:  # ツリーノードがピリオッドの時
                name = str(node[self.LASER_ID]) + "-" + str(node[self.PERIOD])  # レーザーID番号とピリオッド番号を結合
            return name  # 名前を返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   子アイテムをモデルにセット(回帰)
    # ---------------------------------------------------------------------------------------------------
    def setNodeChildItemToModel(self, item, node):
        try:
            data0 = item.data(Qt.ToolTipRole)  # データ取得
            data = self.getItemData(data0)  # チェックステートを取得
            draw = False
            if data[self.TREE_NODE] == GP.NODE.ROOT:
                draw = True
            elif data[self.TREE_NODE] == GP.NODE.TYPE_CODE:
                if data[self.TYPE_CODE] == node[self.TYPE_CODE] or node[self.TYPE_CODE] == '':
                    draw = True
            elif data[self.TREE_NODE] == GP.NODE.TYPE_ID:
                if (data[self.TYPE_ID] == node[self.TYPE_ID]) or node[self.TYPE_ID] == '':
                    draw = True
            elif data[self.TREE_NODE] == GP.NODE.LASER_ID:
                if (data[self.LASER_ID] == node[self.LASER_ID] or node[self.LASER_ID] == 0):
                    draw = True
            elif data[self.TREE_NODE] == GP.NODE.PERIOD:
                if (data[self.PERIOD] == node[self.PERIOD] or node[self.PERIOD] == 0):
                    draw = True
            if draw:
                item.setData(data)  # 子アイテムにデータをセット
                if data[self.CHECKABLE] == 1:  # チェック可の時
                    item.setCheckable(True)  # チェック可能にする
                    item.setCheckState(data[self.CHECK_STATE])  # チェックステートをセットする
                else:  # チェック不可の時
                    item.setCheckable(False)  # チェック不可にする
                for i in range(item.rowCount()):  # ツリーモデルをすべて実行
                    childItem = item.child(i, 0)  # タイプコードアイテム取得
                    self.setNodeChildItemToModel(childItem, node)  # 子アイテムをモデルにセット
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   フラットベースをモデルにセット
    # ---------------------------------------------------------------------------------------------------
    def setFlatBaseToModel(self):
        try:
            if self.flatBase is not None:  # フラットベースが有る時
                rootItem = self.model.item(0, 0)  # タイプコードアイテム取得
                rootData = rootItem.data(Qt.ToolTipRole)  # データ取得
                rootData = self.getItemData(rootData)  # フラットベースのアイテムを取得
                if rootData is not None:  # フラットベースのアイテムが有る時
                    rootItem.setCheckState(rootData[self.CHECK_STATE])  # アイテムにチェックステートをセット
                    rootItem.setData(list(rootData), Qt.ToolTipRole)  # データセット
                    self.setChildItemToModel(rootItem)
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   子アイテムをモデルにセット(回帰)
    # ---------------------------------------------------------------------------------------------------
    def setChildItemToModel(self, item):
        try:
            for i in range(item.rowCount()):  # ツリーモデルをすべて実行
                childItem = item.child(i, 0)  # タイプコードアイテム取得
                childData = childItem.data(Qt.ToolTipRole)  # データ取得
                childData = self.getItemData(childData)  # チェックステートを取得
                childItem.setData(childData)  # 子アイテムにデータをセット
                if childData[self.CHECKABLE] == 1:  # チェック可の時
                    childItem.setCheckable(True)  # チェック可能にする
                    childItem.setCheckState(childData[self.CHECK_STATE])  # チェックステートをセットする
                else:  # チェック不可の時
                    childItem.setCheckable(False)  # チェック不可にする
                self.setChildItemToModel(childItem)  # 子アイテムをモデルにセット
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # エラー表示
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   アイテムのデータをセット
    # ---------------------------------------------------------------------------------------------------
    def setData(self, node):
        try:
            node = np.array(node, 'O')  # numpy配列化
            if self.flatBase is not None:
                index = np.where(
                    (self.flatBase[:, :self.CHECK_STATE] == node[:self.CHECK_STATE]).all(axis=1))  # チェックステートの前までの比較
                if len(index) > 0:  # インデックスが有る時
                    self.flatBase[index] = node  # データをセット

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   指定したノードのチェックステートセット
    # ---------------------------------------------------------------------------------------------------
    def setCheckState(self, flatList, node, checkState):
        try:
            node = np.array(node, 'O')  # numpy配列化
            index = np.where((flatList[:, 1:self.CHECK_STATE] == node[1:self.CHECK_STATE]).all(axis=1))[
                0]  # ツリーノードのインデックス取得 (axis=1)を忘れないように！
            if len(index) > 0:  # インデックスが有る時
                flatList[index, self.CHECK_STATE] = checkState  # 親のチェックステートをセット

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   子供のリストを取得する
    # ---------------------------------------------------------------------------------------------------
    def getChildren(self, srcList, node):
        try:
            node = np.array(node, 'O')  # numpy配列化
            children = []  # 子供のリストを初期化
            treeNode = node[self.TREE_NODE]  # ツリーノード
            if treeNode == GP.NODE.ROOT:  # ツリーノードがルートの時
                children = srcList[(srcList[:, self.TREE_NODE] == GP.NODE.TYPE_CODE)]  # ツリーノードがTYPE_CODEのリストを取得
            elif treeNode == GP.NODE.TYPE_CODE:  # ツリーノードがタイプコードの時
                children = srcList[(srcList[:, self.TREE_NODE] == GP.NODE.TYPE_ID) &  # ツリーノードがTYPE_IDかつ
                                   (srcList[:, self.TYPE_CODE] == node[self.TYPE_CODE])]  # タイプコードまでが一致するリストを取得
            elif treeNode == GP.NODE.TYPE_ID:  # ツリーノードがタイプIDの時
                children = srcList[(srcList[:, self.TREE_NODE] == GP.NODE.LASER_ID) &  # ツリーノードがLASER_IDかつ
                                   (srcList[:, 2:self.TYPE_ID + 1] == node[2:self.TYPE_ID + 1]).all(
                                       axis=1)]  # タイプIDまでが一致するリストを取得
            elif treeNode == GP.NODE.LASER_ID:  # ツリーノードがタイプIDの時
                children = srcList[(srcList[:, self.TREE_NODE] == GP.NODE.PERIOD) &  # ツリーノードがPERIODかつ
                                   (srcList[:, 2:self.LASER_ID + 1] == node[2:self.LASER_ID + 1]).all(
                                       axis=1)]  # レーザーIDまでが一致するリストを取得
            else:  # ツリーノードがピリオッドの時
                pass  # 子供のリストは空
            return children  # 子供のリストを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # エラー表示

    # ---------------------------------------------------------------------------------------------------
    #   指定したタイプコードのデータを取得
    # ---------------------------------------------------------------------------------------------------
    def getItemData(self, node):
        try:
            node = np.array(node, 'O')  # numpy配列化
            if self.flatBase is not None:  # フラットベースが有る時
                item = self.flatBase[(self.flatBase[:, self.TREE_NODE:self.CHECK_STATE] ==
                                      node[self.TREE_NODE:self.CHECK_STATE]).all(
                    axis=1)]  # ツリーノードからチェックステートの前まで同一のアイテム取得
                if len(item) > 0:
                    return item[0]  # アイテムを返す
            return None  # Noneを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   チェックしているツリーリスト作成
    # ---------------------------------------------------------------------------------------------------
    def getCheckedTree(self, flatList, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if flatList is not None:  # フラットベースが有る時
                checkedList = flatList[(flatList[:, self.CHECK_STATE] != Qt.Unchecked)]  # チェックされているフラットリストトを取得
                if len(checkedList) > 0:  # フラットリストが有る時
                    root = self.getRoot(checkedList)  # ルートノードを取得する
                    self.setCheckState(checkedList, root, Qt.Checked)  # ルートのチェックステートセット
                    self.setChildCheckState(checkedList, root, Qt.Checked)  # 子供のトリステートをチェックに設定する(再帰メソッド)
                    return self.returnList(checkedList, p)  # 実行時間を表示してからデータを返す
            return self.returnNone(p)  # Noneを表示してからNoneを返す

        except Exception as e:  # 例外                                                                          # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #  チェック済のタイプコードリストを返す
    # ---------------------------------------------------------------------------------------------------
    def getTypeCodeList(self):
        try:
            if self.flatBase is not None:
                typeCodeList = self.flatBase[(self.flatBase[:, self.TREE_NODE] == GP.NODE.TYPE_ID) &
                                             (self.flatBase[:, self.CHECK_STATE] != Qt.Unchecked)]  # タイプコードリストをを作成
                typeCodeList = np.unique(typeCodeList[:, self.TYPE_CODE])  # タイプコードリストををセット
                return typeCodeList  # タイプコードリストをを返す
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #  チェック済のタイプIDリストを返す
    # ---------------------------------------------------------------------------------------------------
    def getTypeIdList(self):
        try:
            if self.flatBase is not None:
                typeIdList = self.flatBase[(self.flatBase[:, self.TREE_NODE] == GP.NODE.TYPE_ID) &
                                           (self.flatBase[:, self.CHECK_STATE] != Qt.Unchecked)]  # タイプIDリストを作成
                typeIdList = np.unique(typeIdList[:, self.TYPE_ID])  # タイプIDリストをセット
                return typeIdList  # タイプIDリストを返す
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #  チェック済のレーザーIDリストを返す
    # ---------------------------------------------------------------------------------------------------
    def getLaserIdList(self):
        try:
            if self.flatBase is not None:
                laserIdList = self.flatBase[(self.flatBase[:, self.TREE_NODE] == GP.NODE.LASER_ID) &
                                            (self.flatBase[:, self.CHECK_STATE] == Qt.Checked)]  # レーザーIDリストを作成
                laserIdList = np.unique(laserIdList[:, self.LASER_ID])  # レーザーIDリストをセット
                return laserIdList  # レーザーIDリストを返す
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   学習単位名を取得
    # ---------------------------------------------------------------------------------------------------
    def getUnitName(self, LEARN_UNIT):
        try:
            UNIT_NAME = None  # 学習単位名を初期化
            if LEARN_UNIT == GP.LEARN_UNIT.TYPE_CODE:  # 学習単位がタイプコードの時
                typeCodeList = self.getTypeCodeList()  # タイプコードリスト取得
                if len(typeCodeList) == 1:  # タイプコードが一つの時
                    UNIT_NAME = typeCodeList[0]  # 学習単位名を転写
            elif LEARN_UNIT == GP.LEARN_UNIT.TYPE_ID:  # 学習単位がタイプIDの時
                typeIdList = self.getTypeIdList()  # タイプIDリスト取得
                if len(typeIdList) == 1:  # タイプIDが一つの時
                    UNIT_NAME = typeIdList[0]  # 学習単位名を転写
            else:  # 学習単位がレーザーIDの時
                UNIT_NAME = GP.LEARN_UNIT.LASER_ID  # 学習単位名を転写
            if UNIT_NAME is not None:  # 学習単位名が有る時
                UNIT_NAME = UNIT_NAME.replace('-', '_')  # '-'を'_'に置き換える
            return UNIT_NAME  # 学習単位名を返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   学習単位名リストを取得する
    # ---------------------------------------------------------------------------------------------------
    def getUnitNameList(self, LEARN_UNIT):
        try:
            nameList = None  # 学習単位名を初期化
            if LEARN_UNIT == GP.LEARN_UNIT.TYPE_CODE:  # 学習単位がタイプコードの時
                typeCodeList = self.getTypeCodeList()  # タイプコードリスト取得
                if len(typeCodeList) > 0:  # タイプコードリストが有る時
                    nameList = typeCodeList  # 学習単位名を転写
            elif LEARN_UNIT == GP.LEARN_UNIT.TYPE_ID:  # 学習単位がタイプIDの時
                typeIdList = self.getTypeIdList()  # タイプIDリスト取得
                if len(typeIdList) > 0:  # タイプIDリストが有る時
                    nameList = typeIdList  # 学習単位名を転写
            else:  # 学習単位がレーザーIDの時
                laserIdList = self.getLaserIdList()  # レーザーIDリスト取得
                if len(laserIdList) > 0:  # レーザーIDリストが有る時
                    nameList = [GP.LEARN_UNIT.LASER_ID]  # 学習単位名を転写
            if nameList is not None and len(nameList) > 0:  # 習単位名が有る時
                nameList = [name.replace('-', '_') for name in nameList]  # '-'を'_'に置き換える
                return nameList  # nameListを返す
            return None  # Noneを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #  ペアレントノードを返す
    # ---------------------------------------------------------------------------------------------------
    def getParentNode(self, node):
        try:
            if self.flatBase is not None:
                node = np.array(node, 'O')  # numpy配列化しないとall()が使えない
                if node[self.TREE_NODE] == GP.NODE.PERIOD:
                    parentNode = self.flatBase[(self.flatBase[:, self.TREE_NODE] == GP.NODE.LASER_ID) &
                                               (self.flatBase[:, 2:self.LASER_ID + 1] == node[2:self.LASER_ID + 1]).all(
                                                   axis=1)]
                elif node[self.TREE_NODE] == GP.NODE.LASER_ID:
                    parentNode = self.flatBase[(self.flatBase[:, self.TREE_NODE] == GP.NODE.TYPE_ID) &
                                               (self.flatBase[:, 2:self.TYPE_ID + 1] == node[2:self.TYPE_ID + 1]).all(
                                                   axis=1)]
                elif node[self.TREE_NODE] == GP.NODE.TYPE_ID:
                    parentNode = self.flatBase[(self.flatBase[:, self.TREE_NODE] == GP.NODE.TYPE_CODE) &
                                               (self.flatBase[:, 2:self.TYPE_CODE + 1] == node[
                                                                                          2:self.TYPE_CODE + 1]).all(
                                                   axis=1)]
                elif node[self.TREE_NODE] == GP.NODE.TYPE_CODE:
                    parentNode = self.flatBase[(self.flatBase[:, self.TREE_NODE] == GP.NODE.ROOT)]
                else:  # ROOT
                    parentNode = None  # Noneをセット
                if parentNode is not None and len(parentNode) > 0:  # ペアレントノードが有る時
                    return parentNode[0]  # ペアレントノードを返す
            return None  # Noneを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ***************************************************************************************************
    #   イベント処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   ツリー更新
    # ---------------------------------------------------------------------------------------------------
    def UPDATE_TREE(self):
        try:
            p = self.progress  # プログレス転写
            self.startNewLevel(len(self.slaveList) + 1, p)  # 新しいレベルの進捗開始
            for slave in self.slaveList:  # スレーブーリストをすべて実行
                slave.updateMasterSignal.emit()  # スレーブにマスター更新通知
            self.laserIdList = self.getLaserIdList()  # チェック済のレーザーIDリストをセットする
            GP.TREE.saveData(p)  # 保存データをDBに書き込む
            self.endLevel(p)                                                                            # 現レベルの終了
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e, p)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ツリービュークリック時処理
    # ---------------------------------------------------------------------------------------------------
    def treeItemClicked(self, node):
        try:
            if self.flatBase is not None:  # フラットベースが有る時
                node = np.array(node, 'O')  # numpy配列化
                if node[self.CHECKABLE] == 1:  # チェック可の時
                    self.setChildCheckState(self.flatBase, node, node[self.CHECK_STATE])  # 子のチェックステートをノードのチェックステートにセット
                    parentNode = self.getParentNode(node)  # ペアレントノードを取得
                    while parentNode is not None:
                        self.setNodeTriStateOne(parentNode)  # ペアレントノードのトリステートをセット
                        parentNode = self.getParentNode(parentNode)  # ペアレントノードを取得
                    rootItem = self.model.item(0, 0)  # タイプコードアイテム取得
                    if rootItem is not None:  # フラットベースのアイテムが有る時
                        self.setNodeChildItemToModel(rootItem, node)
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass


# =======================================================================================================
#   クラス MasterTreeClass
# =======================================================================================================
class MasterTreeWidgetClass(BaseTreeWidgetClass):
    # ---------------------------------------------------------------------------------------------------
    #   初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, title, TABLE_NAME):
        try:
            BaseTreeWidgetClass.__init__(self, title, TABLE_NAME)  # スーパークラス初期化
            self.treeType = GP.TREE_TYPE.MASTER  # ツリータイプ
            self.setStyleSheet("background:lightblue; color:red;font-size:9pt" + ";")  # オブジェクトのスタイルを設定する
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.connectButtons()  # タブのオブジェクトとメソッドを結合
            pass

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            main = QVBoxLayout()  # メインレイアウト生成（垂直レイアウト）
            main.setAlignment(Qt.AlignTop)  # 上詰め
            buttonLayout = QHBoxLayout()  # 釦レイアウト生成（水平レイアウト）
            self.setExeButton(buttonLayout, ["UPDATE_TREE", "更新"])  # 機種ツリー更新
            self.setExeButton(buttonLayout, ["INITIALIZE_TREE", "初期化"])  # 機種選択ツリー初期化
            main.addLayout(buttonLayout)  # メインレイアウト本体に釦レイアウトを追加
            self.setLabelStyle2(main, "機種選択", "gray", "white", 40, "12pt")  # 表題ラベル
            main.addWidget(self.myTreeView)  # メインレイアウト本体に機種選択ツリービューを追加
            return main  # メインレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #  チェックツリーを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeCheckTree(self):
        try:
            if self.flatBase is not None:  # フラットベースが有る時
                self.makeCheckTreeFromFlatBase(self.flatBase)  # ツリービュー初期化
                self.laserIdList = self.getLaserIdList()  # チェック済のレーザーIDリストをセットする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return  # 終了

    # ---------------------------------------------------------------------------------------------------
    #   フラットベースからチェックステート付きのツリーモデルを作成
    # ---------------------------------------------------------------------------------------------------
    def makeCheckTreeFromFlatBase(self, flatList):
        try:
            model = self.model
            #            model.setHorizontalHeaderLabels("モデルツリー")                                            # モデルのテキストをセット
            model.clear()  # モデルをクリア
            root = self.getRoot(flatList)  # ルートノードを取得する
            if root is not None:  # チェックリストが有る時
                # ルートツリー
                rootItem = self.makeCheckNode(root)  # ルートアイテム生成
                model.appendRow(rootItem)  # モデルに追加
                self.makeCheckTreeFromFlatBase_child(flatList, rootItem, root)  # フィルターをかけたツリーリストを作成する(再帰メソッド)

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return []  # []を返す

    # ---------------------------------------------------------------------------------------------------
    #   子アイテムを生成する(再帰メソッド)
    # ---------------------------------------------------------------------------------------------------
    def makeCheckTreeFromFlatBase_child(self, flatList, parentItem, node):
        try:
            children = self.getChildren(flatList, node)  # 子リスト取得
            for child in children:  # 子リストをすべて実行
                childItem = self.makeCheckNode(child)  # タイプコードアイテム生成
                parentItem.appendRow(childItem)  # モデルに追加
                self.makeCheckTreeFromFlatBase_child(flatList, childItem, child)  # 子アイテムを生成する(再帰)

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ノードデータからチェックノードアイテムを生成
    # ---------------------------------------------------------------------------------------------------
    def makeCheckNode(self, nodeData):
        try:
            nodeName = self.getNodeName(nodeData)  # ノード名取得
            item = QStandardItem(nodeName)  # スタンダードアイテム生成
            item.setCheckable(True)  # チェック可能にする
            item.setTristate(True)  # トリステート
            item.setCheckState(nodeData[self.CHECK_STATE])  # チェックステートをセットする
            item.setData(list(nodeData), Qt.ToolTipRole)  # データセット
            return item  # スタンダードアイテムを返す

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #  LSTからフラットベースを生成する
    # ---------------------------------------------------------------------------------------------------
    def makeBase(self, lstFlatBase, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            if lstFlatBase is not None:
                self.flatBase = self.makeTreeList(lstFlatBase, p)  # フラットベースを作成
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外
            self.showError(e, p)  # 例外を表示
            return  # 終了

    # ---------------------------------------------------------------------------------------------------
    #   LSTからツリーリストを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeTreeList(self, lstList, p=None):
        try:
            if lstList is not None:  # LSTリストとCAUSE辞書が有る時
                written = False  # 書き込み完了フラグを初期化
                LST = GP.CONT.LST  # LSTを転写
                TABLE = self.TABLE_NAME  # 自身のテーブル名
                typeCodeList = np.unique(lstList[:, LST.TYPE_CODE])  # タイプコードリストを作成
                self.startNewLevel(len(typeCodeList), p)  # 新しいレベルの進捗開始
                treeList = []  # ツリーリスト初期化
                # ルートを作成
                data = [TABLE, GP.NODE.ROOT, "", "", 0, 0, "", Qt.Checked, 1]  # データセット
                treeList += [data]  # ツリーリストに追加
                # タイプコードリストを作成
                for typeCode in typeCodeList:  # タイプコードリストをすべて実行
                    typeCodeData = lstList[lstList[:, LST.TYPE_CODE] == typeCode]  # タイプコードのデータを抽出
                    data = [TABLE, GP.NODE.TYPE_CODE, typeCode, "", 0, 0, "", Qt.Checked, 1]  # データセット
                    treeList += [data]  # ツリーリストに追加
                    # レーザータイプIDリストを作成
                    typeIdList = np.unique(typeCodeData[:, LST.LASER_TYPE_ID])  # タイプIDリストを作成
                    self.startNewLevel(len(typeIdList), p)  # 新しいレベルの進捗開始
                    for typeId in typeIdList:  # タイプIDリストをすべて実行
                        typeIdData = typeCodeData[typeCodeData[:, LST.LASER_TYPE_ID] == typeId]  # タイプIDのデータを抽出
                        data = [TABLE, GP.NODE.TYPE_ID, typeCode, typeId, 0, 0, "", Qt.Checked, 1]  # データセット
                        treeList += [data]  # ツリーリストに追加
                        length = len(typeIdData)  # レーザータイプID長さ
                        data = np.empty((length, self.LENGTH), 'O')  # 結合
                        data[:, self.TREE_NAME] = TABLE  # テーブル名
                        data[:, self.TREE_NODE] = "laserId"  # ツリーノード
                        data[:, self.TYPE_CODE] = typeIdData[:, LST.TYPE_CODE]  # タイプコード
                        data[:, self.TYPE_ID] = typeIdData[:, LST.LASER_TYPE_ID]  # レーザータイプID
                        data[:, self.LASER_ID] = typeIdData[:, LST.LASER_ID]  # レーザーID
                        data[:, self.PERIOD] = 0  # ピリオッド
                        data[:, self.CAUSE] = ""  # CAUSE
                        data[:, self.CHECK_STATE] = Qt.Checked  # チェックステートをチェックにする
                        data[:, self.CHECKABLE] = 1  # チェッカブルをチェック可にする
                        treeList += list(data)  # ツリーリストに追加
                        emit(p)  # 進捗バーにシグナルを送る
                    self.endLevel(p)  # 現レベルの終了
                self.endLevel(p)  # 現レベルの終了
                treeList = np.array(treeList, 'O')  # ツリーリストを返す
                return self.returnList(treeList)  # 実行時間を表示してからデータを返す
            emit(p)
            return self.returnNone()  # 実行時間を表示してからデータを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ***************************************************************************************************
    #   イベント処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   機種選択ツリー初期化
    # ---------------------------------------------------------------------------------------------------
    def INITIALIZE_TREE(self):
        try:
            p = self.progress  # プログレスセット
            self.startNewLevel(3, p)  # 新しいレベルの進捗開始
            LST = GP.CONT.LST  # LSTを転写
            if GP.SVR.DBSServer.existsLocTable(LST):  # LSTが有る時
                query = self.makeObjectQuery(LST)  # オブジェクトのフィールド名からセレクトクエリーを作成
                lstFlatBase = GP.SVR.DBSServer.makeLocFlatListFromQuery(LST, query, p)  # LSTのフラットベースをすべて読み込む
                self.makeBase(lstFlatBase, p)  # 機種選択ツリー初期化
                self.makeCheckTree()  # オブジェクトのベース作成
                self.deleteObject(lstFlatBase)  # オブジェクトを削除してメモリーを解放する
                GP.TREE.saveData(p)  # 保存データをDBに書き込む
                for slave in self.slaveList:  # スレーブーリストをすべて実行
                    slave.updateMasterSignal.emit()  # スレーブにマスター更新通知
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e, p)  # 例外を表示


# =======================================================================================================
#   スーパークラス スレーブツリーウイジェットクラス
# =======================================================================================================
class SlaveTreeWidgetClass(BaseTreeWidgetClass):
    updateMasterSignal = pyqtSignal()  # マスター更新シグナル

    # ---------------------------------------------------------------------------------------------------
    #   初期化
    # ---------------------------------------------------------------------------------------------------
    def __init__(self, title, TABLE_NAME, MASTER):  # 初期化
        try:
            BaseTreeWidgetClass.__init__(self, title, TABLE_NAME)
            self.MASTER = MASTER
            self.treeType = GP.TREE_TYPE.SLAVE  # ツリータイプ
            self.LABEL = GP.PCONT.CH.LABEL  # CHのラベルをセットする
            self.layout = self.createLayout()  # レイアウト生成
            self.setLayout(self.layout)  # レイアウトを自分にセット
            self.loadParameters()  # パラメータのデータをオブジェクトと自分にセット
            self.layout.addWidget(self.myTreeView)  # メニューに機種選択ツリービューを追加
            self.connectTreeButtons(self.parameter)  # オブジェクトとメソッドを結合
            self.updateMasterSignal.connect(self.UPDATE_MASTER)  # マスター更新シグナルを結合

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   レイアウト設定
    # ---------------------------------------------------------------------------------------------------
    def createLayout(self):
        try:
            main = QVBoxLayout()  # メインレイアウト生成（垂直レイアウト）
            main.setAlignment(Qt.AlignTop)  # 上詰め
            buttonLayout = QHBoxLayout()  # 釦レイアウト生成（水平レイアウト）
            self.setExeButton(buttonLayout, ["UPDATE_TREE", "更新"])  # 機種ツリー更新
            self.setExeButton(buttonLayout, ["INITIALIZE_TREE", "初期化"])  # 機種選択ツリー初期化
            main.addLayout(buttonLayout)  # メインレイアウト本体に釦レイアウトを追加
            self.setCheckGroup(main, {"PDG": "稼働中", "REG": "定期交換", "ACC": "異常交換"}, "機種選択")  # チャンバー状態選択フラグ
            main.addWidget(self.myTreeView)  # メインレイアウト本体に機種選択ツリービューを追加
            return main  # メインレイアウトを返す

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #  マスターベースと抽出リストからフラットベースを生成する
    # ---------------------------------------------------------------------------------------------------
    def makeBase(self, p=None):
        try:
            self.startNewLevel(2, p)  # 新しいレベルの進捗開始
            masterBase = self.MASTER.flatBase  # マスターツリーのフラットベースを取得
            if masterBase is not None:  # マスターベースが有る時
                masterBase = self.getCheckedTree(masterBase, p)  # マスターベースをチェックされているものだけにする
                if masterBase is not None:  # マスターベースが有る時
                    self.flatBase = self.makeCauseTree(masterBase, p)  # PRBのCAUSEを加えたツリーを作成
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す

    # ---------------------------------------------------------------------------------------------------
    #   ツリーにPRBのCAUSEを加える
    # ---------------------------------------------------------------------------------------------------
    def makeCauseTree(self, flatList, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            PRB = GP.PCONT.CH.PRB  # CHのPRBを転写
            if flatList is not None:  # フラットベースが有る時
                laserIdList = flatList[flatList[:, self.TREE_NODE] == GP.NODE.LASER_ID]  # フラットベースからレーザーIDリストを作成
                laserIdList = np.unique(laserIdList[:, self.LASER_ID])  # フラットベースからレーザーIDリストを作成
                TABLE_NAME = PRB.PREFIX + PRB.TABLE_NAME  # 前置句を付けたテーブル名をセット
                baseQuery = self.makeCasuseQuery(TABLE_NAME)  # CAUSEを加えたクエリー作成
                causeList = GP.SVR.DBSServer.getLocFlatListFromQuery(PRB, baseQuery, p)  # 原因リストの作成
                if causeList is not None:
                    causeList = causeList[np.in1d(causeList[:, self.LASER_ID], laserIdList)]  # フィルターリストに有るものを抽出
                    if causeList is not None and len(causeList) > 0:  # 原因リストが有る時
                        root_List = None  # ルートリスト初期化
                        root = self.getRoot(flatList)  # ルートノードを取得する
                        if root is not None:  # チェックリストが有る時
                            root_List = self.makeCauseTree_child(flatList, causeList, root)  # フィルターをかけたツリーリストを作成する(再帰メソッド)
                        self.deleteObject(causeList)  # 原因リストを削除してメモリーを解放する
                        if root_List is not None:  # ルートリストが有る時
                            root_List = np.array(root_List, 'O')  # numpy配列化
                            root_List[:, self.TREE_NAME] = self.TABLE_NAME  # ツリー名を設定
                            return self.returnList(root_List, p)  # 実行時間を表示してからデータを返す
            return self.returnNone(p)  # NOneを表示してからNoneを返す

        except Exception as e:  # 例外
            return self.returnError(e, p)  # エラーを表示してからNoneを返す
            pass

    # ---------------------------------------------------------------------------------------------------
    #   CAUSEを加えたクエリー作成
    # ---------------------------------------------------------------------------------------------------
    def makeCasuseQuery(self, TABLE_NAME):
        try:
            query = QueryClass()  # クエリを生成
            query.add("SELECT DISTINCT")  # セレクト
            query.add("'" + self.TABLE_NAME + "',")  # ツリー名
            query.add("'" + GP.NODE.PERIOD + "'" + ",")  # ツリーノード
            query.add("BASE.TYPE_CODE,")  # タイプコード
            query.add("BASE.LASER_TYPE_ID,")  # レーザータイプID
            query.add("BASE.LASER_ID,")  # レーザーID
            query.add("BASE.PERIOD,")  # ピリオッド
            query.add("BASE.CAUSE,")  # 原因
            query.add("0,")  # チェックステート
            query.add("1")  # チェック可否
            query.add("FROM " + TABLE_NAME + " BASE ")  # テーブル
            return query  # フラットリストを返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   チェック済リストと原因リストからノードリストを作成する（再帰メソッド）
    # ---------------------------------------------------------------------------------------------------
    def makeCauseTree_child(self, flatList, causeList, node):
        try:
            if node[self.TREE_NODE] != GP.NODE.ROOT:  # ノードがルートでない時
                fieldNo = self.getFieldNo(node)  # ノードのフィールド番号を取得
                if not node[fieldNo] in np.unique(causeList[:, fieldNo]):  # 子ノードが原因リストに無い時
                    return []  # []を返す
            nodeList = []  # ノードリスト初期化
            if node[self.TREE_NODE] == GP.NODE.LASER_ID:  # ノードがレーザーIDノードの時
                children = self.getChildren(causeList, node)  # 子リストを取得
                children[:, self.CHECK_STATE] = node[self.CHECK_STATE]  # 子リストのチェックステートをセット
                children[:, self.CHECKABLE] = node[self.CHECKABLE]  # 子リストのチェックステートをセット
                nodeList = [node] + list(children)  # ノードと子リストを結合してノードリストにする
            else:  # ノードがピリオッドノードで無い時
                # 孫リストを作成
                children = self.getChildren(flatList, node)  # 子リストを取得
                for child in children:  # 子リストをすべて実行
                    grandChildren = self.makeCauseTree_child(flatList, causeList, child)  # 孫リストを取得
                    nodeList += grandChildren  # ノードリストに孫リストを追加
                if len(nodeList) > 0:  # 子リストが有る時
                    nodeList = [node] + nodeList  # ノードと子リストを結合してノードリストにすする
            return nodeList  # ノードリストを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return []  # 空リストを返す

    # ---------------------------------------------------------------------------------------------------
    #   チェックされているリストを抽出する
    # ---------------------------------------------------------------------------------------------------
    def getCheckedList(self):
        try:
            flatBase = self.flatBase  # 抽出ベースを転写
            if flatBase is not None:  # 抽出ベースが有る時
                checkedList = flatBase[(flatBase[:, self.TREE_NODE] == GP.NODE.PERIOD) &  # ノードがピリオッドかつ
                                       (flatBase[:, self.CHECK_STATE] == Qt.Checked)]  # チェックされているノードを抽出
                if len(checkedList) > 0:  # チェックリストが有る時
                    return np.array(checkedList, 'O')  # チェックリストを返す
            self.showNone()  # None表示
            return None  # チェックリスが無い時はNoneを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #  フラットベースにラベルフィルターをかける
    # ---------------------------------------------------------------------------------------------------
    def labelFilterBase(self):
        try:
            flatBase = self.flatBase  # フラットベースの転写
            if flatBase is not None:  # フラットベースが有る時
                self.makeExtractLabel()  # 抽出ラベルリスト作成
                flatBase[:, self.CHECKABLE] = 1  # まずすべてチェック可にする
                index = np.where((flatBase[:, self.TREE_NODE] == GP.NODE.PERIOD) &  # ツリーノードがピリオッドの時
                                 ~np.in1d(flatBase[:, self.CAUSE], self.extractLabel))[0]  # 抽出ラベルにないインデックスリスト作成
                if len(index) > 0:  # インデックスが有る時
                    flatBase[index, self.CHECK_STATE] = Qt.Unchecked  # チェックを無しにする
                    flatBase[index, self.CHECKABLE] = 0  # チェック不可にする
                return True  # 成功を返す
            return False  # 失敗を返す

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return False  # 失敗を返す

    # ---------------------------------------------------------------------------------------------------
    #   ラベルフィルター変更時ツリーリスト更新
    # ---------------------------------------------------------------------------------------------------
    def updateTreeOnLabelFilterChange(self):
        try:
            if self.labelFilterBase():  # フラットベースにラベルフィルターをかけるのに成功した時
                self.setFlatBaseToModel()  # ツリービュー更新

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #  チェックツリーを作成する
    # ---------------------------------------------------------------------------------------------------
    def makeCheckTree(self):
        try:
            if self.labelFilterBase():  # フラットベースにラベルフィルターをかけるのに成功した時
                self.makeCheckTreeFromFlatBase(self.flatBase)  # ツリービュー初期化
                self.laserIdList = self.getLaserIdList()  # チェック済のレーザーIDリストをセットする

        except Exception as e:  # 例外
            self.showError(e)  # 例外を表示
            return  # 終了

    # ---------------------------------------------------------------------------------------------------
    #   フラットベースからチェックステート付きのツリーモデルを作成
    # ---------------------------------------------------------------------------------------------------
    def makeCheckTreeFromFlatBase(self, flatList):
        try:
            model = self.model
            #            model.setHorizontalHeaderLabels("モデルツリー")                                            # モデルのテキストをセット
            model.clear()  # モデルをクリア
            root = self.getRoot(flatList)  # ルートノードを取得する
            if root is not None:  # チェックリストが有る時
                # ルートツリー
                rootItem = self.makeCheckNode(root)  # ルートアイテム生成
                model.appendRow(rootItem)  # モデルに追加
                self.makeCheckTreeFromFlatBase_child(flatList, rootItem, root)  # フィルターをかけたツリーリストを作成する(再帰メソッド)

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return []  # []を返す

    # ---------------------------------------------------------------------------------------------------
    #   子アイテムを生成する(再帰メソッド)
    # ---------------------------------------------------------------------------------------------------
    def makeCheckTreeFromFlatBase_child(self, flatList, parentItem, node):
        try:
            children = self.getChildren(flatList, node)  # 子リスト取得
            for child in children:  # 子リストをすべて実行
                childItem = self.makeCheckNode(child)  # タイプコードアイテム生成
                parentItem.appendRow(childItem)  # モデルに追加
                self.makeCheckTreeFromFlatBase_child(flatList, childItem, child)  # 子アイテムを生成する(再帰)
            pass

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   ノードデータからチェックノードアイテムを生成
    # ---------------------------------------------------------------------------------------------------
    def makeCheckNode(self, nodeData):
        try:
            nodeName = self.getNodeName(nodeData)  # ノード名取得
            item = QStandardItem(nodeName)  # スタンダードアイテム生成
            item.setTristate(True)  # トリステート
            item.setData(list(nodeData), Qt.ToolTipRole)  # データセット
            if nodeData[self.CHECKABLE] == 1:  # チェック可の時
                item.setCheckable(True)  # チェック可能にする
                item.setCheckState(nodeData[self.CHECK_STATE])  # チェックステートをセットする
            else:  # チェック不可の時
                item.setCheckable(False)  # チェック不可にする
            if nodeData[self.TREE_NODE] == GP.NODE.PERIOD:  # ツリーノードがピリオッドの時
                if nodeData[self.CAUSE] == self.LABEL.REG:  # 原因が定期交換の時
                    item.setForeground(QBrush(QColor('blue')))  # 青色文字にする
                elif nodeData[self.CAUSE] == self.LABEL.ACC:  # 原因が異常交換の時
                    item.setForeground(QBrush(QColor('red')))  # 赤色文字にする
                elif nodeData[self.CAUSE] == self.LABEL.PDG:  # 原因が稼働中の時
                    item.setForeground(QBrush(QColor('green')))  # 緑色文字にする
            return item  # スタンダードアイテムを返す

        except Exception as e:  # 例外                                                                          # 例外
            printError(e)  # 例外を表示
            return None  # Noneを返す

    # ---------------------------------------------------------------------------------------------------
    #   抽出ラベルでフィルターをかけたフラットなリストを抽出する
    # ---------------------------------------------------------------------------------------------------
    def getFilteredTreeList(self, treeList, p=None):
        try:
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            self.makeExtractLabel()  # 抽出ラベルリスト作成
            root_List = []  # ルートリスト初期化
            root = self.getRoot(treeList)  # ルートノードを取得する
            if root is not None:  # チェックリストが有る時
                root_List = self.getFilteredTreeList_child(self.extractLabel, treeList,
                                                           root)  # フィルターをかけたツリーリストを作成する(再帰メソッド)
            self.endLevel(p)                                                                            # 現レベルの終了
            if len(root_List) > 0:  # ルートリストが有る時
                return np.array(root_List, 'O')  # ルートリストを返す
            return []  # []を返す

        except Exception as e:  # 例外
            self.showError(e, p)  # エラー表示
            return []  # []を返す

    # ---------------------------------------------------------------------------------------------------
    #   フィルターをかけたツリーリストを作成する(再帰メソッド)
    # ---------------------------------------------------------------------------------------------------
    def getFilteredTreeList_child(self, extractLabel, treeList, node):
        try:
            childList = []  # 子リスト初期化
            if node[self.TREE_NODE] == GP.NODE.PERIOD:  # ノードがピリオッドノードの時
                if np.in1d(node[self.CAUSE], extractLabel):  # ノードのCAUSEデータが抽出リストに有る時
                    childList = [node]  # 子リストにノードをセット
            else:  # ノードがピリオッドノードで無い時
                children = self.getChildren(treeList, node)  # 子リストを取得
                for child in children:  # 子リストをすべて実行
                    grandChildren = self.getFilteredTreeList_child(extractLabel, treeList, child)  # 孫リストを取得
                    childList += grandChildren  # 子リストに孫リストを追加
                if len(childList) > 0:
                    childList = [node] + childList  # 子リストの頭にノードを加える
            return childList  # 子リストを返す

        except Exception as e:  # 例外
            self.showError(e)  # エラー表示
            return []  # []を返す

    # ---------------------------------------------------------------------------------------------------
    #   抽出ラベルリスト作成
    # ---------------------------------------------------------------------------------------------------
    def makeExtractLabel(self):
        try:
            LABEL = self.LABEL
            self.extractLabel = []
            if self.PDG:  # 稼働中レーザー選択フラグがセットの時
                self.extractLabel += [LABEL.PDG]  # 稼働中レーザーを加える
            if self.REG:  # 定期交換レーザー選択フラグがセットの時
                self.extractLabel += [LABEL.REG]  # 定期交換レーザーを加える
            if self.ACC:  # 異常終了レーザー選択フラグがセットの時
                self.extractLabel += [LABEL.ACC]  # 異常終了レーザーを加える

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ***************************************************************************************************
    #   イベント処理
    # ***************************************************************************************************
    # ---------------------------------------------------------------------------------------------------
    #   マスターのフラットベース変更時処理
    # ---------------------------------------------------------------------------------------------------
    def UPDATE_MASTER(self):
        try:
            p = self.progress  # プログレスセット
            self.startNewLevel(1, p)  # 新しいレベルの進捗開始
            self.makeBase(p)  # ベースツリーを生成する
            self.makeCheckTree()  # オブジェクトのベース作成
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e, p)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   機種選択ツリー初期化
    # ---------------------------------------------------------------------------------------------------
    def INITIALIZE_TREE(self):
        try:
            p = self.progress  # プログレスセット
            self.startNewLevel(2, p)  # 新しいレベルの進捗開始
            self.parameter.PDG = True  # 稼働中セット
            self.parameter.REG = True  # 定期交換セット
            self.parameter.ACC = True  # 異常交換セット
            self.setParametersToObject()  # パラメータをオブジェクトとファイルに書き込み、再度パラメータに書き込む
            self.makeBase(p)  # ベースツリーを生成する
            self.makeCheckTree()  # オブジェクトのベース作成
            GP.TREE.saveData(p)  # 保存データをDBに書き込む
            self.endLevel(p)  # 現レベルの終了

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e, p)  # 例外を表示
            pass

    # ---------------------------------------------------------------------------------------------------
    #   稼働中レーザークリック時処理
    # ---------------------------------------------------------------------------------------------------
    def PDG_EVENT(self, e):
        try:
            self.updateTreeOnLabelFilterChange()  # ラベルフィルター変更時ツリーリスト更新
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   定期交換レーザークリック時処理
    # ---------------------------------------------------------------------------------------------------
    def REG_EVENT(self, e):
        try:
            self.updateTreeOnLabelFilterChange()  # ラベルフィルター変更時ツリーリスト更新
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示

    # ---------------------------------------------------------------------------------------------------
    #   異常終了レーザークリック時処理
    # ---------------------------------------------------------------------------------------------------
    def ACC_EVENT(self, e):
        try:
            self.updateTreeOnLabelFilterChange()  # ラベルフィルター変更時ツリーリスト更新
            pass

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass


# =======================================================================================================
#   スーパークラス　結果ツリーパラメータクラス
# =======================================================================================================
class ResultTreeParameterClass(ParameterClass):
    def __init__(self, TREE_LOG):  # 初期化
        try:
            ParameterClass.__init__(self, TREE_LOG)  # スーパークラスの初期化
            PDG = True  # 稼働中
            REG = True  # 定期交換
            ACC = True  # 異常交換
            self.nameList = [name for name in locals().keys()
                             if (name != 'self') and
                             (name != '__pydevd_ret_val_dict')]  # ローカル変数名リストを作成
            for objectName in self.nameList:  # オブジェクト名リストをすべて実行
                exec("self." + objectName + " = " + objectName)  # オブジェクトのインスタンス変数のセット
            self.loadData()  # パラメータをログファイルから読込

        except Exception as e:  # 例外
            printError(e)  # 例外を表示


# =======================================================================================================
#   クラス Resultツリーウイジェットクラス
# =======================================================================================================
class ResultTreeWidgetClass(SlaveTreeWidgetClass):
    def __init__(self, title, TABLE_NAME, MASTER):
        try:
            self.parameter = ResultTreeParameterClass(GP.TREE_LOG.AGE_RESULT)  # パラメータ
            SlaveTreeWidgetClass.__init__(self, title, TABLE_NAME, MASTER)  # スーパークラスの初期化

        except Exception as e:  # 例外                                                                          # 例外
            self.showError(e)  # 例外を表示
            pass







