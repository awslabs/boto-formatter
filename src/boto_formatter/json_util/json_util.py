"""
This is general JSON utility
"""

import datetime
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def flatten_json(y):
    """
     Flatten JSON
    :param json to be flatten
    :return: flattend json
    """
    output = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            output[name[:-1]] = x

    flatten(y)
    return output


def format_response_for_result_keys(json_object_list, result_keys):
    """
     Iterate over result keys in JSON to get appropriate List
    :param json_object_list -JSON object which contains result_key(or Keys)
    :param result_keys  - List of Keys to be search in JSON
    :return: List of JSON objects
    """
    try:
        for result_key in result_keys:
            if len(json_object_list) > 0:
                json_object_list = json_object_list[result_key]
    except KeyError as err:
        # This is to handle when pagination iterate even though there is no record
        json_object_list = []
        logger.debug(err)
        # logger.error(err)
        # raise ValueError(
        #    "Result Keys {} not found in provided JSON. Decorator service/function is not matching with boto function".format(result_keys))
    except TypeError as err:
        logger.error(err)
        raise ValueError(
            "Result List returned by boto3 function is not in correct format or decorator service/function is not matching with boto function"
        )
    return json_object_list


def format_json_list(json_config, json_object_list, required_only, prefix_columns=None):
    """
    Prior:
    Filter Result Keys
    Append addtional columns
    Compare all objects in JSON List with reference json(json_config) and generate list
    1. Iterate each object in List
    2. Flatten the object
    3. Get Keys of reference JSON
    4. Iterate over reference JSON keys and generate result row
    5. Update result rows with not found keys (Extra Columns)
    :param json_config -reference json
    :param json_object_list  - json list that need to be formatted
    :param required_only  - if interest is only in required only attributes
    :param prefix_columns  -if addtional prefix columns you want to add in response
    :return: return json object list formatted in line with json_config
    """
    result_json_list = []
    json_config_keys = json_config.keys()
    First_record = True
    # 1 Take each object in list
    # 1 Outer Loop
    # if json_object_list is zero size loop will not execute
    for json_object_raw in json_object_list:
        # 2 Flatten the object
        json_object = flatten_json(json_object_raw)
        result_row = {}
        keys_present_list = []
        # 3 Append Prefix columns values like Account, Region
        if prefix_columns:
            for prefix_column_header in prefix_columns.keys():
                result_row[prefix_column_header] = prefix_columns[prefix_column_header]
        # 4. Get keys of reference JSON
        json_object_keys = json_object.keys()
        # 5 Go Through All the keys of reference JSON
        for json_config_key in json_config_keys:
            if json_config_key in json_object_keys:
                result_row[json_config_key] = str(json_object[json_config_key])
                keys_present_list.append(json_config_key)
            else:
                result_row[json_config_key] = ""
        # 6. Append Extra Cloumns as pipe seprated Key/Value
        # If required_only is selected don't need extra columns
        if not required_only:
            extra_rows = [i for i in json_object_keys if i not in keys_present_list]
            for extra_row_key in extra_rows:
                result_row[extra_row_key] = "{}|{}".format(
                    extra_row_key, json_object[extra_row_key]
                )
        # 7 None of key matches for first row raise and exception as it's not valid JSON
        if First_record:
            if len(keys_present_list) == 0:
                raise ValueError(
                    "Zero record keys are matching. Check the JSON result is appropriate format"
                )
        First_record = False
        result_json_list.append(result_row)
    return result_json_list


def format_str_list(json_config, json_object_list, required_only, prefix_columns=None):
    """
    Prior:
    Filter Result Keys
    Append addtional columns
    Iterate each string and convert to JSON

    :param json_config -reference json
    :param json_object_list  - json list that need to be formatted
    :param required_only  - if interest is only in required only attributes
    :param prefix_columns  -if addtional prefix columns you want to add in response
    :return: return json object list formatted in line with json_config
    """
    result_json_list = []
    # Ensure first Key is present
    column_key = list(json_config.keys())[0]
    # 1 Take each string in list
    # 1 Outer Loop
    # if json_object_list is zero size loop will not execute
    for str_obj in json_object_list:
        result_row = {}
        # 2 Append Prefix columns values like Account, Region
        if prefix_columns:
            for prefix_column_header in prefix_columns.keys():
                result_row[prefix_column_header] = prefix_columns[prefix_column_header]
        # 3. Ensure first Key is present
        result_row[column_key] = str_obj
        result_json_list.append(result_row)
    return result_json_list


