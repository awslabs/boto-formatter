import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(
    service_name="efs",
    function_name="describe_file_systems",
    format_type="csv",
    output_to="file",
    pagination="True",
)
def describe_file_systems_fmt():
    result = []
    client = boto3.client("efs")
    paginator = client.get_paginator("describe_file_systems")
    for page in paginator.paginate():
        result.append(page)
    return result


if __name__ == "__main__":
    describe_file_systems_fmt()
