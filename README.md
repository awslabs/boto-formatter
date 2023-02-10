# boto_formatter
## What is boto _formatter?
boto_response_formatter is decorator that convert standard boto3 function response (returned as python list) in flattened JSON or tabular CSV formats for [list of supported services and functions](https://github.com/awslabs/boto-formatter/blob/main/docs/supported_services.md). You can output the response to print, file or send flattened columnar JSON list to another function to continue your process.

## Why should I use boto_response_formatter?
It will reduce your effort of writing custom implementation for common usecase like getting all the lambda functions or list of S3 buckets or any usecase where you simply want to convert your response to readable columnar format or flattened JSON list. It will reduce your effort of writing custom implementation for common usecase like getting all the lambda functions or list of S3 buckets or any usecase where you simply want to convert your response to  readable columnar format or flattened JSON list.

## How it works?
You simply add decorator to your python function and it will convert the response. By adding below decorator client. list functions() response will be converted in attached .csv file in output folder of invoking python script. You can see the difference between .csv and raw json file returned by list functions.

```
import boto3
from  boto_formatter.core_formatter import boto_response_formatter

@boto_response_formatter(service_name="iam", function_name="list_roles", format_type = "csv", output_to="file")
def list_roles_formatter():
    client = boto3.client('iam')
    result = client.list_roles()
    return result



def list_roles():
    client = boto3.client('iam')
    result = client.list_roles()
    return result

list_roles_formatter()
list_roles()

```
## Usage
[Please click on each function to see the usage/example](https://github.com/awslabs/boto-formatter/blob/main/docs/supported_services.md)

## Setup
Click [here](https://github.com/awslabs/boto-formatter/blob/main/docs/setup.md)

## License
This library is licensed under the MIT-0 License. See the LICENSE file.


## Considerations
* Library is not designed for latency-based requirements. So, if you have high latency requirements, please evaluate library in lower enviornments (dev,QA) before using in high latency-based environment.


