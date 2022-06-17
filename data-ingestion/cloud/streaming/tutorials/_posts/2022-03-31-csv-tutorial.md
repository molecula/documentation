---

title: Streaming in a CSV

---


This tutorial will break down into steps how to load a CSV file into FeatureBase using a streaming source, but if you'd rather look at the finished tutorial, please see the full source code at the bottom of this article.


## Configuring account credentials and files

Before we begin, it's always a good idea to make sure you have all the credentials and configuration parameters you need so that you aren't searching halfway through and lose train of thought. For this tutorial we'll need:

* A CSV file to use, as well as the field names in that CSV file

* A working python3 environment to run this code and install required packages

* FeatureBase Cloud credentials 

* The endpoint to an existing Cloud streaming source



| **SECURITY WARNING**                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Note that for the sake of simplicity, in this tutorial, we're hardcoding passwords and other secrets. Please don't do this in any capacity other than as a personal learning exercise! It's very easy to accidentally commit to code repositories or leave in a public place which invites data breaches for yourself or your organization. |


Below represents all of the inputs you must enter to use these code snippets. This offers limited flexibility but does allow you to specify a delimiter, if not a **","** and if your CSV has a header as the first line or not. You will have to put all of the field (column) names in the order they appear in your CSV file and ensure they match the `path` names in your streaming source. For more information on streaming sources, go [here](/data-ingestion/cloud/streaming/streamingoverview).

```python
import csv
import json
import requests
import time

# Full Path of the CSV file
CSV_FILE_PATH = '' # /path/to/file.csv
DELIMETER = ',' #Change to your file's delimeter
HEADER = True #Change if your csv has no header file as the first line
# Full Path of the json file(s) to write to and stream in
JSON_FILE_PATH = '' # /path/to/file.json
# list of the ordered target field names to write to that correlate to each column in your csv file
# e.g. ["id","sepallength","sepalwidth","petallength","petalwidth","species"]
FIELD_NAMES = []

# Leave these blank if don't want to send your records to your streaming source
# FeatureBase Cloud username/password
FEATUREBASE_USERNAME = ''
FEATUREBASE_PASSWORD = ''
# FeatureBase Cloud > Data Sources > {Source} > "Streaming Endpoint" e.g. "https://data.molecula.cloud/v1/sinks/...
FEATUREBASE_STREAMING_ENDPOINT = ''
```

## Convert CSV to JSON Format

The first step is to transform every row in the CSV file into the FeatureBase Cloud schema syntax, which can be seen in further detail at [here](/data-ingestion/cloud/streaming/streamingoverview). The output of this function will create 1 to many properly formatted JSON files for every 1000 records in your CSV file. 

```python
def make_json(csvFilePath, jsonFilePath, fieldnames, delim=',', header=True):
    """ Function to convert a CSV to batches of json files

    Args:
        csvFilePath (path): Path of the target csv to convert to json
        jsonFilePath (path): Path of the target json file to write to
            Note batch sizes will append to this file name
        fieldnames (list): List of the ordered target field names to write to
        delim (str, optional): Delimeter of the csv file Defaults to ','
        header boolean: Indicator if the csv has a header as the first line

    Returns:
        list: A list of all of the json files written to disk
    """

    #Create empty list to track files created
    file_list = []

    print("Opening Molecula JSON Data File "+jsonFilePath)
    f = open(jsonFilePath, 'w', encoding='utf-8') 
    file_list.append(jsonFilePath)

    # Add the pre JSON content ...
    f.write('{ "records": [\n')

    # Open a csv reader called DictReader and pass fieldnames in as the dictionary keys
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf, delimiter=delim, fieldnames=fieldnames)
         
        #
        # Convert each row into a dictionary and add it to data object
        #
        i = 0 # Used to keep track of place in csv file
        j = -2 # Used to keep track of record count
        jlimit = 1000 # Limit of json records per file
        data = {}
        rdelim = ""

        for rows in csvReader:
            if header:
                i = i + 1
            else:
                i = i + 2
            j = j + 1
            if (i > 1):
                # If you hit the json limit, close the file, and the file name to the file list, and start a new file with the start record count
                if (j == jlimit):
                    j = 0
                    f.write('] }')
                    f.close()
                    file_list.append(jsonFilePath+"_"+str(i-2))
                    f = open(jsonFilePath+"_"+str(i-2), 'w', encoding='utf-8')
                    f.write('{ "records": [\n')
                    rdelim = ""

                # #
                # # If any value needs processing/conversion, add logic here
                # #
                row = {}
                delim = ""
                for field in fieldnames:
                    if len(rows[field]) != 0:
                        row[field] = rows[field]
                    delim = ","


                # End for field in fieldnames
                print(row)
                f.write(rdelim+'{ "value": '+json.dumps(row)+'}\n')
                rdelim = ","

    # Close last file
    f.write('] }')
    f.close()

    # Print out and return the full list of files created
    print(f'The following JSON files were created: {file_list}')
    return file_list
  
```


