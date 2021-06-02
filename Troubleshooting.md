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

# 3 - Enviando dados para a sink Avro:
Foi obtida a seguinte mensagem de erro:
2021-05-31 21:18:12,169 ERROR flume.SinkRunner: Unable to deliver event. Exception follows.
org.apache.flume.EventDeliveryException: Failed to send events
	at org.apache.flume.sink.AbstractRpcSink.process(AbstractRpcSink.java:398)
	at org.apache.flume.sink.DefaultSinkProcessor.process(DefaultSinkProcessor.java:67)
	at org.apache.flume.SinkRunner$PollingRunner.run(SinkRunner.java:145)
	at java.lang.Thread.run(Thread.java:748)
Caused by: org.apache.flume.FlumeException: NettyAvroRpcClient { host: localhost, port: 4545 }: RPC connection error
	at org.apache.flume.api.NettyAvroRpcClient.connect(NettyAvroRpcClient.java:177)
	at org.apache.flume.api.NettyAvroRpcClient.connect(NettyAvroRpcClient.java:115)
	at org.apache.flume.api.NettyAvroRpcClient.configure(NettyAvroRpcClient.java:598)
	at org.apache.flume.api.RpcClientFactory.getInstance(RpcClientFactory.java:90)
	at org.apache.flume.sink.AvroSink.initializeRpcClient(AvroSink.java:114)
	at org.apache.flume.sink.AbstractRpcSink.createConnection(AbstractRpcSink.java:217)
	at org.apache.flume.sink.AbstractRpcSink.verifyConnection(AbstractRpcSink.java:277)
	at org.apache.flume.sink.AbstractRpcSink.process(AbstractRpcSink.java:353)
	... 3 more
Caused by: java.io.IOException: Error connecting to localhost/127.0.0.1:4545
	at org.apache.avro.ipc.NettyTransceiver.getChannel(NettyTransceiver.java:261)
	at org.apache.avro.ipc.NettyTransceiver.<init>(NettyTransceiver.java:203)
	at org.apache.avro.ipc.NettyTransceiver.<init>(NettyTransceiver.java:152)
	at org.apache.flume.api.NettyAvroRpcClient.connect(NettyAvroRpcClient.java:165)
	... 10 more
Caused by: java.net.ConnectException: Connection refused: localhost/127.0.0.1:4545
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method)
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717)
	at org.jboss.netty.channel.socket.nio.NioClientBoss.connect(NioClientBoss.java:152)
	at org.jboss.netty.channel.socket.nio.NioClientBoss.processSelectedKeys(NioClientBoss.java:105)
	at org.jboss.netty.channel.socket.nio.NioClientBoss.process(NioClientBoss.java:79)
	at org.jboss.netty.channel.socket.nio.AbstractNioSelector.run(AbstractNioSelector.java:337)
	at org.jboss.netty.channel.socket.nio.NioClientBoss.run(NioClientBoss.java:42)
	at org.jboss.netty.util.ThreadRenamingRunnable.run(ThreadRenamingRunnable.java:108)
	at org.jboss.netty.util.internal.DeadLockProofWorker$1.run(DeadLockProofWorker.java:42)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	... 1 more
2021-05-31 21:18:17,174 INFO sink.AbstractRpcSink: Rpc sink k2: Building RpcClient with hostname: localhost, port: 4545
2021-05-31 21:18:17,174 INFO sink.AvroSink: Attempting to create Avro Rpc client.
2021-05-31 21:18:17,174 INFO api.NettyAvroRpcClient: Using default maxIOWorkers
2021-05-31 21:18:17,183 ERROR flume.SinkRunner: Unable to deliver event. Exception follows.
Erro causado pela falta de um agente recebendo os eventos enviados para a porta 4545. Quando havia "escuta" na porta especificada, o erro não se repetiu.

# 4 - Executando o código com o spark-submit
Foi obtida a seguinte mensagem de erro:
SyntaxError: Non-ASCII character '\xc3' in file /home/hadoop/Projeto_6/app.py on line 14, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details
Causa do erro: arquivo codificado em UTF-8, enquanto o Python tenta interpretar em ASCII
Resolvido incluindo o seguinte comentário na primeira linha do código # coding=utf-8, para indicar ao Python que o arquivo está em UTF-8.

# 5 - Tentando conectar o Spark com o Flume
Foi obtida a seguinte mensagem de erro:
21/06/01 21:13:05 ERROR PythonDStream$$anon$1: Cannot connect to Python process. It's probably dead. Stopping StreamingContext.
py4j.Py4JException: Cannot obtain a new communication channel
