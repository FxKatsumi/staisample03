import queue

# キュータイムアウト時間（秒）
queueTimeOutSec = 1.0
#枠の色（赤）
frame_color = (0,0,255)

# キュー
result_queue: queue.Queue = (
    queue.Queue()
)
