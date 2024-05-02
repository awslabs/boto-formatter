
from typing import List
import logging
from sys import modules
import botocore
import datetime
import os
import boto_formatter.json_util.json_util as json_util
from boto_formatter.service_config_mgr.service_config import ServiceConfig
import json
import boto3

# Set up our logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()

__FILE_NAME_CONFIGURED_SERVICES = "boto_magic_formatter_configured_services.csv"
__FORMAT_TYPE_CSV = "csv"
__PAGINATION_SUPPORT_Y = "Y"


# Decorator
def boto_magic_formatter(**kwargs) -> List:
    """
    boto_magic_formatter 
    :param format_type: json or csv
    :param output_to: print or file or cmd
    :param file_name: User provided file name if you don't want default filename
    :param required_only: format result for required only columns
    :param updated_folder_path: user provided folder_paht if you don't want default folder path
    :param prefix_columns: prefix columns 
    :param s3_bucket: bucket name
    :param s3_bucket_prefix: bucket prefix
    :return: formatted response
    """
    format_type, output_to, file_name, required_only, updated_folder_path, s3_bucket, s3_bucket_prefix = __validate_parameters(
        kwargs)

    def format_decorator(f):
        def wrapped(_session: boto3.Session, service_name: str, function_name: str, **kwargs) -> List:
            """
            Proxy function
            :param _session: boto3.session
            :param service_name: boto3 service name like s3,ec2
            :param function_name: boto3 function like list_buckets
            :param result: dummy variable
            :param arg: additional attributes
            :return: formatted response
            """
            folder_path = None
            try:
                folder_path = os.path.dirname(
                    os.path.abspath(modules[f.__module__].__file__))
            except AttributeError as err:
                logger.error(err)
                logger.debug(
                    "running from command prompt")
                folder_path = os.getcwd()
            if updated_folder_path is not None:
                folder_path = updated_folder_path
            try:
                result = []
                prefix_columns = None
                attributes = None
                json_config = None
                for item_tuple in kwargs.items():
                    if item_tuple[0] == "prefix_columns":
                        try:
                            prefix_columns = item_tuple[1]["prefix_columns"]
                        except KeyError as err:
                    #This is to handle when pagination iterate even though there is no record or result return even though no records
                            logger.debug(err)
                            raise ValueError('prefix_columns is incorrect format : Example format should be {"prefix_columns": {"Column-1":"Value-1", "Column-2":"Value-2",..}}')
                    elif item_tuple[0] == "attributes":
                        attributes = item_tuple[1]        
                function_config = ServiceConfig.get_service_function_details(
                    service_name, function_name)
                json_config = function_config["json_response"]
                response_format = function_config["response_format"]
                pagination_support = function_config["pagination_support"]
                result_keys = function_config["result_keys"]
                # Some columns breaks as comma so for csv format put required only condition
                try: 
                    service_func = _session.client(service_name)
                    if pagination_support == __PAGINATION_SUPPORT_Y:
                        paginator = service_func.get_paginator(function_name)
                        page_iterator = None
                        if attributes:
                            page_iterator = paginator.paginate(**attributes)
                        else:
                            page_iterator = paginator.paginate()
                        for page in page_iterator:
                            for result_key in result_keys:
                                page = page[result_key]
                            result.extend(page)
                    else:
                        if attributes:
                            result = getattr(service_func, function_name)(
                                **attributes)
                        else:
                            result = getattr(service_func, function_name)()
                        for result_key in result_keys:
                            result = result[result_key]
                except KeyError as err:
                    # This is to handle when pagination iterate even though there is no record or result return even though no records
                    result = []
                    logger.debug(err)
                
                # FORMAT_1 : JSON single record
                # FORMAT_2 : JSON contains List of JSON
                # FORMAT_3 : JSON contains List of Strings
                if response_format == "FORMAT_2":
                    result = json_util.format_json_list(
                        json_config, result, required_only, prefix_columns)
                elif response_format == "FORMAT_1":
                    result = json_util.format_json_object(json_config, result)
                elif response_format == "FORMAT_3":
                    result = json_util.format_str_list(
                        json_config, result, required_only, prefix_columns)
                # response = f(result)
                if format_type is not None:
                    result = __format_response(format_type, result)
                if output_to is not None:
                    if output_to == "file":
                        __output_to_file(
                            service_name, function_name, result, format_type, file_name, folder_path)
                    elif output_to == "print" or output_to == "cmd":
                        __ouptput_to_print(result)
                    elif output_to == "s3":
                        __ouptput_to_s3(_session, service_name, function_name, result, format_type, file_name,s3_bucket,s3_bucket_prefix)
                return result
            except botocore.exceptions.ParamValidationError as error:
                logger.error(error)
                raise ValueError(
                    'For service name {} or function name {} in correct Parameter supplied. Error {}'.format(service_name, function_name, error))
            except botocore.exceptions.ClientError as error:
                logger.error(error)
                raise ValueError(
                    'For service name {} or function name {} botocore client error {} is raised'.format(service_name, function_name, error))

            except KeyError as error:
                logger.error(error)
                raise ValueError(
                    'The service name {} or function name {} provided is invalid. Please supply the correct service name and function name.'.format(service_name, function_name))
        return wrapped
    return format_decorator


