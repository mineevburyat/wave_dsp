import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt


FORMAT = pyaudio.paUInt8  # Формат звука (16 бит, стерео)
CHANNELS = 1
RATE = 44100  # Частота дискретизации
CHUNK = 1024  # Размер блока данных


p = pyaudio.PyAudio()

# Запись звука
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []
print(RATE / CHUNK * 1)
for i in range(0, int(RATE / CHUNK * 3)):
    data = stream.read(CHUNK)
    frames.append(data)

# Остановка записи
stream.stop_stream()
stream.close()
print("play.....")
numpydata = np.frombuffer(b''.join(frames), dtype=np.uint8)
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
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True)

stream.write(numpydata)

# Остановка воспроизведения
stream.stop_stream()
stream.close()


# middle = np.mean(numpydata)
# num

with open('np_wave.npy', 'wb') as f:
    np.save(f, numpydata)
np.savetxt('np_vawe.txt', numpydata)

# wv = wave.open('wv_file.wav', 'wb')
# wv.setnchannels(1)
# wv.setsampwidth(1)

# print(wv)

p.terminate()