## Configure FeatureBase HTTP Client

If you enter your username, password, and streaming endpoint, the below code snippets can be used stream the JSON records from the files created to your table in FeatureBase.

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

### Stream in records from the created JSON File

Finally, using the `requests` library, pass in a JSON file to an HTTP POST request making sure to define the content-type as JSON and passing an identity token. If any records fail to process, we will print out the posted records and exit. However, you may want to process errors differently.

```python
def post_records(token, json_file,datahost):
    """ Load in a json file with 1:n records and post them to FeatureBase Cloud via a streaming endpoint (sink)

    Args:
        token string: IDtoken for auth
        json_file (string): 1 to n json records in a file
        datahost (string): Saas streaming endpoint e.g. "https://data.molecula.cloud/v1/sinks/..."

    Returns:
        int: Count of successful records if no errors
    """
    # Read in data
    f = open(json_file)
    data = f.read()
    f.close()

    #Format http requst
    body = data
    headers = {"Content-Type": "tapplication/json",
        "Authorization": f'Bearer {token}'}
    print('Posting Records')

    #Send records
    post = requests.post(datahost, headers=headers,data=body).json()

    #If errors exist, send the body of records, otherwise return the success counts
    if post['error_count'] > 0:
        print(f'There were {post["error_count"]} failed records. System Exiting')
        print(post)
        exit()
    else:
        return post['success_count']
```


## Putting it all together
The below snippet calls all the functions discussed above to convert your CSV file into JSON. Optionally, it sends them to your streaming source if you enter your credentials and endpoint. This will send all of the JSON files created in the first step. 

```python
def main():
    # 
    # Convert CSV to JSON and optionally post records if you have a streaming endpoint
    #
    print("Converting CSV Data "+CSV_FILE_PATH+" to Molecula JSON Data "+JSON_FILE_PATH)
    files = make_json(CSV_FILE_PATH, JSON_FILE_PATH, FIELD_NAMES, DELIMETER, HEADER)
    if FEATUREBASE_USERNAME != '' and FEATUREBASE_PASSWORD != '' and FEATUREBASE_STREAMING_ENDPOINT != '':
        token = featurebase_authenticate(FEATUREBASE_USERNAME,FEATUREBASE_PASSWORD)
        for file in files:
            success = post_records(token,file, FEATUREBASE_STREAMING_ENDPOINT)
            print(f'{success} records ingested')
            time.sleep(1.5) #Allow for time to process records

    print("All done!")

if __name__ == "__main__":
    main()
```

## Full Code Sample
Save the code snippet below to a file name of your choice, fill in all variables under "ENTER ALL VARIABLES HERE", and execute the ```python3 <your name>.py``` command.

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

# Requirements:
# Python 3.6
# This script cannot run longer than 60 minutes as the token will expire
#
# Usage:
#
# python3 <your name>.py
import csv
import json
import requests
import time

# Full Path of the csv file
CSV_FILE_PATH = '' # /path/to/file.csv
DELIMETER = ',' #Change to your file's delimeter
HEADER = True #Change if your csv has no header file as the first line
# Full Path of the json file(s) to write to and stream in
JSON_FILE_PATH = '' # /path/to/file.json
# list of the ordered target field names to write to that correlate to each column in your csv file
# e.g. ["id","sepallength","sepalwidth","petallength","petalwidth","species"]
FIELD_NAMES = []

# Leave these blank if don't want to send your records to your streaming source
# FeatureBase Cloud username/password
FEATUREBASE_USERNAME = ''
FEATUREBASE_PASSWORD = ''
# FeatureBase Cloud > Data Sources > {Source} > "Streaming Endpoint" e.g. "https://data.molecula.cloud/v1/sinks/...
FEATUREBASE_STREAMING_ENDPOINT = ''

