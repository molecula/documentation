---

title: Streaming in a CSV

---


This tutorial will break down into steps how to load a CSV file into FeatureBase using an ingest endpoint, but if you'd rather look at the finished tutorial, please see the full source code at the bottom of this article.


## Configuring account credentials and files

Before we begin, it's always a good idea to make sure you have all the credentials and configuration parameters you need so that you aren't searching halfway through and lose train of thought. For this tutorial we'll need:

* A CSV file to use, as well as the column names in that CSV file.

* A working python3 environment to run this code and install required packages

* FeatureBase Cloud credentials 

* An existing Cloud ingest endpoint



| **SECURITY WARNING**                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Note that for the sake of simplicity, in this tutorial, we're hardcoding passwords and other secrets. Please don't do this in any capacity other than as a personal learning exercise! It's very easy to accidentally commit to code repositories or leave in a public place which invites data breaches for yourself or your organization. |


Below represents all of the inputs you must enter to use these code snippets. This offers limited flexibility but does allow you to specify a delimiter, if not a **","** and if your CSV has a header as the first line or not. You will have to put all of the column names in the order they appear in your CSV file and ensure they match the `path` names in your ingest endpoint. For more information on ingest endpoints, go [here](/data-ingestion/cloud/streaming/streamingoverview).

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
# list of the ordered target column names to write to that correlate to each column in your csv file
# e.g. ["id","sepallength","sepalwidth","petallength","petalwidth","species"]
FIELD_NAMES = []

# Leave these blank if don't want to send your records to your ingest endpoint
# FeatureBase Cloud username/password
FEATUREBASE_USERNAME = ''
FEATUREBASE_PASSWORD = ''
# FeatureBase Cloud > Data Sources > {Source} > "Ingest Endpoint" e.g. "https://data.molecula.cloud/v1/sinks/...
FEATUREBASE_STREAMING_ENDPOINT = ''
```

## Example Data
Below is a small amount of iris (flower) csv records that can be saved as a file in order to follow along. If you'd like to use a much larger dataset but don't have your own data, one can be downloaded [below](/data-ingestion/cloud/streaming/tutorials/csv-tutorial#example-csv)

```csv
id,sepalLength,sepalWidth,petalLength,petalWidth,species
1,5.1,3.5,1.4,0.2,setosa
2,3.1,1.5,2.4,0.9,fake
3,5.9,3.4,1.9,5.2,other
4,4.9,3.8,6.4,1.2,another
```

Inputs for the above iris data above:

```python
# Full Path of the CSV file
CSV_FILE_PATH = '<path to iris csv>' # /path/to/file.csv
DELIMETER = ',' #Change to your file's delimeter
HEADER = True #Change if your csv has no header file as the first line
# Full Path of the json file(s) to write to and stream in
JSON_FILE_PATH = '<path to write iris json files>' # /path/to/file.json
# list of the ordered target column names to write to that correlate to each column in your csv file
FIELD_NAMES = ["id","sepallength","sepalwidth","petallength","petalwidth","species"]
```


You must create a table before you can ingest data. For more information on tables, see [Tables](/data-ingestion/cloud/tables). The command below will create your table. 

It is highly recommended to do table creation within the UI for easier mapping of column types, constraints, and options. Navigate to the "Tables" page and click “New Table", selecting your database, entering "<table-name>" for the name, and entering "table holding flower data" as the description. The primary key for the iris table for this tutorial is a number, so choose `Number` as the ID type.

Once created, go to the "COLUMNS" tab in order to add or delete columns. You will see the _id column that was created during table creation. click "ADD COLUMN" and add the following columns, types, and constraints:

|Column Name | Type | Constraint |
| --- | ----------- |  ----------- |
| sepallength   |  decimal | Scale:2 |
| sepalwidth   |  decimal | Scale:2 |
| petallength   |  decimal | Scale:2 |
| petalwidth   |  decimal | Scale:2 |
| species   |  string | N/A |


You'll need to create an ingest endpoint and table that maps to this data. The bellow schema can be used to create this using either the API or UI:

```shell
{    
    "name": "<endpoint_name>",    
  	"sink_details": {
      "deployment_id": "<database_id>",
      "table": "<table_name>"
    },
    "schema": {
        "type": "json",
        "id_field": "id",
        "allow_missing_fields": false,
        "definition": [
        {
            "name": "id",
            "path": ["id"],
            "type": "id",
            "config": {
              "Mutex": false
            }
        },
        {
            "name": "sepallength",
            "path": ["sepallength"],
            "type": "decimal",
            "config": {
              "Scale": 2
            }
        },
        {
            "name": "sepalwidth",
            "path": ["sepalwidth"],
            "type": "decimal",
            "config": {
              "Scale": 2
            }
        },
        {
            "name": "petallength",
            "path": ["petallength"],
            "type": "decimal",
            "config": {
              "Scale": 2
            }
        },
        {
            "name": "petalwidth",
            "path": ["petalwidth"],
            "type": "decimal",
            "config": {
              "Scale": 2
            }
        },
        {
            "name": "species",
            "path": ["species"],
            "type": "string",
            "config": {
              "Mutex": true
            }
        }]
    }
}
```



## Convert CSV to JSON Format

The first step is to transform every row in the CSV file into the FeatureBase Cloud schema syntax, which can be seen in further detail at [here](/data-ingestion/cloud/streaming/streamingoverview). The output of this function will create 1 to many properly formatted JSON files for every 1000 records in your CSV file. 

```python
def make_json(csvFilePath, jsonFilePath, columnnames, delim=',', header=True):
    """ Function to convert a CSV to batches of json files

    Args:
        csvFilePath (path): Path of the target csv to convert to json
        jsonFilePath (path): Path of the target json file to write to
            Note batch sizes will append to this file name
        columnnames (list): List of the ordered target column names to write to
        delim (str, optional): Delimeter of the csv file Defaults to ','
        header boolean: Indicator if the csv has a header as the first line

    Returns:
        list: A list of all of the json files written to disk
    """

    #Create empty list to track files created
    file_list = []

    print("Writing Molecula JSON Data File "+jsonFilePath)
    f = open(jsonFilePath, 'w', encoding='utf-8') 
    file_list.append(jsonFilePath)

    # Add the pre JSON content ...
    f.write('{ "records": [\n')

    # Open a csv reader called DictReader and pass columnnames in as the dictionary keys
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf, delimiter=delim, fieldnames=columnnames)
         
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
                    print("Writing Molecula JSON Data File "+jsonFilePath+"_"+str(i-2))
                    f = open(jsonFilePath+"_"+str(i-2), 'w', encoding='utf-8')
                    f.write('{ "records": [\n')
                    rdelim = ""

                # #
                # # If any value needs processing/conversion, add logic here
                # #
                row = {}
                delim = ""
                for column in columnnames:
                    if len(rows[column]) != 0:
                        row[column] = rows[column]
                    delim = ","


                # End for column in columnnames
                #print(row)
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

