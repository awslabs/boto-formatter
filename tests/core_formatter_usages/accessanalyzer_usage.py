import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(service_name="accessanalyzer", function_name="list_analyzers", format_type="csv", output_to="file" ,pagination="yes")
def list_analyzers_fmt():
    client = boto3.client('accessanalyzer')
    paginator = client.get_paginator('list_analyzers')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result

@boto_response_formatter(service_name="accessanalyzer", function_name="list_findings", format_type="csv", output_to="file" ,pagination="yes")
def list_findings_fmt():
    client = boto3.client('accessanalyzer')
    paginator = client.get_paginator('list_findings')
    analyzerArn="analyzerArn"
    #analyzerArn="tt"
    result = []
    for page in paginator.paginate(analyzerArn=analyzerArn):
        result.append(page)
    return result


if __name__ == "__main__":
    list_analyzers_fmt()
    list_findings_fmt()
