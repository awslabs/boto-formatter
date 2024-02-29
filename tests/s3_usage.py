import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(
    service_name="s3", function_name="list_buckets", format_type="csv", output_to="file"
)
def list_buckets_fmt():
    client = boto3.client("s3")
    result = client.list_buckets()
    return result


@boto_response_formatter(
    service_name="s3",
    function_name="list_objects_v2",
    format_type="csv",
    output_to="file",
    pagination="True",
)
def list_objects_v2_fmt():
    client = boto3.client("s3")
    paginator = client.get_paginator("list_objects_v2")
    Bucket = ""
    result = []
    for page in paginator.paginate(Bucket=Bucket):
        result.append(page)
    return result


if __name__ == "__main__":
    # list_buckets_fmt()
    list_buckets_fmt()
    # list_objects_v2_fmt()
