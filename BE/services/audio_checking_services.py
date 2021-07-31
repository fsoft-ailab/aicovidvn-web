import librosa
import json
import numpy as np
import matplotlib.pyplot as plt
import cv2
import base64
import os
import noisereduce as nr
from instance import environment
from common import constant
from scipy.signal import find_peaks


class AudioCheckServices():
    # min_period: Min period required of audio
    # max_period: Max period required of audio
    # max_noise_period: Max noise period in audio
    def __init__(self, sr=44800, min_period=10, max_period=20, max_noise_period_weight=0.5):
        self.sr = sr
        self.min_period = min_period
        self.max_period = max_period
        self.max_noise_period_weight = max_noise_period_weight
        self.base_dir = constant.TMP_DIR

    def _convert_range(self, group_range, y, len_y, thres=1000):
        convert_range_result = []
        new_y = np.zeros(len_y)
        for item in group_range:
            first = item[0]
            last = item[1]
            if first - thres >= 0:
                first = first - thres

            if last + thres <= len_y:
                last = last + thres
            else:
                last = len_y
            new_y[first:last] = y[first:last]
            convert_range_result.append([first, last])

        return new_y, convert_range_result

    def _group_peaks_range(self, y, thres=10000):
        peaks, _ = find_peaks(y, height=np.max(y) / 2.5, distance=500)
        result = []
        cur_group = [0, 0]
        is_start = False
        sec_step = False
        for index in range(0, len(peaks)):
            if index == 0:
                cur_group[0] = peaks[index]
                is_start = True
                continue

            if cur_group[1] == 0 and is_start and peaks[index] - cur_group[0] < thres:
                cur_group[1] = peaks[index]
                is_start = False

                if index + 1 == len(peaks) and cur_group[1] != 0:
                    result.append(cur_group)

                continue

            if peaks[index] - cur_group[1] < thres:
                cur_group[1] = peaks[index]
                sec_step = False
            else:
                if cur_group[1] != 0 and not sec_step:
                    result.append(cur_group)
                cur_group = [0, 0]
                cur_group[0] = peaks[index]
                is_start = True
                sec_step = True

            if index + 1 == len(peaks) and cur_group[1] != 0:
                result.append(cur_group)

        return result

    def _generate_waveplot(self, denoised_audio, noise_audio):
        plt.clf()
        # plt.rcParams['figure.figsize'] = (20, 8)
        plt.axis('off')
        plt.plot(noise_audio, label="noise")
        plt.plot(denoised_audio, label="normal")
        plt.legend(loc="upper right", prop={'size': 15})
        base_path = os.path.abspath(self.base_dir)
        save_dir = os.path.join(base_path, 'check-sound.jpg')
        plt.savefig(save_dir)

        img = cv2.imread(save_dir)
        img = cv2.resize(img, (600, 300))
        _, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer).decode()
        plt.close()
        return jpg_as_text

    def _get_noise_audio(self, convert_range_result, y, len_y):
        new_y = y.copy()
        for item in convert_range_result:
            first = item[0]
            last = item[1]
            new_y[first:last] = 0
        return new_y

    def _denoise(self, y, thres_start=10000, thres_end=8000):
        group_range = self._group_peaks_range(y, thres=thres_start)
        denoised_audio, convert_range_result = self._convert_range(group_range, y, len(y), thres=thres_end)
        noise_audio = self._get_noise_audio(convert_range_result, y, len(y))
        return denoised_audio, noise_audio, len(group_range)

    def _get_noise(self, y, thres_start=3000, thres_end=15000):
        group_peak = self._group_peaks_range(y)
        y_noise = y.copy()
        for peak_item in group_peak:
            y_noise[peak_item[0] - thres_start:peak_item[1] + thres_end] = 0
        return y_noise

    def check(self, sound_dir, fix_length=True):
        y, sr = self._load_file(sound_dir=sound_dir, fix_length=fix_length)
        y, _ = librosa.effects.trim(y)
        denoised_audio, noise_audio, count = self._denoise(y, thres_start=10000, thres_end=8000)

        duration = librosa.get_duration(y, sr)
        noise_duration = librosa.get_duration(noise_audio[(noise_audio >= 0.001) | (noise_audio <= -0.001)], sr)
        is_duration_pass = duration >= self.min_period
        is_noise_pass = noise_duration / duration <= self.max_noise_period_weight

        if environment.AUDIO_FILTER == constant.ENABLE_AUDIO_FILTER:
            if not is_noise_pass or count < 3:
                b64_waveplot = self._generate_waveplot(denoised_audio, noise_audio)
                return json.dumps({'duration': is_duration_pass,
                                   'noise': is_noise_pass,
                                   'count': count,
                                   'img': b64_waveplot})
            else:
                return json.dumps({'duration': is_duration_pass,
                                   'noise': is_noise_pass,
                                   'count': count})
        else:
            return json.dumps({'duration': True, 'noise': True, 'count': 3})

    def _load_file(self, sound_dir, fix_length=True):
        y, sr = librosa.load(sound_dir, sr=self.sr, mono=True, res_type="kaiser_fast")
        if fix_length:
            y = librosa.util.fix_length(y, self.sr * self.max_period)
        return y, sr
