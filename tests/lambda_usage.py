import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(service_name="lambda", function_name="list_functions", format_type="csv", output_to="file")
def list_functions():
    client = boto3.client('lambda')
    result = client.list_functions()
    return result


@boto_response_formatter(service_name="lambda", function_name="list_layers", format_type="csv", output_to="file")
def list_layers():
    client = boto3.client('lambda')
    result = client.list_layers(CompatibleRuntime='python3.6')
    return result


if __name__ == "__main__":
    list_functions()
    list_layers()
