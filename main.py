import os # lib methods used for file reading/writing
import re # for extracting individual words and sentences

from statistics import mean # for descriptive statistics
from statistics import stdev


####################################################################################################################

def word_count(text):
	### counts contractions as one word, but does not count apostrophes
	### returns mean and standard deviation
	
	# clean text
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*'?[a-zA-ZäöüÄÖÜ]*" # letters and apostrophes.
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")	
	word_list = re.findall(re_pattern, generic_punctuation)
	WORD_COUNT = len(word_list)
	
	return WORD_COUNT


####################################################################################################################


def sent_length(text):
	### counts the number of words in each sentence
	### counts contractions as one word
	### returns mean and standard deviation
	
	# clean text
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*\\.?" # letters, apostrophes and full stops	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")
	word_list = re.findall(re_pattern, generic_punctuation)
	cleaned_text = " ".join(word_list)	
	sent_list = cleaned_text.split('.')
		
	# count number of words in each sentence and append to a list
	sent_lengths = []	
	for sent in sent_list:
		sent = sent.lstrip()
		word_list = sent.split(" ")
		num_words = 0
		for word in word_list:
			if word != "":
				num_words += 1
		sent_lengths.append(num_words)
	
	# calculate descriptives
	SENT_LENm = mean(sent_lengths)
	SENT_LENsd	= stdev(sent_lengths)
	
	return round(SENT_LENm, 3), round(SENT_LENsd, 3)


####################################################################################################################


def word_length(text):
	### counts contractions as one word
	### does not count apostrophes as characters
	### returns mean and standard deviation
	
	# clean text
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*" # letters and apostrophes
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")
	word_list = re.findall(re_pattern, generic_punctuation)
	
	# count number of letters in each word and append to list
	word_lengths = []
	
	for word in word_list:
		num_chars = 0
		for char in word:
			if char != "'":
				num_chars += 1
		word_lengths.append(num_chars)
			
	#calculate descriptives
	WORD_LENm = round(mean(word_lengths), 3)
	WORD_LENsd = round(stdev(word_lengths), 3)
	
	return round(WORD_LENm, 3), round(WORD_LENsd, 3)


####################################################################################################################


import nltk # pip install nltk

from HanTa import HanoverTagger as ht # pip install HanTa
# tagger library:
# Wartena, C. (2019).
# 	A Probabilistic Morphology Model for German Lemmatization.
# 	Proceedings of the 15th Conference on Natural Language Processing (KONVENS 2019): Long Papers. 40-49.
# 	https://doi.org/10.25968/opus-1527

tagger = ht.HanoverTagger('morphmodel_ger.pgz')
# training corpus:
# Brants, S., Stefanie Dipper, S., Eisenberg, P., Hansen, S., König, E., Lezius, W., Rohrer, C., Smith, G., & Uszkoreit. H. (2004).
# 		TIGER: Linguistic Interpretation of a German Corpus.
# 		Journal of Language and Computation, 2, 597-620.


def noun_overlap(text):
	###  binary measure to check if there is an overlapping noun lemma
	###	 	in adjecent sentences and across all sentences. 
	### returns mean and sd for adjacent sentences and entire text.

	# clean text	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")	
	re_pattern = "[a-zA-ZäöüÄÖÜ0-9]+\\'?[a-zA-ZäöüÄÖÜ0-9]*\\'?[a-zA-ZäöüÄÖÜ0-9]*\\.?\\,?" # letters, apostrophes, commas, and full stops		
	word_list = re.findall(re_pattern, generic_punctuation)		
	cleaned_text = " ".join(word_list)
	sent_list = cleaned_text.split('.')
	
	overlap_scores1 = [] # adjacent sentences only
	overlap_scores = [] # full text
		
	keep_tags = ["NN"]
	
	for sent1 in sent_list:
		if sent1 != "":
			lemma_list1 = []
			idx1 = sent_list.index(sent1)		
			words = nltk.word_tokenize(sent1)
			lemmata1 = tagger.tag_sent(words, taglevel = 1)
			
			for token in lemmata1:
				if token[2] in keep_tags:
					lemma_list1.append(token[1])
				
					
			for sent2 in sent_list:
				if sent2 != "":
					lemma_list2 = []
					idx2 = sent_list.index(sent2)
					words = nltk.word_tokenize(sent2)
					lemmata2 = tagger.tag_sent(words, taglevel = 1)
					
					if idx1 < idx2:
						adjustment = idx2 - idx1
					
						for token in lemmata2:							
							if token[2] in keep_tags:
								lemma_list2.append(token[1])
													
						for lemma in lemma_list2:							
							if lemma in lemma_list1:																

								if adjustment == 1:
									overlap_scores1.append(1)								
								
								score = 1 / adjustment
								overlap_scores.append(score)
								break							
							else:
								overlap_scores1.append(0)
								overlap_scores.append(0)
								break
	
	NOUN_OL1m = mean(overlap_scores1)
	NOUN_OL1sd = stdev(overlap_scores1)
	NOUN_OLm = mean(overlap_scores)
	NOUN_OLsd = stdev(overlap_scores)

	return round(NOUN_OL1m, 5), round(NOUN_OL1sd, 5), round(NOUN_OLm, 5), round(NOUN_OLsd, 5)			


