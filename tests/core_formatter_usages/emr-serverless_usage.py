import boto3
from boto_formatter.core_formatter import boto_response_formatter

@boto_response_formatter(service_name="emr-serverless", function_name="list_applications", format_type="csv", output_to="file",pagination="True" )
def list_applications_fmt():
    client = boto3.client('emr-serverless')
    paginator = client.get_paginator('list_applications')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result

#TODO
#Permission Issues
@boto_response_formatter(service_name="emr-serverless", function_name="list_job_runs", format_type="csv", output_to="file",pagination="True" )
def list_job_runs_fmt():
    client = boto3.client('emr-serverless')
    paginator = client.get_paginator('list_job_runs')
    result = []
    pagination_attributes = {
        "applicationId": "dfdf",
    }
    for page in paginator.paginate(**pagination_attributes):
        result.append(page)
    return result
    
if __name__ == "__main__":
    list_applications_fmt()
    list_job_runs_fmt()
