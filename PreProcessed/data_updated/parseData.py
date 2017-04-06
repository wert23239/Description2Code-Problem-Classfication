import json
import random

tags = ['empty']
dataset = {}

datastructures = ['Array', 'Hash Table', 'Heap', 'Linked List', 'Queue', 'Stack', 'String', 'Two Pointers', 'Binary Indexed Tree', 'Binary Search Tree', 'Segment Tree', 'Tree', 'Trie', 'Graph', 'Union Find']
datastructures_descriptions = set()

DP = ['Backtracking', 'Divide and Conquer', 'Dynamic Programming', 'Memoization']
DP_descriptions = set()

logic = ['Bit Manipulation', 'Brainteaser', 'Design', 'empty', 'Math', 'Reservoir Sampling']
logic_descriptions = set()

search = ['Binary Search', 'Breadth-first Search', 'Depth-first Search', 'Greedy', 'Minimax', 'Sort', 'Topological Sort']
search_descriptions = set()

symbols = '!@#$%^&*()[].,1234567890/\}{|";:<>`~+=-_'

with open('questions.json') as json_data:
	data = json.load(json_data)

	# Gather all tags
	for item in data:
		for tag in item['tags']:
			if tag not in tags:
				tags.append(tag)

	for tag in tags:
		dataset[tag] = []

	#
	for item in data:
		stripped_description = item['description'].strip().replace('\n', ' ').replace('\r',' ').replace('\t', ' ').lower()


		#Removes all symbols
		for char in symbols:
			stripped_description = stripped_description.replace(char, ' ')
		stripped_description = stripped_description.replace('      ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').strip()
		#print(stripped_description)
		if 'Credits' in stripped_description:
			index = stripped_description.index('Credits')
			stripped_description = stripped_description[:index]
			#print(stripped_description)
		for tag in item['tags']:
			dataset[tag].append(stripped_description)
		if len(item['tags']) == 0:
			dataset['empty'].append(stripped_description)



for tag in tags:
	if tag in datastructures:
		
		train_filename = 'train-pos.txt'
		test_filename = 'test-pos.txt'
		test_file = open(test_filename, 'w')
		train_file = open(train_filename, 'w')
		
		for description in dataset[tag]:
			datastructures_descriptions.add(description)
		
		datastructures_descriptions_list = list(datastructures_descriptions)
		random.shuffle(datastructures_descriptions_list)
		
		for i in range(0, len(datastructures_descriptions_list)):
			if i >= .8*len(datastructures_descriptions_list):
				test_file.write(datastructures_descriptions_list[i])
				test_file.write('\n') 	
			else:
				train_file.write(datastructures_descriptions_list[i])
				train_file.write('\n')
		train_file.close()
		test_file.close()

	elif tag in DP or tag in search:
		train_filename = 'train-neg.txt'
		test_filename = 'test-neg.txt'
		test_file = open(test_filename, 'w')
		train_file = open(train_filename, 'w')
		
		for description in dataset[tag]:
			DP_descriptions.add(description)
		
		DP_descriptions_list = list(DP_descriptions)
		random.shuffle(DP_descriptions_list)
		
		for i in range(0, len(DP_descriptions_list)):
			if i >= .8*len(DP_descriptions_list):
				test_file.write(DP_descriptions_list[i])
				test_file.write('\n') 	
			else:
				train_file.write(DP_descriptions_list[i])
				train_file.write('\n')
		train_file.close()
		test_file.close()
	elif tag in logic:
		unsup_filename = 'train-unsup.txt'
		unsup_file = open(unsup_filename, 'w')
		
		for description in dataset[tag]:
			logic_descriptions.add(description)
		
		logic_descriptions_list = list(logic_descriptions)
		random.shuffle(logic_descriptions_list)
		
		for i in range(0, len(logic_descriptions_list)):
			unsup_file.write(logic_descriptions_list[i])
			unsup_file.write('\n') 	
		unsup_file.close()
	"""if tag in datastructures:
		filename = 'datastructures.txt'
		file = open(filename, 'w')
		for description in dataset[tag]:
			datastructures_descriptions.add(description)
		datastructures_descriptions.shuffle()
		for description in datastructures_descriptions:
			file.write(description)
			file.write('\n')
	elif tag in DP:
		filename = 'dp.txt'
		file = open(filename, 'w')
		for description in dataset[tag]:
			DP_descriptions.add(description)
		DP_descriptions.shuffle()
		for description in DP_descriptions:
			file.write(description)
			file.write('\n')
	elif tag in logic:
		filename = 'logic.txt'
		file = open(filename, 'w')
		for description in dataset[tag]:
			logic_descriptions.add(description)
		logic_descriptions.shuffle()
		for description in logic_descriptions:
			file.write(description)
			file.write('\n')
	elif tag in search:
		filename = 'search.txt'
		file = open(filename, 'w')
		for description in dataset[tag]:
			search_descriptions.add(description)
		search_descriptions.shuffle()
		for description in search_descriptions:
			file.write(description)
			file.write('\n')

	"""
#for tag in tags:
	#filename = tag + '.txt'
	#file = open(filename, 'w')
	#for description in dataset[tag]:
	#	file.write(description)
	#	file.write('\n')







#print(dataset['empty'])



		#for tag in item['tags']:

#print(tags)