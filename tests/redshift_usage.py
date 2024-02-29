import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(
    service_name="redshift",
    function_name="describe_clusters",
    format_type="csv",
    output_to="file",
    pagination="True",
)
def describe_clusters_fmt():
    client = boto3.client("redshift")
    paginator = client.get_paginator("describe_clusters")
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


if __name__ == "__main__":
    describe_clusters_fmt()
