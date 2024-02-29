import unittest

import boto3

from boto_formatter.core_formatter import boto_response_formatter


class TestAppflow(unittest.TestCase):
    def test_list_flows(self):
        list_flows_fmt()


@boto_response_formatter(
    service_name="appflow",
    function_name="list_flows",
    format_type="csv",
    output_to="file",
)
def list_flows_fmt():
    client = boto3.client("appflow")
    result = {"flows": []}
    page = client.list_flows()
    result["flows"] += page["flows"]
    while "nextToken" in page:
        page = client.list_flows(nextToken=page["nextToken"])
        result["flows"] += page["flows"]
    return result
