#import nltk,re

#global IV	#Identificador de indice para numerar documentos de vocabulario
#IV = 0
#stopwords = nltk.corpus.stopwords.words('english')
#porter = nltk.PorterStemmer()
#wnl = nltk.WordNetLemmatizer()
#import nltk,re
import re

def print_titulo(tit):
	print '\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
	print '            ' + tit 
	print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'


def guarda_indice(dic,  nombre):
    output_file = open(nombre , 'w')
    for term in sorted(dic):
    	output_file.write(str(term) + "\t" + str(dic[term])+"\n")

    output_file.close()	

def guarda_matriz_u(matriz,  nombre, feature_matrix):
    output_file = open(nombre , 'w')
    matriz_list = matriz.tolist()  
    matriz_list.reverse()
    for term in feature_matrix:
    	output_file.write(str(term) + "\t" + str(matriz_list.pop())+"\n")
   # for w in matriz:
	#    output_file.write(str(matriz[int(w)]))
    #output_file.write(matriz)
    #matriz.tofile(output_file, sep="\n", format="%s")
    output_file.close()	

def guarda_matriz_sigma(matriz,  nombre):
    output_file = open(nombre , 'w')
    matriz_list = matriz.tolist() 
    for term in matriz_list:
    	output_file.write(str(term)+"\n")
    output_file.close()	

def guarda_matriz_vt(matriz,  nombre, indice):
    output_file = open(nombre , 'w')
    for term in sorted(indice):
    	output_file.write(str(term) + ", ")

    matriz_list = matriz.tolist() 
    #matriz_list.reverse()
    for term in matriz_list:
    	output_file.write("\n" + str(term))
    output_file.close()	


def procesa_words(text, c_stopwords, c_porter, c_lematizacion, c_alpha, c_lower):
	#print 'Creando vocabulario...'
    if c_lower:
    	words = [w.lower() for w in text]
    else:
	words = [w for w in text]
   
    #miravocab(vocab, 'Tokens')
    
    if c_stopwords:
	stopwords = nltk.corpus.stopwords.words('english')
	#print 'Vocabulario Elimina STOPWORDS'
	words = [w for w in words if w.lower() not in stopwords]

    if c_alpha:
	#print 'Vocabulario Solo Terminos de letras (Alpha. Sin numeros)'
	words = [w for w in words if w.isalpha()]
	

    if c_porter:
	porter = nltk.PorterStemmer()
	#print 'Vocario aplicado Porter'
	words = [porter.stem(t) for t in words]

    if c_lematizacion:
	wnl = nltk.WordNetLemmatizer()
	#print 'Vocabulario + Lematizacion'
	words=[wnl.lemmatize(t) for t in words]
	
    return words
