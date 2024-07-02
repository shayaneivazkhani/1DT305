from machine import Pin, I2C
import time
import network
import socket

# Initialize I2C
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=1000)

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

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Raspberry Pi Pico page</title>
    <style> 
        html {
            margin: 0;
            padding: 0;
            user-select: none;
        }
        body {
            margin: 0;
            padding: 0;

            overflow: auto;

            background: linear-gradient(95deg,
                var(--doc-background-gradientColor1),
                var(--doc-background-gradientColor2),
                var(--doc-background-gradientColor3),
                var(--doc-background-gradientColor4));
            background-size: 400% 600%;
        }
        body {
            --main-font: 'Arial', sans-serif;
            --main--font--size: clamp(17px, 1.1vw, 30px);
            --heading-font: 'Helvetica', sans-serif;
            --body-font: 'Georgia', serif;
            --code-font: 'Courier New', monospace;
            --custom-font1: 'Droid Sans', sans-serif;
            --custom-font2: 'Oswald', sans-serif;
            --custom-font3: 'Merriweather', serif;
        }
        .dark {
            --doc-background-gradientColor1: #4e1974;
            --doc-background-gradientColor2: #000000;
            --doc-background-gradientColor3: #151e75;
            --doc-background-gradientColor4: #ffffff;
            --doc-divider-horisontal-Color: rgb(163, 239, 243);
            --header-NavBar-Color: rgb(0, 0, 0);
            --header-NavBar-DarkLightToggle--Color: rgb(0, 0, 0);
            --header-NavBar-DarkLightToggleBorder--Color: rgb(176, 146, 146);
            --mainPage--textColor1: #e6e5e6;
            --mainPage--textColor4: #e6e5e6;
        }
        .light {
            --doc-background-gradientColor1: #c1e6fc;
            --doc-background-gradientColor2: #b9aecb;
            --doc-background-gradientColor3: #a5bfd6;
            --doc-background-gradientColor4: #a2a2a2;
            --doc-divider-horisontal-Color: rgb(251, 156, 15);
            --header-NavBar-Color: #1F094D;
            --header-NavBar-DarkLightToggle--Color: rgb(255, 255, 255);
            --header-NavBar-DarkLightToggleBorder--Color: rgb(0, 0, 0);
            --mainPage--textColor1: #35094D;
            --mainPage--textColor4: #0f0216;
        }
        header {
            background-color: #3333338a;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            padding-left: 20px;
            padding-right: 20px;
            border-bottom: 1px solid var(--doc-divider-horisontal-Color);
            color: var(--mainPage--textColor4);
            font-family: var(--heading-font);
            font-size: 16px;
        }
        main {
            padding: 2rem;
            color: var(--mainPage--textColor4);
            font-family: var(--code-font);
            font-weight: 500;
            font-size: 1.2rem;
            text-align: center;
            line-height: 1.6;
        }
        footer {
            background-color: #3333338a;
            position: fixed;
            width: 100%;
            bottom: 0;
            padding: 1rem;
            border-top: 1px solid var(--doc-divider-horisontal-Color);
            color: var(--mainPage--textColor4);
            font-family: var(--body-font);
            font-size: 1.2rem;
            text-align: center;
        }
        #toggle-mode {
            background: var(--header-NavBar-DarkLightToggle--Color);
            font-family: var(--code-font);
            padding: 0.4em 0.5em;
            font-weight: 900;
            color: var(--mainPage--textColor4);
            font-size: 12px;
            border: 2px solid var(--mainPage--textColor4);
            border-radius: 0.6em;
            box-shadow: 0.01em 0.1em;
            cursor: pointer;
        }
        #toggle-mode:hover {
            transform: translate(-0.00em, -1.0px);
            box-shadow: 0.10em 0.15em;
        }
        #toggle-mode:active {
            transform: translate(0.05em, 0.05em);
            box-shadow: 0.01em 0.5px;
        }
    </style>
</head>
<body oncontextmenu="return false">
    <header>
        <h1>Data from Adafruit SHT31-D Temperature & Humidity Sensor</h1>
        <button id="toggle-mode">
            Dark/Light
        </button>
    </header>
    <main>
        <div id="temperature">Temperature is: TEMPERATURE_PLACEHOLDER°C</div>
        <div id="humidity">Humidity is: HUMIDITY_PLACEHOLDER%</div>
    </main>
    <script> 
        const darkModeValue = localStorage.getItem('darkMode');
        const darkMode = darkModeValue ? JSON.parse(darkModeValue) : true;
        const body = document.body;
        const updateMode = (isDark) => {
            if (isDark) {
                body.classList.add('dark');
                body.classList.remove('light');
            } else {
                body.classList.add('light');
                body.classList.remove('dark');
            }
        };
        updateMode(darkMode);
        document.getElementById('toggle-mode').addEventListener('click', () => {
            const currentModeValue = localStorage.getItem('darkMode');
            const currentMode = currentModeValue ? JSON.parse(currentModeValue) : true;
            const newMode = !currentMode;
            localStorage.setItem('darkMode', JSON.stringify(newMode));
            updateMode(newMode);
        });
        const updateSensorData = async () => {
            try {
                const response = await fetch('/update');
                const data = await response.text();
                const [temperature, humidity] = data.split(',').map(s => s.split(':')[1].trim());
                document.getElementById('temperature').textContent = `Temperature is: ${temperature}°C`;
                document.getElementById('humidity').textContent = `Humidity is: ${humidity}%`;
             } catch (error) {
                 console.error('Error fetching sensor data:', error);
            }
        };
        setTimeout(() => {
            setInterval(updateSensorData, 2000);
        }, 3000);
    </script>
</body>
</html>
"""

# Function to update HTML with current sensor data
def update_html_with_sensor_data(html_template, temperature, humidity):
    updated_html = html_template.replace('TEMPERATURE_PLACEHOLDER', f'{temperature:.2f}').replace('HUMIDITY_PLACEHOLDER', f'{humidity:.2f}')
    return updated_html

# Setup network
ssid = 'Wifi-name'
password = 'Wifi-password'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

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
    print('Connect to Server URL: http://' + status[0] + ':80\n')

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        # Read HTTP request (not handling request parsing for simplicity)
        request = cl.recv(1024).decode('utf-8')
        # Split request to get the request line
        request_line = request.split('\n')[0]
        url = request_line.split(' ')[1]
        # Start a measurement
        start_measurement()
        # Read the measurement
        data = read_measurement()
        humidity, temperature = process_measurement(data)
        
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
            )
        else:
            # Handle 404 Not Found
            response = (
                'HTTP/1.1 404 Not Found\r\n'
                'Content-Type: text/plain\r\n'
                'Content-Length: 13\r\n\r\n'
                '404 Not Found'
            )
            
        cl.send(response.encode('utf-8'))
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')
