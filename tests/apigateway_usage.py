import boto3
from boto_formatter.core_formatter import boto_response_formatter


# No Pagination
@boto_response_formatter(
    service_name="apigateway",
    function_name="get_rest_apis",
    format_type="csv",
    output_to="file",
)
def list_rest_apis():
    client = boto3.client("apigateway")
    result = client.get_rest_apis()
    return result


if __name__ == "__main__":
    list_rest_apis()