####################################################################################################################


def verb_overlap(text):
	###  binary measure to check if there is an overlapping verb lemma
	###	 	in adjecent sentences and across all sentences.
	### 	effect is weakened as sentences become more distant. 

	# clean text	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")	
	re_pattern = "[a-zA-ZäöüÄÖÜ0-9]+\\'?[a-zA-ZäöüÄÖÜ0-9]*\\'?[a-zA-ZäöüÄÖÜ0-9]*\\.?\\,?" # letters, apostrophes, commas, and full stops		
	word_list = re.findall(re_pattern, generic_punctuation)		
	cleaned_text = " ".join(word_list)
	sent_list = cleaned_text.split('.')	
	
	overlap_scores1 = [] # adjacent sentences only
	overlap_scores = [] # full text
		
	keep_tags = ["VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP"]
	
	for sent1 in sent_list:
		if sent1 != "":
			lemma_list1 = []
			idx1 = sent_list.index(sent1)		
			words = nltk.word_tokenize(sent1)
			lemmata1 = tagger.tag_sent(words, taglevel = 1)
			
			for token in lemmata1:
				if token[2] in keep_tags:
					lemma_list1.append(token[1])
				
					
			for sent2 in sent_list:
				if sent2 != "":
					lemma_list2 = []
					idx2 = sent_list.index(sent2)
					words = nltk.word_tokenize(sent2)
					lemmata2 = tagger.tag_sent(words, taglevel = 1)
					
					if idx1 < idx2:
						adjustment = idx2 - idx1
					
						for token in lemmata2:							
							if token[2] in keep_tags:
								lemma_list2.append(token[1])
													
						for lemma in lemma_list2:							
							if lemma in lemma_list1:																

								if adjustment == 1:
									overlap_scores1.append(1)								
								
								score = 1 / adjustment
								overlap_scores.append(score)
								break							
							else:
								overlap_scores1.append(0)
								overlap_scores.append(0)
								break
	
	VERB_OL1m = mean(overlap_scores1)
	VERB_OL1sd = stdev(overlap_scores1)
	VERB_OLm = mean(overlap_scores)
	VERB_OLsd = stdev(overlap_scores)
	
	return round(VERB_OL1m, 5), round(VERB_OL1sd, 5), round(VERB_OLm, 5), round(VERB_OLsd, 5)


####################################################################################################################



def content_word_overlap(text):
	###  binary measure to check if there is an overlapping noun, verb, or adjective lemma
	###	 	in adjecent sentences and across all sentences.
	### 	effect is weakened as sentences become more distant. 

	# clean text	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")	
	re_pattern = "[a-zA-ZäöüÄÖÜ0-9]+\\'?[a-zA-ZäöüÄÖÜ0-9]*\\'?[a-zA-ZäöüÄÖÜ0-9]*\\.?\\,?" # letters, commas, apostrophes, and full stops.	
	word_list = re.findall(re_pattern, generic_punctuation)			
	cleaned_text = " ".join(word_list)
	sent_list = cleaned_text.split('.')	
	
	overlap_scores1 = [] # adjacent sentences only
	overlap_scores = [] # full text
		
	keep_tags = ["VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP", "NN", "ADJD", "ADJA"]
	
	for sent1 in sent_list:
		if sent1 != "":
			lemma_list1 = []
			idx1 = sent_list.index(sent1)		
			words = nltk.word_tokenize(sent1) # lemmatization
			lemmata1 = tagger.tag_sent(words, taglevel = 1)
			
			for token in lemmata1:
				if token[2] in keep_tags:
					lemma_list1.append(token[1])
				
					
			for sent2 in sent_list:
				if sent2 != "":
					lemma_list2 = []
					idx2 = sent_list.index(sent2)
					words = nltk.word_tokenize(sent2)
					lemmata2 = tagger.tag_sent(words, taglevel = 1)
					
					if idx1 < idx2:
						adjustment = idx2 - idx1
					
						for token in lemmata2:							
							if token[2] in keep_tags:
								lemma_list2.append(token[1])
													
						for lemma in lemma_list2:							
							if lemma in lemma_list1:																

								if adjustment == 1:
									overlap_scores1.append(1)								
								
								score = 1 / adjustment
								overlap_scores.append(score)
								break							
							else:
								overlap_scores1.append(0)
								overlap_scores.append(0)
								break
	
	CONTENT_OL1m = mean(overlap_scores1)
	CONTENT_OL1sd = stdev(overlap_scores1)
	CONTENT_OLm = mean(overlap_scores)
	CONTENT_OLsd = stdev(overlap_scores)
	
	return round(CONTENT_OL1m, 5), round(CONTENT_OL1sd, 5), round(CONTENT_OLm, 5), round(CONTENT_OLsd, 5)		


