import usb.core
import usb.util

# находим наше устройство
dev = usb.core.find(idVendor=0x051d, idProduct=0x0002)

# оно было найдено?
if dev is None:
    raise ValueError('Device not found')

# поставим активную конфигурацию. Без аргументов, первая же
# конфигурация будет активной
# dev.set_configuration()

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]