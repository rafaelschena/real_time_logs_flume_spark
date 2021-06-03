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
Traceback (most recent call last):
  File "/home/hadoop/Projeto_6/app.py", line 24, in <module>
    palavras = linhas.flatMap(lambda line: line.split(" "))
Causa: bug na cópia de código. 

#6 - Tentando conectar o Spark com o Flume
Foi obtidas as seguintes mensagens de erro:
Traceback (most recent call last):
  File "/home/hadoop/Projeto_6/app.py", line 38, in <module>
    ssc.awaitTermination()  # Aguarda a computação ser finalizada
  File "/opt/spark/python/lib/pyspark.zip/pyspark/streaming/context.py", line 192, in awaitTermination
  File "/opt/spark/python/lib/py4j-0.10.7-src.zip/py4j/java_gateway.py", line 1257, in __call__
  File "/opt/spark/python/lib/py4j-0.10.7-src.zip/py4j/protocol.py", line 328, in get_return_value
py4j.protocol.Py4JJavaError: An error occurred while calling o27.awaitTermination.
: org.apache.spark.SparkException: An exception was raised by Python:
Traceback (most recent call last):
  File "/opt/spark/python/lib/pyspark.zip/pyspark/streaming/util.py", line 68, in call
    r = self.func(t, *rdds)
  File "/opt/spark/python/lib/pyspark.zip/pyspark/streaming/dstream.py", line 173, in takeAndPrint
    taken = rdd.take(num + 1)
  File "/opt/spark/python/lib/pyspark.zip/pyspark/rdd.py", line 1360, in take
    res = self.context.runJob(self, takeUpToNumLeft, p)
  File "/opt/spark/python/lib/pyspark.zip/pyspark/context.py", line 1069, in runJob
    sock_info = self._jvm.PythonRDD.runJob(self._jsc.sc(), mappedRDD._jrdd, partitions)
  File "/opt/spark/python/lib/py4j-0.10.7-src.zip/py4j/java_gateway.py", line 1257, in __call__
    answer, self.gateway_client, self.target_id, self.name)
  File "/opt/spark/python/lib/py4j-0.10.7-src.zip/py4j/protocol.py", line 328, in get_return_value
    format(target_id, ".", name), value)
Py4JJavaError: An error occurred while calling z:org.apache.spark.api.python.PythonRDD.runJob.
: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 31.0 failed 1 times, most recent failure: Lost task 0.0 in stage 31.0 (TID 29, localhost, executor driver): org.apache.spark.api.python.PythonException: Traceback (most recent call last):
  File "/opt/spark/python/lib/pyspark.zip/pyspark/worker.py", line 377, in main
    process()
  File "/opt/spark/python/lib/pyspark.zip/pyspark/worker.py", line 372, in process
    serializer.dump_stream(func(split_index, iterator), outfile)
  File "/opt/spark/python/lib/pyspark.zip/pyspark/rdd.py", line 2499, in pipeline_func
  File "/opt/spark/python/lib/pyspark.zip/pyspark/rdd.py", line 2499, in pipeline_func
  File "/opt/spark/python/lib/pyspark.zip/pyspark/rdd.py", line 352, in func
  File "/opt/spark/python/lib/pyspark.zip/pyspark/rdd.py", line 1861, in combineLocally
  File "/opt/spark/python/lib/pyspark.zip/pyspark/shuffle.py", line 238, in mergeValues
    for k, v in iterator:
  File "/opt/spark/python/lib/pyspark.zip/pyspark/streaming/flume.py", line 123, in func
  File "/opt/spark/python/lib/pyspark.zip/pyspark/streaming/flume.py", line 38, in utf8_decoder
    return s.decode('utf-8')
  File "/usr/lib64/python2.7/encodings/utf_8.py", line 16, in decode
    return codecs.utf_8_decode(input, errors, True)