def format_json_object(json_config, json_object_raw):
    """
    Compare Json_object with reference json(json_config) and generate JSON Object
    1. Flatten the object
    2. Get Keys of reference JSON
    3. Iterate over reference JSON keys and generate result row
    4. Update result rows with not found keys (Extra Columns)
    :param json_config -reference json
    :param json_object_raw  - json object to be formatted
    :return: return json object formated in line with json_config
    """
    json_config_keys = json_config.keys()
    # 2 Flatten the object
    json_object = flatten_json(json_object_raw)
    result_row = {}
    keys_present_list = []
    # 3. Get keys of reference JSON
    json_object_keys = json_object.keys()
    # 4 Go Through All the keys of reference JSON
    for json_config_key in json_config_keys:
        if json_config_key in json_object_keys:
            result_row[json_config_key] = str(json_object[json_config_key])
            keys_present_list.append(json_config_key)
        else:
            result_row[json_config_key] = ""
    # 5. Append Extra Cloumns as pipe seprated Key/Value
    extra_rows = [i for i in json_object_keys if i not in keys_present_list]
    for extra_row_key in extra_rows:
        result_row[extra_row_key] = "{}|{}".format(
            extra_row_key, json_object[extra_row_key]
        )

    return result_row


def get_csv_data(result_json_list):
    """
    :param flattend json object list
    :return: list of comma seperated string
    """
    csv_data = []
    if len(result_json_list) > 0:
        logger.debug(result_json_list)
        csv_data.append(",".join(result_json_list[0].keys()))
        for json_obj in result_json_list:
            csv_data.append(",".join(json_obj.values()))
    return csv_data


def print_csv_response(csv_data):
    """
    :param list of comma seperated string
    :return: None
    """
    for csv_value in csv_data:
        print(csv_value)


def get_output_path():
    """
    :return: output_path
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    return dir_path


def get_file_path(service_name, function_name, dir_path, file_type):
    """
     Generate file path based on service_name and function_name
    :param service_name like s3, lambda
    :param function_name like list_buckets
    :return: None
    """
    if not os.path.exists(dir_path):
        ValueError("Invalid Path to store the file  {}".format(dir_path))
    current_date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    file_name = "{}_{}_{}.{}".format(
        service_name, function_name, current_date, file_type
    )
    output_path = os.path.join(dir_path, "output")
    logger.info("Output directory path {} ".format(output_path))
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    file_path = os.path.join(output_path, file_name)
    logger.info("File Path {}".format(file_path))
    return file_path


def save_csv(csv_data, service_name, function_name, dir_path):
    """
     save file as .csv
    :param csv_data data in list of comma seperated strings
    :param service_name like s3, lambda
    :param function_name like list_buckets
    :return: None
    """
    file_full_path = None
    if len(csv_data) > 0:
        file_full_path = get_file_path(service_name, function_name, dir_path, "csv")
        f = open(file_full_path, "w")
        for row in csv_data:
            f.write(row + "\n")
        print("RESULT : File is generated at location {} ".format(file_full_path))
    else:
        print("RESULT : No records . ")
    return file_full_path


def save_json(json_data, service_name, function_name, dir_path=None):
    """
     save file as .json
    :param json_data json formatted data
    :param service_name like s3, lambda
    :param function_name like list_buckets
    :return: None
    """
    file_full_path = None
    if len(json_data) > 0:
        json_data_list = dict()
        json_data_list["result"] = json_data
        file_full_path = get_file_path(service_name, function_name, dir_path, "json")
        json_data_list = json.dumps(json_data_list, indent=4, default=str)
        # Writing to sample.json
        with open(file_full_path, "w") as outfile:
            outfile.write(json_data_list)
        print("RESULT : File is generated at location {} ".format(file_full_path))
    else:
        print("RESULT : No records . ")
    return file_full_path


def save_file(json_data, service_name, function_name, dir_path=None):
    file_full_path = get_file_path(service_name, function_name, dir_path, "json")
    # Writing to sample.json
    with open(file_full_path, "w") as outfile:
        outfile.write(json_data)
    print("RESULT : File is generated at location {} ".format(file_full_path))
