# streaming-app
Streaming app demo



## Overview

┌───────────────────┐┌──────────────────┐
│                   ││                  │
│   Mock Service    ││    Processor     │
│                   ││                  │
└───────────────────┘└──────────────────┘
┌───────────┐ ┌───────────┐ ┌───────────┐
│           │ │           │ │           │
│  Kafka    │ │  Flink    │ │ Cassandra │
│           │ │           │ │           │
└───────────┘ └───────────┘ └───────────┘

## Features and notes
- Real-time data processing
- Scalable architecture
- Fault-tolerant design
- Integration with Kafka for messaging
- Use of Flink for stream processing
- Cassandra for data storage
- Mock service for testing and development
- Detailed documentation and examples
- KRaft is used, so no need for Zookeeper