UnicodeDecodeError: 'utf8' codec can't decode byte 0xe4 in position 17: invalid continuation byte

	at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:452)
	at org.apache.spark.api.python.PythonRunner$$anon$1.read(PythonRunner.scala:588)
	at org.apache.spark.api.python.PythonRunner$$anon$1.read(PythonRunner.scala:571)
	at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:406)
	at org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)
	at scala.collection.Iterator$GroupedIterator.fill(Iterator.scala:1124)
	at scala.collection.Iterator$GroupedIterator.hasNext(Iterator.scala:1130)
	at scala.collection.Iterator$$anon$11.hasNext(Iterator.scala:409)
	at org.apache.spark.shuffle.sort.BypassMergeSortShuffleWriter.write(BypassMergeSortShuffleWriter.java:125)
	at org.apache.spark.scheduler.ShuffleMapTask.runTask(ShuffleMapTask.scala:99)
	at org.apache.spark.scheduler.ShuffleMapTask.runTask(ShuffleMapTask.scala:55)
	at org.apache.spark.scheduler.Task.run(Task.scala:121)
	at org.apache.spark.executor.Executor$TaskRunner$$anonfun$10.apply(Executor.scala:408)
	at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:1360)
	at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:414)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)

Driver stacktrace:
	at org.apache.spark.scheduler.DAGScheduler.org$apache$spark$scheduler$DAGScheduler$$failJobAndIndependentStages(DAGScheduler.scala:1889)
	at org.apache.spark.scheduler.DAGScheduler$$anonfun$abortStage$1.apply(DAGScheduler.scala:1877)
	at org.apache.spark.scheduler.DAGScheduler$$anonfun$abortStage$1.apply(DAGScheduler.scala:1876)
	at scala.collection.mutable.ResizableArray$class.foreach(ResizableArray.scala:59)
	at scala.collection.mutable.ArrayBuffer.foreach(ArrayBuffer.scala:48)
	at org.apache.spark.scheduler.DAGScheduler.abortStage(DAGScheduler.scala:1876)
	at org.apache.spark.scheduler.DAGScheduler$$anonfun$handleTaskSetFailed$1.apply(DAGScheduler.scala:926)
	at org.apache.spark.scheduler.DAGScheduler$$anonfun$handleTaskSetFailed$1.apply(DAGScheduler.scala:926)
	at scala.Option.foreach(Option.scala:257)
	at org.apache.spark.scheduler.DAGScheduler.handleTaskSetFailed(DAGScheduler.scala:926)
	at org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.doOnReceive(DAGScheduler.scala:2110)
	at org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.onReceive(DAGScheduler.scala:2059)
	at org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.onReceive(DAGScheduler.scala:2048)
	at org.apache.spark.util.EventLoop$$anon$1.run(EventLoop.scala:49)
	at org.apache.spark.scheduler.DAGScheduler.runJob(DAGScheduler.scala:737)
	at org.apache.spark.SparkContext.runJob(SparkContext.scala:2061)
	at org.apache.spark.SparkContext.runJob(SparkContext.scala:2082)
	at org.apache.spark.SparkContext.runJob(SparkContext.scala:2101)
	at org.apache.spark.api.python.PythonRDD$.runJob(PythonRDD.scala:153)
	at org.apache.spark.api.python.PythonRDD.runJob(PythonRDD.scala)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
	at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
	at py4j.Gateway.invoke(Gateway.java:282)
	at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
	at py4j.commands.CallCommand.execute(CallCommand.java:79)
	at py4j.GatewayConnection.run(GatewayConnection.java:238)
	at java.lang.Thread.run(Thread.java:748)
Caused by: org.apache.spark.api.python.PythonException: Traceback (most recent call last):
  File "/opt/spark/python/lib/pyspark.zip/pyspark/worker.py", line 377, in main
    process()
  File "/opt/spark/python/lib/pyspark.zip/pyspark/worker.py", line 372, in process
    serializer.dump_stream(func(split_index, iterator), outfile)
  File "/opt/spark/python/lib/pyspark.zip/pyspark/rdd.py", line 2499, in pipeline_func
  File "/opt/spark/python/lib/pyspark.zip/pyspark/rdd.py", line 2499, in pipeline_func
  File "/opt/spark/python/lib/pyspark.zip/pyspark/rdd.py", line 352, in func
  File "/opt/spark/python/lib/pyspark.zip/pyspark/rdd.py", line 1861, in combineLocally
  File "/opt/spark/python/lib/pyspark.zip/pyspark/shuffle.py", line 238, in mergeValues
    for k, v in iterator:
  File "/opt/spark/python/lib/pyspark.zip/pyspark/streaming/flume.py", line 123, in func
  File "/opt/spark/python/lib/pyspark.zip/pyspark/streaming/flume.py", line 38, in utf8_decoder
    return s.decode('utf-8')
  File "/usr/lib64/python2.7/encodings/utf_8.py", line 16, in decode
    return codecs.utf_8_decode(input, errors, True)
