"""
"""
from __future__ import division

import math
import os
import warnings

import numpy as np
import scipy.io.wavfile
import scipy.signal
from picklable_itertools import cycle
from picklable_itertools.extras import partition_all
from tqdm import tqdm
from keras.utils.data_utils import Sequence

class DataSequence(Sequence):

    def __init__(self, dirname, sample_rate, fragment_length, batch_size, fragment_stride, nb_output_bins, learn_all_outputs, use_ulaw):
        self.batch_size = batch_size
        self.use_ulaw = use_ulaw
        self.sample_rate = sample_rate
        self.dirname = dirname
        self.fragment_length = fragment_length
        self.fragment_stride = fragment_stride
        ulaw_extension = '.ulaw' if use_ulaw else ''
        self.cache_extension = ".%d%s.npy" % (self.sample_rate, ulaw_extension)
        # Filenames with extension to allow quickly finding wavs that have not yet
        # been processed
        self.wavs, self.caches = self.find_wavs_and_caches()
        self.process_wavs()
        sequences = self.load_caches()
        self.indices = []
        for sequence in sequences:
            for index in range(0, len(sequence) - self.fragment_length, self.fragment_stride):
                self.indices.append(index)
        self.x = np.concatenate(sequences)

    def __len__(self):
        print("len is %d" % (len(self.indices) // self.batch_size))
        return len(self.indices) // self.batch_size

    def __getitem__(self, idx):
        X = np.zeros((self.batch_size, self.fragment_length, 256), dtype='uint8')
        Y = np.zeros((self.batch_size, self.fragment_length, 256), dtype='uint8')
        for batch_index, start_index in enumerate(range(idx * self.batch_size, (idx + 1) * self.batch_size)):
           for fragment_index, sequence_index in enumerate(range(start_index, start_index + self.fragment_length)):
               X[batch_index][fragment_index][self.x[sequence_index]] = 1
               Y[batch_index][fragment_index][self.x[sequence_index + 1]] = 1
        return (X, Y)

    def find_wavs_and_caches(self):
        wav_files = {fn.name[0:-4] for fn in os.scandir(self.dirname) if fn.name.endswith('.wav')}
        caches = {fn.name[0:-len(self.cache_extension)] for fn in os.scandir(self.dirname) if fn.name.endswith(self.cache_extension)}
        return (wav_files, caches)

    def process_wavs(self):
       for wav_file in self.wavs - self.caches:
           sequence = process_wav(wav_file)
           np.save(os.path.join(set_dirname, "%s%s" % (wav_file, cache_extension)), sequence)


    def load_caches(self):
       return [np.load(fn.path, encoding='bytes') for fn in os.scandir(self.dirname) if fn.name.endswith(self.cache_extension)]

    def process_wav(self, wav):
        filename = os.path.join(self.dirname, "%s.wav" % wav)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            file_sample_rate, audio = scipy.io.wavfile.read(filename)
            audio = wav_to_float(ensure_mono(audio))
            if self.use_ulaw:
                audio = ulaw(audio)
            audio = ensure_sample_rate(self.sample_rate, file_sample_rate, audio)
            audio = float_to_uint8(audio)
        return audio


    def ulaw(x, u=255):
        x = np.sign(x) * (np.log(1 + u * np.abs(x)) / np.log(1 + u))
        return x


def float_to_uint8(x):
    x += 1.
    x /= 2.
    uint8_max_value = np.iinfo('uint8').max
    x *= uint8_max_value
    x = x.astype('uint8')
    return x


def wav_to_float(x):
    try:
        max_value = np.iinfo(x.dtype).max
        min_value = np.iinfo(x.dtype).min
    except:
        max_value = np.finfo(x.dtype).max
        min_value = np.iinfo(x.dtype).min
    x = x.astype('float64', casting='safe')
    x -= min_value
    x /= ((max_value - min_value) / 2.)
    x -= 1.
    return x


def ulaw2lin(x, u=255.):
    max_value = np.iinfo('uint8').max
    min_value = np.iinfo('uint8').min
    x = x.astype('float64', casting='safe')
    x -= min_value
    x /= ((max_value - min_value) / 2.)
    x -= 1.
    x = np.sign(x) * (1 / u) * (((1 + u) ** np.abs(x)) - 1)
    x = float_to_uint8(x)
    return x

def ensure_sample_rate(desired_sample_rate, file_sample_rate, mono_audio):
    if file_sample_rate != desired_sample_rate:
        mono_audio = scipy.signal.resample_poly(mono_audio, desired_sample_rate, file_sample_rate)
    return mono_audio


def ensure_mono(raw_audio):
    """Just use first channel."""
    if raw_audio.ndim == 2:
        raw_audio = raw_audio[:, 0]
    return raw_audio

