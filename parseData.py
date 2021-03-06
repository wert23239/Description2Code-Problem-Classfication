import json
import random
import string

stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant', 'cannot', 'could', 'couldnt', 'did', 'didnt', 'do', 'does', 'doesnt', 'doing', 'dont', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hes', 'her', 'here', 'heres', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 'ive', 'if', 'in', 'into', 'is', 'isnt', 'it', 'its', 'its', 'itself', 'lets', 'me', 'more', 'most', 'mustnt', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shant', 'she', 'shed', 'shell', 'shes', 'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres', 'these', 'they', 'theyd', 'theyll', 'theyre', 'theyve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasnt', 'we', 'wed', 'well', 'were', 'weve', 'were', 'werent', 'what', 'whats', 'when', 'whens', 'where', 'wheres', 'which', 'while', 'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont', 'would', 'wouldnt', 'you', 'youd', 'youll', 'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves']
tags = ['empty', 'Search']
dataset = {}

datastructures = ['Array', 'Hash Table', 'Heap', 'Linked List', 'Queue', 'Stack', 'String', 'Two Pointers', 'Binary Indexed Tree', 'Binary Search Tree', 'Segment Tree', 'Tree', 'Trie', 'Graph', 'Union Find']
datastructures_descriptions = set()

DP = ['Backtracking', 'Divide and Conquer', 'Dynamic Programming', 'Memoization']
DP_descriptions = set()

logic = ['Bit Manipulation', 'Brainteaser', 'Design', 'empty', 'Math', 'Reservoir Sampling']
logic_descriptions = set()

search = ['Binary Search', 'Breadth-first Search', 'Depth-first Search', 'Greedy', 'Minimax', 'Sort', 'Topological Sort', 'Search']
search_descriptions = set()

symbols = '\'!@#$%^&*()[].,1234567890/\}{|";:<>`~+=?-_'

def removeExtraneousCharacters(string_to_remove):
	string_to_remove = string_to_remove.strip().replace('\n', ' ').replace('\r',' ').replace('\t', ' ').lower()
	#Removes all symbols
	for char in symbols:
		string_to_remove = string_to_remove.replace(char, ' ')
	for word in stopwords:
		temp = ' ' + word + ' '
		if temp in string_to_remove:
			string_to_remove = string_to_remove.replace(temp, ' ')
	for char in string.ascii_lowercase:
		temp = ' ' + char + ' '
		if temp in string_to_remove:
			string_to_remove = string_to_remove.replace(temp, ' ')
	string_to_remove = string_to_remove.replace('      ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').strip()
	return string_to_remove

def crossFoldValidation(num_folds, descriptions_list, test_filename, train_filename):
	for fold in range(1,num_folds+1):
		train_filename_full = train_filename + '-' + str(fold) + '.txt'
		test_filename_full = test_filename + '-' + str(fold) + '.txt'
		test_file = open(test_filename_full, 'w')
		train_file = open(train_filename_full, 'w')
		
		for i in range(0, len(descriptions_list)):
			if i < (1/num_folds)*fold*len(descriptions_list) and i >= (1/num_folds)*(fold-1)*len(descriptions_list):
				test_file.write(descriptions_list[i])
				if i != len(descriptions_list):
					test_file.write('\n') 	
			else:
				train_file.write(descriptions_list[i])
				train_file.write('\n')

		train_file.close()
		test_file.close()

with open('questions.json') as json_data:
	data = json.load(json_data)

	# Gather all tags
	for item in data:
		for tag in item['tags']:
			if tag not in tags:
				tags.append(tag)

	for tag in tags:
		dataset[tag] = []

	for item in data:
		stripped_description = item['description']
		#Removes all symbols and stop words
		stripped_description = removeExtraneousCharacters(stripped_description)
		#print(stripped_description)
		if 'Credits' in stripped_description:
			index = stripped_description.index('Credits')
			stripped_description = stripped_description[:index]
			#print(stripped_description)

		# Add these lines for duplicates
		for tag in item['tags']:
			dataset[tag].append(stripped_description)
			break

		if len(item['tags']) == 0:
			dataset['empty'].append(stripped_description)

with open('dpNewRecords.txt') as dp_records:
	current_string = ""
	for line in dp_records:
		current_string += ' ' + line.strip()
		current_string = removeExtraneousCharacters(current_string)
		if "~~~" in line:
			dataset['Dynamic Programming'].append(current_string)
			current_string = ""
			continue
		
	

with open('searchNewRecords.txt') as search_records:
	current_string = ""
	for line in search_records:
		current_string += ' ' + line.strip()
		current_string = removeExtraneousCharacters(current_string)
		if "~~~" in line:
			dataset['Search'].append(current_string)
			current_string = ""
			continue




for tag in tags:
	if tag in datastructures:
		for description in dataset[tag]:
		 	datastructures_descriptions.add(description)
		
		datastructures_descriptions_list = list(datastructures_descriptions)
		random.shuffle(datastructures_descriptions_list)
		crossFoldValidation(5, datastructures_descriptions_list, 'test-pos', 'train-pos')

	elif tag in DP or tag in search:
		for description in dataset[tag]:
			DP_descriptions.add(description)
		
		DP_descriptions_list = list(DP_descriptions)
		random.shuffle(DP_descriptions_list)
		crossFoldValidation(5, DP_descriptions_list, 'test-neg', 'train-neg')

	elif tag in logic:
		unsup_filename = 'train-unsup.txt'
		unsup_file = open(unsup_filename, 'w')
		
		for description in dataset[tag]:
			logic_descriptions.add(description)
		
		logic_descriptions_list = list(logic_descriptions)
		random.shuffle(logic_descriptions_list)
		
		for i in range(0, len(logic_descriptions_list)):
			unsup_file.write(logic_descriptions_list[i])
			if i != len(logic_descriptions_list):
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

