# -*- coding: utf-8 -*-
import json as json
import codecs
import sqlite3 as sqlite
import rfc822
import datetime
from utilitarios import print_titulo
import os.path

print_titulo('Procesar JSON de archivos Tweets')

#VARIABLES DE CONFIGURACIÓN GLOBAL
total=1
acum_error=1
#dataset_dir="/home/mguevara/data/geograficos"
#dataset_dir="/home/mguevara/data/eventos"
dataset_dir="/Users/miguelguevara/Documents/data/elecciones"
#dataset_dir="/home/mguevara/data/elecciones"

#dataset_id = str(0)
#data_out_dir="/home/mguevara/datageograficos/"

#elecciones concertaciòn primarias, en MAC lab
dataset_id = "CNCRTA13"
data_out_dir="/Users/miguelguevara/Documents/dataelecciones/"

#dataset_id = "OSCR13"
#data_out_dir="/home/mguevara/dataeventos/"


#dataset_id = "US12"
#data_out_dir="/home/mguevara/dataElectionUS12/"

#dataset_id = "STGO12"
#data_out_dir="/home/mguevara/dataElectionSTGO12/"

#dataset_id = "CDP13"
#data_out_dir="/home/mguevara/dataElectionCDP13/"

name_db = "tweets"+ dataset_id +".db"
log= "errores.log"

usuarios={}

