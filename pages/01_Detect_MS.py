from common.detectmain import appmain

# ＜Azure＞
from common.azure import VisionAPI

# 精度しきい値
probability_threshold = 0.9

# プログラム開始
if __name__ == "__main__":
    # メイン処理
    appmain("Microsoft", "バナナ、リンゴ、オレンジのみを学習したモデル", VisionAPI, probability_threshold)
