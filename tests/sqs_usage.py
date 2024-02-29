import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(
    service_name="sqs",
    function_name="list_queues",
    format_type="csv",
    output_to="file",
    pagination="True",
)
def list_queues_fmt():
    client = boto3.client("sqs")
    paginator = client.get_paginator("list_queues")
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


if __name__ == "__main__":
    list_queues_fmt()
