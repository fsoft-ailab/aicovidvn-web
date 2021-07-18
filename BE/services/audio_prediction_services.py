import pickle
import numpy as np
import librosa
import librosa.display
import os
import gc
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import tensorflow.keras.backend as K

from common import constant

# scaled_model = pickle.load(open("models/scaled-3-30-start-0-10-p100.pkl", 'rb'))
# loaded_model = pickle.load(open("models/svm-3-30-start-0-10-p100-prob.pkl", 'rb'))
# explained_model = pickle.load(open("models/explainer-3-30-start-0-10-p100-prob.pkl", 'rb'))
# vgg16_cough_bg = pickle.load(open("models/explainer-bg-denoise-cough-waveplot.pkl", 'rb'))
# vgg16_nose_bg = pickle.load(open("models/explainer-bg-denoise-breathe-nose-waveplot.pkl", 'rb'))
# vgg16_mouth_bg = pickle.load(open("models/explainer-bg-denoise-breathe-mouth-waveplot.pkl", 'rb'))
vgg16_cough_model = tf.keras.models.load_model("models/vgg16-denoise-cough-waveplot.h5")
vgg16_nose_model = tf.keras.models.load_model("models/vgg16-denoise-breathe-nose-waveplot.h5")
vgg16_mouth_model = tf.keras.models.load_model("models/vgg16-denoise-breathe-mouth-waveplot.h5")

e_cache = {
    "mouth": None,
    "nose": None,
    "cough": None
}


class AudioPredCNNService():
    def __load_audio(self, sound_dir):
        y, _ = librosa.load(sound_dir, sr=self.sr, mono=True, res_type="kaiser_fast")
        y = librosa.util.fix_length(y, self.sr * self.max_period)
        return y, len(y)

    def __generate_waveplot(self, y):
        plt.clf()
        plt.rcParams['figure.figsize'] = (10, 8)
        plt.axis('off')
        librosa.display.waveplot(y, sr=self.sr, x_axis='off', ax=None)
        base_path = os.path.abspath(self.base_dir)
        save_dir = os.path.join(base_path, 'waveplot.jpg')
        plt.savefig(save_dir)

        img = cv2.imread(save_dir)
        img = cv2.resize(img, (224, 224))
        img = tf.keras.applications.vgg16.preprocess_input(img)
        plt.close()
        return img

    def predict(self, sound_dir, type="cough"):
        self.sound_dir = sound_dir
        y, _ = self.__load_audio(sound_dir)
        img = self.__generate_waveplot(y)
        pred = self.__predict(np.asarray([img]), type)[0]
        K.clear_session()
        gc.collect()
        return float(pred[0])

    def __predict(self, imgs, type):
        if type == "cough":
            return self.vgg16_cough_model.predict(imgs)
        elif type == "mouth":
            return self.vgg16_mouth_model.predict(imgs)
        else:
            return self.vgg16_nose_model.predict(imgs)

    def visualize(self, sound_dir, dest=None, class_index=0, type="cough"):
        self.sound_dir = sound_dir
        y, _ = self.__load_audio(sound_dir)
        img = self.__generate_waveplot(y)

        K.clear_session()
        input_img = np.expand_dims(img, 0)

        if 'nose' == type:
            load_model = self.vgg16_nose_model
        elif type == "mouth":
            load_model = self.vgg16_mouth_model
        else:
            load_model = self.vgg16_cough_model

        gradModel = tf.keras.Model(
            inputs=[load_model.inputs],
            outputs=[load_model.get_layer('block3_conv1').output,  # block5_conv3
                     load_model.output])

        with tf.GradientTape() as tape:
            (convOutputs, predictions) = gradModel(input_img)
            label = class_index if class_index else predictions[0] > 0.5
            loss = predictions[0] if label else 1 - predictions[0]

        grads = tape.gradient(loss, convOutputs)

        castConvOutputs = tf.cast(convOutputs > 0, "float32")
        castGrads = tf.cast(grads > 0, "float32")
        guidedGrads = castConvOutputs * castGrads * grads

        convOutputs = convOutputs[0]
        guidedGrads = guidedGrads[0]

        weights = tf.reduce_mean(guidedGrads, axis=(0, 1))
        cam = tf.reduce_sum(tf.multiply(weights, convOutputs), axis=-1)
        cam = np.maximum(cam, 0)  # ReLU so we only get positive importance
        cam = cv2.resize(cam, (img.shape[1], img.shape[0]), cv2.INTER_NEAREST)
        cam = cam / cam.max()

        cam = np.uint8(255 * cam)
        cam = cv2.applyColorMap(cam, cv2.COLORMAP_JET)
        feature_dir = dest if dest else os.path.join(self.base_dir, "explain.jpg")
        cv2.imwrite(feature_dir, cam * .8 + img)

        K.clear_session()
        gc.collect()
        return feature_dir

    def __init__(self, sr=44800, max_period=30, submit_id=None, submit_time=None):
        self.sr = sr
        self.max_period = max_period
        self.submit_id = submit_id
        self.submit_time = submit_time
        self.base_dir = constant.TMP_DIR
        self.vgg16_cough_model = vgg16_cough_model
        self.vgg16_nose_model = vgg16_nose_model
        self.vgg16_mouth_model = vgg16_mouth_model
        if submit_id is not None:
            self.base_dir = "{}/{}".format(self.base_dir, submit_id)