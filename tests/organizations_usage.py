import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(
    service_name="organizations",
    function_name="list_accounts",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def list_accounts_fmt():
    client = boto3.client("organizations")
    paginator = client.get_paginator("list_accounts")
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(
    service_name="organizations",
    function_name="list_policies",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def list_policies_fmt():
    client = boto3.client("organizations")
    paginator = client.get_paginator("list_policies")
    result = []
    attributes = {"Filter": "SERVICE_CONTROL_POLICY"}
    for page in paginator.paginate(**attributes):
        result.append(page)
    return result


if __name__ == "__main__":
    list_accounts_fmt()
    list_policies_fmt()
