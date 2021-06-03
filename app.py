# coding=utf-8
import sys
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.flume import FlumeUtils

if __name__ == "__main__":

	# Criar spark context. Necessario quando a execucao for atraves do spark-submit
	conf = SparkConf().setAppName("Imprime na tela").set("master", "local")

	sc = SparkContext(conf = conf)

	# Frequência de update
	INTERVALO_BATCH = 10

	# Criando o StreamingContext
	ssc = StreamingContext(sc, INTERVALO_BATCH)

	# Cria um objeto DStream que puxa um streaming de dados do Apache Flume
	flumeStream = FlumeUtils.createStream(ssc, 'localhost', 4545)
	
	# Divide cada linha em palavras
	palavras = flumeStream.flatMap(lambda line: line.split(" "))

	# Conta cada palavra em cada batch
	pares = palavras.map(lambda palavra: (palavra, 1)) # Big Data Big Data -- (Big, 1) (Big, 1)
	contaPalavras = pares.reduceByKey(lambda x, y: x + y) # (Big, 2)
	
	# Imprime os 10 primeiros elementos de cada RDD gerado no DStream
	contaPalavras.pprint()

	# Salva o resultado das contagens em arquivo texto
	contaPalavras.saveAsTextFiles('tweet', suffix=None)


	ssc.start()             # Inicia a coleta e processamento do stream de dados
	ssc.awaitTermination()  # Aguarda a computação ser finalizada
	
