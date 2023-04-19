# 【wallprime】Custom Visionで物体検出
# https://remix-yh.net/1156/

# Custom Vision 使用する画像内の物体の検出
# https://microsoftlearning.github.io/AI-102JA-Designing-and-Implementing-a-Microsoft-Azure-AI-Solution/Instructions/18-object-detection.html

from common.detectmain import appmain

# ＜Azure＞
from common.azure import VisionAPI

# 精度しきい値
# probability_threshold = 0.92
probability_threshold = 0.8

# プログラム開始
if __name__ == "__main__":
    # メイン処理
    appmain("Microsoft", "フォレックス ロゴマークのみを学習したモデル(80)", VisionAPI, probability_threshold)
