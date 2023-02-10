import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(service_name="rds", function_name="describe_db_clusters", format_type="csv", output_to="file",pagination="True" )
def describe_db_clusters_fmt():
    client = boto3.client('rds')
    paginator = client.get_paginator('describe_db_clusters')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="rds", function_name="describe_db_instances", format_type="csv", output_to="file",pagination="True" )
def describe_db_instances_fmt():
    client = boto3.client('rds')
    paginator = client.get_paginator('describe_db_instances')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="rds", function_name="describe_db_security_groups", format_type="csv", output_to="file",pagination="True" )
def describe_db_security_groups_fmt():
    client = boto3.client('rds')
    paginator = client.get_paginator('describe_db_security_groups')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="rds", function_name="describe_db_snapshots", format_type="csv", output_to="file",pagination="True" )
def describe_db_snapshots_fmt():
    client = boto3.client('rds')
    paginator = client.get_paginator('describe_db_snapshots')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="rds", function_name="describe_global_clusters", format_type="csv", output_to="file",pagination="True" )
def describe_global_clusters_fmt():
    client = boto3.client('rds')
    paginator = client.get_paginator('describe_global_clusters')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result

if __name__ == "__main__":
    describe_db_clusters_fmt()
    describe_db_instances_fmt()
    describe_db_security_groups_fmt()
    describe_db_snapshots_fmt()
    describe_global_clusters_fmt()

