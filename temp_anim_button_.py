from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.animation import FuncAnimation
import serial
import os


root = Tk()
root.title('Имя файла')
root.geometry('400x400')

port = 'COM4'
baudrate = 9600
ser = serial.Serial(port=port, baudrate=baudrate, timeout=3)
ser.reset_input_buffer()

times = []
temps = []

def format_time(event):
    entry = event.widget
    text = entry.get()

    if len(text) == 2 and text.isdigit():
        entry.insert(END, ':')

Label(root, text='Старт ЧЧ:ММ').pack(anchor='w', padx=10, pady=5)
entry_start = ttk.Entry(root)
entry_start.pack(fill='x', padx=10)
entry_start.bind('<KeyRelease>', format_time)

Label(root, text='Конец ЧЧ:ММ').pack(anchor='w', padx=10, pady=5)
entry_stop = ttk.Entry(root)
entry_stop.pack(fill='x', padx=10)
entry_stop.insert(0,"12:10")
entry_stop.bind('<KeyRelease>', format_time)

Label(root, text='Название файла:').pack(anchor='w', padx=10, pady=5)
entry_name = ttk.Entry(root)
entry_name.pack(fill='x', padx=10)
entry_name.insert(0,"Plot_temp")

fig, ax = plt.subplots()
plt.title('График температуры')
ax.set_xlabel('Реальное время')
ax.set_ylabel('Температура °C')
plt.grid(True)

line_, = ax.plot([], [], marker='x', linestyle='-', color='green')

def animate(i):
    if ser.in_waiting > 0:
        line__ = ser.readline().decode('utf-8').strip()

        if line_:
            temp = float(line__)
            temps.append(temp)
            now_time = datetime.now().strftime('%H:%M')
            times.append(now_time)

            now = datetime.now()

            if len(times) == 1:
                entry_start.delete(0, END)
                entry_start.insert(0, now_time)

                stop_ = now + timedelta(minutes=10)
                stop_ = stop_.strftime('%H:%M')

                entry_stop.delete(0, END)
                entry_stop.insert(0, stop_)

            ax.set_xticks(range(len(times)))
            ax.set_xticklabels(times)

            line_.set_data(range(len(times)), temps)

            size = 10

            if len(times) > size:
                ax.set_xlim(len(times) - size, len(times) - 1)

            else:
                ax.set_xlim(0, max(1, len(times) - 1))

            fig.autofmt_xdate(rotation=45)

            ax.relim()
            ax.autoscale_view()
    return line_

ani = FuncAnimation(fig, animate, interval=1000, blit=False)

def save_img(format):
    global times, temps

    start_t = entry_start.get().strip()
    stop_t = entry_stop.get().strip()

    f_name = f"{entry_name.get().strip() or "Plot_temp"}.{format}"

    if os.path.exists(f_name):
        messagebox.showwarning('Ошибка сохранения', f'Файл с именем {f_name} уже существует. \n Измените название файла')
        return

    f_time = []
    f_temp = []

    for t, temp in zip(times, temps):
        if start_t <= t <= stop_t:
            f_temp.append(temp)
            f_time.append(t)

    if not f_time:
        messagebox.showwarning('Ошибка', "В указаном промежутке времени нет данных. \nПроверте значения Start и Stop.")
        return

    fig_c, ax_c = plt.subplots()
    plt.title(f'График температуры с {start_t} по {stop_t}')
    ax_c.set_xlabel('Реальное время')
    ax_c.set_ylabel('Температура °C')
    plt.grid(True)

    step = max(1, len(f_time) // 5)

    positions = range(0, len(f_time), step)
    labels = [f_time[idx] for idx in positions]

    ax_c.set_xticks(positions)
    ax_c.set_xticklabels(labels)
    ax_c.plot(range(len(f_time)), f_temp, marker='x', linestyle='-', color='green')

    ax_c.tick_params(axis='x', labelrotation=45)

    fig_c.savefig(f_name, bbox_inches='tight')
    plt.close(fig_c)
    messagebox.showinfo('Успех', f'Файл {f_name} успешно сохранён')

btn_png = ttk.Button(root, text='Save as PNG', command= lambda: save_img('png'))
btn_jpeg = ttk.Button(root, text='Save as JPEG', command=lambda: save_img('jpeg'))

btn_png.pack()
btn_jpeg.pack()

plt.show(block=False)
root.mainloop()
ser.close()
plt.close('all')