UnicodeDecodeError: 'utf8' codec can't decode byte 0xe4 in position 17: invalid continuation byte

	at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:452)
	at org.apache.spark.api.python.PythonRunner$$anon$1.read(PythonRunner.scala:588)
	at org.apache.spark.api.python.PythonRunner$$anon$1.read(PythonRunner.scala:571)
	at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:406)
	at org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)
	at scala.collection.Iterator$GroupedIterator.fill(Iterator.scala:1124)
	at scala.collection.Iterator$GroupedIterator.hasNext(Iterator.scala:1130)
	at scala.collection.Iterator$$anon$11.hasNext(Iterator.scala:409)
	at org.apache.spark.shuffle.sort.BypassMergeSortShuffleWriter.write(BypassMergeSortShuffleWriter.java:125)
	at org.apache.spark.scheduler.ShuffleMapTask.runTask(ShuffleMapTask.scala:99)
	at org.apache.spark.scheduler.ShuffleMapTask.runTask(ShuffleMapTask.scala:55)
	at org.apache.spark.scheduler.Task.run(Task.scala:121)
	at org.apache.spark.executor.Executor$TaskRunner$$anonfun$10.apply(Executor.scala:408)
	at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:1360)
	at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:414)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	... 1 more


	at org.apache.spark.streaming.api.python.TransformFunction.callPythonTransformFunction(PythonDStream.scala:95)
	at org.apache.spark.streaming.api.python.TransformFunction.apply(PythonDStream.scala:78)
	at org.apache.spark.streaming.api.python.PythonDStream$$anonfun$callForeachRDD$1.apply(PythonDStream.scala:179)
	at org.apache.spark.streaming.api.python.PythonDStream$$anonfun$callForeachRDD$1.apply(PythonDStream.scala:179)
	at org.apache.spark.streaming.dstream.ForEachDStream$$anonfun$1$$anonfun$apply$mcV$sp$1.apply$mcV$sp(ForEachDStream.scala:51)
	at org.apache.spark.streaming.dstream.ForEachDStream$$anonfun$1$$anonfun$apply$mcV$sp$1.apply(ForEachDStream.scala:51)
	at org.apache.spark.streaming.dstream.ForEachDStream$$anonfun$1$$anonfun$apply$mcV$sp$1.apply(ForEachDStream.scala:51)
	at org.apache.spark.streaming.dstream.DStream.createRDDWithLocalProperties(DStream.scala:416)
	at org.apache.spark.streaming.dstream.ForEachDStream$$anonfun$1.apply$mcV$sp(ForEachDStream.scala:50)
	at org.apache.spark.streaming.dstream.ForEachDStream$$anonfun$1.apply(ForEachDStream.scala:50)
	at org.apache.spark.streaming.dstream.ForEachDStream$$anonfun$1.apply(ForEachDStream.scala:50)
	at scala.util.Try$.apply(Try.scala:192)
	at org.apache.spark.streaming.scheduler.Job.run(Job.scala:39)
	at org.apache.spark.streaming.scheduler.JobScheduler$JobHandler$$anonfun$run$1.apply$mcV$sp(JobScheduler.scala:257)
	at org.apache.spark.streaming.scheduler.JobScheduler$JobHandler$$anonfun$run$1.apply(JobScheduler.scala:257)
	at org.apache.spark.streaming.scheduler.JobScheduler$JobHandler$$anonfun$run$1.apply(JobScheduler.scala:257)
	at scala.util.DynamicVariable.withValue(DynamicVariable.scala:58)
	at org.apache.spark.streaming.scheduler.JobScheduler$JobHandler.run(JobScheduler.scala:256)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)

