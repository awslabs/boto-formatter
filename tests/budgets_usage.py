import boto3

from boto_formatter.core_formatter import boto_response_formatter

try:
    from session_mgr.iam_session_mgr import IAMSessionManager
except ImportError:
    pass


@boto_response_formatter(
    service_name="budgets",
    function_name="describe_budgets",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def describe_budget_fmt():
    client = boto3.client("budgets")
    paginator = client.get_paginator("describe_budgets")
    result = []
    for page in paginator.paginate(AccountId="AccountId"):
        result.append(page)
    return result


@boto_response_formatter(
    service_name="budgets",
    function_name="describe_budgets",
    format_type="csv",
    output_to="file",
    pagination="yes",
)
def describe_budget_fmt_36():
    try:
        _session = IAMSessionManager().get_iam_session("AccountId")
        client = _session.client("budgets")
    except:
        client = boto3.client("budgets")
    paginator = client.get_paginator("describe_budgets")
    result = []
    for page in paginator.paginate(AccountId="AccountId"):
        result.append(page)
    return result


if __name__ == "__main__":
    # describe_budget_fmt()
    describe_budget_fmt_36()