####################################################################################################################


def type_token_ratio(text):
	### gives the percentage of new content words (nouns, adjectives, verbs, adverbs) among all content words in the text
		
	# clean text	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*\\.?\\,?" # letters, commas, apostrophes and full stops		
	word_list = re.findall(re_pattern, generic_punctuation) # convert text into a list of words			
	cleaned_text = " ".join(word_list)
	sent_list = cleaned_text.split('.')
	
	content_tokens = []
	content_types = []
	
	keep_tags = ["VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP" "NN", "ADJD", "ADJA", "ADV"]
	
	for sent in sent_list:
		if sent != "":
			words = nltk.word_tokenize(sent)
			lemmata = tagger.tag_sent(words, taglevel = 1)
			
			for lemma in lemmata:
				if lemma[2] in keep_tags:
					content_tokens.append(lemma[1])
					
					if lemma[1] not in content_types:
						content_types.append(lemma[1])
						
	TTR = len(content_types) / len(content_tokens) * 100
	
	return round(TTR, 3)
	
	
####################################################################################################################


def syntactic_complexity(text):
	### measures sytactic complexity as a proportion of the number of sytactic heads (NP and VP) to the total number of constituents
	### lower numbers indicate more complex syntax

	# clean text	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")	
	re_pattern = "[a-zA-ZäöüÄÖÜ0-9]+\\'?[a-zA-ZäöüÄÖÜ0-9*\\'?[a-zA-ZäöüÄÖÜ0-9]*\\.?\\,?" # letters, full stops, commas, and apostrophes		
	word_list = re.findall(re_pattern, generic_punctuation)		
	cleaned_text = " ".join(word_list)
	sent_list = cleaned_text.split('.')

	keep_tags = ["NN" "NE", "VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP"]
	
	complexity_scores = []
	
	for sent in sent_list:
		if sent != "":
			heads = 0
			constituents = 0
			
			words = nltk.word_tokenize(sent)
			lemmata = tagger.tag_sent(words, taglevel = 1)
		
			for lemma in lemmata:
				if lemma[2] in keep_tags:
					heads += 1
				if lemma[1] != '--':
					constituents += 1
				
			complexity_score = heads / constituents
			
			complexity_scores.append(complexity_score)
	
	SYNT_COMPm = mean(complexity_scores)
	SYNT_COMPsd = stdev(complexity_scores)
	
	return round(SYNT_COMPm, 3), round(SYNT_COMPsd, 3) 


####################################################################################################################


def konjunktiv_density(text):
	### measures the percentage of sentences that include at least one konjunktiv clause

	# clean text	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")	
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*\\.?\\,?" # letters, apostrophes, full stops, and commas		
	word_list = re.findall(re_pattern, generic_punctuation)			
	cleaned_text = " ".join(word_list)
	sent_list = cleaned_text.split('.')

	keep_tags = ["KOUS", "KOUI"]
		
	sent_count = 0
	konjunktiv_count = 0
	
	for sent in sent_list:
		if sent != "":
			sent_count += 1
			
			words = nltk.word_tokenize(sent)
			lemmata = tagger.tag_sent(words, taglevel = 1)
			
			for lemma in lemmata:
				if lemma[2] in keep_tags:
					konjunktiv_count += 1
					break
	
	KONJUNKTIVperc = konjunktiv_count / sent_count * 100
	
	return round(KONJUNKTIVperc, 3)
	
	
