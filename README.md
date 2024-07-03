##### Course: 1DT305 – Tillämpad Internet of Things, introduktion ST24, Linnæus University
##### Assignment: mandatory public project repo 
##### By: Shayan Eivaz Khani
##### Uni-Username: se223xv

# Overview
I will use a Raspberry Pi Pico WH with Adafruit SHT31-D Temperature & Humidity Sensor to show the temprature and humidity of a room.
Apart from buying the materials needed and the time it takes for the delivery and soldering header strip pins that comes with the Adafruit sensor, this project will not take more than 30 minutes to assemble and program by following the description below.

# Objective
Sometimes while studying i feel a bit cold, specially during the winter because of the cold weather in Sweden and this disrupts my workflow/concentration. Most of those times i have come to realize that it has more to do with my eating routines rather than if the room is actually cold. The goal of this project is to make a device that i can just connect whenever i plan sit down to work for couple of hours. This device will repeatedly measure the temprature of the room so i can just click 2 buttons whenever needed on my laptop to get the measurments quickly so that i know for sure if i need to take break and go eat something or is it that the room is too cold and i have to turn on a heater or close the window.

# Materials needed

![“›” 2024-07-03 at 14 37 40](https://github.com/shayaneivazkhani/1DT305/assets/105381967/7f2b73b6-3288-4d83-9687-c681199d48a8)

I bought the materials for my project from [electrokit](https://www.electrokit.com)

| units | Link                                                       | Price (SEK) | Reason needed |
|-------|------------------------------------------------------------|-------------|----------|
| 1 | Raspberry Pi Pico WH                                           | 88   |  Being able to connect to the Adafruit sensor and recieve data from it to show the temperature and humidity|
| 1 | USB-kabel A-hane - micro B hane 1.8m                           | 32   |  Power up and program Raspberry Pi Pico WH via computer               |
| 1 | Adafruit Sensirion SHT31-D Temperatur & luftfuktighetssensor   | 184  |  Measure temperature and humidity               |
| 1 | Kopplingsdäck 400 anslutningar                                 | 40   |  Connect electrical components without need for soldering               |
| 1 | Kopplingsdäck 170 anslutningar                                 | 35   |  Connect electrical components without need for soldering                  |
| 1 | Labbsladd 20-pin 15cm hane/hane                                | 29   |  Electrical conductivity         |

#### total cost: 408 SEK


# Step 1 of 2: Putting everything together
How all the electronics is connected, aside from the usb that connects the Raspberry Pi Pico to the computer: 
![“›” 2024-07-02 at 05 57 47](https://github.com/shayaneivazkhani/1DT305/assets/105381967/ede26b74-6c30-48c4-85a4-f14c98a7a5f3)

# Step 2 of 2: Computer setup and usage

### Setup and usage (beginner):
Simplest guide to set up your computer whether you have Mac or Windows is by following this guide [Raspberry Pi Pico W LESSON 1: Write Your First Program for Absolute Beginners](https://www.youtube.com/watch?v=SL4_oU9t8Ss&list=PLGs0VKk2DiYz8js1SJog21cDhkBqyAhC5) and just replacing the code with what i have written in file `temperature_humidity_sensor.py` [here.](https://github.com/shayaneivazkhani/1DT305/blob/main/temperature_humidity_sensor.py)
But remember to provide your wifi credentials (very important!) in lines 207–208 in file `temperature_humidity_sensor.py` [here](https://github.com/shayaneivazkhani/1DT305/blob/main/temperature_humidity_sensor.py)
```
ssid = 'Wifi-name'
password = 'Wifi-password'
```

Then all you have to do is to press the green START/PLAY button at the top left of the Thonny window. 

<img width="799" alt="“›” 2024-07-02 at 08 17 50" src="https://github.com/shayaneivazkhani/1DT305/assets/105381967/5e1d05df-5f79-4fbb-a821-1cc32c6636d9">

After pressing the START/PLAY button if you look at the bottom of the Thonny window, a blue URL will be printed if your wifi credentials is correct, and pressing the blue URL  will open your browser and take you to the webpage that the Raspberry Pi Pico provides and updates with values from the temprature sensor.

<img width="956" alt="“›” 2024-07-02 at 08 20 46" src="https://github.com/shayaneivazkhani/1DT305/assets/105381967/d9f0661a-75ea-49fd-850e-fd004b83a65f">


### Setup (experienced):
I used Thonny to flash the Pi Pico. Just provide your wifi credentials in lines 207–208.

# Details about the project

## Higher level description of the fundamental parts of the project code

 Hardest part about this project was to not use a external library for reading the sensor measurments, instead opening the datasheet for SHT3x-DIS SENSIRION and trying to understand the low level timing diagram of input to the sensor and correct reading format of the 48 bits when it outputs as the measurments.
#### lines 9–31 in temperature_humidity_sensor.py
```
# Sensor's I2C address
sensor_address = 0x44

# Command to start measurement (Measurement commands in single shot mode, 0x2C0D –> Repeatability set to medium, ClockStretching set to enabled)
measurement_command = bytearray([0x2C, 0x0D])

def start_measurement():
    i2c.writeto(sensor_address, measurement_command)

def read_measurement():
    # Reading 6 bytes: 2 bytes temperature, 1 byte checksum, 2 bytes humidity, 1 byte checksum
    data = i2c.readfrom(sensor_address, 6)
    return data

def process_measurement(data):
    temperature_raw = data[0] << 8 | data[1]
    humidity_raw = data[3] << 8 | data[4]
    
    # Convert raw values to actual temperature and humidity
    temperature = -45 + 175 * (temperature_raw / 65535)
    humidity = 100 * (humidity_raw / 65535)
    
    return humidity, temperature
```

And most important part of creating the server was to differentiate the HTTP start line to decide if the client only wants the page (GET / HTTP/1.1) or just the latest measurment from the sensor (GET /update HTTP/1.1).
#### lines 253–271 in temperature_humidity_sensor.py
```
if url == '/':
            # Update HTML template with current values
            updated_html = update_html_with_sensor_data(html_template, temperature, humidity)
            
            # Send HTTP response
            response = (
                'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/html\r\n'
                'Content-Length: {}\r\n\r\n'
                '{}'.format(len(updated_html), updated_html)
            )
        elif url == '/update':
            # Send just the temperature and humidity data
            response_data = 'Temperature: {:.2f}, Humidity: {:.2f}'.format(temperature, humidity)
            response = (
                'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/plain\r\n'
                'Content-Length: {}\r\n\r\n'
                '{}'.format(len(response_data), response_data)
```

## Transmitting the data / connectivity 

Data that is measured from the sensor is placed inside a `html_template` and is transmitted to the client over the Wi-Fi network over TCP/IP. The Pi Pico is set up as a web server, listening for HTTP requests on port 80 and responding with HTML content or plain text based on the type of incoming request. The `html_template` contains code that will update the temperature and humidiy values by making automatic requests to the server every 0,5 seconds. I choose to connect the Pi Pico to the wifi because this device will be in my room when it's used, and my room has a Wifi router that is allways turned on.

I set up the HTTP server based on page 21 of the Raspberry Pi Pico's [documentation](https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf?_gl=1*q9tyvf*_ga*MTc4NTg2NTY3Mi4xNzIwMDIxMDI2*_ga_22FD70LWDS*MTcyMDAzMDAzMy4yLjEuMTcyMDAzMDA1NC4wLjAuMA..) found [here](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) 


Most imortant part of setting up the server is following:
#### Initializing and configuring a WLAN Interface (WiFi Interface) on the Raspberry Pi Pico W, i.e. enabling the Wi-Fi capabilities of the hardware, then start to connect to the wifi router (the access point).
##### lines 210–212
```
wlan = network.WLAN(network.STA_IF) ––> Creates a WLAN object that provides various methods we can use to control and manage Wi-Fi connections (a Wifi interface in our case) via the Wi-Fi hardware on the Pi Pico. network.STA_IF: parameter configures the WLAN interface to operate in "Station" mode. Configuringthe WLAN as a station means the device will act as a client that connects to an existing wireless network (similar to how a smartphone or laptop connects to a Wi-Fi network). This is opposed to "Access Point" mode, where the device would create its own Wi-Fi network for other devices to connect to.
wlan.active(True)                   ––> Powers on the WLAN hardware (Wifi hardware) which is necessary for starting searching for and connecting to Wi-Fi networks.
wlan.connect(ssid, password)        ––> Begins to connect to the specified Wi-Fi network using the provided SSID (network name) and password.
```

#### Create a Socket object to accept HTTP requests on port 80 from any network interface on the Raspberry Pi Pico WH
##### lines 232–235
```
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]  ––> *
s = socket.socket()                              ––> Creates a new socket object. A socket is an TCP/IP endpoint for HTTP communication.
s.bind(addr)                                     ––> Binds the socket to an address, i.e. assigning a specific IP address and port number to the socket allowing it to listen for incoming HTTP connections for incoming connections on that adress.
s.listen(1)                                      ––>  Puts the socket into listening mode, waiting for incoming connection requests. The parameter specifies the maximum number of queued connections. In this case, it allows only one connection to be queued while the server is busy handling the current connection.
```

###### * socket.getaddrinfo('0.0.0.0', 80): This is a function in Python's socket module takes a host name and port number and returns a list of tuples each containing information  in a format that can be used by the network functions, to bind a socket in our case.
###### * 0.0.0.0: This IP address is a special address used to bind the socket to any IP address assigned to the machine (e.g. 192.168.1.5 on Wi-Fi, another number on Ethernet, etc.) This is useful when you want the server to be accessible regardless of which interface the request comes through (e.g. Wi-Fi, Ethernet if available). 
###### * 80: This is the default port for HTTP traffic. By specifying port 80, the server is set up to handle HTTP requests, which is typical for a web server.
###### * [0][-1]: The use of negative indexing in Python, such as -1 in [0][-1], is a feature that allows accessing elements from the end of a list. Here we choose the last element ,[-1], of the first tuple, [0].

## Presenting the data and the platform

I did not use any external platform for creating the UI and connecting it to the data recieved by the Pi Pico. I used CSS inside `<style>` tag in the `html_template` that is sent to the client when it makes a request by opening the URL that is printed out in Thonny, to style the data/page that the client would see. I also added javascript in code in the `html_template` so that the client's browser will use short polling to continuosly get the current temprature and humidity of the room from the sensor connected to the Pi Pico without having to refresh the web page. No database is needed because the webpage always shows the latest measurement data.

<img width="1489" alt="“›” 2024-07-02 at 04 39 10" src="https://github.com/shayaneivazkhani/1DT305/assets/105381967/466a5217-7ffa-432b-ae76-0a9a85cb44a2">

# Summary
This is how the physical part of the project will look:
![“›” 2024-07-02 at 06 29 10](https://github.com/shayaneivazkhani/1DT305/assets/105381967/26c887c0-4dd1-4c46-b840-2ffe18d73f32)

This is how the software part of the project will look:
![“›” 2024-07-02 at 07 49 06](https://github.com/shayaneivazkhani/1DT305/assets/105381967/a25ce281-f958-453b-84d7-976bcaa29442)


#### Future improvements: 
Adding a OLED screen so that the dynamically assigned IP adress of the server would be available without the need for depending on Thonny and also connecting external power supply via 12V battery that cuts down to 5V via a voltage regulator so that the project would not need a laptop for functioning.