def make_json(csvFilePath, jsonFilePath, fieldnames, delim=',', header=True):
    """ Function to convert a CSV to batches of json files

    Args:
        csvFilePath (path): Path of the target csv to convert to json
        jsonFilePath (path): Path of the target json file to write to. 
            Note batch sizes will append to this file name
        fieldnames (list): List of the ordered target field names to write to
        delim (str, optional): Delimiter of the csv file Defaults to ','.
        header boolean: Indicator if the csv has a header as the first line

    Returns:
        list: A list of all of the json files written to disk
    """

    #Create empty list to track files created
    file_list = []

    print("Opening Molecula JSON Data File "+jsonFilePath)
    f = open(jsonFilePath, 'w', encoding='utf-8') 
    file_list.append(jsonFilePath)

    # Add the pre JSON content ...
    f.write('{ "records": [\n')

    # Open a csv reader called DictReader and pass fieldnames in as the dictionary keys
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf, delimiter=delim, fieldnames=fieldnames)
         
        #
        # Convert each row into a dictionary and add it to data object
        #
        i = 0 # Used to keep track of place in csv file
        j = -2 # Used to keep track of record count
        jlimit = 1000 # Limit of json records per file
        data = {}
        rdelim = ""

        for rows in csvReader:
            if header:
                i = i + 1
            else:
                i = i + 2
            j = j + 1
            if (i > 1):
                # If you hit the json limit, close the file, and the file name to the file list, and start a new file with the start record count
                if (j == jlimit):
                    j = 0
                    f.write('] }')
                    f.close()
                    file_list.append(jsonFilePath+"_"+str(i-2))
                    f = open(jsonFilePath+"_"+str(i-2), 'w', encoding='utf-8')
                    f.write('{ "records": [\n')
                    rdelim = ""

                # #
                # # If any value needs processing/conversion, add logic here
                # #
                row = {}
                delim = ""
                for field in fieldnames:
                    if len(rows[field]) != 0:
                        row[field] = rows[field]
                    delim = ","


                # End for field in fieldnames
                print(row)
                f.write(rdelim+'{ "value": '+json.dumps(row)+'}\n')
                rdelim = ","

    # Close last file
    f.write('] }')
    f.close()

    # Print out and return the full list of files created
    print(f'The following JSON files were created: {file_list}')
    return file_list


def featurebase_authenticate(username, password):
    """A helper function to retrieve an OAuth 2.0 token 'IdToken' which will be
     used to make authenticated HTTP API calls.

    Args:
        username (string): Cloud Username
        password (string): Cloud Password

    Raises:
        Exception: Fail if credential are incorrect

    Returns:
        string: IDToken for authentication
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


def post_records(token, json_file,datahost):
    """ Load in a json file with 1:n records and post them to FeatureBase Cloud via a streaming endpoint (sink)

    Args:
        token string: IDtoken for auth
        json_file (string): 1 to n json records in a file
        datahost (string): Saas streaming endpoint e.g. "https://data.molecula.cloud/v1/sinks/..."

    Returns:
        int: Count of successful records if no errors
    """
    # Read in data
    f = open(json_file)
    data = f.read()
    f.close()

    #Format http requst
    body = data
    headers = {"Content-Type": "tapplication/json",
        "Authorization": f'Bearer {token}'}
    print('Posting Records')

    #Send records
    post = requests.post(datahost, headers=headers,data=body).json()

    #If errors exist, send the body of records, otherwise return the success counts
    if post['error_count'] > 0:
        print(f'There were {post["error_count"]} failed records. System Exiting')
        print(post)
        exit()
    else:
        return post['success_count']


def main():
    # 
    # Convert CSV to JSON and optionally post records if you have a streaming endpoint
    #
    print("Converting CSV Data "+CSV_FILE_PATH+" to Molecula JSON Data "+JSON_FILE_PATH)
    files = make_json(CSV_FILE_PATH, JSON_FILE_PATH, FIELD_NAMES, DELIMETER, HEADER)
    if FEATUREBASE_USERNAME != '' and FEATUREBASE_PASSWORD != '' and FEATUREBASE_STREAMING_ENDPOINT != '':
        token = featurebase_authenticate(FEATUREBASE_USERNAME,FEATUREBASE_PASSWORD)
        for file in files:
            success = post_records(token,file, FEATUREBASE_STREAMING_ENDPOINT)
            print(f'{success} records ingested')
            time.sleep(1.5) #Allow for time to process records

    print("All done!")

if __name__ == "__main__":
    main()
```
