import boto3
from boto_formatter.core_formatter import boto_response_formatter

@boto_response_formatter(service_name="redshift-serverless", function_name="list_namespaces", format_type="csv", output_to="file",pagination="True" )
def list_namespaces_fmt():
    client = boto3.client('redshift-serverless')
    paginator = client.get_paginator('list_namespaces')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="redshift-serverless", function_name="list_workgroups", format_type="csv", output_to="file",pagination="True" )
def list_workgroups_fmt():
    client = boto3.client('redshift-serverless')
    paginator = client.get_paginator('list_workgroups')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


if __name__ == "__main__":
    list_namespaces_fmt()
    list_workgroups_fmt()
