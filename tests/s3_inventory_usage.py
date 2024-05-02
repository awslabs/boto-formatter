import boto3
from boto_formatter.boto_magic_formatter import boto_magic_formatter
from boto_formatter.boto_magic_formatter import boto_magic_save_file

# Generic function returns the flattend JSON list
@boto_magic_formatter()
def list_resources(_session, service_name, function_name, **kwargs):
    result = None
    return result

# Boto magic utility function to save the file.
@boto_magic_save_file(format_type="csv",file_name ="list_bucket_inventory_configurations")
def save_file(result):
    return result

if __name__ == "__main__":
    #list_bucket_analytics_configurations()
    _session = boto3.session.Session()
    # Step 1 : Get List of buckets
    resource_list = list_resources(_session, "s3", "list_buckets")
    consolidated_list = []
    # Step 2 : Iterate over each bucket and get the inventory configurations
    for resource in resource_list:
        try:
            attributes = {"Bucket": resource["Name"]}
            print("Bucket : {}".format(resource["Name"]))
            #Step 2-A : Ingest prefix column for source bucket name
            prefix_columns = {"prefix_columns": {"SourceBucketName":resource["Name"]}}
             # Step 2-B : Get inventory configuration for each bucket and update the consolidated list.
            consolidated_list.extend(list_resources(_session, "s3", "list_bucket_inventory_configurations", attributes=attributes, prefix_columns=prefix_columns))
        except Exception as e:
            print(e)
            pass
    #Step 3  : Save consolidate file
    save_file(consolidated_list)


