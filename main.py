import os # lib methods used for file reading/writing
import re # for extracting individual words and sentences

from statistics import mean # for descriptive statistics
from statistics import stdev


####################################################################################################################

def word_count(text):
	### counts contractions as one word, but does not count apostrophes
	### returns mean and standard deviation
	
	# clean text
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*'?[a-zA-ZäöüÄÖÜ]*" # Regex pattern catches all letters and apostrophes.
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'") # Replace non-standard punctuation	
	word_list = re.findall(re_pattern, generic_punctuation) # converts text into a string of words	
	WORD_COUNT = len(word_list)
	
	return WORD_COUNT


####################################################################################################################


def sent_length(text):
	### counts the number of words in each sentence
	### counts contractions as one word
	### returns mean and standard deviation
	
	# clean text
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*\\.?" # catch all letters, apostrophes and full stops	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'") # replace non-standard punctuation	
	word_list = re.findall(re_pattern, generic_punctuation) # convert text into a list of words	
	clean_text = " ".join(word_list) # rejoin as a clean text

	
	sent_list = clean_text.split('.') # split text into list of sentences, w/fullstop delimiter
		
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
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*" # catch all letters and apostrophes
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'") # replace non-standard punctuation	
	word_list = re.findall(re_pattern, generic_punctuation) # convert text into a list of words	
	
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
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'") # Replace non-standard punctuation	
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*\\.?\\,?" # catch all letters, apostrophes and full stops	
	
	word_list = re.findall(re_pattern, generic_punctuation) # convert text into a list of words	
	
	
	clean_text = " ".join(word_list) # rejoin as a clean text

	sent_list = clean_text.split('.') # split text into list of sentences
		
	concrete_scores = []
	
	for sent in sent_list:
		sent = sent.lstrip() 
	
		words = nltk.word_tokenize(sent) # lemmatization
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
	### counts the number of words in a text tagged as pronoun 'PPER'
	### score is calculated by dividing the number of pronouns by the word count, and multiplying by 1000
	
	
	# clean text
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'") # replace non-standard punctuation	
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*\\.?\\,?" # catch all letters, apostrophes, full stops, and commas
	
	word_list = re.findall(re_pattern, generic_punctuation) # convert text into a list of words	
	
	clean_text = " ".join(word_list) # rejoins as a clean text

	sent_list = clean_text.split('.') # split text into a list of sentences
		
	pronoun_count = 0
	
	for sent in sent_list:
		sent = sent.lstrip() 
	
		words = nltk.word_tokenize(sent) # lemmatization
		lemmata = tagger.tag_sent(words, taglevel = 1)

		for token in lemmata:
			if token[2] == 'PPER':
				pronoun_count += 1

	
	num_words = word_count(text)
	
	PRONOUN = pronoun_count / num_words * 100
	
	return round(PRONOUN, 3)
			

####################################################################################################################


def subordinate_clause(text):
	### calculates the percentage of subordinate particles incidence in a text.
	### divides the number of subordinate particles by the total word count and multiplies by 1000
	
	generic_punctuation = text.replace('!', '.').replace('?', '.').replace('’', "'").replace('‘', "'") # Replace non-standard punctuation
	re_pattern = "[a-zA-ZäöüÄÖÜ]+\\'?[a-zA-ZäöüÄÖÜ]*\\'?[a-zA-ZäöüÄÖÜ]*\\.?\\,?" # Regex pattern catches all letters, apostrophes and full stops		
	
	word_list = re.findall(re_pattern, generic_punctuation) # converts text into a string of words	
		
	clean_text = " ".join(word_list) # rejoins as a clean text

	sent_list = clean_text.split('.') # split text into a list of sentences
		
	num_words = word_count(text)
	
	sub_count = 0
	
	for sent in sent_list:
		sent = sent.lstrip() 
		
		if sent != "":
			
			# lemmatization
			words = nltk.word_tokenize(sent)
			lemmata = tagger.tag_sent(words, taglevel = 1) # sentence as list of lemmas
			
			for i in lemmata:
				if i[2] == 'KOUS': # find subordinate particle
					sub_count += 1

																	
	SUB_PARTS = (sub_count / num_words) * 1000
		
	return round(SUB_PARTS, 3)
			

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
	
		print("\r {} 0%            100%".format(title), end='\r')
		fname = open('usr_input/' + title, 'r') # Open file in read mode
		read_file = fname.read() # Set file as a string
		fname.close()
		
		WORD_COUNT = word_count(read_file)
		print("\r {} 0% >>         100%".format(title), end='\r')
		
		SENT_LENm, SENT_LENsd = sent_length(read_file)
		print("\r {} 0% >>>>        100%".format(title), end='\r')
		
		WORD_LENm, WORD_LENsd = word_length(read_file)
		print("\r {} 0% >>>>>>      100%".format(title), end='\r')
		
		CONCRETEm, CONCRETEsd = concreteness(read_file)
		print("\r {} 0% >>>>>>>>    100%".format(title), end='\r')
		
		PRONOUN = pronouns(read_file)
		print("\r {} 0% >>>>>>>>>>> 100%".format(title), end='\r')
			
						
		data_dict[title] = (WORD_COUNT, SENT_LENm, SENT_LENsd, WORD_LENm, WORD_LENsd, CONCRETEm, CONCRETEsd, PRONOUN)
		

	return data_dict


####################################################################################################################

				
from csv import writer # write CSV file

def data_array(dct, dt):
	### takes data dictionary created in extract_data() function and date_time string as input
	### writes a CSV data array to the *usr_output* folder for all texts in data dictionary
	### CSV file can be loaded into R, SPSS, Excel, etc for statistical analysis
		
	with open('usr_output/data_array_' + dt + '.csv', 'w') as data_csv:
			
		data_headers = ["Title","WORD_COUNT","SENT_LENm","SENT_LENsd","WORD_LENm","\
		WORD_LENsd","CONCRETEm","CONCRETEsd", "FREQUENCYm", "FREQUENCYsd", "PRONOUN"]
		
		writer(data_csv).writerow(data_headers)
		
		titles = []	# alphabetise the data array	
		for title in dct:
			titles.append(title)		
		titles.sort() 

		for title in titles:
			data_line = title, dct[title][0], dct[title][1], dct[title][2], dct[title][3], dct[title][4], dct[title][5], dct[title][6], dct[title][7]
			writer(data_csv).writerow(data_line)			
				
		data_footer = ["Title of text","Word count","Number of words in sentence, mean","Number of words in sentence, std dev","Word length, letters, mean","\
		Word length, letters, std dev", "Word concreteness, mean","Word concreteness, std dev", "Pronoun incidence"]
		
		writer(data_csv).writerow(data_footer)


####################################################################################################################


from datetime import datetime # write current date and time to output files			
def main():
	### triggers the program
	
	dt_string = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")		
	text_data = make_data_dict()
	
	data_array(text_data, dt_string)



### RUN THE PROGRAM			
main()			
			

	
	
	
	
	
	
	
	
	
	
