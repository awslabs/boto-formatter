import boto3
from boto_formatter.core_formatter import boto_response_formatter
from botocore.exceptions import ClientError


@boto_response_formatter(
    service_name="ecs",
    function_name="list_clusters",
    format_type="csv",
    output_to="file",
    pagination="True",
)
def list_clusters_fmt():
    result = []
    try:
        client = boto3.client("ecs")
        paginator = client.get_paginator("list_clusters")
        for page in paginator.paginate():
            result.append(page)
    except ClientError as e:
        print(e)
    print(result)
    return result


@boto_response_formatter(
    service_name="ecs",
    function_name="list_services",
    format_type="csv",
    output_to="file",
    pagination="True",
)
def list_services_fmt():
    client = boto3.client("ecs")
    paginator = client.get_paginator("list_services")
    result = []
    try:
        # cluster= The short name or full Amazon Resource Name (ARN) of the cluster to use when filtering the ListServices results. If you do not specify a cluster, the default cluster is assumed.
        for page in paginator.paginate(cluster=""):
            result.append(page)
    except ClientError as e:
        print(e)
    return result


@boto_response_formatter(
    service_name="ecs",
    function_name="list_tasks",
    format_type="csv",
    output_to="file",
    pagination="True",
)
def list_tasks_fmt():
    client = boto3.client("ecs")
    paginator = client.get_paginator("list_tasks")
    result = []
    # cluster= The short name or full Amazon Resource Name (ARN) of the cluster to use when filtering the ListServices results. If you do not specify a cluster, the default cluster is assumed.
    for page in paginator.paginate():
        result.append(page)
    return result


if __name__ == "__main__":
    list_clusters_fmt()
    # list_services_fmt()
    # list_tasks_fmt()
    # print(result)
