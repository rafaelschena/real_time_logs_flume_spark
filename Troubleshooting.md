# Troubleshooting:
## 1 - Gravando os dados do Twitter na sink HDFS
Foi obtida a seguinte mensagem de erro:
2021-05-29 19:13:58,104 ERROR hdfs.HDFSEventSink: process failed
java.lang.NullPointerException: Expected timestamp in the Flume event headers, but it was null
	at com.google.common.base.Preconditions.checkNotNull(Preconditions.java:204)
	at org.apache.flume.formatter.output.BucketPath.replaceShorthand(BucketPath.java:251)
	at org.apache.flume.formatter.output.BucketPath.escapeString(BucketPath.java:460)
	at org.apache.flume.sink.hdfs.HDFSEventSink.process(HDFSEventSink.java:379)
	at org.apache.flume.sink.DefaultSinkProcessor.process(DefaultSinkProcessor.java:67)
	at org.apache.flume.SinkRunner$PollingRunner.run(SinkRunner.java:145)
	at java.lang.Thread.run(Thread.java:748)
2021-05-29 19:13:58,104 ERROR flume.SinkRunner: Unable to deliver event. Exception follows.

Causa do erro: Mensagem enviada à sink esperava um timestamp que não havia neste formato de dados.


Solução: descrita na própria documentação do Flume, em: http://flume.apache.org/releases/content/1.9.0/FlumeUserGuide.html#hdfs-sink
Configurar o parâmetro da sink hdfs.useLocalTimeStamp como true.


## 2 - Replicando o streaming do Twitter para uma sink Avro:
Foi obtida a seguinte mensagem de erro:
2021-05-31 19:56:42,428 ERROR flume.SinkRunner: Unable to deliver event. Exception follows.
org.apache.flume.EventDeliveryException: Failed to send events
O erro foi causado por uma configuração incorreta do agente Flume. Quando a fonte está conectada a mais de um canal, a descrição do fluxo deve ser feita conforme o exemplo abaixo:
```
# Descrevendo o fluxo de dados
a1.sources.r1.channels = c1 c2
a1.sinks.k1.channel = c1
a1.sinks.k2.channel = c2
```

