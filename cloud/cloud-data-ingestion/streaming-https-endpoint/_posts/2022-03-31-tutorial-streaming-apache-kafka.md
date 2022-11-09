---
title: Tutorial - streaming From Apache Kafka
---

 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes.

This tutorial will provide an example of one way you can ingest data from Apache Kafka to FeatureBase Cloud.

## Before you begin

{% include cloud/database-dependencies.md %}

## Installing the Kafka Client Library

For the purpose of this tutorial the official [Confluent Kafka library for Python](https://docs.confluent.io/kafka-clients/python/current/overview.html). It is a python library wrapped around their C-lanaguage library `librdkafka`.

While not required it's strongly recommended to run in a [virtual environment](https://docs.python.org/3/library/venv.html).

To install run:

```python
python3 -m pip install confluent-kafka
```

## Configuring account credentials and topics

Before we begin it’s always a good idea to make sure you have all the credentials and configuration parameters you need so that you aren’t searching halfway through and lose train of thought. For this tutorial we’ll need:

- Details about the Kafka cluster bootstrap server (which is also a Kafka Broker).

- Any credentials and permissions needed (if cluster secured) to read from the Kafka topic.

- FeatureBase Cloud credentials. If you don’t have an account yet then [sign up for a free trial](https://www.featurebase.com/cloud) (no credit card needed).

- The endpoint to an [existing Cloud ingest endpoint](/cloud/cloud-data-ingestion/streaming-https-endpoint/create-ingest-endpoint). In this tutorial you'll find the [schema](#creating-a-featurebase-source-schema) needed to create a new one and follow along, but a source will need to be configured and an endpoint available for configuration before testing with your data.

| SECURITY WARNING                                                                                                                                                                                                                                                                                                                      |
|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Note that for the sake of simplicity in this tutorial we’re hardcoding passwords and other secrets. Please don’t do this in any capacity other than as a personal learning exercise! It’s very easy to accidently commit to code repositories or leave in a public place and invites data breaches for yourself or your organization. |

```python
KAFKA_TOPICS = ['test']

KAFKA_BROKER = '<broker hostname>:9092'

# If security is enabled on your Kafka cluster then modify
# the following constants to reflect your configuration.
KAFKA_SASL_MECHANISM = 'PLAINTEXT'
KAFKA_SECURITY_PROTOCOL = 'PLAINTEXT'
KAFKA_SASL_USERNAME = None
KAFKA_SASL_PASSWORD = None

# FeatureBase Cloud username/password
FEATUREBASE_USERNAME = '{FeatureBase Username}'
FEATUREBASE_PASSWORD = '{FeatureBase Password}'

# FeatureBase Cloud > Data Sources > {Source} > "Ingest Endpoint"
FEATUREBASE_STREAMING_ENDPOINT = 'https://data.featurebase.com/v2/sinks/{Endpoint ID}'
```

#### Create a Fake Data Generator

There's a neat library to generate fake data in python called [Faker](https://pypi.org/project/Faker/).

In addition to the base Faker library let's also add a community addon that generates fake flights called [faker_airtravel](https://pypi.org/project/faker_airtravel/). It generates objects like the following Python objects (note the single quotes which denote a Python dict, not JSON). We'll also generate a unique flight identifier (`flight_id`) and insert it into each object as well.

```python
>>>fake.flight()

{'airline': 'Maya Island Air',
 'origin': {'Airport': 'Noi Bai Airport',
  'iata': 'HAN',
  'icao': 'VVNB',
  'City': 'Hanoi',
  'State': 'Ha Noi',
  'Country': 'Vietnam'},
 'destination': {'Airport': 'Geneva Airport',
  'iata': 'GVA',
  'icao': 'LSGG',
  'City': 'Geneva',
  'State': 'Canton of Geneva',
  'Country': 'Switzerland'},
 'stops': 'non-stop',
 'price': 641,
 'flight_id': 123}
```



To install let's run `pip install faker faker_airtravel` and add the following near the top of your python script:

```python
from faker import Faker
from faker_airtravel import AirTravelProvider

fake = Faker()
fake.add_provider(AirTravelProvider)
```

## Setting up the Kafka Client

For more documentation on the Confluent python client, please check out their official documentation at [Kafka Python Client - Confluent Documentation](https://docs.confluent.io/kafka-clients/python/current/overview.html).

### Create a Kafka Producer

Since we want to produce and consume data with this script we'll create a thread function to setup a Kafka producer and write 1 billion messages. We'll also append the fake data object by appending a unique ID column (`flight_id`).

```python
def producer_thread():
    fake = Faker()
    fake.add_provider(AirTravelProvider)

    producer = Producer({
      'bootstrap.servers': KAFKA_BROKER,
      'sasl.mechanism'   : KAFKA_SASL_MECHANISM,
      'security.protocol': KAFKA_SECURITY_PROTOCOL,
      'sasl.username'    : KAFKA_SASL_USERNAME,
      'sasl.password'    : KAFKA_SASL_PASSWORD,
    })

    #Can make this a higher range for more records
    for flight_id in range(100):
      flight  = fake.flight()
      flight['flight_id'] = flight_id + 1
      message = json.dumps(flight)
      producer.produce(KAFKA_TOPICS[0], message)
```

### Creating a Kafka consumer

First we’ll create a Kafka consumer and provide an error callback.

```python
from confluent_kafka import Consumer, KafkaError, KafkaException

def error_cb(err):
    """ The error callback is used for generic client errors. These
        errors are generally to be considered informational as the client will
        automatically try to recover from all errors, and no extra action
        is typically required by the application.
        For this example however, we terminate the application if the client
        is unable to connect to any broker (_ALL_BROKERS_DOWN) and on
        authentication errors (_AUTHENTICATION). """

    print("Client error: {}".format(err))
    if err.code() == KafkaError._ALL_BROKERS_DOWN or \
       err.code() == KafkaError._AUTHENTICATION:
        # Any exception raised from this callback will be re-raised from the
        # triggering flush() or poll() call.
        raise KafkaException(err)

# Create a Kafka consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'sasl.mechanism'   : KAFKA_SASL_MECHANISM,
    'security.protocol': KAFKA_SECURITY_PROTOCOL,
    'sasl.username'    : KAFKA_SASL_USERNAME,
    'sasl.password'    : KAFKA_SASL_PASSWORD,
    'group.id'         : str(uuid.uuid1()),
    'auto.offset.reset': 'earliest',
    'error_cb'         : error_cb,
})
```

### Subscribing Kafka consumer to a topic

We’ll then pass in a list of topics that we want to listen to. For this tutorial we only have a single topic however we still need to pass it as a list.

```python
consumer.subscribe(KAFKA_TOPICS)
```

### Start processing messages from topics

Once the Kafka consumer is configured and topics have been subscribed, we’ll start an event loop to poll for new messages. If there are no errors we’ll call `on_message()` which will simply print the contents of the message for now.

```python
  def on_message(content):
    print(content)

  try:
    while True:
        msg = consumer.poll(0.1)  # Wait for message or event/error
        if msg is None:
            # No message available within timeout.
            # Initial message consumption may take up to `session.timeout.ms`
            # for the group to rebalance and start consuming.
            continue
        if msg.error():
            # Errors are typically temporary, print error and continue.
            print('Consumer error: {}'.format(msg.error()))
            continue

        # No error, continue processing.
        content = msg.value()
        on_message(content)

  except KeyboardInterrupt:
      pass

  finally:
      # Leave group and commit final offsets
      consumer.close()
```

## Configure FeatureBase HTTP Client

### Authenticate and retrieve Identity Token

Using the `requests` library, we'll send an HTTP POST request with your username and password. If successful, the API will return a JSON object containing your credentials. For the purpose of further API calls, the property of interest is the `IdToken`.

```python
def featurebase_authenticate(username, password):
  """A helper function to retrieve an OAuth 2.0 token 'IdToken' which will be
     used to make authenticated HTTP API calls.
  """

  # Send HTTP POST request
  response = requests.post(
    url  = "https://id.featurebase.com",
    json = { 'USERNAME' : username, 'PASSWORD' : password })

  # Check for a HTTP 200 OK status code to confirm success.
  if response.status_code != 200:
    raise Exception(
      "Failed to authenticate. Response from authentication service:\n" +
      response.text)

  # On a successful authentication, you should retrieve the IdToken located in
  # the response at 'AuthenticationResult.IdToken'. This will be needed for any
  # further API calls.
  json  = response.json()

  token = json['AuthenticationResult']['IdToken']
  return token
```

### Modify Processing to Push Data

First we’re going to add a token argument to the existing `on_message()` function so we can perform authenticated HTTP requests.

```
def on_message(content, token):
  print(content)
```

Next we’ll process the message content and transform them to fit the schema required to push data to FeatureBase.

Remember that the schema for fake flights (when converted to JSON) looks like the following:

```json
{"airline": "Maya Island Air",
 "origin": {"Airport": "Noi Bai Airport",
  "iata": "HAN",
  "icao": "VVNB",
  "City": "Hanoi",
  "State": "Ha Noi",
  "Country": "Vietnam"},
 "destination": {"Airport": "Geneva Airport",
  "iata": "GVA",
  "icao": "LSGG",
  "City": "Geneva",
  "State": "Canton of Geneva",
  "Country": "Switzerland"},
 "stops": "non-stop",
 "price": 641,
 "flight_id": 1}
```

#### Create A Table

You must create a table before you can ingest data. For more information on tables, see [Tables](/cloud/cloud-data-ingestion/tables). The command below will create your table.

It is highly recommended to do table creation within the UI for easier mapping of column types, constraints, and options. Navigate to the "Tables" page and click “New Table", selecting your database, entering "flights" for the name, and entering "table holding flight data" as the description. The primary key for the flight table for this tutorial is a number, so choose Number as the ID type.

Once created, go to the "COLUMNS" tab in order to add or delete columns. You will see the _id column that was created during table creation. click "ADD COLUMN" and add the following columns, types, and constraints:

|Column Name | Type | Constraint |
| --- | ----------- |  ----------- |
| airline   |  string | N/A |
| stops   |  string | N/A |
| price   |  decimal | Scale:2 |
| origin_airport   |  string | N/A |
| origin_iata   |  string | N/A |
| origin_icao   |  string | N/A |
| origin_loc_city   |  string | N/A |
| origin_loc_state   |  string | N/A |
| origin_loc_country   |  string | N/A |
| destination_airport   |  string | N/A |
| destination_iata   |  string | N/A |
| destination_icao   |  string | N/A |
| destination_loc_city   |  string | N/A |
| destination_loc_state   |  string | N/A |
| destination_loc_country   |  string | N/A |

#### Creating a FeatureBase Ingest Schema

When creating an ingest endpoint in FeatureBase, we need to provide a JSON schema to make incoming records to table columns. For the fake flight dataset you can use the following in the UI

```json
[
  {
    "name": "airline",
    "path": ["airline"]
  },
  {
    "name": "stops",
    "path": ["stops"]
  },
  {
    "name": "price",
    "path": ["price"]
  },
  {
    "name": "origin_airport",
    "path": ["origin","airport"]
  },
  {
    "name": "origin_iata",
    "path": ["origin","iata"]
  },
  {
    "name": "origin_icao",
    "path": ["origin","icao"]
  },
  {
    "name": "origin_loc_city",
    "path": ["origin","city"]
  },
  {
    "name": "origin_loc_state",
    "path": ["origin","state"]
  },
  {
    "name": "origin_loc_country",
    "path": ["origin","country"]
  },

  {
    "name": "destination_airport",
    "path": ["destination","airport"],
    "type": "string"
  },
  {
    "name": "destination_iata",
    "path": ["destination","iata"],
    "type": "string"
  },
  {
    "name": "destination_icao",
    "path": ["destination","icao"]
  },
  {
    "name": "destination_loc_city",
    "path": ["destination","city"]
  },
  {
    "name": "destination_loc_state",
    "path": ["destination","state"]
  },
  {
    "name": "destination_loc_country",
    "path": ["destination","country"]
  },
  {
    "name": "_id",
    "path": ["flight_id"]
  }
]
```

#### Writing to FeatureBase

After modifying the `on_message()` function to better reflect the schema we get the following:

```python
def on_message(message, token):
  """Callback function which takes content pull from a subscribed Kafka queue,
     transforms it to the schema required by FeatureBase Cloud, and writes
     directly to the sink to make it immediately available for querying.
  """
  records = map(lambda record : { 'value' : json.loads(record) }, [message])
  payload = { 'records' : list(records) }
  payload = json.dumps(payload)

  #
  # Send request to push data into FeatureBase Cloud
  #
  # See: https://docs.featurebase.com/cloud/cloud-data-ingestion/streaming-https-endpoint/stream-ingest-endpoint
  #
  response = requests.post(
    url     = FEATUREBASE_STREAMING_ENDPOINT,
    data    = payload,
    headers = {
      # Need to pass the OAuth 2.0 IdToken we retrieved after authenticating
      # with https://id.featurebase.com.
      'Authorization' : f'Bearer {token}',
      # The FeatureBase Cloud REST API requires the request body to be JSON.
      'Content-Type'  : 'application/json'
    })


  if response.status_code != 200:
    print(response.text)

  # Throw error if an error occurred
  response.raise_for_status()
```

## Running the producer and consumer threads

Tying together all the pieces here you can see how we can launch the infinite message producer and consumer threads after we authenticate to FeatureBase.

```python
if __name__ == "__main__":
  # Login to FeatureBase Cloud and get identity token.
  token = featurebase_authenticate(FEATUREBASE_USERNAME, FEATUREBASE_PASSWORD)
  print(f'OAuth 2.0 Token:\n{token}\n---')
  produce_thread = Thread(target=producer_thread, args=())
  consume_thread = Thread(target=consumer_thread, args=(token,))
  produce_thread.start()
  consume_thread.start()
  consume_thread.join()
```

## Full Code Sample

Most of this code should look familiar if following the walthrough above, but some liberty was taken to improve performance by micro batching records together when writing to FeatureBase.

```python
# Copyright 2022 Molecula Corp. (DBA FeatureBase)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from threading import Thread
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException

# Using faker along with the addon Airtravel provider.
from faker import Faker
from faker_airtravel import AirTravelProvider

import uuid
import json
import time
import requests



###########################################################

KAFKA_TOPICS = ['test']

# If security is enabled on your Kafka cluster then modify
# the following constants to reflect your configuration.
KAFKA_BROKER = '{Broker Hostname}:9092'

KAFKA_SASL_MECHANISM = 'PLAINTEXT'
KAFKA_SECURITY_PROTOCOL = 'PLAINTEXT'
KAFKA_SASL_USERNAME = None
KAFKA_SASL_PASSWORD = None

# FeatureBase Cloud username/password
FEATUREBASE_USERNAME = '{Username}'
FEATUREBASE_PASSWORD = '{Password}'

# FeatureBase Cloud > Data Sources > {Source} > "Ingest Endpoint"
FEATUREBASE_STREAMING_ENDPOINT = 'https://data.featurebase.com/v2/sinks/{Endpoint ID}'

###########################################################



def featurebase_authenticate(username, password):
  """A helper function to retrieve an OAuth 2.0 token 'IdToken' which will be
     used to make authenticated HTTP API calls.
  """

  # Send HTTP POST request
  response = requests.post(
    url  = "https://id.featurebase.com",
    json = { 'USERNAME' : username, 'PASSWORD' : password })

  # Check for a HTTP 200 OK status code to confirm success.
  if response.status_code != 200:
    raise Exception(
      "Failed to authenticate. Response from authentication service:\n" +
      response.text)

  # On a successful authentication, you should retrieve the IdToken located in
  # the response at 'AuthenticationResult.IdToken'. This will be needed for any
  # further API calls.
  json  = response.json()

  token = json['AuthenticationResult']['IdToken']
  return token



def on_message(batch, token):
  """Callback function which takes content pull from a subscribed Kafka queue,
     transforms it to the schema required by FeatureBase Cloud, and writes
     directly to the sink to make it immediately available for querying.
  """

  count = len(batch)
  print(f'  Sending {count} records to FeatureBase.')
  records = map(lambda record : { 'value' : json.loads(record) }, batch)
  payload = { 'records' : list(records) }
  payload = json.dumps(payload)

  #
  # Send request to push data into FeatureBase Cloud
  #
  # See: https://docs.featurebase.com/cloud/cloud-data-ingestion/streaming-https-endpoint/stream-ingest-endpoint
  #
  response = requests.post(
    url     = FEATUREBASE_STREAMING_ENDPOINT,
    data    = payload,
    headers = {
      # Need to pass the OAuth 2.0 IdToken we retrieved after authenticating
      # with https://id.featurebase.com.
      'Authorization' : f'Bearer {token}',
      # The FeatureBase Cloud REST API requires the request body to be JSON.
      'Content-Type'  : 'application/json'
    })


  if response.status_code != 200:
    print(response.text)

  # Throw error if an error occurred
  response.raise_for_status()



def error_cb(err):
    """ The error callback is used for generic client errors. These
        errors are generally to be considered informational as the client will
        automatically try to recover from all errors, and no extra action
        is typically required by the application.
        For this example however, we terminate the application if the client
        is unable to connect to any broker (_ALL_BROKERS_DOWN) and on
        authentication errors (_AUTHENTICATION). """

    print("Client error: {}".format(err))
    if err.code() == KafkaError._ALL_BROKERS_DOWN or \
       err.code() == KafkaError._AUTHENTICATION:
        # Any exception raised from this callback will be re-raised from the
        # triggering flush() or poll() call.
        raise KafkaException(err)





def producer_thread():
    """Generates 100 (but change range to scale this up) fake airline flights using Faker and an addon provider
       called Airtravel. These fake flights are pushed into the Kafka topic.
    """
    print('Starting to produce messages.')
    fake = Faker()
    fake.add_provider(AirTravelProvider)

    producer = Producer({
      'bootstrap.servers': KAFKA_BROKER,
      'sasl.mechanism'   : KAFKA_SASL_MECHANISM,
      'security.protocol': KAFKA_SECURITY_PROTOCOL,
      'sasl.username'    : KAFKA_SASL_USERNAME,
      'sasl.password'    : KAFKA_SASL_PASSWORD,
    })

    #make this a higher number to see more records flow in
    for flight_id in range(100):
      #
      # >>>fake.flight()
      #
      # {'airline': 'Maya Island Air',
      # 'origin': {'airport': 'Noi Bai Airport',
      #   'iata': 'HAN',
      #   'icao': 'VVNB',
      #   'city': 'Hanoi',
      #   'state': 'Ha Noi',
      #   'country': 'Vietnam'},
      # 'destination': {'airport': 'Geneva Airport',
      #   'iata': 'GVA',
      #   'icao': 'LSGG',
      #   'city': 'Geneva',
      #   'state': 'Canton of Geneva',
      #   'country': 'Switzerland'},
      # 'stops': 'non-stop',
      #  "price": 641,
      #  "flight_id": 1}
      #
      flight  = fake.flight()

      # Add 'flight_id' property to object
      flight['flight_id'] = flight_id + 1

      message = json.dumps(flight)
      producer.produce(KAFKA_TOPICS[0], message)

    # Ensure all messages are written to topic
    producer.flush()





def consumer_thread(token):
  """Infinite event loop to listen for and process messages from
      subscribed Kafka topics.
  """
  # Create a confluent consumer. Note this resets the offset to earliest each time the script is run
  consumer = Consumer({
      'bootstrap.servers': KAFKA_BROKER,
      'sasl.mechanism'   : KAFKA_SASL_MECHANISM,
      'security.protocol': KAFKA_SECURITY_PROTOCOL,
      'sasl.username'    : KAFKA_SASL_USERNAME,
      'sasl.password'    : KAFKA_SASL_PASSWORD,
      'group.id'         : str(uuid.uuid1()),
      'auto.offset.reset': 'earliest',
      'error_cb'         : error_cb,
  })

  # Subscribe to Kafka topics
  consumer.subscribe(KAFKA_TOPICS)

  # Create batch buffer
  batch = []
  prior = time.time()

  # Start processing messages from topic(s)
  try:
    print('starting consumer loop')
    while True:
        now = time.time()
        msg = consumer.poll(0.1)  # Wait for message or event/error
        BATCH_SIZE_LIMIT = 500
        batch_size = len(batch)
        if (now - prior > 1 or batch_size > BATCH_SIZE_LIMIT) and batch_size > 0:
          # Flush records batch to FeatureBase sink every 1 sec or if the number
          # of records in batch is greater than 100.
          on_message(batch[:BATCH_SIZE_LIMIT], token)
          batch = batch[BATCH_SIZE_LIMIT:]
          prior = now
          continue
        if msg is None:
            # No message available within timeout.
            # Initial message consumption may take up to `session.timeout.ms`
            # for the group to rebalance and start consuming.
            continue
        if msg.error():
            # Errors are typically temporary, print error and continue.
            print('Consumer error: {}'.format(msg.error()))
            continue

        # No error, add to next batch.
        content = msg.value()
        batch.append(content)
        print(content)

  except KeyboardInterrupt:
      pass

  finally:
      # Leave group and commit final offsets
      consumer.close()



if __name__ == "__main__":
  # Login to FeatureBase Cloud and get identity token. Then produce and consume messages until interupted.
  token = featurebase_authenticate(FEATUREBASE_USERNAME, FEATUREBASE_PASSWORD)
  produce_thread = Thread(target=producer_thread, args=())
  consume_thread = Thread(target=consumer_thread, args=(token,))
  produce_thread.start()
  consume_thread.start()
  consume_thread.join()
```
