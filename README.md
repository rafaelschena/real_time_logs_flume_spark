# Processamento de Streaming de Dados em Tempo Real Com Apache Hadoop, Apache Flume e Spark Streaming

## Projeto nº6 da Formação Cientista de Dados da Data Science Academy

***Disclaimer**: O projeto em questão tem apenas fins didáticos, desenvolvido em ambiente de teste e com dados públicos, sem qualquer preocupação com a segurança dos dados e sem a pretensão de servir de modelo para qualquer implementação em ambiente de produção. Os requisitos necessários para reprodução deste experimento são instalações funcionais do Apache Flume, Apache Hadoop e Apache Spark, com todos os requisitos necessários para cada um destes pacotes. Neste trabalho especificamente foi utilizada a máquina virtual fornecida pela Data Science Academy como ambiente de testes e desenvolvimento. Para utilização do Twitter como fonte do streaming de dados também são necessárias as chaves de acesso para desenvolvedor conforme mostrado adiante.*

O objetivo deste projeto é criar um pipeline de dados em streaming com processamento em tempo real utilizando ferramentas do ecossistema Hadoop, como o Apache Flume para ingestão de dados, o sistema de arquivos HDFS do Hadoop para armazenamento em *cluster* e Apache Spark para processamento em tempo real. Como fonte de dados em tempo real será utilizado o *Twitter*, que será acessado através da API para o Apache Flume. A figura 1 ilustra o fluxograma do processamento de dados, com os dados sendo coletados da fonte em tempo real pelo Apache Flume, armazenados no HBase e processados em tempo real com o Spark Streaming.

![Fluxograma](fig1.png)

O projeto será executado em 3 etapas, a saber:
1. Estabelecimento do *Flume Agent* que coleta os dados do *Twitter* em tempo real, e distribui para duas *sinks*, o Apache HBase para armazenamento em *cluster* e o Spark Streaming para processamento em tempo real;
2. Armazenamento dos dados no cluster Hadoop diretamente no sistema de arquivos HDFS;
3. Processamento dos dados em tempo real com o Spark Streaming.


## Etapa 1: Estabelecimento do *Flume Agent*:

Para estabelecimento do *Flume agent* foi seguido o template mostrado na documentação do [Apache Flume](http://flume.apache.org/releases/content/1.9.0/FlumeUserGuide.html), conforme mostrado no exemplo abaixo, onde são declaradas as fontes, os *sinks* e os canais do agente, e em seguida cada um destes componentes são descritos:

```
# example.conf: A single-node Flume configuration

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source
a1.sources.r1.type = netcat
a1.sources.r1.bind = localhost
a1.sources.r1.port = 44444

# Describe the sink
a1.sinks.k1.type = logger

# Use a channel which buffers events in memory
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```
Para o estabelecimento de um agente como o mostrado na figura 1, é necessária a substituição da fonte r1 pela fonte do *Twitter*, a substituição da sink k1 pela fonte do HDFS e a criação de mais uma fonte do tipo *avro* para fazer a conexão com o Apache Spark.


Alteração da fonte r1 para a fonte Twitter, seguindo a documentação do Apache Flume:

```
a1.sources = r1
a1.channels = c1
a1.sources.r1.type = org.apache.flume.source.twitter.TwitterSource
a1.sources.r1.channels = c1
a1.sources.r1.consumerKey = YOUR_TWITTER_CONSUMER_KEY
a1.sources.r1.consumerSecret = YOUR_TWITTER_CONSUMER_SECRET
a1.sources.r1.accessToken = YOUR_TWITTER_ACCESS_TOKEN
a1.sources.r1.accessTokenSecret = YOUR_TWITTER_ACCESS_TOKEN_SECRET
a1.sources.r1.maxBatchSize = 10
a1.sources.r1.maxBatchDurationMillis = 200
```

As configurações do arquivo agent.conf são exibidas abaixo:
# Colocar o arquivo completo
```
# example.conf: A single-node Flume configuration

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source
a1.sources = r1
a1.channels = c1
a1.sources.r1.type = org.apache.flume.source.twitter.TwitterSource
a1.sources.r1.channels = c1
a1.sources.r1.consumerKey = YOUR_TWITTER_CONSUMER_KEY
a1.sources.r1.consumerSecret = YOUR_TWITTER_CONSUMER_SECRET
a1.sources.r1.accessToken = YOUR_TWITTER_ACCESS_TOKEN
a1.sources.r1.accessTokenSecret = YOUR_TWITTER_ACCESS_TOKEN_SECRET
a1.sources.r1.maxBatchSize = 10
a1.sources.r1.maxBatchDurationMillis = 200


# Describe the sink
a1.sinks.k1.type = logger

# Use a channel which buffers events in memory
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```

## Etapa 2: Armazenamento dos dados do Twitter no HDFS:

A gravação dos dados no HDFS se dá através da configuração de uma sink HDFS e sua ligação com o canal do Flume. Em nosso experimento, foi utilizada a mesma configuração mostrada no exemplo da documentação do Apache Flume:

```
a1.sinks.k1.type = hdfs
a1.sinks.k1.channel = c1
a1.sinks.k1.hdfs.path = /flume/events/%y-%m-%d/%H%M/%S
a1.sinks.k1.hdfs.filePrefix = events-
a1.sinks.k1.hdfs.round = true
a1.sinks.k1.hdfs.roundValue = 10
a1.sinks.k1.hdfs.roundUnit = minute
```
Uma amostra log do console exibido durante a gravação dos dados do Twitter para o HDFS através do Flume pode ser visto no arquivo Twitter_to_HDFS.log anexo.

No arquivo Troubleshooting.md pode ser vista a resolução de um problema ocorrido durante esta gravação, bem como sua causa e a solução encontrada.

## Etapa 3: Processamento dos dados com o Spark Streaming:
