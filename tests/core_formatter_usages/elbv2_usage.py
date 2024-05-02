import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(service_name="elbv2", function_name="describe_load_balancers", format_type="csv", output_to="file" ,pagination="True")
def describe_load_balancers_fmt():
    result = []
    client = boto3.client('elbv2')
    paginator = client.get_paginator('describe_load_balancers')
    for page in paginator.paginate():
        result.append(page)
    return result


if __name__ == "__main__":
    describe_load_balancers_fmt()
