# ＜Amazon＞

import io
import pandas as pd
from PIL import Image
import streamlit as st
import boto3

from common.datacol import colName, colProbability, colX_start, colY_start, colX_end, colY_end

# キーワード
LabelsKey = 'Labels'
NameKey = 'Name'
ConfidenceKey = 'Confidence'
InstancesKey = 'Instances'
BoundingBoxKey = 'BoundingBox'
LeftKey = 'Left'
TopKey = 'Top'
WidthKey = 'Width'
HeightKey = 'Height'

# Rekognitionクライアントを作成
rekognition = boto3.client('rekognition')

# 画像API処理
@st.cache
def VisionAPI(img, probability_threshold):
    stat = ""

    try:
        # サイズ取得
        hh, ww, cc = img.shape[:3]

        # 表を作成
        columns = [colName, colProbability, colX_start,colY_start,colX_end,colY_end]
        df = pd.DataFrame(columns = columns)

        # 画像形式変換
        image = Image.fromarray(img)
        png = io.BytesIO() # 空のio.BytesIOオブジェクトを用意
        image.save(png, format='png') # 空のio.BytesIOオブジェクトにpngファイルとして書き込み
        b_frame = png.getvalue() # io.BytesIOオブジェクトをbytes形式で読みとり

        # ラベル検出を実行
        response = rekognition.detect_labels(
                                Image={'Bytes': b_frame },
                                MaxLabels=10)

        # レスポンスから個々のラベル情報を取得
        for i, label in enumerate(response[LabelsKey]):
            # ラベル名を取得
            label_name = label[NameKey]
            # 信頼度を取得
            confidence = label[ConfidenceKey]

            if confidence >= probability_threshold:
                # ラベルの追加情報を取得
                for instance in label[InstancesKey]:
                    # バウンディングボックス情報を取得
                    bbox = instance[BoundingBoxKey]

                    # バウンディングボックスの値を重ねる画像の大きさにスケーリング
                    left = ww * bbox[LeftKey]
                    top = hh * bbox[TopKey]
                    width = ww * bbox[WidthKey]
                    height = hh * bbox[HeightKey]

                    x_e = left + width
                    y_e = top + height

                    # 表に追加
                    tmp_se = pd.Series([label_name, confidence, left, top, x_e, y_e], index=columns)
                    df = df.append(tmp_se, ignore_index=True)

    except Exception as e:
        stat = "エラー：" + str(e)

    return df, stat
