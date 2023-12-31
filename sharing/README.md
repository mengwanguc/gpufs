### Emulate time-slice sharing using Kafka


```
sudo apt update
sudo apt install default-jdk
java -version
```

Add this to the end of .bashr_rc

```
export JAVA_HOME=$(/usr/libexec/java_home)
export PATH=$JAVA_HOME/bin:$PATH
```

reload terminal





```
wget https://dlcdn.apache.org/kafka/3.6.1/kafka_2.13-3.6.1.tgz
tar -xzf kafka_2.13-3.6.1.tgz
cd kafka_2.13-3.6.1
bin/zookeeper-server-start.sh config/zookeeper.properties
```

another terminal

```
bin/kafka-server-start.sh config/server.properties
```

```
pip install kafka-python
```


```
bash bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic batch_requests
```