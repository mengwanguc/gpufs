### Emulate time-slice sharing using Kafka


```
sudo apt update
sudo apt install -y default-jdk
```

confirm it's installed
```
java --version
```


Add this to the end of .bashrc

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



```
python main-emulator.py  --epoch 1 --profile-batches -1 --workers 8 --gpu-type=p100 --gpu-count=1 --arch=resnet50 --emulator-version=1 ~/data/imagenette2
```