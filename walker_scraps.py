from nltk import stopwords

filtered_words = [word for word in word_list if word not in stopwords.words('english')]

def comp(list1, list2):
	walker_count = 0
	nomatches = []
	for i in list1:

		if i in list2:
			walker_count +=1
		else:
			nomatches.append(i)

	return walker_count*1.0/len(list1), nomatches
