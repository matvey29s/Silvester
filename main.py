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
cache_frame_data=False
# Инициализация данных
heart_rate_1 = []
heart_rate_2 = []
oxygen_level_1 = []
oxygen_level_2 = []
adc_values = [[] for _ in range(4)] # Для 4 тензодатчиков

value=np.zeros(4,dtype=float)
value1=np.zeros(4)
np.set_printoptions(precision=2, suppress=True)

# Максимальное количество точек на графиках
MAX_POINTS = 100

# Настройка графиков
fig, axs = plt.subplots(2, 4, figsize=(15, 8))
lines = [None] * 8

# Заголовки графиков
titles = [
  'Сердцебиение 1 датчика',
  'Сердцебиение 2 датчика',
  'Кислород в крови 1 датчика',
  'Кислород в крови 2 датчика',
  'АЦП Тензодатчик 1',
  'АЦП Тензодатчик 2',
  'АЦП Тензодатчик 3',
  'АЦП Тензодатчик 4'
]

# Инициализация графиков

ax = axs[0 // 4, 0 % 4]
lines[0], = ax.plot([], [], label=titles[0])
ax.set_ylim(40, 200)
ax.set_xlim(0, MAX_POINTS)
ax.set_title(titles[0])
ax.set_ylabel('Ударов в минуту')
ax.legend()
ax.grid()

ax = axs[1 // 4, 1 % 4]
lines[1], = ax.plot([], [], label=titles[1])
ax.set_ylim(40, 200)
ax.set_xlim(0, MAX_POINTS)
ax.set_title(titles[1])
ax.set_ylabel('Ударов в минуту')
ax.legend()
ax.grid()

ax = axs[2 // 4, 2 % 4]
lines[2], = ax.plot([], [], label=titles[2])
ax.set_ylim(80, 110)
ax.set_xlim(0, MAX_POINTS)
ax.set_title(titles[2])
ax.set_ylabel('%')
ax.legend()
ax.grid()

ax = axs[3 // 4, 3 % 4]
lines[3], = ax.plot([], [], label=titles[3])
ax.set_ylim(80, 110)
ax.set_xlim(0, MAX_POINTS)
ax.set_title(titles[3])
ax.set_ylabel('%')
ax.legend()
ax.grid()

ax = axs[4 // 4, 4 % 4]
lines[4], = ax.plot([], [], label=titles[4])
ax.set_ylim(0, 4200)
ax.set_xlim(0, MAX_POINTS)
ax.set_title(titles[4])
ax.set_ylabel('Значение 12-битного АЦП')
ax.legend()
ax.grid()

ax = axs[5 // 4, 5 % 4]
lines[5], = ax.plot([], [], label=titles[5])
ax.set_ylim(0, 4200)
ax.set_xlim(0, MAX_POINTS)
ax.set_title(titles[5])
ax.set_ylabel('Значение 12-битного АЦП')
ax.legend()
ax.grid()

ax = axs[6 // 4, 6 % 4]
lines[6], = ax.plot([], [], label=titles[6])
ax.set_ylim(0, 4200)
ax.set_xlim(0, MAX_POINTS)
ax.set_title(titles[6])
ax.set_ylabel('Значение 12-битного АЦП')
ax.legend()
ax.grid()

ax = axs[7 // 4, 7 % 4]
lines[7], = ax.plot([], [], label=titles[7])
ax.set_ylim(0, 4200)
ax.set_xlim(0, MAX_POINTS)
ax.set_title(titles[7])
ax.set_ylabel('Значение 12-битного АЦП')
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
  
  if heart_rate_2:
    lines[1].set_ydata(heart_rate_2)
    lines[1].set_xdata(range(len(heart_rate_2)))
  
  if oxygen_level_1:
    lines[2].set_ydata(oxygen_level_1)
    lines[2].set_xdata(range(len(oxygen_level_1)))
  
  if oxygen_level_2:
    lines[3].set_ydata(oxygen_level_2)
    lines[3].set_xdata(range(len(oxygen_level_2)))
  
  for i in range(4):
    if len(adc_values[i]) > 0:
      lines[i + 4].set_ydata(adc_values[i])
      lines[i + 4].set_xdata(range(len(adc_values[i])))

# Запуск потока для получения данных
import threading
threading.Thread(target=receive_data, daemon=True).start()

# Анимация
ani = animation.FuncAnimation(fig, update, interval=100)

plt.tight_layout()
plt.show()
