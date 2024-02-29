import boto3
import botocore
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(
    service_name="eks",
    function_name="describe_cluster",
    format_type="csv",
    output_to="file",
)
def describe_cluster_fmt():
    result = []
    try:
        client = boto3.client("eks")
        result = client.describe_cluster(name="string")

    except client.exceptions.ResourceNotFoundException as e:
        print(e)
    return result


@boto_response_formatter(
    service_name="eks",
    function_name="list_clusters",
    format_type="csv",
    output_to="file",
    pagination="True",
)
def list_clusters_fmt():
    client = boto3.client("eks")
    paginator = client.get_paginator("list_clusters")
    result = []

    # cluster= The short name or full Amazon Resource Name (ARN) of the cluster to use when filtering the ListServices results. If you do not specify a cluster, the default cluster is assumed.
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(
    service_name="eks",
    function_name="list_fargate_profiles",
    format_type="csv",
    output_to="file",
    pagination="True",
)
def list_fargate_profiles_fmt():
    result = []
    try:
        client = boto3.client("eks")
        paginator = client.get_paginator("list_fargate_profiles")
        result = []
        pagination_attributes = {
            "clusterName": "dfdf",
        }
        for page in paginator.paginate(**pagination_attributes):
            result.append(page)
    except client.exceptions.ResourceNotFoundException as e:
        print(e)
    return result


if __name__ == "__main__":
    # describe_cluster_fmt()
    # list_clusters_fmt()
    list_fargate_profiles_fmt()
