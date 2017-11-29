"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
任务2: 哪个电话号码的通话总时间最长? 不要忘记，用于接听电话的时间也是通话时间的一部分。
输出信息:
"<telephone number> spent the longest time, <total time> seconds, on the phone during
September 2016.".

提示: 建立一个字典，并以电话号码为键，通话总时长为值。
这有利于你编写一个以键值对为输入，并修改字典的函数。
如果键已经存在于字典内，为键所对应的值加上对应数值；
如果键不存在于字典内，将此键加入字典，并将它的值设为给定值。
"""
def calculate_time():
	""" 计算每个电话号码的通话时间
	"""
	call_time = {}
	for call in calls:
		if call[0] in call_time:
			call_time[call[0]] += int(call[3])
		else:
			call_time[call[0]] = int(call[3])

		if call[1] in call_time:
			call_time[call[1]] += int(call[3])
		else:
			call_time[call[1]] = int(call[3])
	return call_time

def calculate_longest_time():
	""" 计算通话时间最长的电话号码
	"""
	call_time = calculate_time()
	phone_of_longest_call = max(call_time, key=call_time.get)
	print(call_time[phone_of_longest_call])
	return phone_of_longest_call

def calculate_longest_time_phone():
	""" 计算通话时间最长的电话号码
	"""
	call_time = calculate_time()
	longest_time_phone = None
	longest_time = 0

	for phone in call_time:
		if int(call_time[phone]) > longest_time:
			longest_time = call_time[phone]
			longest_time_phone = [phone]
		elif int(call_time[phone]) == longest_time:
			longest_time_phone.append(phone)

	if (len(longest_time_phone) == 1):
		return "{} spent the longest time, {} seconds, on the phone during September 2016.".format(longest_time_phone[0], longest_time)
	else:
		return "{} spent the longest time, {} seconds, on the phone during September 2016.".format(longest_time_phone, longest_time)

# print(len(calculate_time()))
print(calculate_longest_time())
print(calculate_longest_time_phone())