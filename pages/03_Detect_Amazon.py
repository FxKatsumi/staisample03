# ＜Amazon＞

import os
import sys
import streamlit as st

# 認証ファイル
aws_config_path = "\.aws\config"
aws_credentials_path = "\.aws\credentials"

# 環境変数
# windows
USERPROFILE_env_win = "USERPROFILE"

# 認証ファイル作成
def MakeCredential():

    try:
        # プラットフォーム取得
        plat = sys.platform

        # ホームパス設定
        if plat == "win32": # Windows
            home_path = os.environ.get(USERPROFILE_env_win, '~')
        if plat == "darwin": # Mac
            home_path = "~"
        if plat in ("linux", "linux2"): # Linux
            home_path = "~"

        config_path = home_path + aws_config_path
        # print(config_path)
        credentials_path = home_path + aws_credentials_path
        # print(credentials_path)

        # print(os.path.exists(config_path))
        if os.path.exists(config_path) == False: # configファイルなし？
            with open(config_path, mode='x', encoding='UTF-8') as f:
                f.write(st.secrets.aws_settings.config01 + '\n')
                f.write(st.secrets.aws_settings.config02 + '\n')
                f.write(st.secrets.aws_settings.config03 + '\n')
                print("config01")

        # print(os.path.exists(credentials_path))
        if os.path.exists(credentials_path) == False: # credentialsファイルなし？
            with open(credentials_path, mode='x', encoding='UTF-8') as f:
                f.write(st.secrets.aws_settings.credentials01 + '\n')
                f.write(st.secrets.aws_settings.credentials02 + '\n')
                f.write(st.secrets.aws_settings.credentials03 + '\n')
                print("credentials01")

    except Exception as e:
        pass

# 認証ファイル作成
MakeCredential()


from common.detectmain import appmain

# ＜Amazon＞

from common.google import VisionAPI

# 精度しきい値
probability_threshold = 0.7

# プログラム開始
if __name__ == "__main__":
    # メイン処理
    appmain("Amazon", "", VisionAPI, probability_threshold)
