# boto_formatter
## What is boto _formatter?
boto_response_formatter is decorator that convert standard boto3 function response (returned as python list) in flattened JSON or tabular CSV formats for [list of supported services and functions](https://github.com/awslabs/boto-formatter/blob/main/docs/supported_services.md). You can output the response to print, file or send flattened columnar JSON list to another function to continue your process.

 boto_formatter simplifies the process and reduce the need of writing custom codebase potentially of 100s of line of code to 4-5 lines for simple usecases like generating list of lambda fucntions or list of cloudfront distriubtions with all the attributes that Pyton SDK provides.

## How it works?
You simply add decorator to your python function ( the  function which is returning   list from boto3 function) and it will convert the list to flatten JSON or comman seperate values (CSV). 

<p align="center">
  <img src="imgs/boto_formatter.PNG"  title="boto_formatter">

By adding  decorator **@boto_response_formatter** to a function as example shown below in  list_policies_fmt() function the response of the function will be converted to .csv . Generated csv response will also be saved in a file iam_list_polices_<date>.csv in a output folder located in the same directory of invoking python script. 
You can also notice the difference in lines of code when using boto_formatter and without boto_formatter to achive the same result of parsing and flattening the json response.

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


		return result

list_policies_fmt()
list_policies_without_boto_formatter()

```


## Setup
For Installation setup click [here](https://github.com/awslabs/boto-formatter/blob/main/docs/setup.md)


## Usage
[Please click on each function to see the usage/example](https://github.com/awslabs/boto-formatter/blob/main/docs/supported_services.md)

Click on service to see the usage 
<table>
<tbody>
<tr>
<th>Service</th>
<th>Functions</th>
</tr>
<tr>
<th>General usage</th>
<th><a href="https://github.com/awslabs/boto-formatter/blob/main/tests/general_usage.py">General usage</a></th>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/accessanalyzer_usage.py">accessanalyzer</a></td>
<td>
<ul>
<li>1.list_analyzers</li>
<li>2.list_findings</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/apigateway_usage.py">apigateway</a></td>
<td>
<ul>
<li>3.get_rest_apis</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/budgets_usage.py">budgets</a></td>
<td>
<ul>
<li>4.describe_budgets</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/cloudfront_usage.py">cloudfront</a></td>
<td>
<ul>
<li>5.list_distributions</li>
<li>6.list_functions</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/cloudtrail_usage.py">cloudtrail</a></td>
<td>
<ul>
<li>7.list_trails</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/cloudwatch_usage.py">cloudwatch</a></td>
<td>
<ul>
<li>8.list_dashboards</li>
<li>9.list_metrics</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/codecommit_usage.py">codecommit</a></td>
<td>
<ul>
<li>10.list_repositories</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/dynamodb_usage.py">dynamodb</a></td>
<td>
<ul>
<li>11.list_tables</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/ec2_usage.py">ec2</a></td>
<td>
<ul>
<li>12.describe_addresses</li>
<li>13.describe_flow_logs</li>
<li>14.describe_instances</li>
<li>15.describe_network_acls</li>
<li>16.describe_route_tables</li>
<li>17.describe_security_groups</li>
<li>18.describe_security_group_rules</li>
<li>19.describe_snapshots</li>
<li>20.describe_subnets</li>
<li>21.describe_transit_gateways</li>
<li>22.describe_volumes</li>
<li>23.describe_vpcs</li>
<li>24.describe_vpc_endpoints</li>
<li>25.describe_vpc_peering_connections</li>
<li>26.describe_vpn_connections</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/ecs_usage.py">ecs</a></td>
<td>
<ul>
<li>27.list_clusters</li>
<li>28.list_services</li>
<li>29.list_tasks</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/efs_usage.py">efs</a></td>
<td>
<ul>
<li>30.describe_file_systems</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/eks_usage.py">eks</a></td>
<td>
<ul>
<li>31.describe_cluster</li>
<li>32.list_clusters</li>
<li>33.list_fargate_profiles</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/elasticache_usage.py">elasticache</a></td>
<td>
<ul>
<li>34.describe_cache_clusters</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/elbv2_usage.py">elbv2</a></td>
<td>
<ul>
<li>35.describe_load_balancers</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/emr-serverless_usage.py">emr-serverless</a></td>
<td>
<ul>
<li>36.list_applications</li>
<li>37.list_job_runs</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/emr_usage.py">emr</a></td>
<td>
<ul>
<li>38.list_clusters</li>
<li>39.list_instance_fleets</li>
<li>40.list_notebook_executions</li>
<li>41.list_studios</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/iam_usage.py">iam</a></td>
<td>
<ul>
<li>42.list_users</li>
<li>43.list_access_keys</li>
<li>44.list_account_aliases</li>
<li>45.list_attached_group_policies</li>
<li>46.list_attached_role_policies</li>
<li>47.list_attached_user_policies</li>
<li>48.list_group_policies</li>
<li>49.list_groups</li>
<li>50.list_policies</li>
<li>51.list_roles</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/kms_usage.py">kms</a></td>
<td>
<ul>
<li>52.list_keys</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/lambda_usage.py">lambda</a></td>
<td>
<ul>
<li>53.list_functions</li>
<li>54.list_layers</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/organizations_usage.py">organizations</a></td>
<td>
<ul>
<li>55.list_accounts</li>
<li>56.list_policies</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/rds_usage.py">rds</a></td>
<td>
<ul>
<li>57.describe_db_clusters</li>
<li>58.describe_db_instances</li>
<li>59.describe_db_security_groups</li>
<li>60.describe_db_snapshots</li>
<li>61.describe_global_clusters</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/redshift-serverless_usage.py">redshift-serverless</a></td>
<td>
<ul>
<li>62.list_namespaces</li>
<li>63.list_workgroups</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/redshift_usage.py">redshift</a></td>
<td>
<ul>
<li>64.describe_clusters</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/route53_usage.py">route53</a></td>
<td>
<ul>
<li>65.list_cidr_blocks</li>
<li>66.list_hosted_zones</li>
<li>67.list_hosted_zones_by_vpc</li>
<li>68.list_vpc_association_authorizations</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/route53domains_usage.py">route53domains</a></td>
<td>
<ul>
<li>69.list_domains</li>
<li>70.list_prices</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/s3_usage.py">s3</a></td>
<td>
<ul>
<li>71.create_bucket</li>
<li>72.list_buckets</li>
<li>73.list_multipart_uploads</li>
<li>74.list_objects_v2</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/sns_usage.py">sns</a></td>
<td>
<ul>
<li>75.list_subscriptions</li>
<li>76.list_topics</li>
</ul>
</td>
</tr>
<tr>
<td> <a href="https://github.com/awslabs/boto-formatter/blob/main/tests/sqs_usage.py">sqs</a></td>
<td>
<ul>
<li>77.list_queues</li>
</ul>
</td>
</tr>
</tbody>
<table>



## License
This library is licensed under the MIT-0 License. See the LICENSE file.


## Considerations
* Library is not designed for latency-based requirements. So, if you have high latency requirements, please evaluate library in lower enviornments (dev,QA) before using in high latency-based environment.
* When the format_type is selected as "csv" ;boto_formatter will skip the columns which contains "," in value.


