# https://sasuwo.org/image-classification/#toc5
# https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local
import os 
import cv2 
import glob
import numpy as np 
from sklearn.model_selection import train_test_split
from keras.utils import np_utils


#フォルダをクラス名にする
path = "../data/img"
folders = os.listdir(path)

#フォルダ名を抽出
classes = [f for f in folders if os.path.isdir(os.path.join(path, f))]
n_classes = len(classes)


#画像とラベルの格納
X = []
Y = []


#画像を読み込みリサイズする
for label,class_name in enumerate(classes):
  files = glob.glob(path + "/" +  class_name + "/*.jpg")
  for file in files:
    img = cv2.imread(file)
    img = cv2.resize(img,dsize=(224,224))
    X.append(img)
    Y.append(label)

#精度を上げるために正規化
X = np.array(X)
X = X.astype('float32')
X /= 255.0

#ラベルの変換

Y = np.array(Y)
Y = np_utils.to_categorical(Y,n_classes)
Y[:5]

#学習データとテストデータに分ける(テストデータ2割、学習データ8割)
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2)
#学習データ(8割)
print(X_train.shape)
#テストデータ(2割)
print(X_test.shape)
#学習データ(8割)
print(Y_train.shape)
#テストデータ(2割)
print(Y_test.shape)