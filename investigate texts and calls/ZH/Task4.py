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
任务4:
电话公司希望辨认出可能正在用于进行电话推销的电话号码。
找出所有可能的电话推销员:
这样的电话总是向其他人拨出电话，
但从来不发短信、接收短信或是收到来电


请输出如下内容
"These numbers could be telemarketers: "
<list of numbers>
电话号码不能重复，每行打印一条，按字母顺序输出。
"""
def has_use_message(number):
	""" 是否使用过(发送和接受)短信
	"""
	for text in texts:
		if text[0] == number or text[1] == number:
			return True
	return False

def has_receive_call(number):
	""" 是否接过电话
	"""
	for call in calls:
		if call[1] == number:
			return True
	return False

def phone_numbers():
	""" 获取所有的电话号码的集合
	"""
	phones = set()
	for call in calls:
		phones.add(call[0])
		phones.add(call[1])

	for text in texts:
		phones.add(text[0])
		phones.add(text[1])

	return phones

def get_telemarketers():
	""" 获取电话推销的电话号码
	"""
	phones = phone_numbers()
	telemarketers = []
	for phone in phones:
		if not has_use_message(phone) and not has_receive_call(phone):
			telemarketers.append(phone)
	return telemarketers

def print_telemarketers():
	""" 打印结果
	"""
	print("These numbers could be telemarketers: ")
	telemarketers = get_telemarketers()
	telemarketers = sorted(telemarketers)
	for phone in telemarketers:
		print(phone)

print_telemarketers()
