import pyaudio
import time
import numpy
from scipy.fft import fft
from scipy.signal.windows import blackman

p = pyaudio.PyAudio()

input_device = None
audio_frame_buffer = None

# Get devices
count = p.get_device_count()
devices = [p.get_device_info_by_index(index)
           for index in range(count)]
input_devices = [device for device in devices
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
    input_device = device_choice
else:
    input_device = input_devices[0]["index"]


def callback(in_data, frame_count, time_info, status):
    frames = memoryview(in_data).cast("f")
    frame_values = numpy.array(frames.tolist())
    global audio_frame_buffer
    if audio_frame_buffer is None:
        audio_frame_buffer = numpy.zeros([4 * frame_count])
    audio_frame_buffer[0:-frame_count] = audio_frame_buffer[frame_count:]
    audio_frame_buffer[-frame_count:] = numpy.array(frame_values)
    window = blackman(4 * frame_count)
    audio_spectrum = fft(audio_frame_buffer * window)
    audio_spectrum_db = 20 * numpy.log10(numpy.abs(audio_spectrum[0:2 * frame_count]) / (2 * frame_count))
    texture_coords = numpy.linspace(20, 145, 8).astype(numpy.int8)
    texture = audio_spectrum_db[texture_coords]
    print(texture)
    return in_data, pyaudio.paContinue


device_info = p.get_device_info_by_index(input_device)
stream = p.open(format=pyaudio.paFloat32,
                input=True, output=False,
                input_device_index=input_device,
                channels=device_info["maxInputChannels"],
                rate=int(device_info["defaultSampleRate"]),
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
p.terminate()
