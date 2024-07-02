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
I bought the materials needed from [electrokit](https://www.electrokit.com)

| units | Link                                                       | Price (SEK) |
|-------|------------------------------------------------------------|-------------|
| 1 | Raspberry Pi Pico WH                                           | 88   |
| 1 | USB-kabel A-hane - micro B hane 1.8m                           | 32   |
| 1 | Adafruit Sensirion SHT31-D Temperatur & luftfuktighetssensor   | 184  |
| 1 | Kopplingsdäck 400 anslutningar                                 | 40   |
| 1 | Kopplingsdäck 170 anslutningar                                 | 35   |
| 1 | Labbsladd 20-pin 15cm hane/hane                                | 29   |

#### total cost: 408 SEK

# Step 1 of 2: Putting everything together
How all the electronics is connected, aside from the usb that connects the Raspberry Pi Pico to the computer: 
![“›” 2024-07-02 at 05 57 47](https://github.com/shayaneivazkhani/1DT305/assets/105381967/ede26b74-6c30-48c4-85a4-f14c98a7a5f3)

# Step 2 of 2: Computer setup and usage
I used Thonny to flash the Pi Pico.

# Details about the project

## Higher level description of the fundamental parts of the project code

 Hardest part about this project was to not use a external library for reading the sensor measurments, instead opening the datasheet for SHT3x-DIS SENSIRION and trying to understand the low level timing diagram of input to the sensor and correct reading format of the 48 bits when it outputs as the measurments.
#### lines 9–31 in temperature_humidity_sensor.py
```
# Sensor's I2C address
sensor_address = 0x44

# Command to start measurement (single shot mode, high repeatability)
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

And most important part of creating the server was to differentiate the HTTP start line to decide if the client only wants the page (GET / HTTP/1.1) or just the latest measurment from the sensor (GET '/update' HTTP/1.1).
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
I created a local HTTP server on the Pi Pico and when the client connects to the via URL that is printed out in thonny, the Pi Pico will read values from humidity sensor and then replace that value with named placeholders (`TEMPERATURE_PLACEHOLDER`, `HUMIDITY_PLACEHOLDER`) inside the defined `html_template` and send that html to the client. The html have code that afterwards starts to update the html provided by itself with latest values from the sensor every 2 seconds. I choose 2 seconds because if i also wanted to connect my phone at the same time my laptops browser was connected to it, then one of the browsers would not be able to make requests because of the single threaded server would be busy with handling previous requests. This little adjustment made it possible to serve 2 clients that would both make continous requsts for updated measurments from the server almost at the same time without having to implement a asynchronous server request handler option. 

## Presenting the data
I used CSS inside `<style>` tag in the `html_template` to style the data/page that the client would see. I also added javascript code so that the client will use short polling to continuosly get the current temprature and humidity of the room from the sensor connected to the Pi Pico without having to refresh the web page.

<img width="1489" alt="“›” 2024-07-02 at 04 39 10" src="https://github.com/shayaneivazkhani/1DT305/assets/105381967/466a5217-7ffa-432b-ae76-0a9a85cb44a2">

# Summary
This is how the physical part of the project will look:
![“›” 2024-07-02 at 06 29 10](https://github.com/shayaneivazkhani/1DT305/assets/105381967/26c887c0-4dd1-4c46-b840-2ffe18d73f32)

#### Future improvements: add a OLED screen so that the dynamically assigned IP adress of the server would be available without the need for depending on Thonny and also connecting external power supply via 12V battery that cuts down to 5V via a voltage regulator so that the project would not need a laptop for functioning.

