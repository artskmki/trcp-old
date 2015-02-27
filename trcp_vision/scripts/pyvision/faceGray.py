# -*- coding: utf-8 -*-
import cv2
import numpy as np
  
if __name__ == '__main__':
  
    # カメラ映像の取得
    cap = cv2.VideoCapture(0)
    # 顔探索用の機械学習ファイルを取得
    cascade = cv2.CascadeClassifier("data/haarcascades/haarcascade_frontalface_alt.xml")
    while(1):
        ret, im = cap.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray,(gray.shape[1]/2,gray.shape[0]/2))
        # 顔探索(画像,縮小スケール,最低矩形数)
        face = cascade.detectMultiScale(gray, 1.1, 3)
        # 顔検出した部分を長方形で囲う
        for (x, y, w, h) in face:
            cv2.rectangle(gray, (x, y),(x + w, y + h),(0, 50, 255), 3)
  
        # 画像表示
        cv2.imshow("Show Image",gray)
        # キーが押されたらループから抜ける
        if cv2.waitKey(10) > 0:
            cap.release()
            cv2.destroyAllWindows()
            break
  
    # キャプチャー解放
    cap.release()
    # ウィンドウ破棄
    cv2.destroyAllWindows()
