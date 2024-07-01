Course: 1DT305 – Tillämpad Internet of Things, introduktion ST24

Where: Linnæus University

By: Shayan Eivaz Khani

Uni-Username: se223xv



# Overview

I will use raspberry pi pico with Adafruit SHT31-D Temperature & Humidity Sensor to show the temprature and humidity of a room.

# Material

• Raspberry pi pico

• Adafruit SHT31-D Temperature & Humidity Sensor


# Computer Setup

I used Thonny to flash the Pi Pico.

# Putting everything together


# The code
```
import network
import socket
import time
from machine import Pin

led = Pin(15, Pin.OUT)

ssid = 'wifi_name'
password = 'wifi_password'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Pico W</title>
    </head>
    <body>
        <h1>Pico W</h1>
        <p>Hello World</p>
    </body>
</html>
"""

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('Server ip = ' + status[0] + '\n')

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        response = html
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')



```


# Transmitting the data / connectivity
I will create a local HTTP server on the Pi Pico and read values from humidity sensor and then send that value inside an HTML file to the client that makes requests to the server.

# Presenting the data

I will use CSS to style the data inside the HTML file. I will also add javascript code so that the client will use short polling to continuosly get the current temprature and humidity of the room from the sensor connected to the Pi Pico.

# Finalizing the design
