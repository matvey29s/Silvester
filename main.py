import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket



# Настройки UDP
UDP_IP = "192.168.4.2"
UDP_PORT = 48700


# Создание сокета
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


# Инициализация данных
heart_rate_1 = []
heart_rate_2 = []
oxygen_level_1 = []
oxygen_level_2 = []
adc_values = [[] for _ in range(4)]

value=np.zeros(4,dtype=float)
value1=np.zeros(4)
np.set_printoptions(precision=2, suppress=True)

# Максимальное количество точек на графиках
MAX_POINTS = 100

# Настройка графиков
fig, axs = plt.subplots(2, 4, figsize=(15, 8))
lines = [None] * 8
texts=[]


y_max_lims = [110,110,110,110,4200,4200,4200,4200]
y_min_lims = [50,50,80,80,0,0,0,0]


y_labels = ['Ударов в минуту',
            'Ударов в минуту',
            '%',
            '%',
            'Значение 12-битного АЦП',
            'Значение 12-битного АЦП',
            'Значение 12-битного АЦП',
            'Значение 12-битного АЦП'
            ]


titles =   ['Сердцебиение 1 датчика',
            'Сердцебиение 2 датчика',
            'Кислород в крови 1 датчика',
            'Кислород в крови 2 датчика',
            'АЦП Тензодатчик 1',
            'АЦП Тензодатчик 2',
            'АЦП Тензодатчик 3',
            'АЦП Тензодатчик 4'
            ]


# Инициализация графиков
for i in range(8):
    ax = axs[i // 4, i % 4]
    lines[i], = ax.plot([], [], label=titles[i])
    text = axs[i // 4, i % 4].text(0.9, 0.9, '', transform=axs[i // 4, i % 4].transAxes,
                                       fontsize=20, verticalalignment='top', horizontalalignment='right')
    ax.set_ylim(y_min_lims[i], y_max_lims[i])
    ax.set_xlim(0, MAX_POINTS)
    ax.set_title(titles[i])
    ax.set_ylabel(y_labels[i])
    texts.append(text)
    ax.legend()
    ax.grid()


# Функция для получения данных по UDP
def receive_data():
    while True:
        data, _ = sock.recvfrom(1024) # Получаем данные
        data = list(data)
        if len(data) == 10 and data[0] == 160 and data[-1] == 254:
            # Обработка массива АЦП
            for i in range(4):
                adc_value = (data[2*i + 1] * 256 + data[2*i + 2])
                value[i] = float(data[2 * i + 1] * 256 + data[2 * i + 2]) * 0.0008058608
                adc_values[i].append(adc_value)


        elif len(data) == 6 and data[0] == 80 and data[-1] == 152:
            # Обработка массива сердцебиения и кислорода
            heart_rate_1.append(data[1])
            heart_rate_2.append(data[2])
            oxygen_level_1.append(data[3])
            oxygen_level_2.append(data[4])
            value1[0] = data[1]
            value1[1] = data[2]
            value1[2] = data[3]
            value1[3] = data[4]
        # Удаление старых значений, если превышено максимальное количество точек
        if len(heart_rate_1) > MAX_POINTS:
            heart_rate_1.pop(0)
        if len(heart_rate_2) > MAX_POINTS:
            heart_rate_2.pop(0)
        if len(oxygen_level_1) > MAX_POINTS:
            oxygen_level_1.pop(0)
        if len(oxygen_level_2) > MAX_POINTS:
            oxygen_level_2.pop(0)
        for i in range(4):
            if len(adc_values[i]) > MAX_POINTS:
                adc_values[i].pop(0)
        print(value,value1)

# Функция обновления графиков
def update(frame):
    if heart_rate_1:
        lines[0].set_ydata(heart_rate_1)
        lines[0].set_xdata(range(len(heart_rate_1)))
        texts[0].set_text(f'{heart_rate_1[-1]}')

    if heart_rate_2:
        lines[1].set_ydata(heart_rate_2)
        lines[1].set_xdata(range(len(heart_rate_2)))
        texts[1].set_text(f'{heart_rate_2[-1]}')

    if oxygen_level_1:
        lines[2].set_ydata(oxygen_level_1)
        lines[2].set_xdata(range(len(oxygen_level_1)))
        texts[2].set_text(f'{oxygen_level_1[-1]}')

    if oxygen_level_2:
        lines[3].set_ydata(oxygen_level_2)
        lines[3].set_xdata(range(len(oxygen_level_2)))
        texts[3].set_text(f'{oxygen_level_2[-1]}')

    for i in range(4):

        if len(adc_values[i]) > 0:
            lines[i + 4].set_ydata(adc_values[i])
            lines[i + 4].set_xdata(range(len(adc_values[i])))
            texts[i+4].set_text(f'{value[i]:.2f}')


# Запуск потока для получения данных
import threading
threading.Thread(target=receive_data, daemon=True).start()

# Анимация
ani = animation.FuncAnimation(fig, update, interval=100,cache_frame_data=False)

plt.tight_layout()
plt.show()
