# ＜Azure＞

import io
import requests
import pandas as pd
from PIL import Image
import streamlit as st

from common.datacol import colName, colProbability, colX_start, colY_start, colX_end, colY_end

# Azure URL
azure_url = st.secrets.azure_settings.azure_url
# iteration Id
iterationId = st.secrets.azure_settings.iterationId
# Predictionキー
PredictionKey = st.secrets.azure_settings.PredictionKey

# jsonキーワード
predictionsKey = 'predictions'
tagNameKey = 'tagName'
probabilityKey = 'probability'
boundingBoxKey = 'boundingBox'
heightKey = 'height'
widthKey = 'width'
leftKey = 'left'
topKey = 'top'

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

        # http通信設定
        headers={'content-type':'application/octet-stream','Prediction-Key':PredictionKey}

        # 画像形式変換
        image = Image.fromarray(img)
        png = io.BytesIO() # 空のio.BytesIOオブジェクトを用意
        image.save(png, format='png') # 空のio.BytesIOオブジェクトにpngファイルとして書き込み
        b_frame = png.getvalue() # io.BytesIOオブジェクトをbytes形式で読みとり

        # REST API実行
        response =requests.post(azure_url+'?'+iterationId,data=b_frame,headers=headers)

        # 通信の結果からバウンディングボックスの情報を取得
        objects = response.json()[predictionsKey]

        # 認識した物体ごとにループ
        for obj in objects:
            if obj[probabilityKey] >= probability_threshold:
                # 要素抽出
                name = obj[tagNameKey]

                # 日本語が使用できないため英語に変換
                if name == 'リンゴ':
                    name = 'Apple'
                elif name == 'バナナ':
                    name = 'Banana'
                elif name == 'オレンジ':
                    name = 'Orange'

                probability = obj[probabilityKey]
                h = obj[boundingBoxKey][heightKey] * hh
                w = obj[boundingBoxKey][widthKey] * ww
                x = obj[boundingBoxKey][leftKey] * ww
                y = obj[boundingBoxKey][topKey] * hh
                x_e = x + w
                y_e = y + h

                # 表に追加
                tmp_se = pd.Series([name, probability, x, y, x_e, y_e], index=columns)
                df = df.append(tmp_se, ignore_index=True)

    except Exception as e:
        stat = "エラー：" + str(e)

    return df, stat