def procesa(file):
	global total
	global acum_error	
	global out
	global log	
	global tweets_por_archivo
	global acum_nuevo_archivo
	global usuarios
	#se deben codificar a unicode utf-8 de lo contrario resultan errores con caracteres extraños
	f = codecs.open(file, encoding='utf-8', mode='r')
	
	
	DATABASE_NAME = os.path.join(data_out_dir, name_db)
	is_new_database = os.path.exists(DATABASE_NAME)

	connection = sqlite.connect(DATABASE_NAME)

	if not is_new_database:
		cursor = connection.cursor()
		cursor.executescript("""
		  create table tweet(
			id primary key,
			dataset_id,			
			created_at, 
			text, 
			user_id, 	
			user_name, 
			user_screen_name, 
			user_lang, 
			user_location, 
			user_created_at, 			
			user_followers_count, 
			user_friends_count,
			user_following,
			place, 
			coordinates, 
			hashtags, 
			in_reply_to_user_id_str, 
			retweeted, 
			retweet_count
		   );
		""")

	cursor = connection.cursor()

	ln = 1
	tw=1
	lgn=1
	for l in f:	
		try:	
		    content = json.loads(str(l))
		    #print "BIEN!"	        	
	 	    if "text" in content: 		   
			   #Exportación para Base de datos
			   #INFORMACION BASICA
			   ########################################
			    id= u"{0[id]}".format(content)
			    user_id = u"{0[user][id]}".format(content)		    
			    created_temp = u"{0[created_at]}".format(content)	    		   
			    created_at = datetime.datetime(*rfc822.parsedate(created_temp)[:6])
			    text = u"{0[text]}".format(content)


			   #RELACIONADO AL RETWEET
			    retweet_count =  u"{0[retweet_count]}".format(content)
			    retweeted = u"{0[retweeted]}".format(content)
			    in_reply_to_user_id_str = u"{0[in_reply_to_user_id_str]}".format(content)    
			   
				#HASHTAGS Y URLS
			    #cadena+= u"{0[entities][urls]}".format(content) + "\t"
			    #url = u"{0[entities][urls][url]}".format(content)
			    #indices = u"{0[entities][urls][indices]}".format(content)
			    indices = u"{0[entities][urls]}".format(content)
			    hashtags= u"{0[entities][hashtags]}".format(content)
			   
				#DE LOCALIZACION Y GEOGRAFICOS
			    
			    #cadena+= u"{0[geo]}".format(content) +"\t"
			    coordinates = u"{0[coordinates]}".format(content)
			    place = u"{0[place]}".format(content) +"\t"
			    #cadena+= u"{0[source]}".format(content) +"\n"

				#DE USUARIO Y VINCULACION
			    user_location = u"{0[user][location]}".format(content)
			    created_temp = u"{0[user][created_at]}".format(content)	    		   
			    user_created_at = datetime.datetime(*rfc822.parsedate(created_temp)[:6])

			    #cadena+= u"{0[user][created_at]}".format(content) +"\t"
			  #user_id = u"{0[user][id]}".format(content)
			    user_name = u"{0[user][name]}".format(content)
			    user_lang = u"{0[user][lang]}".format(content)
			    user_followers_count = u"{0[user][followers_count]}".format(content)
			    user_friends_count = u"{0[user][friends_count]}".format(content)
			    user_following = u"{0[user][following]}".format(content)
			    user_screen_name = u"{0[user][screen_name]}".format(content)

				#VARIADOS PARA NALISIS USUARIO
			   # cadena+= u"{0[created_at]}".format(content) +"\t"
			   # cadena+= u"{0[user][id]}".format(content) +"\t"
			   # cadena+= u"{0[user][screen_name]}".format(content) +"\t"
			   # cadena+= u"{0[user][name]}".format(content) +"\t"
			   # cadena+= u"{0[user][lang]}".format(content) +"\t"
			   # cadena+= u"{0[user][followers_count]}".format(content) +"\t"
			   # cadena+= u"{0[user][friends_count]}".format(content) +"\n"
			    #cadena+= u"{0[user][following]}".format(content) +"\n"
                   
			    #OBTIENE UN ARCHIVO CON LOS ID DE LOS USUARIOS
		         #id_usuario = u"{0[user][id]}".format(content)
			    #if id_usuario not in usuarios:
				#   usuarios[id_usuario]= u"{0[user][screen_name]}".format(content)
				 #  cadena+= id_usuario + "\t" +  u"{0[user][screen_name]}".format(content) + "\n"
                   #"""
												
			    cursor.execute("insert or replace into tweet(id, dataset_id,created_at, user_id, user_name, user_screen_name, user_lang, user_location, user_created_at, place, coordinates, user_followers_count, user_friends_count, user_following, text, hashtags, in_reply_to_user_id_str, retweeted, retweet_count) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (id,dataset_id, created_at, user_id, user_name, user_screen_name, user_lang, user_location, user_created_at, place, coordinates, user_followers_count, user_friends_count, user_following, text, hashtags, in_reply_to_user_id_str, retweeted, retweet_count))
		    	    tw += 1
			    total += 1
			   
		except ValueError:
			#print "\nERROR AL LEER LINEA ",ln
			lg.write("Total:" + str(total) + " " +str(l))
			#lg.write("\n")
			lgn += 1
			acum_error += 1
			#print l
	
		ln = ln + 1

	connection.commit()
	

	print "\n\tEstadisticas del Archivo procesado"
	print "\t\tTweets extraidos: " + str(tw-1)
	print "\t\tLineas no leídas: " + str(lgn-1)


	
#INICIA PRINCIPAL
def configura():
	global dataset_dir
	global out
	global log
	global tweets_por_archivo
	global o
	global lg

	print_titulo("Configuraciones iniciales")
	files = os.listdir(dataset_dir)	
	directorios = dict()	
	acum = 1
	for name in files:
	    path = os.path.join(dataset_dir, name)
	    if not(os.path.isfile(path)):
		directorios[acum] = name	
		print "\t" + str(acum) + ") " + name	
		acum+=1
	#print f_json

	m=raw_input("Indique directorio a procesar " + dataset_dir + " : ")
	dataset_dir = os.path.join(dataset_dir, directorios[int(m)])

	log1 = os.path.join(data_out_dir,log) #arcvhivo abierto para guardar errores	
	print "Archivo con tweets erróneos: " + log1
	#m=raw_input("...continuar")
	
	#abre log
	lg = codecs.open(log1, encoding='utf-8', mode='w')

	return 	dataset_dir


def iniciar(cwd):
	print_titulo("Elija el archivo a procesar, ENTER para todos")
	files = os.listdir(cwd)
	files.sort()
	#print type(files2)
	#print files2
	acum = 0
	f_json = dict()

	for name in files:
	    if name[-5:] == ".json":	
		acum+=1
		f_json[acum] = name	
		print "\t" + str(acum) + ") " + name	
	#print f_json
	m=raw_input(": ")
	ac=1
	if m == "" or m =="0":
	    for file in f_json:
		aprocesar = cwd + "/" + f_json[int(file)]
		print_titulo("Procesando Archivo: " +str(ac)+ " " + aprocesar)
		procesa(aprocesar)
		ac+=1
	
	else:
	    aprocesar= cwd + "/" + f_json[int(m)]
	    print "Procesando: " + aprocesar
	    procesa(aprocesar)


	
cwd = configura()
iniciar(cwd)


print_titulo('Estadisticas FINALES')
print "\tTweets extraidos: " + str(total-1)
print "\tTweets erróneos: " + str(acum_error-1)  
print_titulo("FIN EJECUCION")

lg.close()

	
	
#file= '/home/mguevara/datasets/tweets/12Jul-3.json'