If you enter your username, password, and ingest endpoint, the below code snippets can be used stream the JSON records from the files created to your table in FeatureBase.

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
    """ Load in a json file with 1:n records and post them to FeatureBase Cloud via an ingest endpoint (sink)

    Args:
        token string: IDtoken for auth
        json_file (string): 1 to n json records in a file
        datahost (string): Cloud ingest endpoint e.g. "https://data.molecula.cloud/v1/sinks/..."

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
    post = requests.post(datahost, headers=headers,data=body)
    if post.status_code != 200:
        print(post.text)

    # Retry posting the records once if anything went wrong
    try:
        post.json()['records']
    except KeyError:
        print('Some Issue Occurred')
    else:
        if 'ProvisionedThroughputExceededException' in str(post.json()['records']):
            time.sleep(1)
            post = requests.post(datahost, headers=headers,data=body)

    #If errors exist, send the body of records, otherwise return the success counts
    if post.json()['error_count'] > 0:
        print(f'There were {post.json()["error_count"]} failed records. System Exiting')
        print(post.json())
        exit()
    else:
        return post.json()['success_count']
```


## Putting it all together
The below snippet calls all the functions discussed above to convert your CSV file into JSON. Optionally, it sends them to your ingest endpoint if you enter your credentials and endpoint. This will send all of the JSON files created in the first step. 

```python
def main():
    # 
    # Convert CSV to JSON and optionally post records if you have an ingest endpoint
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
# list of the ordered target column names to write to that correlate to each column in your csv file
# e.g. ["id","sepallength","sepalwidth","petallength","petalwidth","species"]
FIELD_NAMES = []

# Leave these blank if don't want to send your records to your ingest endpoint
# FeatureBase Cloud username/password
FEATUREBASE_USERNAME = ''
FEATUREBASE_PASSWORD = ''
# FeatureBase Cloud > Data Sources > {Source} > "Ingest Endpoint" e.g. "https://data.molecula.cloud/v1/sinks/...
FEATUREBASE_STREAMING_ENDPOINT = ''

def make_json(csvFilePath, jsonFilePath, columnnames, delim=',', header=True):
    """ Function to convert a CSV to batches of json files

    Args:
        csvFilePath (path): Path of the target csv to convert to json
        jsonFilePath (path): Path of the target json file to write to. 
            Note batch sizes will append to this file name
        columnnames (list): List of the ordered target column names to write to
        delim (str, optional): Delimiter of the csv file Defaults to ','.
        header boolean: Indicator if the csv has a header as the first line

    Returns:
        list: A list of all of the json files written to disk
    """

    #Create empty list to track files created
    file_list = []

    print("Writing Molecula JSON Data File "+jsonFilePath)
    f = open(jsonFilePath, 'w', encoding='utf-8') 
    file_list.append(jsonFilePath)

    # Add the pre JSON content ...
    f.write('{ "records": [\n')

    # Open a csv reader called DictReader and pass columnnames in as the dictionary keys
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf, delimiter=delim, fieldnames=columnnames)
         
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
                    print("Writing Molecula JSON Data File "+jsonFilePath+"_"+str(i-2))
                    f = open(jsonFilePath+"_"+str(i-2), 'w', encoding='utf-8')
                    f.write('{ "records": [\n')
                    rdelim = ""

                # #
                # # If any value needs processing/conversion, add logic here
                # #
                row = {}
                delim = ""
                for column in columnnames:
                    if len(rows[column]) != 0:
                        row[column] = rows[column]
                    delim = ","


                # End for column in columnnames
                #print(row)
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
    """ Load in a json file with 1:n records and post them to FeatureBase Cloud via an ingest endpoint (sink)

    Args:
        token string: IDtoken for auth
        json_file (string): 1 to n json records in a file
        datahost (string): Cloud ingest endpoint e.g. "https://data.molecula.cloud/v1/sinks/..."

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
    post = requests.post(datahost, headers=headers,data=body)
    if post.status_code != 200:
        print(post.text)

    # Retry posting the records once if anything went wrong
    try:
        post.json()['records']
    except KeyError:
        print('Some Issue Occurred')
    else:
        if 'ProvisionedThroughputExceededException' in str(post.json()['records']):
            time.sleep(1)
            post = requests.post(datahost, headers=headers,data=body)

    #If errors exist, send the body of records, otherwise return the success counts
    if post.json()['error_count'] > 0:
        print(f'There were {post.json()["error_count"]} failed records. System Exiting')
        print(post.json())
        exit()
    else:
        return post.json()['success_count']


