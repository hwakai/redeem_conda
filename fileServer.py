import os
import numpy as np
import math
import csv
from staticImport import *
from gpiBase import GpiBaseClass

#=======================================================================================================
#   クラス FILEServerClass
#=======================================================================================================
class FILEServerClass(GpiBaseClass):
    #---------------------------------------------------------------------------------------------------
    #   クラス変数
    #---------------------------------------------------------------------------------------------------
    _singleton = None                                                                                   # シングルトンを初期化

    #---------------------------------------------------------------------------------------------------
    #   初期化
    #---------------------------------------------------------------------------------------------------
    def __init__(self):                                                                                 # 初期化
        try:
            if FILEServerClass._singleton is None:                                                      # クラス変数の_singletonの有無を確認
                GpiBaseClass.__init__(self, None)                                                       # スーパークラスの初期化
            pass

        except Exception as e:                                                                          # 例外
            printError(e)                                                                               # 例外を表示

    #---------------------------------------------------------------------------------------------------
    #   シングルトン呼び出し
    #---------------------------------------------------------------------------------------------------
    @classmethod
    def getInstance(self):
        if FILEServerClass._singleton is None:                                                          # クラス変数の_singletonの有無を確認
            FILEServerClass._singleton = FILEServerClass()                                              # クラスを生成して_singletonにセット
        return FILEServerClass._singleton                                                               # _singletonを返す

    #---------------------------------------------------------------------------------------------------
    #   追加ファイルをログファイルにマージする
    #---------------------------------------------------------------------------------------------------
    def mergeFile(self, object, srcPath, p=None):
        try:
            self.startNewLevel(1, p)                                                                    # 新しいレベルの進捗開始
            dstPath = object.targetPath                                                                 # ログパスを取得
            with open(file=srcPath,mode="r",encoding="utf-8") as readFile:                              # "utf-8"でファイルをオープン
                dataList = readFile.readlines()                                                         # すべての行を読み込み
                if len(dataList) > 1:                                                                   # 有効行が有る時
                    with open(file=dstPath,mode="a",encoding="utf-8") as writeFile:                     # "utf-8"でファイルをオープン
                        writeFile.writelines(dataList[1:])                                              # データリストをファイルに書き込む
            self.endLevel(p)                                                                            # 現レベルの終了

        except Exception as e:                                                                          # 例外
            self.showError(e, p)                                                                        # エラー表示
            pass

    #---------------------------------------------------------------------------------------------------
    #   保存データをファイルに書き込む
    #---------------------------------------------------------------------------------------------------
    def saveToCsvFile(self, logPath, object, baseType, p=None):
        try:
            dirName = os.path.dirname(logPath)                                                          # ディレクトリ名
            if not os.path.exists(dirName):                                                             # ディレクトリの有無を確認
                os.makedirs(dirName)                                                                    # 途中のディレクトリを含めてディレクトリを作成
            # データの書き込み
            if baseType == GP.BASE_TYPE.F_BASE:                                                         # ベースタイプがフラットベースの時
                if object.flatBase is not None:                                                         # フラットベースが有る時
                    block = self.getLaserBlock(object)                                                  # レーザーブロック長
                    blocks = math.ceil(len(object.flatBase) / block)                                    # ブロック数
                    self.startNewLevel(blocks, p)                                                       # 新しいレベルの進捗開始
                    # CSV を作成
                    with open(file=logPath,mode="w",encoding="utf-8") as f:                             # "utf-8"でファイルをオープン
                        writer = csv.writer(f, delimiter="\t", lineterminator='\n')                     # CSVライター設定
                        writer.writerow(object.tableDesc.colName)                                       # コラム名を書き込む
                        for i in range(blocks):                                                         # ブロック数実行
                            writer.writerows(object.flatBase[i*block:(i+1)*block])                      # 一回の行数をまとめて書き込み
                            emit(p)                                                                     # 進捗バーにシグナルを送る
                    return self.returnResult(True, p)                                                   # 実行時間を表示してからデータを返す

            elif baseType == GP.BASE_TYPE.L_BASE:                                                       # ベースタイプがレーザー辞書の時
                if object.laserBase is not None:                                                        # レーザーベース辞書が有る時
                    self.startNewLevel(len(object.laserBase), p)                                        # 新しいレベルの進捗開始
                    # CSV を作成
                    with open(file=logPath,mode="w",encoding="utf-8") as f:                             # "utf-8"でファイルをオープン
                        writer = csv.writer(f, delimiter="\t", lineterminator='\n')                     # CSVライター設定
                        writer.writerow(object.tableDesc.colName)                                       # コラム名を書き込む
                        for LASER_ID, dataList in object.laserBase.items():                             # レーザーベース辞書をすべて実行
                            writer.writerows(dataList)                                                  # レーザーIDデータ書き込み
                            emit(p)                                                                     # 進捗バーにシグナルを送る
                    return self.returnResult(True, p)                                                   # 実行時間を表示してからデータを返す

            elif baseType == GP.BASE_TYPE.P_BASE:                                                       # ベースタイプがピリオッド辞書の時
                if object.periodBase is not None:                                                       # ピリオッドベース辞書が有る時
                    self.startNewLevel(len(object.periodBase), p)                                       # 新しいレベルの進捗開始
                    # CSV を作成
                    with open(file=logPath,mode="w",encoding="utf-8") as f:                             # "utf-8"でファイルをオープン
                        writer = csv.writer(f, delimiter="\t", lineterminator='\n')                     # CSVライター設定
                        writer.writerow(object.tableDesc.colName)                                       # コラム名を書き込む
                        for (LASER_ID, PERIOD), pData in object.periodBase.items():                     # ピリオッドベース辞書をすべて実行
                            writer.writerows(pData)                                                     # レーザーIDデータ書き込み
                            emit(p)                                                                     # 進捗バーにシグナルを送る
                    return self.returnResult(True, p)                                                   # 実行時間を表示してからデータを返す

            return self.returnResult(None, p)                                                           # Noneを表示してからデータを返す

        except Exception as e:                                                                          # 例外
            return self.returnResultError(e, p)                                                         # エラーを表示してからFalseを返す


    #---------------------------------------------------------------------------------------------------
    #   保存データをファイルに書き込む
    #---------------------------------------------------------------------------------------------------
    def saveToCsvFileTest(self, object, strPath, baseType, baseList, p=None):
        try:
            dirName = os.path.dirname(strPath)                                                          # ディレクトリ名
            if not os.path.exists(dirName):                                                             # ディレクトリの有無を確認
                os.makedirs(dirName)                                                                    # 途中のディレクトリを含めてディレクトリを作成
            blocks = 100                                                                                # ブロック数
            # データの書き込み
            if baseList is not None:                                                                    # ベースリストが有る時
                block = math.ceil(len(baseList) / blocks)                                               # ブロックサイズ
                if baseType == GP.BASE_TYPE.F_BASE:                                                     # ソースがフラットベースの時
                    self.startNewLevel(blocks, p)                                                       # 新しいレベルの進捗開始
                    # CSV を作成
                    with open(file=strPath,mode="w",encoding="utf-8") as f:                             # "utf-8"でファイルをオープン
                        writer = csv.writer(f, delimiter="\t", lineterminator='\n')                     # CSVライター設定
                        writer.writerow(object.tableDesc.colName)                                       # コラム名を書き込む
                        for i in range(blocks):                                                         # ブロック数実行
                            writer.writerows(baseList[i*block:(i+1)*block])                             # 一回の行数をまとめて書き込み
                            emit(p)                                                                     # 進捗バーにシグナルを送る
                    return self.returnResult(True, p)                                                   # 実行時間を表示してからデータを返す

                elif baseType == GP.BASE_TYPE.L_BASE:                                                   # ソースがレーザー辞書の時
                    self.startNewLevel(len(baseList), p)                                                # 新しいレベルの進捗開始
                    # CSV を作成
                    with open(file=strPath,mode="w",encoding="utf-8") as f:                             # "utf-8"でファイルをオープン
                        writer = csv.writer(f, delimiter="\t", lineterminator='\n')                     # CSVライター設定
                        writer.writerow(object.tableDesc.colName)                                       # コラム名を書き込む
                        for LASER_ID, dataList in baseList.items():                                     # レーザーベース辞書をすべて実行
                            writer.writerows((dataList))                                                # レーザーIDデータ書き込み
                            emit(p)                                                                     # 進捗バーにシグナルを送る
                    return self.returnResult(True, p)                                                   # 実行時間を表示してからデータを返す

                elif baseType == GP.BASE_TYPE.P_BASE:                                                   # ソースがピリオッド辞書の時
                    self.startNewLevel(len(baseList), p)                                                # 新しいレベルの進捗開始
                    # CSV を作成
                    with open(file=strPath,mode="w",encoding="utf-8") as f:                             # "utf-8"でファイルをオープン
                        writer = csv.writer(f, delimiter="\t", lineterminator='\n')                     # CSVライター設定
                        writer.writerow(object.tableDesc.colName)                                       # コラム名を書き込む
                        for (LASER_ID, PERIOD), pData in baseList.items():                              # ピリオッドベース辞書をすべて実行
                            writer.writerows(pData)                                                     # レーザーIDデータ書き込み
                            emit(p)                                                                     # 進捗バーにシグナルを送る
                    return self.returnResult(True, p)                                                   # 実行時間を表示してからデータを返す
            emit(p)
            self.showNone(p)                                                                            # None表示
            return False                                                                                # 偽を返す

        except Exception as e:                                                                          # 例外
            return self.returnResultError(e, p)                                                         # エラーを表示してからFalseを返す