# Direct function
def boto_magic_response_formatter(_session: boto3.Session, service_name: str, function_name: str,**kwargs) -> List:
    """
    boto_magic_formatter
    :param format_type: json or csv
    :param output_to: print or file or cmd
    :param file_name: User provided file name if you don't want default filename
    :param required_only: format result for required only columns
    :param updated_folder_path: user provided folder_paht if you don't want default folder path
    :param prefix_columns: prefix columns 
    :param s3_bucket: bucket name
    :param s3_bucket_prefix: bucket prefix
    :param prefix_columns: prefix_columns as json dictionary 
    :param attributes: attributes required for boto3 function
    :return: formatted response
    """
    prefix_columns = None
    attributes = None
    json_config = None
    result = []
    format_type, output_to, file_name, required_only, updated_folder_path, s3_bucket, s3_bucket_prefix = __validate_parameters(
        kwargs)
    for item_tuple in kwargs.items():
        if item_tuple[0] == "prefix_columns":
            try:
                prefix_columns = item_tuple[1]["prefix_columns"]
            except KeyError as err:
            # This is to handle when pagination iterate even though there is no record or result return even though no records
                logger.debug(err)
                raise ValueError('prefix_columns is incorrect format : Example format should be {"prefix_columns": {"Column-1":"Value-1", "Column-2":"Value-2",..}}')
        elif item_tuple[0] == "attributes":
            attributes = item_tuple[1]
    folder_path = None

    try:
        folder_path = os.getcwd()
    except AttributeError as err:
        logger.error(err)
        logger.debug(
            "running from command prompt")

    if updated_folder_path is not None:
        folder_path = updated_folder_path
    try:
        function_config = ServiceConfig.get_service_function_details(
            service_name, function_name)
        json_config = function_config["json_response"]
        response_format = function_config["response_format"]
        pagination_support = function_config["pagination_support"]
        result_keys = function_config["result_keys"]
        # Some columns breaks as comma so for csv format put required only condition
        try: 
            service_func = _session.client(service_name)
            if pagination_support == __PAGINATION_SUPPORT_Y:
                paginator = service_func.get_paginator(function_name)
                page_iterator = None
                if attributes:
                    page_iterator = paginator.paginate(**attributes)
                else:
                    page_iterator = paginator.paginate()
                for page in page_iterator:
                    for result_key in result_keys:
                        page = page[result_key]
                    result.extend(page)
            else:
                if attributes:
                    result = getattr(service_func, function_name)(
                        **attributes)
                else:
                    result = getattr(service_func, function_name)()
                for result_key in result_keys:
                    result = result[result_key]
        except KeyError as err:
            # This is to handle when pagination iterate even though there is no record or result return even though no records
            result = []
            logger.debug(err)
        
        # FORMAT_1 : JSON single record
        # FORMAT_2 : JSON contains List of JSON
        # FORMAT_3 : JSON contains List of Strings
        if response_format == "FORMAT_2":
            result = json_util.format_json_list(
                json_config, result, required_only, prefix_columns)
        elif response_format == "FORMAT_1":
            result = json_util.format_json_object(json_config, result)
        elif response_format == "FORMAT_3":
            result = json_util.format_str_list(
                json_config, result, required_only, prefix_columns)
        if format_type is not None:
            result = __format_response(format_type, result)
        if output_to is not None:
            if output_to == "file":
                __output_to_file(
                    service_name, function_name, result, format_type, file_name, folder_path)
            elif output_to == "print" or output_to == "cmd":
                __ouptput_to_print(result)
            elif output_to == "s3":
                __ouptput_to_s3(_session, service_name, function_name, result, format_type, file_name,s3_bucket,s3_bucket_prefix)
    except botocore.exceptions.ParamValidationError as error:
        logger.error(error)
        raise ValueError(
            'For service name {} or function name {} in correct Parameter supplied. Error {}'.format(service_name, function_name, error))
    except botocore.exceptions.ClientError as error:
        logger.error(error)
        raise ValueError(
            'For service name {} or function name {} botocore client error {} is raised'.format(service_name, function_name, error))

    except KeyError as error:
        logger.error(error)
        raise ValueError(
            'The service name {} or function name {} provided is invalid. Please supply the correct service name and function name.'.format(service_name, function_name))

    return result


