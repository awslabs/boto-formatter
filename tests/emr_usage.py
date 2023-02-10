import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(service_name="emr", function_name="list_clusters", format_type="csv", output_to="file" ,pagination="True")
def list_clusters_fmt():
    client = boto3.client('emr')
    paginator = client.get_paginator('list_clusters')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="emr", function_name="list_instance_fleets", format_type="csv", output_to="file" ,pagination="True")
def list_instance_fleets_fmt():
    client = boto3.client('emr')
    paginator = client.get_paginator('list_instance_fleets')
    result = []
    for page in paginator.paginate(ClusterId=""):
        result.append(page)
    return result


@boto_response_formatter(service_name="emr", function_name="list_notebook_executions", format_type="csv", output_to="file" ,pagination="True")
def list_notebook_executions_fmt():
    client = boto3.client('emr')
    paginator = client.get_paginator('list_notebook_executions')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="emr", function_name="list_studios", format_type="csv", output_to="file" ,pagination="True")
def list_studios_fmt():
    client = boto3.client('emr')
    paginator = client.get_paginator('list_studios')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result





if __name__ == "__main__":
    list_clusters_fmt()
    #list_instance_fleets_fmt()
    list_studios_fmt()
    list_notebook_executions_fmt()


