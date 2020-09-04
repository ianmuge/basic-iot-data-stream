Based on the work of: https://github.com/Dineshkarthik/real-time-IoT-data-streaming

Flow:
- Stream from mobile app to tcp socket ran on fastapi.
- Emit data to kafka topic
- Topic read by logstash and 
- Forwarded into elasticsearch
- Visualized in Kibana