####################################################################################################################


def konjunktiv_length(text):
	### returns the mean and sd of konjuntiv clause length throughout a text
	### counts the number of words from and including the particle until the next verb
	### give preference to the auxiliary or modal verb as the last part of the clause
	
	# clean text	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")	
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*\\.?\\,?" # letters, apostrophes, commas, and full stops		
	word_list = re.findall(re_pattern, generic_punctuation)		
	cleaned_text = " ".join(word_list)
	sent_list = cleaned_text.split('.')

	konj_tags = ["KOUS", "KOUI"]
	verb_tags = ["VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP"]
	
	konj_lengths = []
	
	for sent in sent_list:
		if sent != "":		
			words = nltk.word_tokenize(sent)
			lemmata = tagger.tag_sent(words, taglevel = 1)
		
			for lemma in lemmata:
				if lemma[2] in konj_tags: # find konjunktive particle
					start_idx = lemmata.index(lemma)					
					distance = 1
					
					for lemma2 in lemmata[start_idx:]:
						distance += 1
						if lemma2[2] in verb_tags:						
							konj_lengths.append(distance)
							break
	
	if len(konj_lengths) > 1:					
		KONJ_LENm = mean(konj_lengths)
		KONJ_LENsd = stdev(konj_lengths)
			
	if len(konj_lengths) == 1:
		KONJ_LENm = konj_lengths[0]
		KONJ_LENsd = 0
		
	if len(konj_lengths) == 0:
		KONJ_LENm = 0
		KONJ_LENsd = 0							
				
	return round(KONJ_LENm, 3), round(KONJ_LENsd, 3)


####################################################################################################################


from csv import reader # read csv files

def concreteness(text):
	### rates concreteness of noun lemmas, POS tag "NN"
	### returns mean and standard deviation of nouns that exist in the database	

	### concreteness rating database by:	
	#   Charbonnier, J. & Wartena, C. (2020).
	#  		Predicting the Concreteness of German Words.
	#  		Proceedings of the 5th Swiss Text Analytics Conference (SwissText) 
	#		& 16th Conference on Natural Language Processing (KONVENS)
	
	
	# extract database to dictionary
	conc_dict = {}
	with open('program_files/concrete_de.csv', mode = 'r') as csv_file:
		conc_csv = reader(csv_file)
	
		for line in conc_csv:			
			tup = line[0].split(":")
			word = tup[0]
			rating = tup[1]
			conc_dict[word] = rating
		
	# clean text	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*\\.?\\,?" # letters, apostrophes, commas, and full stops		
	word_list = re.findall(re_pattern, generic_punctuation)			
	cleaned_text = " ".join(word_list)
	sent_list = cleaned_text.split('.')
		
	concrete_scores = []
	
	for sent in sent_list:
		sent = sent.lstrip() 
	
		words = nltk.word_tokenize(sent)
		lemmata = tagger.tag_sent(words, taglevel = 1)
			
		content_words = []
		for token in lemmata:
			if token[2] == 'NN':
				if token[1] in conc_dict:
					concrete_scores.append(float(conc_dict[token[1]]))
	
	CONCRETEm = mean(concrete_scores)
	CONCRETEsd = stdev(concrete_scores)

	return round(CONCRETEm, 3), round(CONCRETEsd, 3)

		
####################################################################################################################


def pronouns(text):
	### counts the percentage of words in a text tagged as pronoun 'PPER'
	
	# clean text
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'")	
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*\\.?\\,?" # letters, apostrophes, full stops, and commas	
	word_list = re.findall(re_pattern, generic_punctuation)	
	cleaned_text = " ".join(word_list) # rejoins as a clean text
	sent_list = cleaned_text.split('.') # split text into a list of sentences
	
	keep_tags = ["PPER"]
		
	pronoun_count = 0
	
	for sent in sent_list:
		sent = sent.lstrip() 
	
		words = nltk.word_tokenize(sent) # lemmatization
		lemmata = tagger.tag_sent(words, taglevel = 1)

		for token in lemmata:
			if token[2] in keep_tags:
				pronoun_count += 1

	
	num_words = word_count(text)
	
	PRONOUN = pronoun_count / num_words * 100
	
	return round(PRONOUN, 3)
			

####################################################################################################################


