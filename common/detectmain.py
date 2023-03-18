
import queue
import av
import cv2
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

from common.header import queueTimeOutSec, frame_color, result_queue
from common.datacol import colName, colProbability, colX_start, colY_start, colX_end, colY_end

# 処理中フラグ
busy = 0

# コールバック
def callback(frame):
    global busy
    stat = ""

    try:
        if busy == 0: # 処理中以外？
            try:
                busy = not 0 # 処理中

                # 画像形式変換
                img = frame.to_ndarray(format="bgr24")

                # 画像API処理
                df, stat = VisionAPIFunc(img, probability_threshold)

                # 結果描画
                for index, row in df.iterrows():
                    # 枠描画
                    cv2.rectangle(img, (int(row[colX_start]),int(row[colY_start])), (int(row[colX_end]),int(row[colY_end])), frame_color, 1)
                    # ラベル表示
                    cv2.putText(img,
                                text=row[colName] + ': ' + str(row[colProbability]),
                                org=(int(row[colX_start])+5,int(row[colY_start])),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1.0,
                                color=frame_color,
                                thickness=2,
                                lineType=cv2.LINE_4)

            except:
                raise

            finally:
                busy = 0 # 処理終了

    except Exception as e:
        stat = "エラー：" + str(e)

    result_queue.put(stat) # メッセージ

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# メイン処理
def appmain(title, note, ApiFunc, threshold):
    global probability_threshold
    global VisionAPIFunc

    try:
        # 画像API処理関数
        VisionAPIFunc = ApiFunc
        # 精度しきい値
        probability_threshold = threshold

        # タイトル
        st.title(f"物体検知 <{title}>")
        # 説明
        if note != None:
            st.text(note)

        # 映像表示
        streaming_placeholder = st.empty()
        # メッセージ表示
        labels_placeholder = st.empty()

        # 映像表示
        with streaming_placeholder.container():
            # WEBカメラ
            webrtc_ctx = webrtc_streamer(
                key="object-detection",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
                video_frame_callback=callback,
                media_stream_constraints={"video": True, "audio": False},
                async_processing=True,
                translations={
                    "start": "開始",
                    "stop": "停止",
                    "select_device": "カメラ切替",
                    "media_api_not_available": "Media APIが利用できない環境です",
                    "device_ask_permission": "メディアデバイスへのアクセスを許可してください",
                    "device_not_available": "メディアデバイスを利用できません",
                    "device_access_denied": "メディアデバイスへのアクセスが拒否されました",
                },
            )

        if webrtc_ctx.state.playing: # 映像配信中？
            panels = labels_placeholder

            while webrtc_ctx.state.playing: # 配信中
                try:
                    # キューの取得
                    ret = result_queue.get(timeout=queueTimeOutSec) # メッセージ
                except queue.Empty:
                    ret = ""

                if ret != "": # メッセージあり？
                    panels.error(ret) # エラー表示

    except Exception as e:
        st.error("エラー：" + str(e)) # エラー表示
