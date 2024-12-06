# https://radioprog.ru/post/1025

import os
dir = '.'
files = os.listdir(dir)
for f in files:
    if f.endswith('.wav'):
        fp = open(f, 'rb')
        sig = fp.read(4).decode()
        is_add_fmt = False
        # print(os.path.getsize(f), end=' ')
        if sig != 'RIFF':
            print(fp.name, 'is not RIFF!')
            fp.close()
            continue
        sizechunk = int.from_bytes(fp.read(4), 'little') - 8
        sig_wav = fp.read(4).decode()
        if sig_wav != "WAVE":
            print(fp.name, "is not wave file!")
            fp.close()
            continue
        if fp.read(4).decode() != "fmt ":
            print("Ожидается fmt секция!")
            fp.close()
            continue
        print(fp.name, sizechunk)
        size_chunk_header = int.from_bytes(fp.read(4), 'little')
        if size_chunk_header > 16:
            print("Имеются доп данные!")
            is_add_fmt = True
        compress_code = int.from_bytes(fp.read(2), 'little')
        num_channels = int.from_bytes(fp.read(2), 'little')
        samp_rate = int.from_bytes(fp.read(4), 'little')
        bytes_per_sec = int.from_bytes(fp.read(4), 'little')
        block_size = int.from_bytes(fp.read(2), 'little')
        bits_quant = int.from_bytes(fp.read(2), 'little')
        
        print("\t размер заголовка формата", size_chunk_header)
        print("\t код компрессии ", compress_code)
        print("\t каналов ", num_channels)
        print("\t частота дескредитации ", samp_rate)
        print("\t байт в секунду ", bytes_per_sec)
        print("\t размер блока ", block_size)
        print("\t битов на сэмпл ", bits_quant)
        if is_add_fmt:
            add_fmt_size = int.from_bytes(fp.read(2), 'little')
            print("\t размер дополнительных заголовков ", add_fmt_size)
        if fp.read(4).decode() != "data":
            fp.close()
            print("ожидалось секция данные!")
            continue
        size_data_section = int.from_bytes(fp.read(4), 'little')
        print("\t размер секции данных ", size_data_section)
        for _ in range(size_data_section // block_size):
            if fp.read(block_size) == '':
                print("the end")
        while True:
            b = fp.read(1)
            if b:
                print(b, end=' ')
            else:
                break
        fp.close()
