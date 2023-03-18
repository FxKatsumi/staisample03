from common.detectmain import appmain

# ＜Google＞
from common.google import VisionAPI

# 精度しきい値
probability_threshold = 0.7

# プログラム開始
if __name__ == "__main__":
    # メイン処理
    appmain("Google", "", VisionAPI, probability_threshold)
