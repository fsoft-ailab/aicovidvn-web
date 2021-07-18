import librosa
import json
import numpy as np
import matplotlib.pyplot as plt
import cv2
import base64
import os
from instance import environment
from common import constant
from scipy.signal import find_peaks


class AudioCheckServices():
    # min_period: Min period required of audio
    # max_period: Max period required of audio
    # max_noise_period: Max noise period in audio
    def __init__(self, sr=44800, min_period=10, max_period=20, max_noise_period=3):
        self.sr = sr
        self.min_period = min_period
        self.max_period = max_period
        self.max_noise_period = max_noise_period
        self.base_dir = constant.TMP_DIR

    def _group_peaks_range(self, y, thres=10000):
        peaks, _ = find_peaks(y, height=np.max(y) / 2, distance=500)
        result = []
        cur_group = [0, 0]
        is_start = True
        for index in range(0, len(peaks)):
            if index == 0:
                cur_group[0] = peaks[index]
                continue

            if cur_group[1] == 0 or is_start:
                cur_group[1] = peaks[index]
                is_start = False
                continue

            if peaks[index] - cur_group[1] < thres:
                cur_group[1] = peaks[index]
            else:
                result.append(cur_group)
                cur_group = [0, 0]
                cur_group[0] = peaks[index]
                is_start = True

            if index + 1 == len(peaks):
                result.append(cur_group)

        return result

    def _generate_waveplot(self, y):
        plt.clf()
        plt.rcParams['figure.figsize'] = (10, 8)
        plt.axis('off')
        librosa.display.waveplot(y, sr=self.sr, x_axis='off', ax=None)
        base_path = os.path.abspath(self.base_dir)
        save_dir = os.path.join(base_path, 'check-sound.jpg')
        plt.savefig(save_dir)

        img = cv2.imread(save_dir)
        img = cv2.resize(img, (224, 224))
        _, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer).decode()
        plt.close()
        return jpg_as_text

    def _get_noise(self, y, thres_start=3000, thres_end=15000):
        group_peak = self._group_peaks_range(y)
        y_noise = y.copy()
        for peak_item in group_peak:
            y_noise[peak_item[0] - thres_start:peak_item[1] + thres_end] = 0
        return y_noise

    def check(self, sound_dir, fix_length=True):
        y, sr = self._load_file(sound_dir=sound_dir, fix_length=fix_length)
        b64_waveplot = self._generate_waveplot(y)
        y, _ = librosa.effects.trim(y)
        duration = librosa.get_duration(y, sr)
        noise_duration = librosa.get_duration(self._get_noise(y), sr)
        is_duration_pass = duration >= self.min_period
        is_noise_pass = noise_duration <= self.max_noise_period

        if environment.AUDIO_FILTER == constant.ENABLE_AUDIO_FILTER:
            return json.dumps({'duration': is_duration_pass,
                               'noise': is_noise_pass,
                               'img': b64_waveplot})
        else:
            return json.dumps({'duration': True, 'noise': True})

    def _load_file(self, sound_dir, fix_length=True):
        y, sr = librosa.load(sound_dir, sr=self.sr, mono=True, res_type="kaiser_fast")
        if fix_length:
            y = librosa.util.fix_length(y, self.sr * self.max_period)
        return y, sr
