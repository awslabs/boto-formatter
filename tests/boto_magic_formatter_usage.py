"""

FAQ 1 : What are configuratoin options for boto_magic_formatter
boto_magic_formatter Decorator configuration options:
1. format_type: Options are --> csv|json Defaut is json.
2. output_to: Options are --> print|cmd|s3 . Default is None. 
3. file_name: Options are --> file_name in string format. Default is system generated.
4. s3_bucket: Options are --> S3 Bucket Name in string format. Default is None. This is required only 
when you want to save the file in S3 Bucket
5. s3_bucket_prefix Options are --> S3 Bucket Prefix in string format. Default is None

Place holder function configuration options:
1. _session: boto3 session (Mandatory).
2. service_name: boto3 service name (Mandatory). 
3. function_name: boto3 function_name (Mandatory)
4. attributes: Optional in a format attributes = {"<attribute_name>" : "<attribute_value>"}
5. prefix_columns: Optional in a format {"prefix_columns": {"<cloumn_name>":"<cloumn_value>"}}

"""

import boto3
from boto_formatter.boto_magic_formatter import boto_magic_formatter



@boto_magic_formatter(format_type="csv", output_to="file")
def list_resources_to_file(_session, service_name, function_name, **attributes):
    """
    Place holder function. Decorator does all the magic and generate the result.
    """
    result = None
    return result


"""
Returns flatten Json list for further processing
"""
@boto_magic_formatter()
def list_resources(_session, service_name, function_name, **kwargs):
    """
    Place holder function. Decorator does all the magic and generate the result.
    """
    result = None
    return result

"""
Save .csv file on S3 bucket
"""
@boto_magic_formatter(format_type="json", output_to="s3", s3_bucket="abcbucket")
def list_resources_to_s3(_session, service_name, function_name, **kwargs):
    """
    Place holder function. Decorator does all the magic and update the result.
    """
    result = None
    return result


if __name__ == "__main__":
    _session = boto3.session.Session()
    """
    Example 1 : Generate .csv file containing list of AWS resources .
    Notice that you are using the same list_resource_to_file proxy function to generate a CSV file containing a list of AWS resources.
    """
    list_resources_to_file(_session, "accessanalyzer", "list_analyzers")
    list_resources_to_file(_session, "s3", "list_buckets")
    list_resources_to_file(_session, "lambda", "list_functions")
    list_resources_to_file(_session, "iam", "list_roles",)
    list_resources_to_file(_session, "ssm", "describe_instance_information")
    
    """
    Example 2 : Generate List of AWS resources in .csv format by passing input to function
    like list all objects in specific S3 bucket
    """
    # If perticular function takes input you can pass input as a attribute like BucketName
    attributes = {"Bucket" : "abcbucket"}
    list_resources_to_file(_session, "s3", "list_objects_v2", attributes=attributes)


    """
    Example 3 : Upload the result to s3 bucket.
    """
    # If perticular function takes input you can pass input as a attribute like BucketName
    list_resources_to_s3(_session, "lambda", "list_functions")

