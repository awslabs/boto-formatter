import boto3
from boto_formatter.core_formatter import boto_response_formatter


@boto_response_formatter(service_name="ec2", function_name="describe_addresses", format_type="csv", output_to="file" )
def describe_addresses_fmt():
    client = boto3.client('ec2')
    result = client.describe_addresses()
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_flow_logs", format_type="csv", output_to="file" ,pagination="True")
def describe_flow_logs_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_flow_logs')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_instances", format_type="csv", output_to="file" ,pagination="True")
def describe_instances_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_instances')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_network_acls", format_type="csv", output_to="file" ,pagination="True")
def describe_network_acls_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_network_acls')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_route_tables", format_type="csv", output_to="file" ,pagination="True")
def describe_route_tables_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_route_tables')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_security_groups", format_type="csv", output_to="file" ,pagination="True")
def describe_security_groups_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_security_groups')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_security_group_rules", format_type="csv", output_to="file" ,pagination="True")
def describe_security_group_rules_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_security_group_rules')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_snapshots", format_type="csv", output_to="file" ,pagination="True")
def describe_snapshots_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_snapshots')
    OwnerIds = ["self"]
    result = []
    for page in paginator.paginate(OwnerIds=OwnerIds):
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_subnets", format_type="csv", output_to="file" ,pagination="True")
def describe_subnets_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_subnets')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_transit_gateways", format_type="csv", output_to="file" ,pagination="True")
def describe_transit_gateways_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_transit_gateways')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_volumes", format_type="csv", output_to="file" ,pagination="True")
def describe_volumes_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_volumes')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_vpcs", format_type="csv", output_to="file" ,pagination="True")
def describe_vpcs_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_vpcs')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_vpc_endpoints", format_type="csv", output_to="file" ,pagination="True")
def describe_vpc_endpoints_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_vpc_endpoints')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_vpc_endpoints", format_type="csv", output_to="file" ,pagination="True")
def describe_describe_vpc_endpoints_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_vpc_endpoints')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_vpc_peering_connections", format_type="csv", output_to="file" ,pagination="True")
def describe_vpc_peering_connections_fmt():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_vpc_peering_connections')
    result = []
    for page in paginator.paginate():
        result.append(page)
    return result


@boto_response_formatter(service_name="ec2", function_name="describe_vpn_connections", format_type="csv", output_to="file" )
def describe_vpn_connections_fmt():
    client = boto3.client('ec2')
    result = client.describe_vpn_connections()
    return result


if __name__ == "__main__":
    describe_addresses_fmt()
    describe_flow_logs_fmt()
    describe_instances_fmt()
    describe_network_acls_fmt()
    describe_route_tables_fmt()
    describe_security_groups_fmt()
    describe_security_group_rules_fmt()
    describe_snapshots_fmt()
    describe_subnets_fmt()
    describe_transit_gateways_fmt()
    describe_volumes_fmt()
    describe_vpcs_fmt()
    describe_vpc_endpoints_fmt()
    describe_vpc_peering_connections_fmt()
    describe_vpn_connections_fmt()
