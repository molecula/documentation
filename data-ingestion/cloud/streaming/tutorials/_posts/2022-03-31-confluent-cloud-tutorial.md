---

title: Streaming from Confluent Cloud

---

 **⚠ WARNING:** This page contains information that only applies to FeatureBase Cloud. Additionally, this page represents a work in progress that is subject to frequent changes. 

For the purpose of this walkthrough it is assumed that a Kafka cluster is deployed and an existing Kafka topic is already being written to.

This tutorial will break down into steps how to pull from Kafka and write to FeatureBase, but if you'd rather look at the finished tutorial then please see the full source code at the bottom of this article.





## Configuring account credentials and topics

Before we begin it's always a good idea to make sure you have all the credentials and configuration parameters you need so that you aren't searching halfway through and lose train of thought. For this tutorial we'll need:

* Details about the Kafka cluster bootstrap server (which is also a Kafka Broker).

* An API key and secret with permission to read from the Kafka topic.

* FeatureBase Cloud credentials. If you don't have an account yet then [sign up for a free trial](https://www.molecula.com/start-free-trial/) (no credit card needed).

* An existing Cloud ingest endpoint.



| **SECURITY WARNING**                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Note that for the sake of simplicity in this tutorial we're hardcoding passwords and other secrets. Please don't do this in any capacity other than as a personal learning exercise! It's very easy to accidently commit to code repositories or leave in a public place and invites data breaches for yourself or your organization. |

```python
CONFLUENT_TOPICS = ['pageviews']

# Go to:the Cluster overview in https://confluent.cloud and then:
# "Cluster settings" and copy "Bootstrap server"
CONFLUENT_BOOSTRAP_SERVER = '<SOME BOOTSTRAP SERVER>:9092'

# Go to:the cluster overview in https://confluent.cloud and then:
# "CLI and tools" > "Kafka Connect" > "Create Kafka cluster API key & secret"
CONFLUENT_KEY    = ''
CONFLUENT_SECRET = ''

# FeatureBase Cloud username/password
FEATUREBASE_USERNAME = ''
FEATUREBASE_PASSWORD = ''

# FeatureBase Cloud > Data Sources > {Source} > "Ingest Endpoint"
FEATUREBASE_STREAMING_ENDPOINT = ''
```







## Setting up Confluent Kafka Client

