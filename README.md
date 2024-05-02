# boto_formatter
# What is boto _formatter?

The boto_magic_formatter is a tool that handles several common tasks when working with boto3 and listing of AWS resources:
1. It automatically handles pagination of AWS responses, 
   stitching together data from multiple pages into a single output.
2. It flattens out nested JSON structures into a consistent tabular format. 
3. It allows you to output the processed data to a file, print it to standard out,
   send it to another command, or upload it to S3 (TBD).
4. It can convert the data to either csv or json format.
In summary, the boto_magic_formatter takes care of pagination, flattening, 
consistent output formatting, and output destination for AWS data, returning it as a csv or json file.

For list of supported services and functions [Click Here](#Supported-services-functions)
# How it works?
You simply add **@boto_magic_formatter** decorator to your placeholder python function and decorator will do all the magic . 



The **@boto_magic_formatter** decorator can be added to a generic function like list_resources() to automatically convert the function's response to a .csv format. When used, the decorator will save the converted csv output to a file called list_resources<date>.csv in an output folder located in the same directory as the invoking python script. 

Using the **@boto_magic_formatter** decorator reduces the amount of code needed to parse and flatten the consistent json response from the function without worrying about detail of boto3 function. Without the decorator, additional lines of code would be required to manually handle the json parsing,flattenign in consistent way and csv conversion that the decorator performs automatically.


Below is example demonstrate the simplification of generating list of aws resources using  magic formatter.

**Without magic formatter**

```
import boto3


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


		return result

    def dummy_csv_save_function(result):
        print(save_file)

if __name__ == "__main__":
    list_policies_without_boto_formatter()

```
**With boto_magic_formatter**
Boto_magic formatter takes care of flattening the data, converting it to CSV format, managing pagination, and generating the output file, removing those burdens from the user.
```
import boto3
from boto_formatter.boto_magic_formatter import boto_magic_formatter

@boto_magic_formatter(format_type="csv", output_to="file")
def list_resources_to_file(_session, service_name, function_name, **attributes):
    result = None
    return result

if __name__ == "__main__":
    _session = boto3.session.Session()
    list_resources_to_file(_session, "iam", "list_policies")

```

<p align="center">
  <img src="imgs/boto_formatter.PNG"  title="boto_formatter">

# Installation 

**boto-formatter** is distributed on PyPI. Easiest way to install it is with pip.For building Installation from source code click [here](https://github.com/awslabs/boto-formatter/blob/main/docs/setup.md)

Create a virtual environment (optional):

```
python3 -m venv .venv
```
Activate enviornment:

```
source .venv/bin/activate
```

Install boto-formatter and boto3:

```
pip install boto-formatter
pip install boto3
```



Run boto-formatter code:

```
import boto3
from boto_formatter.boto_magic_formatter import boto_magic_formatter


"""
Configuration options:
1. format_type: Specify "csv" or "json" format (default is json)
2. output_to: Choose file, print/command, or S3 for output 
3. file_name: For file output, specify a custom file name 
4. Prefix_columns: Prepend static columns like AccountID to output
"""
@boto_magic_formatter(format_type="csv", output_to="file")
def list_resources_to_file(_session, service_name, function_name, attributes):
    """
    Place holder function. Decorator does all the magic.
    """
    result = None
    return result



if __name__ == "__main__":
    _session = boto3.session.Session()
    list_resources_to_file(_session, "lambda", "list_functions")

```

# FAQ

## What are the available service names, functions, and attributes that I can access in the boto_magic_formatter library and how can I get information about them?

**Option 1** : [List of supported services and functions](#Supported-services-functions)

**Option2** :Generate a .csv file listing all the supported service names and function names that boto_magic_formatter supports, you can use the 
function:generate_configured_services_file(). Code snippet Below -->
```
from boto_formatter.boto_magic_formatter import generate_configured_services_file
if __name__ == "__main__":
    generate_configured_services_file()
```





## Passing the information to function as  **attributes
**When calling functions for use cases like listing S3 bucket objects or EMR cluster instance fleets, identifying attributes need to be passed in. For example, to retrieve a list of objects in an S3 bucket, you would pass the specific bucket name. And to get instance fleets for an EMR cluster, you would pass the cluster ID. You can pass this information to the function as attributes**

**Code snippet Below -->**
```
import boto3
from boto_formatter.boto_magic_formatter import boto_magic_formatter

@boto_magic_formatter(format_type="csv", output_to="file")
def list_resources_to_file(_session, service_name, function_name, **attributes):
    result = None
    return result

if __name__ == "__main__":
    _session = boto3.session.Session()
    # If perticular function takes input you can pass input as a attribute like BucketName
    attributes = {"Bucket" : "abhi-abc-bucket"}
    list_resources_to_file(_session, "s3", "list_objects_v2", attributes=attributes)
    attributes = {"ClusterId" : "abc"}
    list_resources_to_file(_session, "emr", "list_instance_fleets", attributes=attributes)

```



## Usage of attributes output chaining (passing one function output to another function as input) and prefix_columns .
**For example usecase of identify all S3 buckets with inventory settings enabled, you first need to retrieve a list of all S3 buckets. Then, for each bucket, check if inventory configuration is enabled. You also need to store the source bucket name with the inventory configuration result for reference. Function chaining can be utilized to perform these actions sequentially, while prefix_columns allows appending supplemental columns to the output that indicate the source bucket for each record returned.**

**Code snippet Below -->**

```
import boto3
from boto_formatter.boto_magic_formatter import boto_magic_formatter
from boto_formatter.boto_magic_formatter import boto_magic_save_file

# Generic function returns the flattend JSON list
@boto_magic_formatter()
def list_resources(_session, service_name, function_name, **kwargs):
    result = None
    return result

# Boto magic utility function to save the file.
@boto_magic_save_file(format_type="csv",file_name ="list_bucket_inventory_configurations")
def save_file(result):
    return result

if __name__ == "__main__":
    #list_bucket_analytics_configurations()
    _session = boto3.session.Session()
    # Step 1 : Get List of buckets
    resource_list = list_resources(_session, "s3", "list_buckets")
    consolidated_list = []
    # Step 2 : Iterate over each bucket and get the inventory configurations
    for resource in resource_list:
        try:
            attributes = {"Bucket": resource["Name"]}
            print("Bucket : {}".format(resource["Name"]))
            #Step 2-A : Ingest prefix column for source bucket name
            prefix_columns = {"prefix_columns": {"SourceBucketName":resource["Name"]}}
             # Step 2-B : Get inventory configuration for each bucket and update the consolidated list.
            consolidated_list.extend(list_resources(_session, "s3", "list_bucket_inventory_configurations", attributes=attributes, prefix_columns=prefix_columns))
        except Exception as e:
            print(e)
            pass
    #Step 3  : Save consolidate file
    save_file(consolidated_list)
```

## Example : Upload the created list to the specified S3 bucket.

**Code snippet Below -->**

```
import boto3
from boto_formatter.boto_magic_formatter import boto_magic_formatter
@boto_magic_formatter(format_type="json", output_to="s3", s3_bucket="test-bucket")
def list_resources_to_s3(_session, service_name, function_name, **kwargs):
    result = None
    return result

if __name__ == "__main__":
    _session = boto3.session.Session()
    list_resources_to_s3(_session, "lambda", "list_functions")
```


## Example : Use the boto_formatter library to retrieve a list of all available resources that are supported.
**Code snippet Below -->**

```
import boto3
from boto_formatter.boto_magic_formatter import get_configured_services
from boto_formatter.boto_magic_formatter import boto_magic_formatter


@boto_magic_formatter(format_type="csv", output_to="file")
def list_resources(_session, service_name, function_name):
    result = None
    return result


def list_all_resoruces():
    _session = boto3.session.Session()
    service_function_list = get_configured_services()
    for service in service_function_list:
        service_name = service["service_name"]
        function_list = service["function_list"]
        for function_details in function_list:
            # Check if function doesn't take any input like Bucket Name
            if "pagination_attributes" in function_details.keys():
                pass 
            else:
                print("Service :{} Function {} ".format(
                    service_name, function_details["function_name"]))
                list_resources(_session, service_name, function_details["function_name"])


if __name__ == "__main__":
    list_all_resoruces()

```


## Example : Use the boto_formatter library to retrieve a list of lambda functions across regions
**Code snippet Below -->**

```
import boto3
from boto_formatter.boto_magic_formatter import boto_magic_formatter
from boto_formatter.boto_magic_formatter import boto_magic_save_file

@boto_magic_formatter()
def list_resources(_session, service_name, function_name):
    result = None
    return result


# Boto magic utility function to save the file.
@boto_magic_save_file(format_type="csv",file_name ="list_of_all_lambda_functions")
def save_file(result):
    return result

if __name__ == "__main__":
    consolidated_list = []
    _session = boto3.session.Session()
    region_list = list_resources(_session, "account", "list_regions")
    for region in region_list:
        if region["RegionOptStatus"]=='ENABLED' or region["RegionOptStatus"]=='ENABLED_BY_DEFAULT':
         
            region_name = region["RegionName"]
            _session = boto3.session.Session(region_name = region_name)
            prefix_columns = {"prefix_columns": {"region":region_name}}
            print("For region {}".format(region_name))
            consolidated_list.extend(list_resources(_session, "lambda", "list_functions", prefix_columns=prefix_columns))

    save_file(consolidated_list)
```
## Use of boto_magic_response_formatter function instead Decorator
**Code snippet Below -->**

```
import boto3
from boto_formatter.boto_magic_formatter import boto_magic_response_formatter

if __name__ == "__main__":
    _session = boto3.session.Session()
    boto_magic_response_formatter(_session, "account", "list_regions",format_type="csv",output_to="file")
    boto_magic_response_formatter(_session, "lambda", "list_functions",format_type="csv",output_to="file")

```




## Configuration options for the boto_magic_formatter decorator and placeholder Python function.

boto_magic_formatter Decorator configuration options:
1. format_type: Options are --> csv|json Defaut is json.
2. output_to: Options are --> print|cmd|s3 . Default is None. 
3. file_name: Options are --> file_name in string format. Default is system generated.
4. s3_bucket: Options are --> S3 Bucket Name in string format. Default is None. This is required only 
when you want to save the file in S3 Bucket
5. s3_bucket_prefix Options are --> S3 Bucket Prefix in string format. Default is None

Place holder function configuration options:
1. _session: boto3 session (Mandatory).
2. service_name: boto3 service name (Mandatory). 
3. function_name: boto3 function_name (Mandatory)
4. attributes: Optional in a format attributes = {"<attribute_name>" : "<attribute_value>"}
5. prefix_columns: Optional in a format {"prefix_columns": {"<cloumn_name>":"<cloumn_value>"}}

## Expand the capabilities of the boto_formatter tool to enable more AWS services /boto3 functions.

The boto_formatter configuration driven. There is a separate [<service_name>. json](https://github.com/awslabs/boto-formatter/tree/main/src/boto_formatter/service_config_mgr/service_configs) configuration file for each AWS service and it’s corresponding functions.
These configuration files are also supported in [resource_lister](https://github.com/awslabs/resource-lister)

**To add new service**: You simply create <new_service_name>. json file and update the corresponding configurations and **boto_formatter will automatically pickup the new service**.

**To modify existing service**: You open the <existing_service_name>. json and update the corresponding configurations and boto_formatter will automatically pickup the new service.

**To add or modify functions**: You open the <existing_service_name>. json and update the corresponding configurations and boto_formatter will automatically pickup the new service.


**Step-by-step instructions for how to create a configuration file will be provided shortly**

## Previous version : boto_core_formatter usage.

Previous version is still supported you can use boto_response_formatter
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
```
[Check previous version examples here](https://github.com/awslabs/boto-formatter/blob/main/tests/core_formatter_usages)






# Supported-services-functions

|service_name            |function_name                                 |function_description                                                                                                                                                                               |mandatory_attributes|optional_attributes     |
|------------------------|----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|------------------------|
|accessanalyzer          |list_analyzers                                |Retrieves a list of analyzers.                                                                                                                                                                     |                    |                        |
|accessanalyzer          |list_findings                                 |Returns information about the access key IDs associated with the specified IAM user                                                                                                                |analyzerArn         |                        |
|accessanalyzer          |list_findings_v2                              |list_findings_v2                                                                                                                                                                                   |analyzerArn         |                        |
|account                 |list_regions                                  |list_regions                                                                                                                                                                                       |                    |                        |
|acm                     |list_certificates                             |Retrieves a list of certificate ARNs and domain names                                                                                                                                              |                    |                        |
|amp                     |list_scrapers                                 |PrometheusService :The ListScrapers operation lists all of the scrapers in your account                                                                                                            |                    |                        |
|amp                     |list_workspaces                               |Lists all of the Amazon Managed Service for Prometheus workspaces in your account                                                                                                                  |                    |                        |
|apigateway              |get_rest_apis                                 |List All Rest APIs                                                                                                                                                                                 |                    |                        |
|budgets                 |describe_budgets                              |Lists all the buedgets                                                                                                                                                                             |                    |AccountId               |
|cleanrooms              |list_collaborations                           |Lists collaborations the caller owns is active in or has been invited to.                                                                                                                          |                    |                        |
|cloudformation          |list_stacks                                   |List of Clouformation Stacks                                                                                                                                                                       |                    |                        |
|cloudformation          |list_stack_sets                               |stack sets that are associated                                                                                                                                                                     |                    |                        |
|cloudfront              |list_distributions                            |List CloudFront distributions                                                                                                                                                                      |                    |                        |
|cloudfront              |list_functions                                |Gets a list of all CloudFront functions in your Amazon Web Services account                                                                                                                        |                    |                        |
|cloudtrail              |list_trails                                   |Lists trails                                                                                                                                                                                       |                    |                        |
|cloudwatch              |list_dashboards                               |List of the dashboards for your account                                                                                                                                                            |                    |                        |
|cloudwatch              |list_metrics                                  |List the specified metrics                                                                                                                                                                         |                    |                        |
|codecommit              |list_repositories                             |Gets information about one or more repositories.                                                                                                                                                   |                    |                        |
|dynamodb                |list_tables                                   |Returns a list of tables                                                                                                                                                                           |                    |                        |
|ec2                     |describe_addresses                            |Describes the specified Elastic IP addresses                                                                                                                                                       |                    |                        |
|ec2                     |describe_flow_logs                            |List VPCFlow logs                                                                                                                                                                                  |                    |                        |
|ec2                     |describe_instances                            |List All Ec2 instances                                                                                                                                                                             |                    |                        |
|ec2                     |describe_network_acls                         |Descirbe Network ACL                                                                                                                                                                               |                    |                        |
|ec2                     |describe_route_tables                         |Descirbe Route Tables                                                                                                                                                                              |                    |                        |
|ec2                     |describe_security_groups                      |List All Security Groups                                                                                                                                                                           |                    |                        |
|ec2                     |describe_security_group_rules                 |List All Security Groups Rules                                                                                                                                                                     |                    |                        |
|ec2                     |describe_snapshots                            |Describe Snapshot                                                                                                                                                                                  |                    |OwnerIds                |
|ec2                     |describe_subnets                              |Descirbe Route Tables                                                                                                                                                                              |                    |                        |
|ec2                     |describe_transit_gateways                     |List All transit_gateways                                                                                                                                                                          |                    |                        |
|ec2                     |describe_volumes                              |Descirbe Volumes                                                                                                                                                                                   |                    |                        |
|ec2                     |describe_vpcs                                 |Descirbe VPCs                                                                                                                                                                                      |                    |                        |
|ec2                     |describe_vpc_endpoints                        |List VPC endpoints                                                                                                                                                                                 |                    |                        |
|ec2                     |describe_vpc_peering_connections              |List vpc peering connections Snapshot                                                                                                                                                              |                    |                        |
|ec2                     |describe_vpn_connections                      |List VPCFlow logs                                                                                                                                                                                  |                    |                        |
|ecs                     |list_clusters                                 |List ECS Clusters                                                                                                                                                                                  |                    |                        |
|ecs                     |list_services                                 |List ECS services                                                                                                                                                                                  |cluster             |                        |
|ecs                     |list_tasks                                    |list_tasks                                                                                                                                                                                         |cluster             |                        |
|efs                     |describe_file_systems                         |Returns the description of a specific Amazon EFS file system                                                                                                                                       |                    |                        |
|eks                     |describe_cluster                              |List EKS Clusters                                                                                                                                                                                  |name                |                        |
|eks                     |list_clusters                                 |List EKS Clusters                                                                                                                                                                                  |                    |                        |
|eks                     |list_fargate_profiles                         |List Farget profiles                                                                                                                                                                               |clusterName         |                        |
|elasticache             |describe_cache_clusters                       |Provisioned cluster                                                                                                                                                                                |                    |                        |
|elbv2                   |describe_load_balancers                       |All of your load balancers.                                                                                                                                                                        |                    |                        |
|emr-serverless          |list_applications                             |Lists applications                                                                                                                                                                                 |                    |                        |
|emr-serverless          |list_job_runs                                 |Lists job runs                                                                                                                                                                                     |applicationId       |                        |
|emr                     |list_clusters                                 |List Clusters                                                                                                                                                                                      |                    |                        |
|emr                     |list_instance_fleets                          |List Instance fleets of EMR Cluster                                                                                                                                                                |ClusterId           |                        |
|emr                     |list_notebook_executions                      |List Notebook executions                                                                                                                                                                           |                    |                        |
|emr                     |list_studios                                  |List Studios                                                                                                                                                                                       |                    |                        |
|iam                     |list_users                                    |Lists the IAM users                                                                                                                                                                                |                    |                        |
|iam                     |list_access_keys                              |Returns information about the access key IDs associated with the specified IAM user                                                                                                                |                    |                        |
|iam                     |list_account_aliases                          |Lists the account alias associated with the Amazon Web Services account                                                                                                                            |                    |                        |
|iam                     |list_attached_group_policies                  |Lists all managed policies that are attached to the specified IAM group                                                                                                                            |GroupName           |                        |
|iam                     |list_attached_role_policies                   |Lists all managed policies that are attached to the specified IAM role                                                                                                                             |RoleName            |                        |
|iam                     |list_attached_user_policies                   |Lists all managed policies that are attached to the specified IAM role                                                                                                                             |UserName            |                        |
|iam                     |list_group_policies                           |Lists all managed policies that are attached to the specified IAM role                                                                                                                             |GroupName           |                        |
|iam                     |list_groups                                   |Lists all managed policies that are attached to the specified IAM role                                                                                                                             |                    |                        |
|iam                     |list_policies                                 |List All the IAM Polices                                                                                                                                                                           |                    |                        |
|iam                     |list_roles                                    |Roles                                                                                                                                                                                              |                    |                        |
|kms                     |list_keys                                     |Gets a list of all KMS keys.                                                                                                                                                                       |                    |                        |
|lambda                  |list_functions                                |List Lambda Functions                                                                                                                                                                              |                    |                        |
|lambda                  |list_layers                                   |List Layers                                                                                                                                                                                        |                    |                        |
|organizations           |list_accounts                                 |List accounts in Organization                                                                                                                                                                      |                    |                        |
|organizations           |list_policies                                 |List Policies in  Organization                                                                                                                                                                     |                    |Filter                  |
|rds                     |describe_db_clusters                          |Amazon Aurora DB clusters                                                                                                                                                                          |                    |                        |
|rds                     |describe_db_instances                         |Provisioned RDS instances                                                                                                                                                                          |                    |                        |
|rds                     |describe_db_security_groups                   |Returns a list of DBSecurityGroup descriptions                                                                                                                                                     |                    |                        |
|rds                     |describe_db_snapshots                         |Returns information about DB snapshots.                                                                                                                                                            |                    |                        |
|rds                     |describe_global_clusters                      |Aurora global database clusters                                                                                                                                                                    |                    |                        |
|redshift-serverless     |list_namespaces                               |List Name spaces                                                                                                                                                                                   |                    |                        |
|redshift-serverless     |list_workgroups                               |List work groups                                                                                                                                                                                   |                    |                        |
|redshift                |describe_clusters                             |Amazon Redshift returns all clusters                                                                                                                                                               |                    |                        |
|resourcegroupstaggingapi|get_resources                                 |Resources                                                                                                                                                                                          |Key                 |                        |
|route53                 |list_cidr_blocks                              |Returns a paginated list of CIDR collections in the Amazon Web Services account (metadata only)                                                                                                    |CollectionId        |                        |
|route53                 |list_hosted_zones                             |Retrieves a list of the public and private hosted zones that are associated with the current Amazon Web Services account                                                                           |                    |                        |
|route53                 |list_hosted_zones_by_vpc                      |Retrieves a list of the public and private hosted zones that are associated with the current Amazon Web Services account                                                                           |VPCId               |                        |
|route53                 |list_vpc_association_authorizations           |Gets a list of the VPCs that were created by other accounts and that can be associated with a specified hosted zone because youve submitted one or more CreateVPCAssociationAuthorization requests.|HostedZoneId        |                        |
|route53domains          |list_domains                                  |Domain names registered with Amazon Route 53                                                                                                                                                       |                    |                        |
|route53domains          |list_prices                                   |Lists the following prices for either all the TLDs supported by Route 53                                                                                                                           |                    |                        |
|s3                      |list_bucket_analytics_configurations          |Lists the analytics configurations for the bucket                                                                                                                                                  |Bucket              |                        |
|s3                      |list_bucket_intelligent_tiering_configurations|Lists the S3 Intelligent-Tiering configuration                                                                                                                                                     |Bucket              |                        |
|s3                      |list_bucket_inventory_configurations          |Lists the S3 Inventory configuration                                                                                                                                                               |Bucket              |                        |
|s3                      |list_bucket_metrics_configurations            |List Bucket Metrics Configurations                                                                                                                                                                 |Bucket              |                        |
|s3                      |list_directory_buckets                        |list_directory_buckets                                                                                                                                                                             |                    |                        |
|s3                      |list_buckets                                  |List of S3 buckets                                                                                                                                                                                 |                    |                        |
|s3                      |list_multipart_uploads                        |list buckets                                                                                                                                                                                       |Bucket              |                        |
|s3                      |list_objects_v2                               |List Objects                                                                                                                                                                                       |Bucket              |                        |
|sagemaker               |list_domains                                  |Lists the domains.                                                                                                                                                                                 |                    |                        |
|sagemaker               |list_images                                   |Lists the Images.                                                                                                                                                                                  |                    |                        |
|sagemaker               |list_models                                   |Lists the Images.                                                                                                                                                                                  |                    |                        |
|sagemaker               |list_projects                                 |Lists the Projects.                                                                                                                                                                                |                    |                        |
|sagemaker               |list_user_profiles                            |Lists user profiles.                                                                                                                                                                               |                    |                        |
|sns                     |list_subscriptions                            |List subscriptions                                                                                                                                                                                 |                    |                        |
|sns                     |list_topics                                   |Returns a list of topics                                                                                                                                                                           |                    |                        |
|sqs                     |list_queues                                   |Returns a list of queues                                                                                                                                                                           |                    |                        |
|ssm                     |describe_instance_information                 |Describe Instance Information                                                                                                                                                                      |                    |                        |


## License
This library is licensed under the MIT-0 License. See the LICENSE file.

## Considerations
- When the format_type is selected as "csv" ;boto_formatter will skip the columns which contains "," in value.
- Majority of the cases Library returns formatted response of all the attributes that Python SDK provides. However, it doesn't assure 100 % coverage of all the attributes that Python SDK provides.
- Library is not designed for latency-based requirements. So, if you have high latency requirements, please evaluate library in lower enviornments (dev,QA) before using in high latency-based environment.


