import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(
    service_name="dynamodb",
    function_name="list_tables",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def list_tables_fmt():
    client = boto3.client("dynamodb")
    paginator = client.get_paginator("list_tables")
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


if __name__ == "__main__":
    list_tables_fmt()
