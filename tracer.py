#!/bin/python3

from collections import defaultdict
import matplotlib.pyplot as plt
import serial
import time

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=None
)

def combine_pairs(array):
	combined_pairs = []
	start_time = None
	for i in range(len(array) - 1):
		if array[i][0] == 0 and array[i + 1][0] == 1:
			start_time = array[i][1]
		elif array[i][0] == 1 and array[i + 1][0] == 0:
			if start_time is not None:
				combined_pairs.append((start_time, array[i][1] - start_time))
				start_time = None
	return combined_pairs

function_names = ["idle_main", "os_sched", "os_tick", "os_init", "os_run", "os_yield", "os_delay", "os_exit", "thread_init", "semaphore_init", "semaphore_wait", "semaphore_signal", "assert_handler", "systick_handler"]
events = defaultdict(list)
while sum(len(function) for function in events.values()) < 4000:
	data = ser.read(2)
	event = int(data[0])
	function = int(data[1])
	events[function].append((event, time.time()))

fig, ax = plt.subplots()
cmap = plt.get_cmap('tab20').colors
for function in events.keys():
	ax.broken_barh(combine_pairs(events[function]), (function * 10, 9), color=cmap[function])
ax.set_yticks(range(5, 10 * len(function_names), 10), labels=function_names)
ax.grid(True)

plt.show()
