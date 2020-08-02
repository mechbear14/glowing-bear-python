from typing import List, Dict
import pyaudio
import numpy
from scipy.fft import fft
from scipy.signal.windows import blackman
from os import path
from PIL import Image


class TextureBuilder:
    def __init__(self, audio_devices: List[Dict]):
        self.device_id = -1
        self.sampling_rate = 0
        self.channels = 0

        self.audio_devices = audio_devices
        input_devices = [device for device in audio_devices
                         if device["maxInputChannels"] > 0]

        if len(input_devices) < 1:
            raise IOError("No input devices available")
        elif len(input_devices) > 1:
            indices = [device["index"] for device in input_devices]
            device_choice = -1
            while indices.count(device_choice) == 0:
                for device in input_devices:
                    print(device)
                device_choice = int(input("Select an input device: "))
            device_id = device_choice
            self.set_device_id(device_id)
        else:
            device_id = input_devices[0]["index"]
            self.set_device_id(device_id)

        self.time_buffer = None
        self.freq_buffer = None

    def set_device_id(self, device_id: int):
        self.device_id = device_id
        device_info = self.audio_devices[device_id]
        self.channels = device_info["maxInputChannels"]
        self.sampling_rate = int(device_info["defaultSampleRate"])

    def make_texture(self, in_data, frame_count, time_info, status):
        frames = memoryview(in_data).cast("f")
        frame_values = numpy.array(frames.tolist())
        if self.time_buffer is None:
            self.time_buffer = numpy.zeros([4 * frame_count])
        self.time_buffer[0:-frame_count] = self.time_buffer[frame_count:]
        self.time_buffer[-frame_count:] = numpy.array(frame_values)
        window = blackman(4 * frame_count)
        audio_spectrum = fft(self.time_buffer * window)
        self.freq_buffer = 20 * numpy.log10(numpy.abs(audio_spectrum[0:2 * frame_count]) / (2 * frame_count))
        return in_data, pyaudio.paContinue


class GlowImage:
    def __init__(self, filepath: str):
        self.image = None
        self.buffer = None
        self.set_image_path(filepath)

    def set_image_path(self, filepath: str):
        current_path = path.abspath(path.curdir)
        while self.image is None:
            if filepath[0] == "/":
                image_path = filepath
            else:
                image_path = path.join(current_path, filepath)
            try:
                self.image = Image.open(image_path)
            except OSError:
                print(OSError.strerror)
            else:
                brightness = numpy.array(self.image.convert("L")) / 255
                rows, cols = brightness.shape
                row = numpy.flip(numpy.arange(0, rows)).reshape((rows, 1)).repeat(cols, axis=1)
                col = numpy.arange(0, cols).reshape((1, cols)).repeat(rows, axis=0)
                buffer_data = numpy.array([row, col, brightness])
                self.buffer = buffer_data.reshape(rows * cols * 3, order='F').astype(numpy.float)
