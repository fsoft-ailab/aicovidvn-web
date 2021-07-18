# import pickle
# import numpy as np
# import librosa
# import librosa.display
# import os
# import gc
# import cv2
# import tensorflow as tf
# import matplotlib.pyplot as plt
# import tensorflow.keras.backend as K
#
# from utils import utils
# from utils.draw_cnn_explain_service import CNNExplain
# from common import constant
#
# # scaled_model = pickle.load(open("models/scaled-3-30-start-0-10-p100.pkl", 'rb'))
# # loaded_model = pickle.load(open("models/svm-3-30-start-0-10-p100-prob.pkl", 'rb'))
# # explained_model = pickle.load(open("models/explainer-3-30-start-0-10-p100-prob.pkl", 'rb'))
# vgg16_cough_bg = pickle.load(open("models/explainer-bg-denoise-cough-waveplot.pkl", 'rb'))
# vgg16_nose_bg = pickle.load(open("models/explainer-bg-denoise-breathe-nose-waveplot.pkl", 'rb'))
# vgg16_mouth_bg = pickle.load(open("models/explainer-bg-denoise-breathe-mouth-waveplot.pkl", 'rb'))
# vgg16_cough_model = tf.keras.models.load_model("models/vgg16-denoise-cough-waveplot.h5")
# vgg16_nose_model = tf.keras.models.load_model("models/vgg16-denoise-breathe-nose-waveplot.h5")
# vgg16_mouth_model = tf.keras.models.load_model("models/vgg16-denoise-breathe-mouth-waveplot.h5")
#
# e_cache = {
#     "mouth": None,
#     "nose": None,
#     "cough": None
# }
#
#
# class AudioPredCNNService():
#     def __load_audio(self, sound_dir):
#         y, _ = librosa.load(sound_dir, sr=self.sr, mono=True, res_type="kaiser_fast")
#         y = librosa.util.fix_length(y, self.sr * self.max_period)
#         return y, len(y)
#
#     def __generate_waveplot(self, y):
#         plt.clf()
#         plt.rcParams['figure.figsize'] = (10, 8)
#         plt.axis('off')
#         librosa.display.waveplot(y, sr=self.sr, x_axis='off', ax=None)
#         base_path = os.path.abspath(self.base_dir)
#         save_dir = os.path.join(base_path, 'waveplot.jpg')
#         plt.savefig(save_dir)
#
#         img = cv2.imread(save_dir)
#         img = cv2.resize(img, (224, 224))
#         img = tf.keras.applications.vgg16.preprocess_input(img)
#         plt.close()
#         return img
#
#     def predict(self, sound_dir, type="cough"):
#         self.sound_dir = sound_dir
#         y, _ = self.__load_audio(sound_dir)
#         img = self.__generate_waveplot(y)
#
#         if type == "cough":
#             predict_result = self.vgg16_cough_model.predict(np.asarray([img]))[0]
#         elif type == "mouth":
#             predict_result = self.vgg16_mouth_model.predict(np.asarray([img]))[0]
#         else:
#             predict_result = self.vgg16_nose_model.predict(np.asarray([img]))[0]
#
#         K.clear_session()
#         gc.collect()
#         return predict_result
#
#     def visualize(self, sound_dir, dest=None, type="cough"):
#         self.sound_dir = sound_dir
#         y, _ = self.__load_audio(sound_dir)
#         img = self.__generate_waveplot(y)
#
#         if dest is None:
#             cnn_exp = CNNExplain(dest="{}/{}".format(self.base_dir, "explain.jpg"))
#         else:
#             cnn_exp = CNNExplain(dest=dest)
#
#         if type == "cough":
#             if e_cache['cough'] is None:
#                 e = cnn_exp.get_explainer(vgg16_cough_model, vgg16_cough_bg)
#                 e_cache['cough'] = e
#             else:
#                 e = e_cache['cough']
#         elif type == "mouth":
#             if e_cache['mouth'] is None:
#                 e = cnn_exp.get_explainer(vgg16_mouth_model, vgg16_mouth_bg)
#                 e_cache['mouth'] = e
#             else:
#                 e = e_cache['mouth']
#         else:
#             if e_cache['nose'] is None:
#                 e = cnn_exp.get_explainer(vgg16_nose_model, vgg16_nose_bg)
#                 e_cache['nose'] = e
#             else:
#                 e = e_cache['nose']
#
#         feature_dir = cnn_exp.get_explain_image(e, img)
#         K.clear_session()
#         utils.resize_img(feature_dir, height=0.9, width=1, s_h=0.3, s_w=0, save=True)
#         gc.collect()
#         return feature_dir
#
#     def __init__(self, sr=44800, max_period=30, submit_id=None, submit_time=None):
#         self.sr = sr
#         self.max_period = max_period
#         self.submit_id = submit_id
#         self.submit_time = submit_time
#         self.base_dir = constant.TMP_DIR
#         self.vgg16_cough_model = tf.keras.models.load_model("models/vgg16-denoise-cough-waveplot.h5")
#         self.vgg16_nose_model = tf.keras.models.load_model("models/vgg16-denoise-breathe-nose-waveplot.h5")
#         self.vgg16_mouth_model = tf.keras.models.load_model("models/vgg16-denoise-breathe-mouth-waveplot.h5")
#         if submit_id is not None:
#             self.base_dir = "{}/{}".format(self.base_dir, submit_id)
#
# # class AudioPredSVMService():
# #     # Load audio from temp directory
# #     def __load_audio(self, sound_dir):
# #         y, _ = librosa.load(sound_dir, sr=self.sr)
# #         self.y = y
# #         self.audio_length = len(y)
# #
# #     # Padding audio using effective length
# #     def __padding_audio(self):
# #         effective_length = self.sr * self.max_period
# #         new_y = np.zeros(effective_length, dtype=self.y.dtype)
# #
# #         if self.audio_length < effective_length:
# #             new_y[0:self.audio_length] = self.y
# #         else:
# #             new_y[0:effective_length] = self.y[0:effective_length]
# #
# #         self.y = new_y.astype(np.float32)
# #
# #     # Calculate magnitude
# #     def __cal_magnitude(self, a):
# #         result = np.zeros((len(a)), dtype=np.float32)
# #
# #         for i in range(0, len(a)):
# #             a[i, :] = np.square(a[i, :])
# #             result[i] = np.sqrt(np.sum(a[i, :]))
# #
# #         return np.array(result)
# #
# #     def __pre_processing(self):
# #         self.mfccs = librosa.feature.mfcc(self.y, sr=self.sr, n_mfcc=self.n_mfcc)
# #         pca_result = self.pca.fit_transform(self.mfccs)
# #         pca_mag = self.__cal_magnitude(pca_result)
# #         mfccs_mean = np.mean(self.mfccs, axis=1)
# #         result = np.append(mfccs_mean, pca_mag)
# #         result = result.reshape(-1, len(result))
# #         result = scaled_model.transform(result)
# #         return result
# #
# #     def __get_feature_index(self, data):
# #         shap_values = self.explained_model.shap_values(data, nsamples=100)
# #         negative_label = shap_values[1][0]
# #         feature_indexs = np.nonzero(negative_label != 0)
# #         return feature_indexs[0]
# #
# #     def __init__(self, sr=44800, n_mfcc=128, n_components=50,
# #                  max_period=30):
# #         self.sr = sr
# #         self.max_period = max_period
# #         self.n_mfcc = n_mfcc
# #         self.pca = PCA(n_components=n_components)
# #
# #         # Check model is not empty
# #         if loaded_model is not None:
# #             self.svm_model = loaded_model
# #
# #         # Check scale model
# #         if scaled_model is not None:
# #             self.scaled_model = scaled_model
# #
# #         # Check explainer model
# #         if explained_model is not None:
# #             self.explained_model = explained_model
# #
# #     def _get_feature_image(self, data):
# #         try:
# #             feature_indexs = self.__get_feature_index(data)
# #             fig, ax = plt.subplots(figsize=(14, 5))
# #             X = librosa.stft(self.y)
# #             Xdb = librosa.amplitude_to_db(abs(X))
# #             # librosa.display.specshow(self.mfccs, sr=self.sr, x_axis='time')
# #             librosa.display.specshow(Xdb, sr=self.sr, x_axis='time')
# #             lims = ax.get_ylim()
# #             ax.hlines(feature_indexs, lims[0], lims[1], color='linen', linestyle='--',
# #                       linewidth=1.5, alpha=0.5, label='Abnormal')
# #             ax.legend()
# #
# #             fig.savefig('tmp/tmp.jpg')
# #
# #             return utils.get_base64_image_from_dir(img_dir='tmp/tmp.jpg', height=0.9, width=1, s_h=0.3, s_w=0)
# #         except Exception as e:
# #             raise e
# #
# #     def predict(self, sound_dir):
# #         self.sound_dir = sound_dir
# #         self.__load_audio(self.sound_dir)
# #         self.__padding_audio()
# #         result = self.__pre_processing()
# #         predict_result = list(self.svm_model.predict_proba(result)[0])
# #         return predict_result
# #
# #     def visualize(self, sound_dir):
# #         self.sound_dir = sound_dir
# #         self.__load_audio(self.sound_dir)
# #         self.__padding_audio()
# #         result = self.__pre_processing()
# #         feature_image = self._get_feature_image(result)
# #         return feature_image
