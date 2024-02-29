"""
Read all the service definations from service_configs and store the values
in dictionary.

"""
import logging
import os
import json

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def get_service_name(file_name):
    """
    File should be in .json format
    This function strip last four character .json and return value
    :param file_name
    :return: service_name
    """
    json_file_name = None
    try:
        json_file_name = file_name[0 : len(file_name) - 5]
    except Exception as err:
        logger.error(err)
        ERROR_MESSAGE = " Invalid file {} found in service_config directory. service_config shoudl contain only .json files".format(
            file_name
        )
        raise ValueError(ERROR_MESSAGE)

    return json_file_name


class ServiceConfig:
    """This class hold the  values from service_configs"""

    __data = {}

    @classmethod
    def load_all_service_data(cls):
        """Load config values for all services"""
        try:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            dir_path_service = os.path.join(dir_path, "service_configs")
            for service_file in os.listdir(dir_path_service):
                service_name = get_service_name(service_file)
                logger.info("{}.json found ".format(service_name))
                file_path = os.path.join(dir_path_service, service_file)
                f = open(file_path)
                temp_data = json.load(f)
                service_name = temp_data["service_name"]
                ServiceConfig.__data[service_name] = {}
                ServiceConfig.__data[service_name]["service_name"] = service_name
                for function_details in temp_data["functions"]:
                    function_name = function_details["function_name"]
                    ServiceConfig.__data[service_name][
                        function_name
                    ] = ServiceConfig.__process_function_details(function_details)
                f.close()
        except KeyError as err:
            logger.error(
                "Please check service_config.json file . File syntax is not correct."
            )
            raise err
        except FileNotFoundError as err:
            logger.error(
                "File service_config.json file is not Found. Please check aws_account_config.json file exists"
            )
            raise err
        except IOError as err:
            logger.error(
                " IO error while loading the file aws_account_config.json {}. ".format(
                    err
                )
            )
            raise err

    @classmethod
    def load_service_data(cls, service_name):
        """Load config values for perticular service from <service_name>.json file in service_configs folder"""
        logger.info("loading Data for service_name {}...".format(service_name))
        try:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            dir_path_service = os.path.join(dir_path, "service_configs")
            for service_file in os.listdir(dir_path_service):
                if service_name == get_service_name(service_file):
                    file_path = os.path.join(dir_path_service, service_file)
                    f = open(file_path)
                    temp_data = json.load(f)
                    service_name = temp_data["service_name"]
                    ServiceConfig.__data[service_name] = {}
                    ServiceConfig.__data[service_name]["service_name"] = service_name
                    for function_details in temp_data["functions"]:
                        function_name = function_details["function_name"]
                        ServiceConfig.__data[service_name][
                            function_name
                        ] = ServiceConfig.__process_function_details(function_details)
                    f.close()
        except KeyError as err:
            logger.error(
                "Please check service_config.json file . File syntax is not correct."
            )
            raise err
        except FileNotFoundError as err:
            logger.error(
                "File service_config.json file is not Found. Please check aws_account_config.json file exists"
            )
            raise err
        except IOError as err:
            logger.error(
                " IO error while loading the file aws_account_config.json {}. ".format(
                    err
                )
            )
            raise err

    @classmethod
    def get_service_function_details(cls, service_name, function_name):
        function_config = None
        try:
            if service_name in ServiceConfig.__data.keys():
                if function_name in ServiceConfig.__data[service_name]:
                    function_config = ServiceConfig.__data[service_name][function_name]
            else:
                ServiceConfig.load_service_data(service_name)
                # Second Iteration don't catch the exception
                function_config = ServiceConfig.__data[service_name][function_name]
        except KeyError as err:
            ERROR_MESSAGE = " Either Service config  {}.json not found in service_configs folder or function {} is not defined in {}.json".format(
                service_name, function_name, service_name
            )
            logger.error(err)
            raise ValueError(ERROR_MESSAGE)
        return function_config

    @classmethod
    def __process_function_details(cls, function_details):
        """Add required only json_response"""
        json_response_required = dict()
        json_response = function_details["json_response"]
        for key in json_response.keys():
            if json_response[key] == "required":
                json_response_required[key] = json_response[key]
        function_details["json_response_required"] = json_response_required
        return function_details