For more documentation on the Confluent python client, please check out their official documentation at [Kafka Python Client &#124; Confluent Documentation](https://docs.confluent.io/kafka-clients/python/current/overview.html). 

For convienence, the following sample was modified from one of Confluent's examples. The original source can be found here: [confluent-kafka-python/confluent_cloud.py](https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/confluent_cloud.py)

### Creating a Kafka consumer

First we'll create a Kafka consumer and provide an error callback.

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

  # Create a confluent consumer 
  consumer = Consumer({
      'bootstrap.servers': CONFLUENT_BOOSTRAP_SERVER,
      'sasl.mechanism'   : 'PLAIN',
      'security.protocol': 'SASL_SSL',
      'sasl.username'    : CONFLUENT_KEY,
      'sasl.password'    : CONFLUENT_SECRET,
      'group.id'         : str(uuid.uuid1()),
      'auto.offset.reset': 'earliest',
      'error_cb'         : error_cb,
  })
```

### Subscribing Kafka consumer to a topic

We'll then pass in a list of topics that we want to listen to. For this tutorial we only have a single topic however we still need to pass it as a list.

```python
consumer.subscribe(CONFLUENT_TOPICS)
```

### Start processing messages from topics

Once the Kafka consumer is configured and topics have been subscribed, we'll start an event loop to poll for new messages. If there are no errors we'll call `on_message()` which will simply print the contents of the message for now.

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
    url  = "https://id.molecula.cloud", 
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

First we're going to add a token argument to the existing `on_message()` function so we can perform authenticated HTTP requests.

```python
def on_message(content, token):
  print(content)
```

Next we'll process the message content and transform them to fit the schema required to push data to FeatureBase.



In writing this tutorial, the Confluent provided Kafka Connect datagen connector was used along with the "pageviews" generator. Messages from this generator look like the following:

```json
{"viewtime":6671,"userid":"User_2","pageid":"Page_64"}
```



The first thing that is done is to parse the message. Since this is a JSON message we'll use the built in `json` library.

```python
import json

# ...

def on_message(content, token):

  # Parse and convert JSON object to python dict
  content = json.loads(content)

```



Then we'll transform it to match the FeatureBase Cloud schema syntax which can be seen in more details in [here](/data-ingestion/cloud/streaming/streamingoverview).



```python

def on_message(content, token):

  # ...

  # Since only a single record is passed per Kafka message, we can just create
  # an array of a single object with the content as the value of the 'value'
  # property.
  payload = { 'records' : [ { 'value' : content } ] }
  payload = json.dumps(payload)
  print('Payload: ')
  print(payload)

```

Finally using the `requests` library, send an HTTP POST request making sure to define the content-type as JSON and passing an identity token. If an error occurs we'll throw an exception, however you may want to process errors differently.

```python
def on_message(content, token):

  # ...

  response = requests.post(
    url     = FEATUREBASE_STREAMING_ENDPOINT, 
    data    = payload,
    headers = { 
      'Authorization' : f'Bearer {token}', 
      'Content-Type'  : 'application/json'
    })

  if response.status_code != 200:
    print(response.text)

  # Throw error if an error occurred
  response.raise_for_status()
```



## Full Code Sample

```python
# Copyright 2022 Molecula Corp.
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

from confluent_kafka import Consumer, KafkaError, KafkaException
import uuid
import json
import requests

###########################################################

CONFLUENT_TOPICS = ['pageviews']

# Go to:the Cluster overview in https://confluent.cloud and then:
# "Cluster settings" and copy "Bootstrap server"
CONFLUENT_BOOSTRAP_SERVER = '<SOME BOOTSTRAP SERVER>:9092'

# Go to:the cluster overview in https://confluent.cloud and then:
# "CLI and tools" > "Kafka Connect" > "Create Kafka cluster API key & secret"
CONFLUENT_KEY    = ''
CONFLUENT_SECRET = ''

# FeatureBase Cloud username/password
FEATUREBASE_USERNAME = ''
FEATUREBASE_PASSWORD = ''

# FeatureBase Cloud > Data Sources > {Source} > "Ingest Endpoint"
FEATUREBASE_STREAMING_ENDPOINT = ''

###########################################################


def featurebase_authenticate(username, password):
  """A helper function to retrieve an OAuth 2.0 token 'IdToken' which will be
     used to make authenticated HTTP API calls.
  """

  # Send HTTP POST request
  response = requests.post(
    url  = "https://id.molecula.cloud", 
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


def on_message(content, token):
  """Callback function which takes content pull from a subscribed Kafka queue, 
     transforms it to the schema required by FeatureBase Cloud, and writes 
     directly to the sink to make it immediately available for querying.
  """
  #
  # Using the pageview datagen connector provided by Confluent Cloud which 
  # creates messages that look like this:
  #
  # {"viewtime":6671,"userid":"User_2","pageid":"Page_64"}
  # {"viewtime":6681,"userid":"User_7","pageid":"Page_73"}
  # {"viewtime":6691,"userid":"User_2","pageid":"Page_73"}
  # {"viewtime":6701,"userid":"User_3","pageid":"Page_89"}
  # ...
  #
  # Your data will likely be very different and needs to be parsed accordingly!
  #

  # Parse and convert JSON object to python dict
  content = json.loads(content)
  
  #
  # Convert to FeatureBase Cloud format.
  #
  # For more details read our documentation on this topics at: 
  # https://docs.molecula.cloud/data-ingestion/cloud/streaming/streamingoverview
  #
  # {
  #   "records": [
  #     { "value": { <JSON blob containing columns of first record> } },
  #     { "value": { <JSON blob containing columns of second record> } },
  #     ...
  #   ]
  # }

  # Since only a single record is passed per Kafka message, we can just create
  # an array of a single object with the content as the value of the 'value'
  # property.
  payload = { 'records' : [ { 'value' : content } ] }
  payload = json.dumps(payload)
  print('Payload: ')
  print(payload)

  #
  # Send request to push data into FeatureBase Cloud
  #
  # See: https://docs.molecula.cloud/data-ingestion/cloud/streaming/ingeststreamingsource
  #
  response = requests.post(
    url     = FEATUREBASE_STREAMING_ENDPOINT, 
    data    = payload,
    headers = { 
      # Need to pass the OAuth 2.0 IdToken we retrieved after authenticating 
      # with https://id.molecula.cloud.
      'Authorization' : f'Bearer {token}', # 
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


if __name__ == "__main__":
  # Login to FeatureBase Cloud and get identity token.
  token = featurebase_authenticate(FEATUREBASE_USERNAME, FEATUREBASE_PASSWORD)

  # Create a confluent consumer 
  consumer = Consumer({
      'bootstrap.servers': CONFLUENT_BOOSTRAP_SERVER,
      'sasl.mechanism'   : 'PLAIN',
      'security.protocol': 'SASL_SSL',
      'sasl.username'    : CONFLUENT_KEY,
      'sasl.password'    : CONFLUENT_SECRET,
      'group.id'         : str(uuid.uuid1()),
      'auto.offset.reset': 'earliest',
      'error_cb'         : error_cb,
  })

  # Subscribe to Kafka topics
  consumer.subscribe(CONFLUENT_TOPICS)

  # Start processing messages from topic(s)
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
        on_message(content, token)

  except KeyboardInterrupt:
      pass

  finally:
      # Leave group and commit final offsets
      consumer.close()
```
