import glob
from chardet.universaldetector import UniversalDetector

detector = UniversalDetector()
for filename in glob.glob("img/bmp.cpp"):
    print(filename.ljust(60), end='')
    detector.reset()
    for line in open(filename, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    print(detector.result)