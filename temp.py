import matplotlib.pyplot as plt
import serial
import time

port = 'COM4'
baudrate = 9600
dot = 20
temps = []
times = []
time_ = time.time()

ser = serial.Serial(port, baudrate, timeout=3)
ser.reset_input_buffer()

while len(temps) < dot:
    line = ser.readline().decode('utf-8').strip()

    temp = float(line)
    temps.append(temp)
    times.append(round(time.time() - time_, 1))

if temps:
    plt.plot(times, temps, marker='o', markersize=5, color='orange')
    plt.title('График температуры')
    plt.xlabel('Время в сек.')
    plt.ylabel('Температура °C')
plt.show()