def __validate_parameters(kwargs) -> tuple:
    format_type = None
    output_to = None
    file_name = None
    updated_folder_path = None
    required_only = None
    s3_bucket = None
    s3_bucket_prefix = None

    for kwargs_key in kwargs.keys():
        kwargs_key = kwargs_key.lower().strip()
        kwargs_value = kwargs[kwargs_key].lower().strip()
        if kwargs_key == "required_only":
            required_only = "Yes"
        elif kwargs_key == "file_name":
            file_name = kwargs_value
        elif kwargs_key == "folder_path":
            updated_folder_path = kwargs_value
        elif kwargs_key == "s3_bucket":
            s3_bucket = kwargs_value
        elif kwargs_key == "s3_bucket_prefix":
            s3_bucket_prefix = kwargs_value
        elif kwargs_key == "format_type":
            format_type = kwargs_value
            if format_type != "json" and format_type != __FORMAT_TYPE_CSV:
                raise ValueError(
                    "The supported options for format_type are csv and json")
        elif kwargs_key == "output_to":
            output_to = kwargs_value
            if output_to != "file" and output_to != "print" and output_to != "cmd" and output_to != "s3":
                raise ValueError("Support output_to are file,print,cmd and s3")

    return (format_type, output_to, file_name, updated_folder_path,
            required_only, s3_bucket, s3_bucket_prefix)


def __format_response(format_type: str, result: List) -> List:
    if format_type == __FORMAT_TYPE_CSV:
        return json_util.get_csv_data(result)
    else:
        return result


def __get_out_file_name(service_name, function_name, format_type, file_name):
    """
    Function to generate output file_name
    """
    if format_type is None:
        format_type = "json"
    if file_name is None:
        current_date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name = "{}_{}_{}.{}".format(
            service_name, function_name, current_date, format_type)
    else:
        file_name = "{}.{}".format(file_name, format_type)
    return file_name


def __get_out_file_path(service_name, function_name, result, format_type,
                        file_name, folder_path):
    """
    Function to generate output file path
    """
    file_path = None
    try:
        file_name = __get_out_file_name(service_name, function_name, format_type, file_name)
        output_path = os.path.join(folder_path, "output")
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        file_path = os.path.join(output_path, file_name)

    except FileNotFoundError as error:
        logger.error(error)
        raise ValueError('Invalid folder_path: {}'.format(folder_path))
    return file_path


def __output_to_file(service_name, function_name, result, format_type,
                     file_name, folder_path):
    """
    Function to send output to file
    """
    file_path = __get_out_file_path(
        service_name, function_name, result, format_type, file_name, folder_path)
    if format_type == __FORMAT_TYPE_CSV:
        __save_csv(result, file_path)
    else:
        __save_json(result, file_path)


def __ouptput_to_print(json_list_data):
    """
    Function to print output to command prompt
    """
    for _value in json_list_data:
        print(_value)


def __ouptput_to_s3(_session, service_name, function_name, result, format_type, file_name, s3_bucket, s3_bucket_prefix=None):
    """
    Function to save file on S3 bucket
    """
    try:
        file_name = __get_out_file_name(service_name, function_name, format_type, file_name)
        s3 = _session.resource('s3')
        s3_object = None
        if s3_bucket_prefix is None:
            s3_object = s3.Object(s3_bucket, file_name)
        else:
            s3_object = s3.Object(s3_bucket, s3_bucket_prefix + "/" + file_name).put(Body=content)
        if format_type == __FORMAT_TYPE_CSV:
            content = ""
            for row in result:
                content = content + f'{row}\n'
            s3_object.put(Body=content)
        else:
            if len(result) > 0:
                json_data_dict = dict()
                json_data_dict["result"] = result
                s3_object.put(Body=(bytes(json.dumps(json_data_dict, indent=4, default=str).encode('UTF-8'))))

    except botocore.exceptions.ClientError as err:
        status = err.response["ResponseMetadata"]["HTTPStatusCode"]
        errcode = err.response["Error"]["Code"]
        if status == 404:
            logging.exception("Error in request, %s", errcode)
            raise ValueError("Error in uploading file on S3 Bucket .Please verify s3_bucket {}, s3_bucket_prefix {}".format(s3_bucket,s3_bucket_prefix))
        elif status == 403:
            logging.exception("Error in request, %s", errcode)
            raise ValueError('Access denied')
        else:
            logging.exception("Error in request, %s", errcode)
            raise ValueError('Invalid bucket ')
    except botocore.exceptions.ParamValidationError as err:
        logging.exception("Invalid parameter, %s", err)
        raise ValueError('Invalid file name {} '.format(file_name))


