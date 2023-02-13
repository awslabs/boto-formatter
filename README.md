# boto_formatter
## What is boto _formatter?
boto_response_formatter is decorator that convert standard boto3 function response (returned as python list) in flattened JSON or tabular CSV formats for [list of supported services and functions](https://gitlab.aws.dev/rajeabh/boto_formatter/-/blob/main/docs/supported_services.md). You can output the response to print, file or send flattened columnar JSON list to another function to continue your process.

## Why should I use boto_response_formatter?
It will reduce your effort of writing custom implementation for common usecase like getting all the lambda functions or list of S3 buckets or any usecase where you simply want to convert your response to readable columnar format or flattened JSON list. It will reduce your effort of writing custom implementation for common usecase like getting all the lambda functions or list of S3 buckets or any usecase where you simply want to convert your response to  readable columnar format or flattened JSON list.

## How it works?
You simply add decorator to your python function and it will convert the response. By adding below decorator client. list functions() response will be converted in attached .csv file in output folder of invoking python script. You can see the difference in lines of code when using boto_formatter and without boto_formatter. You can also see the different in output .csv and raw json file returned by list functions.

<p align="center">
  <img src="imgs/boto_formatter.PNG"  title="boto_formatter">

```
import boto3
from  boto_formatter.core_formatter import boto_response_formatter

# With boto_formatter
@boto_response_formatter(service_name="iam", function_name="list_policies", format_type="csv", output_to="file" ,pagination="yes")
def list_policies_fmt():
    client = boto3.client('iam')
    paginator = client.get_paginator('list_policies')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result

# Without boto_formatter
def list_policies_without_boto_formatter():
	client = boto3.client('iam')
	paginator = client.get_paginator('list_policies')
	result = []
	for page in paginator.paginate():
		for role in page['Policies']:
			json_obj = {}
			json_obj['PolicyName'] = role['PolicyName']
			json_obj['PolicyId'] = role['PolicyId']
			json_obj['Arn'] = role['Arn']
			json_obj['Path']=str(role['Path'])
			json_obj['DefaultVersionId'] = str(role['DefaultVersionId'])
			json_obj['AttachmentCount'] = str(role['AttachmentCount'])
			json_obj['PermissionsBoundaryUsageCount'] = str(role['PermissionsBoundaryUsageCount'])
			json_obj['IsAttachable'] = str(role['IsAttachable'])
			if "Description" in role.keys():
				json_obj['Description'] = str(role['Description'])
			json_obj['CreateDate'] = str(role['CreateDate'])
			json_obj['UpdateDate'] = str(role['UpdateDate'])
			if "Tags" in role.keys():
				json_obj['Tags_Key'] = role['Tags']['Key']
				json_obj['Tags_Value'] = role['Tags']['Value']
			result.append(json_obj)

		print(result)
		return result

list_policies_fmt()
list_policies_without_boto_formatter()

```
## Usage
[Please click on each function to see the usage/example](https://gitlab.aws.dev/rajeabh/boto_formatter/-/blob/main/docs/supported_services.md)

## Setup
Click [here](https://gitlab.aws.dev/rajeabh/boto_formatter/-/blob/main/docs/setup.md)

## License
This library is licensed under the MIT-0 License. See the LICENSE file.


## Considerations
* Library is not designed for latency-based requirements. So, if you have high latency requirements, please evaluate library in lower enviornments (dev,QA) before using in high latency-based environment.
* When the format_type is selected as "csv" ;boto_formatter will skip the columns which contains "," in value.


