from typing import List, Dict

import numpy
import pyaudio


class TextureBuilder:
    def __init__(self):
        self.device_id: int
        self.channels: int
        self.sampling_rate: int
        self.stream: pyaudio.Stream
        self.devices: List[Dict]
        self.frequency_db: numpy.ndarray
        self.texture_id: int

    @staticmethod
    def get_input_devices():
        p = pyaudio.PyAudio()
        devices = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]
        input_devices = [device for device in devices
                         if device["maxInputChannels"] > 0]
        return input_devices
