command-line tool that lets you communicate with a device.

install 
turn on adb debugging on devices(phone)

query for device
adb devices -l

If multiple devices are running, you must specify the target device when you issue the adb command.

for all commands -> 
    adb shell ls /system/bin

cheatsheet here
https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8

`adb shell input touchscreen swipe 500 500 500 500 20000`

ppadb.client()

adb = Client(host='127.0.0.1',port=5037)

device = adb.devices()[0]

device.shell('adb shell input touchscreen swipe 500 500 500 500 20000')

image = device.screencap()

pip install pure-python-adb
https://stackoverflow.com/questions/3437686/how-to-use-adb-to-send-touch-events-to-device-using-sendevent-command

adb shell input tap x y

adb shell input text "insert%syour%stext%shere"

//enter
adb shell input keyevent 66

