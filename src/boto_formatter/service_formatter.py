
import logging
from sys import modules
import os
import boto_formatter.json_util.json_util as json_util
from boto_formatter.service_config_mgr.service_config import ServiceConfig
import time


# Set up our logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def service_response_formatter(service_name, function_name, response, attributes=None):
    """
     service_response_formatter
    :param service_name: example lambda, s3
    :param function_name: example list_functions
    :param response: list of json objects
    :param attributes: format_type,output_to,output_path,pagination,required_only
    :return: formatted response
    """
    format_type = None  # Options are json or csv. Default is json
    output_to = None  # Options are print or file. Default is print
    output_path = None  # Default is none, user can provide custom path
    pagination = False
    required_only = None  # Default is none if required only fields
    # default type is json. Supported types are json,csv
    if attributes is not None:
        if "format_type" in attributes:
            format_type = attributes["format_type"]
        # output_to default is None. Supported options are cmd,file,s3
        if "output_to" in attributes:
            output_to = attributes["output_to"]
        # output_to default is None. Supported options are complete file path or S3 path
        if "output_path" in attributes:
            output_path = attributes["output_path"]
        if "pagination" in attributes:
            if attributes["pagination"] == "True":
                pagination = True
        if "required_only" in attributes:
            required_only = True
    if output_path is None:
        output_path = os.getcwd()
    json_config = None
    result = None
    function_config = ServiceConfig.get_service_function_details(
        service_name, function_name)
    json_config = function_config["json_response"]
    response_format = function_config["response_format"]
    # Some columns breaks as comma so for csv format put required only condition

    start_time = time.time()
    result = __process_response(
        function_config, json_config, format_type, required_only, response, pagination)
    logger.debug("Flattening JSON took--- %s seconds ---" %
                 (time.time() - start_time))
    if format_type:
        result = __format_ouput(result, format_type)
    if output_to:
        result = __ouput_to(service_name, function_name,
                            result, output_to, format_type,
                            output_path, response_format)
    return result


def __process_response(function_config, json_config, format_type, required_only, response, pagination):
    """
    :param function_config : function defined in service_config.json
    :param json_config: reference response
    :param required_only: if present filter the result for required onlydata
    :param response : List of Json object
    :pagination :if present json list is part of pagination
    :return: formatted list of flattend JSON objects
    """
    response_format = function_config["response_format"]
    result_keys = None
    final_result = []
    if "result_keys" in function_config.keys():
        result_keys = function_config["result_keys"]
    if required_only is None and format_type is not None:
        if "csv_enforced_required_only" in function_config.keys() and format_type == "csv":
            required_only = "Yes"
    # FORMAT_1 : JSON single record
    # FORMAT_2 : JSON contains List of JSON
    # FORMAT_3 : JSON contains List of Strings
    if response_format == "FORMAT_2":
        # if pagination then get extended loop
        if pagination:
            for item in response:
                result = item["result"]
                prefix_columns = None
                # prefix_colums work differently in service_formatter and core_formatter
                if "prefix_columns" in item.keys():
                    prefix_columns = item["prefix_columns"]
                for obj in result:
                    final_result.extend(json_util.format_json_list(json_config, json_util.format_response_for_result_keys(
                        obj, result_keys), required_only, prefix_columns))
        else:
            for item in response:
                result = item["result"]
                prefix_columns = None
                if "prefix_columns" in item.keys():
                    prefix_columns = item["prefix_columns"]
                final_result.extend(json_util.format_json_list(json_config, json_util.format_response_for_result_keys(
                    result, result_keys), required_only, prefix_columns))
    elif response_format == "FORMAT_1":
        final_result = json_util.format_json_object(json_config, response)

    elif response_format == "FORMAT_3":
        # if pagination then get extended loop
        if pagination:
            for item in response:
                result = item["result"]
                prefix_columns = None
                # prefix_colums work differently in service_formatter and core_formatter
                if "prefix_columns" in item.keys():
                    prefix_columns = item["prefix_columns"]
                for obj in result:
                    final_result.extend(json_util.format_str_list(json_config, json_util.format_response_for_result_keys(
                        obj, result_keys), required_only, prefix_columns))
        else:
            for item in response:
                result = item["result"]
                prefix_columns = None
                if "prefix_columns" in item.keys():
                    prefix_columns = item["prefix_columns"]
                final_result.extend(json_util.format_str_list(json_config, json_util.format_response_for_result_keys(
                    result, result_keys), required_only, prefix_columns))

    return final_result


def __format_ouput(result, format_type):
    """
    :param result : Flatten JSON list
    :param format_type: currently supported only csv
    :return: formatted list of comma seperated string
    """
    if format_type == "csv":
        return json_util.get_csv_data(result)
    else:
        return result


def __ouput_to(service_name, function_name, result, output_to, format_type, output_path, response_format):
    """
    :param service_name :service_name like s3, lambda
    :param function_name: function name like list_buckets
    :param function_name: processed result
    :param format_type: csv or json
    :param output_path: user provided output_path to save file
    :response_format:FORMAT_1,FORMAT_2,FORMAT_3
    :return: formatted list of comma seperated string
    """
    if output_to == "print":
        return json_util.print_csv_response(result)
    elif output_to == "file" or output_to == "s3":
        if format_type:
            file_path = None
            if format_type == "csv":
                file_path = json_util.save_csv(
                    result, service_name, function_name, output_path)
            else:
                file_path = json_util.save_json(
                    result, service_name, function_name, output_path)
        return file_path
    else:
        return result