def __save_csv(csv_data, file_path):
    """
    Function to save result in  .csv format
    """
    if len(csv_data) > 0:
        with open(file_path, "w") as f:
            for row in csv_data:
                f.write(f'{row}\n')
        print("RESULT : File is generated at location {} ".format(file_path))
    else:
        print("RESULT : No records . ")
    return file_path


def __save_json(json_data, file_path):
    """
    Function to save result in  .json format
    """
    if len(json_data) > 0:
        json_data_dict = dict()
        json_data_dict["result"] = json_data
        json_data_out = json.dumps(json_data_dict, indent=4, default=str)
        with open(file_path, "w") as outfile:
            outfile.write(json_data_out)
        print("RESULT : File is generated at location {} ".format(file_path))
    else:
        print("RESULT : No records . ")
    return file_path


def get_configured_services():
    """
    Function to get configured servics in service_configs
    :param None
    :returns: json list
    """
    return ServiceConfig.get_service_functions_list()


def generate_configured_services_file() -> None:
    """
    Function to generate .csv file for all supported functions that boto_magic_formatter supports
    """
    service_function_list = ServiceConfig.get_service_functions_list()
    to_print_list = []
    item = []
    item.append("service_name")
    item.append("function_name")
    item.append("function_description")
    item.append("mandatory_attributes")
    item.append("optional_attributes")
    to_print_list.append(item)
    for service in service_function_list:
        service_name = service["service_name"]
        function_list = service["function_list"]
        for function_details in function_list:
            item = []
            mandatory_attributes =""
            optional_attributes = ""
            item.append(service_name)
            item.append(function_details["function_name"])
            item.append(function_details["function_description"])
            if "pagination_attributes" in function_details.keys():
                if function_details["pagination_attributes"][0]["is_visible"] == "Y":
                    mandatory_attributes = function_details["pagination_attributes"][0]["attribute_name"]
                else:
                    optional_attributes = function_details["pagination_attributes"][0]["attribute_name"]
            item.append(mandatory_attributes)
            item.append(optional_attributes)
            to_print_list.append(item)
    folder_path = None
    try:
        folder_path = os.getcwd()
    except AttributeError as err:
        logger.error(err)
        logger.debug(
            "running from command prompt")
    file_path = os.path.join(folder_path, __FILE_NAME_CONFIGURED_SERVICES)
    with open(file_path, "w") as file:
        for item in to_print_list:
            file.write(f"{item[0]},{item[1]},{item[2]},{item[3]},{item[4]}\n")
        print("File is generated at {}".format(file_path))
    return file_path


def boto_magic_save_file(format_type: str, **kwargs):
    """
    Save the  json list result in csv or json format.
    Json list is generated by boto_magic_formatter
    :param format_type: json or csv
    :param kwargs: file_name, folder_path
    """
    updated_file_name = None
    update_folder_path = None
    for kwargs_key in kwargs.keys():
        kwargs_key = kwargs_key.lower().strip()
        kwargs_value = kwargs[kwargs_key].lower().strip()
        if kwargs_key == "file_name":
            updated_file_name = kwargs_value
        elif kwargs_key == "folder_path":
            update_folder_path = kwargs_value

    def format_decorator(f):
        def wrapped(result):
            if __validate_format(format_type):
                folder_path = None
                try:
                    folder_path = os.path.dirname(
                        os.path.abspath(modules[f.__module__].__file__))
                except AttributeError as err:
                    logger.error(err)
                    logger.debug(
                        "running from command prompt")
                    folder_path = os.getcwd()
                try:
                    if update_folder_path is not None:
                        folder_path = update_folder_path
                    current_date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
                    if updated_file_name is not None:
                        file_name = "{}.{}".format(updated_file_name, format_type)
                    else:
                        file_name = "{}_{}.{}".format("boto_magic_generated", current_date, format_type)
                    output_path = os.path.join(folder_path, "output")
                    logger.info(
                        "Output directory path {} ".format(output_path))
                    if not os.path.exists(output_path):
                        os.mkdir(output_path)
                    file_path = os.path.join(output_path, file_name)

                    if format_type == __FORMAT_TYPE_CSV:
                        result = json_util.get_csv_data(result)
                        __save_csv(result, file_path)
                    else:
                        __save_json(result, file_path)

                except FileNotFoundError as error:
                    logger.error(error)
                    raise ValueError(
                        'Invalid folder_path: {}'.format(folder_path))
            else:
                raise ValueError("Supported formats are csv and json")
        return wrapped
    return format_decorator


def __validate_format(format_type):
    if format_type == __FORMAT_TYPE_CSV or format_type == "json":
        return True
    else:
        return False
