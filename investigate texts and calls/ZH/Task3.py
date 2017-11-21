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
任务3:
(080)是班加罗尔的固定电话区号。
固定电话号码包含括号，
所以班加罗尔地区的电话号码的格式为(080)xxxxxxx。

第一部分: 找出被班加罗尔地区的固定电话所拨打的所有电话的区号和移动前缀（代号）。
 - 固定电话以括号内的区号开始。区号的长度不定，但总是以 0 打头。
 - 移动电话没有括号，但数字中间添加了
   一个空格，以增加可读性。一个移动电话的移动前缀指的是他的前四个
   数字，并且以7,8或9开头。
 - 电话促销员的号码没有括号或空格 , 但以140开头。

输出信息:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
代号不能重复，每行打印一条，按字母顺序输出。

第二部分: 由班加罗尔固话打往班加罗尔的电话所占比例是多少？
换句话说，所有由（080）开头的号码拨出的通话中，
打往由（080）开头的号码所占的比例是多少？

输出信息:
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
注意：百分比应包含2位小数。
"""
def is_Bangalore(number):
	""" 判断是否是班加罗尔的固定电话
	"""
	return number.startswith('(080)')

def is_fixed_lines(number):
	""" 判断是否是固定电话
	"""
	return number.startswith('(0') and ')' in number

def is_mobile(number):
	""" 判断是否是移动电话号码
	"""
	return len(number.split(' ')) == 2

def id_telemarketers(number):
	""" 判断是否是电话促销员的号码
	"""
	return len(number.split(' ')) == 1 and number.startswith("140")

# print(is_Bangalore("(080)1234567"))
# print(is_Bangalore("(081)1234567"))
# print(is_mobile("01234 56789"))
# print(is_mobile("0123456789"))
# print(id_telemarketers("1401234567"))
# print(id_telemarketers("14012 34567"))
# print(is_fixed_lines("(014)1234567"))
# print(is_fixed_lines("(140)1234567"))

def calculate_prefixes(number):
	if is_fixed_lines(number):
		end = number.index(')')
		return number[:end+1]
	elif is_mobile(number):
		return number.split(' ')[0]
	else:
		return '140'

# print(calculate_prefixes("(080)1234567"))
# print(calculate_prefixes("01234 56789"))
# print(calculate_prefixes("1401234567"))
# print(calculate_prefixes("(014)1234567"))

def called_by_Bangalore():
	""" 由班加罗尔地区打出的电话号码列表
	"""
	phones = []
	for call in calls:
		if is_Bangalore(call[0]):
			phones.append(call[1])
	return phones

def called_code_by_Bangalore():
	""" 由班加罗尔地区打出的电话号码的区号和移动前缀（代号）的列表
	"""
	phones = called_by_Bangalore()
	phone_prefixes = []
	for phone in phones:
		phone_prefixe = calculate_prefixes(phone)
		if phone_prefixe not in phone_prefixes:
			phone_prefixes.append(phone_prefixe)
	return phone_prefixes

# print(called_by_Bangalore())
# print(len(called_by_Bangalore()))
# print(called_code_by_Bangalore())
# print(len(called_code_by_Bangalore()))
def print_code_called_by_Bangalore():
	print("The numbers called by people in Bangalore have codes:")
	phone_prefixes = called_code_by_Bangalore()
	phone_prefixes = sorted(phone_prefixes)
	for phone_prefixe in phone_prefixes:
		print(phone_prefixe)

print_code_called_by_Bangalore()

def Bangalore_to_Bangalore():
	count = 0
	for call in calls:
		if is_Bangalore(call[0]) and is_Bangalore(call[1]):
			count += 1
	return count

print("{} percent of calls from fixed lines in Bangalore are calls to other fixed lines in Bangalore.".format(format(Bangalore_to_Bangalore()*100/len(called_by_Bangalore()), '.2f')))



