import unittest

import boto3

from boto_formatter.core_formatter import boto_response_formatter


class TestS3(unittest.TestCase):
    def test_list_buckets(self):
        list_buckets_fmt()

    def test_list_objects_v2(self):
        list_objects_v2_fmt()


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
    bucket = client.list_buckets()["Buckets"][0].get("Name")
    paginator = client.get_paginator("list_objects_v2")
    result = []
    for page in paginator.paginate(Bucket=bucket):
        result.append(page)
    return result
