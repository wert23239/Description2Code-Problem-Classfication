import json

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

symbols = '!@#$%^&*()[].,1234567890/\}{|";:<>`~'

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
		stripped_description = item['description'].strip().replace('\n', ' ').replace('\r',' ').replace('\t', ' ')
		for char in symbols:
			print(char)
			stripped_descirption = stripped_description.replace(char, ' ')
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
		filename = 'datastructures.txt'
		file = open(filename, 'w')
		for description in dataset[tag]:
			datastructures_descriptions.add(description)
		for description in datastructures_descriptions:
			file.write(description)
			file.write('\n')
	elif tag in DP:
		filename = 'dp.txt'
		file = open(filename, 'w')
		for description in dataset[tag]:
			DP_descriptions.add(description)
		for description in DP_descriptions:
			file.write(description)
			file.write('\n')
	elif tag in logic:
		filename = 'logic.txt'
		file = open(filename, 'w')
		for description in dataset[tag]:
			logic_descriptions.add(description)
		for description in logic_descriptions:
			file.write(description)
			file.write('\n')
	elif tag in search:
		filename = 'search.txt'
		file = open(filename, 'w')
		for description in dataset[tag]:
			search_descriptions.add(description)
		for description in search_descriptions:
			file.write(description)
			file.write('\n')
#for tag in tags:
	#filename = tag + '.txt'
	#file = open(filename, 'w')
	#for description in dataset[tag]:
	#	file.write(description)
	#	file.write('\n')







#print(dataset['empty'])



		#for tag in item['tags']:

#print(tags)