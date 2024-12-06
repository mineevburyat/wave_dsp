# https://habr.com/ru/articles/113239/

import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import struct

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def format_time(x, pos=None):
    global duration, nframes, k
    progress = int(x / float(nframes) * duration * k)
    mins, secs = divmod(progress, 60)
    hours, mins = divmod(mins, 60)
    out = "%d:%02d" % (mins, secs)
    if hours > 0:
        out = "%d:" % hours
    return out

def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return "-inf"

    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)

wav = wave.open("202411151531_989085960151-Зайцева_mainserverdss-1731655896.1060.wav", mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
print(nchannels, sampwidth, framerate, nframes, comptype, compname)
duration = nframes / framerate
w, h = 800, 300
k = nframes / w / 32
DPI = 72
peak = 256 ** sampwidth // 2
print(duration, k, peak)

content = wav.readframes(nframes)
samples = np.frombuffer(content, dtype=types[sampwidth])
print(samples)
plt.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
plt.subplots_adjust(wspace=0, hspace=0)

for n in range(nchannels):
    channel = samples[n::nchannels]

    channel = channel[0::int(k)]
    if nchannels == 1:
        channel = channel - peak
    print(channel)
    axes = plt.subplot(2, 1, n+1)
    axes.plot(channel, "g")
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
    plt.grid(True, color="w")
    axes.xaxis.set_major_formatter(ticker.NullFormatter())

axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
plt.savefig("wave", dpi=DPI)
plt.show()


wav_file=wave.open("output1.wav","w")

# wav params
nchannels = 1
sampwidth = 2

# 44100 is the industry standard sample rate - CD quality.  If you need to
# save on file size you can adjust it downwards. The stanard for low quality
# is 8000 or 8kHz.
nframes = len(channel)
comptype = "NONE"
compname = "not compressed"
wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))

# WAV files here are using short, 16 bit, signed integers for the 
# sample size.  So we multiply the floating point data we have by 32767, the
# maximum value for a short integer.  NOTE: It is theortically possible to
# use the floating point -1.0 to 1.0 data directly in a WAV file but not
# obvious how to do that using the wave module in python.
for sample in samples[-1::-nchannels]:
    # print(sample)
    wav_file.writeframes(struct.pack('h', int(sample) ))

wav_file.close()
