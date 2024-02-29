import sys
import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(
    service_name="route53",
    function_name="list_hosted_zones",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def list_hosted_zones_fmt():
    client = boto3.client("route53")
    paginator = client.get_paginator("list_hosted_zones")
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(
    service_name="route53",
    function_name="list_hosted_zones_by_vpc",
    format_type="csv",
    output_to="file",
)
def list_hosted_zones_by_vpc_fmt():
    client = boto3.client("route53")

    VPCId = ""
    VPCRegion = "us-east-1"
    result = client.list_hosted_zones_by_vpc(VPCId=VPCId, VPCRegion=VPCRegion)
    return result


@boto_response_formatter(
    service_name="route53",
    function_name="list_cidr_blocks",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def list_cidr_blocks_fmt():
    client = boto3.client("route53")
    paginator = client.get_paginator("list_cidr_blocks")
    result = []
    # CollectionId The UUID of the CIDR collection.
    pagination_attributes = {
        "CollectionId": "dfdf",
    }
    for page in paginator.paginate(**pagination_attributes):
        result.append(page)
    return result


if __name__ == "__main__":
    list_hosted_zones_fmt()
    list_hosted_zones_by_vpc_fmt()
    list_cidr_blocks_fmt()
