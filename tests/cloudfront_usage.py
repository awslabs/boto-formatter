import sys
import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(
    service_name="cloudfront",
    function_name="list_distributions",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def list_distributions_fmt():
    client = boto3.client("cloudfront")
    paginator = client.get_paginator("list_distributions")
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(
    service_name="cloudfront",
    function_name="list_functions",
    format_type="csv",
    output_to="file",
)
def list_functions_fmt():
    client = boto3.client("cloudfront")
    result = client.list_functions()
    return result


if __name__ == "__main__":
    list_distributions_fmt()
    list_functions_fmt()
