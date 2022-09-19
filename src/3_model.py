import os
import pickle
from keras.applications.vgg16 import VGG16
from keras.models import Sequential
from keras.models import model_from_json
from keras.models import Model
from keras.layers import Input, Activation, Concatenate, Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam

#vgg16
input_tensor = Input(shape=(224,224,3))
#最後の1000の層を省く
base_model = VGG16(weights='imagenet', input_tensor=input_tensor,include_top=False)

#フォルダをクラス名にする
path = "../data/img"
folders = os.listdir(path)

#フォルダ名を抽出
classes = [f for f in folders if os.path.isdir(os.path.join(path, f))]
n_classes = len(classes)

#後付けで入れたい層の作成
top_model = Sequential()
top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
top_model.add(Dense(n_classes, activation='softmax'))


#結合
model = Model(inputs=base_model.input, outputs=top_model(base_model.output))


#学習させない層
for layer in model.layers[:15]:
  layer.trainable = False

print('# layers=', len(model.layers))

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

model.summary()

#クラス名の保存
pickle.dump(classes, open('classes.sav', 'wb'))
#モデルの保存
model.save('cnn.h5')