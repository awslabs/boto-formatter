import boto3
from boto_formatter.boto_magic_formatter import boto_magic_formatter
@boto_magic_formatter(format_type="csv")
def list_resources_to_s3(_session, service_name, function_name, **kwargs):
    result = None
    return result

if __name__ == "__main__":
    _session = boto3.session.Session()
    list_resources_to_s3(_session, "lambda", "list_functions")
