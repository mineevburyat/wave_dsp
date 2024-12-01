import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt


FORMAT = pyaudio.paUInt8  # Формат звука (16 бит, стерео)
CHANNELS = 1
RATE = 120000  # Частота дискретизации
CHUNK = 1024  # Размер блока данных

# считываение сэмплов
numpydata = np.load('np_wave.npy', 'r')
print(numpydata)
# plot data
fig, ax = plt.subplots(facecolor ='#A0F0CC')
ax.set_ylim(np.min(numpydata) -10 , np.max(numpydata) + 10)
print(np.min(numpydata), np.max(numpydata))
ax.set_yticks([level for level in range(np.min(numpydata), np.max(numpydata)) if level % 10 == 0])
time_step = 1 / RATE
time_axis = [time for time in range(0, len(numpydata)) if time % 3000 == 0]
time_axis_str = [f"{time * time_step:4.2f}" for time in time_axis]
# print(time_axis)
# ax.set_xlim(0, len(numpydata) * time_step)
ax.set_xticks(time_axis, time_axis_str)
ax.grid()
ax.plot(numpydata)
plt.show()
# Воспроизведение записанного звука
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True)

stream.write(numpydata)

# Остановка воспроизведения
stream.stop_stream()
stream.close()


p.terminate()