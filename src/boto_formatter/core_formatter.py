import logging
from sys import modules
import os
import boto_formatter.json_util.json_util as json_util
from boto_formatter.service_config_mgr.service_config import ServiceConfig


# Set up our logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def boto_response_formatter(service_name, function_name, **kwargs):
    """
     boto core response formatter
    :param service_name: example lambda, s3
    :param function_name: example list_functions
    :param format_type: json or csv
    :param output_to: print or file
    :param output_path: file output path
    :param pagination: result is generated through pagination
    :param required_only: format result for required only columns
    :return: formatted response
    """
    required_only = None  # Default is none if required only fields
    format_type = None  # Options are json or csv. Default is json
    output_to = None  # Options are print or file. Default is print
    output_path = None  # Default is none, user can provide custom path
    prefix_columns = None
    pagination = None

    # FORMAT_1 : JSON single record
    # FORMAT_2 : JSON contains List of JSON
    # FORMAT_3 : JSON contains List of Strings
    COMMON_FORMAT = "FORMAT_2"

    # default type is json. Supported types are json,csv
    if "format_type" in kwargs:
        format_type = kwargs["format_type"].lower()
    # output_to default is None. Supported options are cmd,file,s3
    if "output_to" in kwargs:
        output_to = kwargs["output_to"]
    # output_to default is None. Supported options are complete file path or S3 path
    if "output_path" in kwargs:
        output_path = kwargs["output_path"]
    if "prefix_columns" in kwargs:
        prefix_columns = kwargs["prefix_columns"]
    if "pagination" in kwargs:
        pagination = True
    if "required_only" in kwargs:
        required_only = "Yes"

    def format_decorator(f):

        def wrapped(*args, **kwargs):
            response = f(*args, **kwargs)
            # If output_path is not provided set as invoking function directory path
            func_dir_path = None
            try:
                func_dir_path = os.path.dirname(
                    os.path.abspath(modules[f.__module__].__file__))
            except AttributeError as err:
                logger.error(err)
                logger.debug(
                    "running from command prompt")
                func_dir_path = os.getcwd()

            logger.debug("Function directory Path : {}".format(func_dir_path))
            json_config = None
            result = None
            function_config = ServiceConfig.get_service_function_details(
                service_name, function_name)

            json_config = function_config["json_response"]
            response_format = function_config["response_format"]
            # Some columns breaks as comma so for csv format put required only condition

            result = __process_service_func_response(
                function_config, json_config, format_type, required_only, response, prefix_columns, pagination)
            # default result is in flatten json format.
            if format_type:
                result = __format_ouput(result, format_type)
            if output_to:
                result = __ouput_to(service_name, function_name,
                                    result, output_to, format_type,
                                    output_path, func_dir_path, response_format)
            return result
        return wrapped
    return format_decorator


def __process_service_func_response(function_config, json_config, format_type, required_only, response, prefix_columns, pagination):
    """
    :param function_config : function defined in service_config.json
    :param json_config: reference response
    :param format_type: csv,json
    :param required_only: if present filter the result for required onlydata
    :param response : response of base function
    :prefix_columns : Addtional prefix columns to print
    :pagination :if present json list is part of pagination
    :return: formatted list of flattend JSON objects
    """
    response_format = function_config["response_format"]
    result_keys = None
    result = []
    if "result_keys" in function_config.keys():
        result_keys = function_config["result_keys"]
    # Come columns breaks in csv format so added this condition to exclued these columns
    if required_only is None and format_type is not None:
        if "csv_enforced_required_only" in function_config.keys() and format_type == "csv":
            required_only = "Yes"
    # FORMAT_1 : JSON single record
    # FORMAT_2 : JSON contains List of JSON
    # FORMAT_3 : JSON contains List of Strings
    if response_format == "FORMAT_2":
        # if pagination then get extended loop
        if pagination:
            for obj in response:
                result.extend(json_util.format_json_list(json_config, json_util.format_response_for_result_keys(
                    obj, result_keys), required_only, prefix_columns))
        else:
            result = json_util.format_json_list(json_config, json_util.format_response_for_result_keys(
                response, result_keys), required_only, prefix_columns)

    elif response_format == "FORMAT_1":
        result = json_util.format_json_object(json_config, response)

    elif response_format == "FORMAT_3":
        if pagination:
            for obj in response:
                result.extend(json_util.format_str_list(json_config, json_util.format_response_for_result_keys(
                    obj, result_keys), required_only, prefix_columns))
        else:
            result = json_util.format_str_list(json_config, json_util.format_response_for_result_keys(
                response, result_keys), required_only, prefix_columns)
    return result


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


def __ouput_to(service_name, function_name, result, output_to, format_type, output_path, func_dir_path, response_format):
    """
    :param service_name :service_name like s3, lambda
    :param function_name: function name like list_buckets
    :param function_name: processed result
    :param format_type: csv or json
    :param output_path: user provided output_path to save file
    :param func_dir_path: invoking file directory path
    :response_format:FORMAT_1,FORMAT_2,FORMAT_3
    :return: formatted list of comma seperated string
    """
    if output_to == "print":
        return json_util.print_csv_response(result)
    elif output_to == "file" or output_to == "s3":
        if output_path is None:
            output_path = func_dir_path
            logging.debug("Directory Path : {}".format(output_path))
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
