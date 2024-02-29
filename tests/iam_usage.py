import sys
import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(
    service_name="iam",
    function_name="list_access_keys",
    format_type="csv",
    output_to="print",
    pagination="yes",
)
def list_access_keys_fmt():
    client = boto3.client("iam")
    paginator = client.get_paginator("list_access_keys")
    result = []
    for page in paginator.paginate(UserName=""):
        result.append(page)
    return result


@boto_response_formatter(
    service_name="iam",
    function_name="list_roles",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def list_roles_fmt():
    client = boto3.client("iam")
    paginator = client.get_paginator("list_roles")
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


# @boto_response_formatter(service_name="iam", function_name="list_account_aliases", format_type="csv", output_to="file" ,pagination="yes")
def list_account_aliases_fmt():
    result = []
    client = boto3.client("iam")
    paginator = client.get_paginator("list_account_aliases")
    for page in paginator.paginate():
        result.append(page)
    print(result)
    return result


@boto_response_formatter(
    service_name="iam",
    function_name="list_policies",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def list_policies_fmt():
    client = boto3.client("iam")
    paginator = client.get_paginator("list_policies")
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(
    service_name="iam",
    function_name="list_users",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def list_users_fmt():
    client = boto3.client("iam")
    paginator = client.get_paginator("list_users")
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


# @boto_response_formatter(service_name="iam", function_name="list_group_policies", format_type="csv", output_to="file" ,pagination="yes")
def list_group_policies_fmt():
    client = boto3.client("iam")
    paginator = client.get_paginator("list_group_policies")
    result = []
    for page in paginator.paginate(GroupName="MyGroup"):
        result.append(page)
    return result


if __name__ == "__main__":
    # list_access_keys_fmt()
    # list_roles_fmt()
    # list_users_fmt()
    # list_group_policies_fmt()
    list_account_aliases_fmt()
