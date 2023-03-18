# ＜Google＞

import io
import requests
import json
import base64
import pandas as pd
from PIL import Image
import streamlit as st

from common.datacol import colName, colProbability, colX_start, colY_start, colX_end, colY_end

# APIキー
GOOGLE_API_KEY = st.secrets.google_settings.API_KEY
GOOGLE_CLOUD_VISION_API_URL = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_API_KEY}"

# jsonキーワード
RESPONSES_KEY = 'responses'
LOCALIZED_KEY = 'localizedObjectAnnotations'
BOUNDING_KEY = 'boundingPoly'
NORMALIZED_KEY = 'normalizedVertices'
NAME_KEY = 'name'
SCORE_KEY = 'score'
X_KEY = 'x'
Y_KEY = 'y'

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
        headers = { "Content-Type" : "application/json" }

        # 画像形式変換
        image = Image.fromarray(img)
        png = io.BytesIO() # 空のio.BytesIOオブジェクトを用意
        image.save(png, format='png') # 空のio.BytesIOオブジェクトにpngファイルとして書き込み
        b_frame = png.getvalue() # io.BytesIOオブジェクトをbytes形式で読みとり
        base64Image = base64.b64encode(b_frame).decode('utf-8')

        request_data = json.dumps({
            "requests": [
                {
                    "image": {
                        "content": base64Image
                    },
                    "features": [
                        {
                            "type": "OBJECT_LOCALIZATION"
                        }
                    ]
                }
            ]
        })

        # REST API実行
        response = requests.post(GOOGLE_CLOUD_VISION_API_URL, headers=headers, data=request_data)

        objects = response.json()[RESPONSES_KEY][0][LOCALIZED_KEY]

        for obj in objects:
            # バウンディングボックスの左上と右下の角の座標を取得して書き足す
            box = [(v[X_KEY] * ww, v[Y_KEY] * hh) for v in obj[BOUNDING_KEY][NORMALIZED_KEY]]

            # 要素抽出
            name = obj[NAME_KEY]
            probability = obj[SCORE_KEY]
            x = box[0][0]
            y = box[0][1]
            x_e = box[2][0]
            y_e = box[2][1]

            if probability >= probability_threshold:
                # 表に追加
                tmp_se = pd.Series([name, probability, x, y, x_e, y_e], index=columns)
                df = df.append(tmp_se, ignore_index=True)

    except Exception as e:
        stat = "エラー：" + str(e)

    return df, stat
