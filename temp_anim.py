import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import time

port = 'COM4'
baudrate = 9600
ser = serial.Serial(port, baudrate, timeout=3)
ser.reset_input_buffer()

times = []
temps = []

fig, ax = plt.subplots()
plt.title('График температуры')
ax.set_xlabel('Время в сек.')
ax.set_ylabel('Температура °C')
plt.grid(True)
line_, = ax.plot([], [], marker='|', linestyle='-', color='green')

time_ = time.time()


def animate(i):
    line__ = ser.readline().decode('utf-8').strip()

    if line_:
        temp = float(line__)
        temps.append(temp)
        times.append(round(time.time() - time_, 1))

        line_.set_data(times, temps)
        ax.relim()
        ax.autoscale_view(scalex=False, scaley=True)


        if len(times) > 1:
            ax.set_xlim(times[0], max(times) + 1)

    return line_

ani = FuncAnimation(fig, animate, interval=1000, blit=False)

plt.show()
ser.close()