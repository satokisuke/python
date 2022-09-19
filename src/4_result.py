from keras.models import load_model
import pickle
import cv2
import glob

#モデルとクラス名の読み込み
model = load_model('cnn.h5')
classes = pickle.load(open('classes.sav', 'rb'))

#sample画像の前処理
files = glob.glob('../sample/*')
box = []
for file in files:
  img = cv2.imread(file)
  img = cv2.resize(img,dsize=(224,224))
  img = img.astype('float32')
  img /= 255.0
  img = img[None, ...]
  result = model.predict(img)

  #確率が一番大きいクラス
  pred = result.argmax()

  img = cv2.imread(file)
  cv2.imwrite('../output/' + str(classes[pred]) + '/' + file,img)