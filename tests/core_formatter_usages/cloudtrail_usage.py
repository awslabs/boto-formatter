import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(service_name="cloudtrail", function_name="list_trails", format_type="csv", output_to="file" ,pagination="yes")
def list_trails_fmt():
    client = boto3.client('cloudtrail')
    paginator = client.get_paginator('list_trails')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


if __name__ == "__main__":
    list_trails_fmt()