def main():
    # 
    # Convert CSV to JSON and optionally post records if you have an ingest endpoint
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


## Example CSV
If you'd like to go along with a larger csv, a public age csv can be found [here](https://www.kaggle.com/datasets/imoore/age-dataset?resource=download). Note: You will need a Kaggle account to download this.

After downloading the csv, run the following linux command with your new file name of choice in order to null handle all columns with a value of "0".

```shell
sed -e 's/^,/0,/' -e 's/,,/,0,/g' -e 's/,,/,0,/g' -e 's/,$/,0/' AgeDataset-V1.csv > <new file name>.csv
```

The inputs should match the following:

```python
# Full Path of the csv file
CSV_FILE_PATH = '<path to age csv>' # /path/to/file.csv
DELIMETER = ',' #Change to your file's delimeter
HEADER = True #Change if your csv has no header file as the first line
# Full Path of the json file(s) to write to and stream in
JSON_FILE_PATH = '<path to write age json files>' # /path/to/file.json
# list of the ordered target column names to write to that correlate to each column in your csv file
# e.g. ["id","sepallength","sepalwidth","petallength","petalwidth","species"]
FIELD_NAMES = ["id","name","description","gender","country","occupation", "birth_year", "death_year", "death_manner", "death_age"]
```

You'll need to create a table and an ingest endpoint that maps to this data. The table must be created with a "String" primary key and all the columns in the "schema":"definition" below. The json below can be used to create this using either the API or the "schema":"definition" array can be used in the UI:

```json
{    
    "name": "<endpoint_name",    
    "sink_details": {
      "deployment_id": "<database_id>",
      "table": "<table_name>"
    },
    "schema": {
        "type": "json",
        "primary_key_fields": ["id"],
        "allow_missing_fields": false,
        "definition": [
        {
            "name": "id",
            "path": ["id"],
            "type": "string",
            "config": {
              "Mutex": true
            }
        },
        {
            "name": "name",
            "path": ["name"],
            "type": "string",
            "config": {
              "Mutex": true
            }
        },
        {
            "name": "description",
            "path": ["description"],
            "type": "string",
            "config": {
              "Mutex": true
            }
        },
        {
            "name": "gender",
            "path": ["gender"],
            "type": "string",
            "config": {
              "Mutex": true
            }
        },
        {
            "name": "country",
            "path": ["country"],
            "type": "string"
        },
        {
            "name": "occupation",
            "path": ["occupation"],
            "type": "string"
        },
        {
            "name": "birth_year",
            "path": ["birth_year"],
            "type": "int"
        },
        {
            "name": "death_year",
            "path": ["death_year"],
            "type": "int"
        },
        {
            "name": "death_manner",
            "path": ["death_manner"],
            "type": "string"
        },
        {
            "name": "death_age",
            "path": ["death_age"],
            "type": "int"
        }]
    }
  }
```
