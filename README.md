# Multi-protocol Chat Program

This lightweight chat application demonstrates how you can exchange messages over three different transport layers:

1. MQTT (via the public `test.mosquitto.org` broker, or your own)
2. DDS  (Eclipse CycloneDDS)
3. Raw TCP (with a minimal relay server)

All transports share a single, unified, interactive command-line client.

## Installation

```bash
# Clone / copy the repository then:
cd /workspace   # or wherever your project root is
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

cyclonedds can be tricky to compile on some platforms.  If you only care
about MQTT or TCP you can skip it:

```bash
pip install paho-mqtt
```

## Running

### 1. TCP mode (default)

Open **one** terminal and start the relay server:

```bash
python -m chatapp.tcp_server --host 0.0.0.0 --port 9009
```

Then open **two or more** other terminals and run the client:

```bash
python -m chatapp.main --protocol tcp --username alice
python -m chatapp.main --protocol tcp --username bob
```

### 2. MQTT mode

```bash
python -m chatapp.main --protocol mqtt --username alice \
       --host test.mosquitto.org --mqtt_port 1883 --channel myroom
```

Every instance connected to the same *channel* will see the messages.

### 3. DDS mode (CycloneDDS)

```bash
python -m chatapp.main --protocol dds --username alice --channel ChatRoom
```

> NOTE: Make sure `cyclonedds` Python bindings are installed and you have
> the necessary DDS networking permissions.

## How it works

* The `chatapp.protocols` package contains a small abstraction layer.
* Each concrete protocol class (TCP, MQTT, DDS) implements `connect`,
  `send`, and `close` as asynchronous coroutines.
* `chatapp.client.ChatClient` selects the appropriate backend at runtime
  and provides a concise public API.

Feel free to extend the project: add WebSockets, ZeroMQ, etc. 🚀