# CardReader Summary
- This project is to design a Raspberry Pi Zero badge reader to record attendance at meetings.  It uses a picam with the IR filter.
- The administrator interface is an ad hoc web connection.  THe administrator's phone is used to control the application.
- The administrator first loads primary keys to the records they wish to associate with the attendees.  These primary keys are entered by QRCode.
- The administrator then uses the phone UI to set it in read mode.
- Employees hold their barcode near the reader and a Pi library reads and decodes the barcode.


# Procedure
To install git on the Raspberry Pi:
>sudo apt install git

To clone this repository:
>git clone https://github.com/RaisingAwesome/CardReader.git

If picamera has not yet been installed on the Pi for Python3, type:
>sudo pip3 picamera

Run it:
>sudo python3 cardreader.py

Test it in a browser on the network with its IP number as found on your router it is connected to:
>http://192.xxx.xxx.xxx/
