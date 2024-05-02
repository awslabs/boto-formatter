import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(service_name="sns", function_name="list_subscriptions", format_type="csv", output_to="file",pagination="True" )
def list_subscriptions_fmt():
    client = boto3.client('sns')
    paginator = client.get_paginator('list_subscriptions')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="sns", function_name="list_topics", format_type="csv", output_to="file",pagination="True" )
def list_topics_fmt():
    client = boto3.client('sns')
    paginator = client.get_paginator('list_topics')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result




if __name__ == "__main__":
    list_subscriptions_fmt()
    list_topics_fmt()



