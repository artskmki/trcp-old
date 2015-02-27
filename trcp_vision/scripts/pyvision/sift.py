# coding: utf-8

import numpy as np
import cv2
import cv2.cv as cv

def compareImg(detector,kp1,desc1,npimg):# 画像を比較する関数

	# キャプチャ画像の特徴量の検出
	kp2, desc2 = detector.detectAndCompute(npimg, None)

	# BFMatcherをNORM_L2で対応付け
	matcher = cv2.BFMatcher(cv2.NORM_L2)
	# クエリ集合の各ディスクリプタに対して、最も良い上位2個のマッチを取得
	matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2)

	# 距離許容比率
	ratio = 0.75

	# 座標を抽出
	mkp = []
	for m in matches:
		if len(m) == 2 and m[0].distance < m[1].distance * ratio:
			m = m[0]
			mkp.append( kp2[m.trainIdx] )
	matchedXY = np.float32([kp.pt for kp in mkp])

	# 共通点が10ポイント以上あったらその中央の座標を返す
	if len(matchedXY) >= 10:
		x,y = 0,0;
		for i in matchedXY:
			x += i[0]
			y += i[1]
		avgx = int(x / len(matchedXY))
		avgy = int(y / len(matchedXY))
		return (avgx,avgy)

if __name__ == '__main__':

	# キャプチャから探し出す画像ファイルを指定
	comImg = './template.png'
	# 比較元の画像を読み込む（読み込んだ時点でグレースケールのNumpy配列）
	comImgNp = cv2.imread(comImg, 0)

	# 検出器
	detector = cv2.SIFT()
	# 特徴量の検出
	kp1, desc1 = detector.detectAndCompute(comImgNp, None)

	# 表示用のウィンドウを準備
	cv.NamedWindow("camera", 1)

	# カメラからのビデオキャプチャを初期化
	capture = cv.CaptureFromCAM(0)

	# キャプチャの横幅を取得
	camW = int(cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH))
	# キャプチャの高さを取得
	camH = int(cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT))

	# グレースケール変換用のデータ領域を確保
	grayImage = cv.CreateImage ((camW,camH), cv.IPL_DEPTH_8U, 1)

	while True:
		# フレームの画像をキャプチャ
		img = cv.QueryFrame(capture)

	 	if img != None:# キャプチャ開始直後はデータが入っていないので、判定を入れておく
			# キャプチャ画像をグレースケールに変換
			cv.CvtColor(img,grayImage,cv.CV_RGB2GRAY);
			# グレースケール画像をCvMat配列に変換（元はIplimage構造体）
			mat = cv.GetMat(grayImage)
			# CvMat配列をNumpy配列に変換
			npimg = np.asarray(mat)

			# 画像を比較して、中央の座標を取得
			retXY = compareImg(detector,kp1,desc1,npimg);
			if(retXY != None):

				# 元のキャプチャ画像をNumpy配列に変換
				mat2 = cv.GetMat(img)
				baseimg = np.asarray(mat2)

				# 取得した座標を中心点として円を描く
				cv2.circle(baseimg,retXY,10,(255,0,0))
				# 円を描いた画像を描画
				cv2.imshow("camera", baseimg)

			else:# 座標が返ってこなければ元の画像を表示
				# キャプチャした画像をウィンドウに表示
				cv.ShowImage("camera", img)

		if cv.WaitKey(10) == 27: 
			break
	cv.DestroyAllWindows()

