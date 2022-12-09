#TextAnalyzerDE (RADE)

TextAnalyzerDE (RADE) is a readability analyser for German texts, written in Python. It is inspired by Coh-Metrix, an online tool that measures several readability characteristics of English.

I'm in the process of writing a user report of correlation strengths to CEFR ratings.

My access to a testing material (or statistics knowledge for that matter) makes it difficult to do any kind of principle component analysis, but I welcome offers of collaboration.


##Licensing

I'm happy for people to use the components of this program that I myself have written for their own projects, as long as they credit me as per the licence.

***HOWEVER***
Please be aware that there are elements of this program that are derived others, which may or may not specify different license terms, including non-commercial use. Please respect their work by adhering to their respective licences.

Specifically these components are:

**German word concreteness database**
Used to calculate average concreteness ratings for nouns (stored in program files as *concrete_de.csv*.

Creators:
Charbonnier, J. & Wartena, C. (2020). Predicting the Concreteness of German Words. Proceedings of the 5th Swiss Text Analytics Conference (SwissText) & 16th Conference on Natural Language Processing (KONVENS)

URL: http://textmining.wp.hs-hannover.de/datasets.html

**HannoverTagger (HanTa)**
Lemmatiser and part of speech tagging library.

Creator:
Wartena, C. (2019). A Probabilistic Morphology Model for German Lemmatization. Proceedings of the 15th Conference on Natural Language Processing (KONVENS 2019): Long Papers. 40-49. https://doi.org/10.25968/opus-1527

URL: https://github.com/wartaal/HanTa
License: https://github.com/wartaal/HanTa/blob/master/LICENSE

**TIGER corpus**
The training corpus for HanTa

Creator:
Brants, S., Stefanie Dipper, S., Eisenberg, P., Hansen, S., König, E., Lezius, W., Rohrer, C., Smith, G., & Uszkoreit. H. (2004). TIGER: Linguistic Interpretation of a German Corpus. Journal of Language and Computation, 2, 597-620

URL: https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger/
License: https://www.ims.uni-stuttgart.de/documents/ressourcen/korpora/tiger-corpus/license/htmlicense.html


##Instructions

It needs to be run from a terminal or command line. Ensure you have all dependent packages installed - Python3, HanTa, etc. You'll soon know if you need anything because the program won't run!

Download the program script *main.py*, and the folders *program_files* , *usr_input*, and *usr_output* into a directory of your choice. 

**Achtung!**
It is critical that these folders are included in the program directory named exactly as above. For this reason, I have included place holder files (A section of German Wikipedia's 'Die Deutsche Sprache' entry) in the *usr_input* folder, and it's data in the *usr_output* to get around the fact that Github doesn't like empty folders in a repository. 

Paste one or more German texts that you want to analyse into the *usr_input* folder with .txt file extension. Each text file is treated as an individual case in the data output. 

Navigate to the program directory, and run by typing Python3 main.py

Depending the number and size of the text, the analysis may take several moments. Each text will be listed in the output screen as it is being analysed. 

When the program is finished, the message *Abgeschlossen!* will be printed to the screen.
 
A CSV file (comma delimited) will be created in the *usr_output* folder with the name *data_array_date-and-time.csv*. This can be loaded into the statistical package of your choice (R, SPSS, etc.). Ensure to remove the variable description row before performing statistical analysis, and add any additional independent variables (eg. difficulty level, text genre, etc.).


##Variable descriptions
Apart from the title, 26 data variable columns will be created. I'll give a brief description of each one below, as well references to literature. For a great overall introduction to automated readability analysis, I recommend the following:

Graesser, A. C., McNamara, D. S., & Kulikowich, J. M. (2011). Coh-Metrix: Providing multilevel analyses of text characteristics. Educational Researcher, 40(5), 223–234. https://doi.org/10.3102/0013189X11413260

Graesser, A. C., McNamara, D. S., Cai, Z., Conley, M., Li, H., & Pennebaker, J. (2014). Coh-Metrix measures text characteristics at multiple levels of language and discourse. The Elementary School Journal, 115(2), 210–229. https://doi.org/10.1086/678293

###*WORD_COUNT*
The number of words in the text. Contractions are counted as one word.

###*SENT_LENm, SENT_LENsd*

Sentence length (mean and standard deviation) as the number of words per sentence. Again Contractions are counted as one word. This is a crude, yet tried and tested reflection of syntactic complexity - that is, the more words in a sentence, the more constituents.

Flesch, R. (1948). A new readability yardstick. Journal of Applied Psychology, 32(3), 221–233. https://doi.org/10.1037/h0057532

Kincaid, J. P., Fishburne, J., Rogers, R. L., & Chissom, B. S. (1975). Derivation of new readability formulas (Automated Readability Index, Fog Count and Flesch Reading Ease Formula) for navy enlisted personnel


###*WORD_LENm, WORD_LENsd*
Word length by number of letters. Commas in contractions are not counted. Longer words tend to be more abstract and correlate to age of acquisition (we learn them later in life).

Reilly, J., Hung, J., & Westbury, C. (2017). Non‐Arbitrariness in Mapping Word Form to Meaning: Cross‐Linguistic Formal Markers of Word Concreteness. Cognitive Science, 41(4), 1071–1089. https://doi.org/10.1111/cogs.12361


###*NOUN_OL1m, NOUN_OL1sd, NOUN_OLm, NOUN_OLsd*

###*VERB_OL1m, VERB_OL1sd, VERB_OLm, VERB_OLsd*

###*CONTENT_OL1m, CONTENT_OL1sd, CONTENT_OLm, CONTENT_OLsd*
	Overlap between sentences (ending with 1) and across all sentences of various parts of speech. Represents the cognitive mechanism of semantic activation. If a word is repeated throughout a text, it remains active in our brain and is easier to process next time we encounter it. A weakening effect is calculated into the data as the sentences become more distant.

Bock, J. K. (1986). Syntactic persistence in language production. Cognitive Psychology, 18(3), 355–387. https://doi.org/10.1016/0010-0285(86)90004-6

Fine, A. B., & Jaeger, T. F. (2016). The Role of Verb Repetition in Cumulative Structural Priming in Comprehension. Journal of Experimental Psychology. Learning, Memory, and Cognition, 42(9), 1362–1376. https://doi.org/10.1037/xlm0000236

Hoedemaker, R. S., & Gordon, P. C. (2014). It takes time to prime: semantic priming in the ocular lexical decision task. Journal of Experimental Psychology. Human Perception and Performance, 40(6), 2179–2197. https://doi.org/10.1037/a0037677

Spätgens, T., & Schoonen, R. (2018). The semantic network, lexical access, and reading comprehension in monolingual and bilingual children: An individual differences study – corrigendum. Applied Psycholinguistics, 39(2), 461–461. https://doi.org/10.1017/S0142716418000012

###*TTR*
	Type-token ratio for content word lemmas. This is the percentage of new content words that appear throughout a text. The higher the number, the more often we have to access our lexicon.

Jarvis, S. (2013). Capturing the diversity in lexical diversity. Language Learning, 63(s1), 87–106. https://doi.org/10.1111/j.1467-9922.2012.00739.x

###*SYNT_COMPm, SYNT_COMPsd*
	A measure of syntactic complexity calculated as the proportion of syntax tree heads (NPs and VPs) to the number of individual constituents in a sentence. Lower numbers indicate more complex sentences.

Köhler, R., & Altmann, G. (2000). Probability Distributions of Syntactic Units and Properties. Journal of Quantitative Linguistics, 7(3), 189–200. https://doi.org/10.1076/jqul.7.3.189.4114

###*KONJ_PERC*
	A representation of syntactic complexity. The percentage of sentences throughout a text that contain at least one Konjunkitv (subjunctive) clause, such as those starting with *weil * or *dass*.

###*KONJ_LENm, KONJ_LENsd*
	The average length of Konjunktiv (subordinate) clauses throughout a text, calculated as the distance between (and including) the Konjunktiv particle and the verb. This represents the amount of information that must be held in working memory before the the verb is encountered to tie the rest of the sentence together.

Caplan, D., & Waters, G. (2013). Memory mechanisms supporting syntactic comprehension. Psychonomic Bulletin & Review, 20(2), 243–268. https://doi.org/10.3758/s13423-012-0369-9

Gibson, E. (1998). Linguistic complexity: locality of syntactic dependencies. Cognition, 68(1), 1–76. https://doi.org/10.1016/S0010-0277(98)00034-1

Gibson, E., & Warren, T. (2004). Reading-Time Evidence for Intermediate Linguistic Structure in Long-Distance Dependencies. Syntax, 7(1), 55–78. https://doi.org/10.1111/j.1368-0005.2004.00065.x

Hawkins, J. A. (1990). A Parsing Theory of Word Order Universals. Linguistic Inquiry, 21(2), 223–261. https://www.jstor.org/stable/4178670


###*CONCRETEm, CONCRETEsd*
	The mean and standard deviation of concreteness ratings of nouns. When a noun represents a real-world physical object (such as *dog*, *tree*, or *chair*), it is easier to process than a noun that represents an abstract concept (such as *freedom*, *emotion*, etc.). 

Blomberg, F., & Öberg, C. (2015). Swedish and English word ratings of imageability, familiarity and age of acquisition are highly correlated. Nordic Journal of Linguistics, 38(3), 351–364. https://doi.org/10.1017/S0332586515000220

Brysbaert, M., Warriner, A. B., & Kuperman, V. (2014a). Concreteness ratings for 40 thousand generally known English word lemmas. Behavior Research Methods, 46(3), 904–911. https://doi.org/10.3758/s13428-013-0403-5

Brysbaert, M., Stevens, M., De Deyne, S., Voorspoels, W., & Storms, G. (2014b). Norms of age of acquisition and concreteness for 30,000 Dutch words. Acta Psychologica, 150, 80–84. https://doi.org/10.1016/j.actpsy.2014.04.010

###*PRONOUN*
	The percentage of total words in the text that are tagged as a personal pronouns. Pronouns are indicative a narrative genre which, overall tends to be easier to read than informative or argumentative genres.

Simon-Shoshan, M. (2013). Narrativity and the study of stories. Workshop on Computational Models of Narrative. 228-237. 10.4230/OASIcs.CMN.2013.228

###SUMMARY OF VARIABLES
**WORD_COUNT** Number of words in text
**SENT_LENm** Number of words in sentence, mean
**SENT_LENsd** Number of words in sentence, std dev
**WORD_LENm** Word length, letters, mean
**WORD_LENsd** Word length, letters, std dev
**NOUN_OL1m** Noun lemma overlap, adjacent sentences, mean
**NOUN_OL1sd** Noun lemma overlap, adjacent sentences, std dev
**NOUN_OLm** Noun lemma overlap, all sentences, mean
**NOUN_OLsd** Noun lemma overlap, all sentences, std dev
**VERB_OL1m** Verb lemma overlap, adjacent sentences, mean
**VERB_OL1sd** Verb lemma overlap, adjacent sentences, std dev
**VERB_OLm** Verb lemma overlap, all sentences, mean
**VERB_OLsd** Verb lemma overlap, all sentences, std dev
**CONTENT_OL1m** Content word lemma overlap, adjacent sentences, mean
**CONTENT_OL1sd** Content word lemma overlap, adjacent sentences, std dev
**CONTENT_OLm** Content word lemma overlap, all sentences, mean
**CONTENT_OLsd** Content word lemma overlap, all sentences, std dev
**TTR** Type-token ratio, content word lemmas
**SYNT_COMPm** Proportion of NP and VP heads to constituents, mean
**SYNT_COMPsd** Proportion of NP and VP heads to constituents, sd
**KONJ_PERCm** Percentage of sentences with at least on Konjunktiv clause
**KONJ_LENm** Distance between konjunktiv particle and verb, mean
**KONJ_LENsd** Distance between konjunktiv particle and verb, std dev
**CONCRETEm** Word concreteness, mean
**CONCRETEsd** Word concreteness, std dev
**PRONOUN** Pronoun incidence
