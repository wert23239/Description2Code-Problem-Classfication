words = open('stopwordslist')
wordlist = []
for word in words:
	word = word.replace('\n', '').replace("'", '')
	wordlist.append(word)

print(wordlist)