def make_data_dict():
	### create a dictionary of data for all .txt files in usr_input folder
	### texts should be copied as individual text files to the usr_input folder
	
	data_dict = {}
	titles = []

	for file in os.listdir('usr_input/'):#set keynames for dictionary
		
		if file.endswith('.txt'):
			titles.append(file)
					
	titles.sort() # data array in alphabetical order

	for title in titles:
	
		print("\r Analysieren {}".format(title), "\r")
		fname = open('usr_input/' + title, 'r') # Open file in read mode
		read_file = fname.read() # Set file as a string
		fname.close()
		
		WORD_COUNT = word_count(read_file)
		
		SENT_LENm, SENT_LENsd = sent_length(read_file)
		
		WORD_LENm, WORD_LENsd = word_length(read_file)
		
		NOUN_OL1m, NOUN_OL1sd, NOUN_OLm, NOUN_OLsd = noun_overlap(read_file)
		
		VERB_OL1m, VERB_OL1sd, VERB_OLm, VERB_OLsd = verb_overlap(read_file)
		
		CONTENT_OL1m, CONTENT_OL1sd, CONTENT_OLm, CONTENT_OLsd = content_word_overlap(read_file) 
		
		TTR = type_token_ratio(read_file)
		
		SYNT_COMPm, SYNT_COMPsd = syntactic_complexity(read_file)
		
		KONJ_PERC = konjunktiv_density(read_file)
		
		KONJ_LENm, KONJ_LENsd =  konjunktiv_length(read_file)
				
		CONCRETEm, CONCRETEsd = concreteness(read_file)
				
		PRONOUN = pronouns(read_file)
		
			
						
		data_dict[title] = (WORD_COUNT, SENT_LENm, SENT_LENsd, WORD_LENm, WORD_LENsd, NOUN_OL1m, NOUN_OL1sd, NOUN_OLm, NOUN_OLsd, VERB_OL1m, VERB_OL1sd, VERB_OLm, VERB_OLsd, CONTENT_OL1m, CONTENT_OL1sd, CONTENT_OLm, CONTENT_OLsd, TTR, SYNT_COMPm, SYNT_COMPsd, KONJ_PERC, KONJ_LENm, KONJ_LENsd, CONCRETEm, CONCRETEsd, PRONOUN)
		
	print("Abgeschlossen!")
	
	return data_dict


####################################################################################################################

				
from csv import writer # write CSV file

def data_array(dct, dt):
	### takes data dictionary created in extract_data() function and date_time string as input
	### writes a CSV data array to the *usr_output* folder for all texts in data dictionary
	### CSV file can be loaded into R, SPSS, Excel, etc for statistical analysis
		
	with open('usr_output/data_array_' + dt + '.csv', 'w') as data_csv:
			
		data_headers = ["Title","WORD_COUNT","SENT_LENm","SENT_LENsd","WORD_LENm","\
		WORD_LENsd", "NOUN_OL1m", "NOUN_OL1sd", "NOUN_OLm", "NOUN_OLsd", "VERB_OL1m", "VERB_OL1sd", "VERB_OLm", "VERB_OLsd", "CONTENT_OL1m", "CONTENT_OL1sd", "CONTENT_OLm", "CONTENT_OLsd", "TTR", "SYNT_COMPm", "SYNT_COMPsd", "KONJ_PERC", "KONJ_LENm", "KONJ_LENsd", "CONCRETEm","CONCRETEsd", "PRONOUN"]
		
		writer(data_csv).writerow(data_headers)		
		
		titles = []	# alphabetise the data array	
		for title in dct:
			titles.append(title)		
		titles.sort() 

		for title in titles:
			data_line = title, dct[title][0], dct[title][1], dct[title][2], dct[title][3], dct[title][4], dct[title][5], dct[title][6], dct[title][7], dct[title][8], dct[title][9], dct[title][10], dct[title][11], dct[title][12], dct[title][13], dct[title][14], dct[title][15], dct[title][16], dct[title][17], dct[title][18], dct[title][19], dct[title][20], dct[title][21], dct[title][22], dct[title][23], dct[title][24], dct[title][25]
			
			writer(data_csv).writerow(data_line)			



####################################################################################################################


from datetime import datetime # write current date and time to output files			

def main():
	### triggers the program
	
	dt_string = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")		
	text_data = make_data_dict()
	
	data_array(text_data, dt_string)



### RUN THE PROGRAM			
main()
