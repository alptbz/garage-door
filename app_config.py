import os


def get_environ_variable_or_exit(name):
    if name not in os.environ:
        raise Exception(f"Missing {name} in ENVIRONMENT variables")
    return os.environ[name]


PUSHOVER_API_TOKEN = get_environ_variable_or_exit("PUSHOVER_API_TOKEN")
PUSHOVER_USER_ID = get_environ_variable_or_exit("PUSHOVER_USER_ID")
GARAGE_DOOR_TOPIC = get_environ_variable_or_exit("GARAGE_DOOR_TOPIC")
MQTT_HOST = get_environ_variable_or_exit("MQTT_HOST")
MQTT_PORT = int(get_environ_variable_or_exit("MQTT_PORT"))
PUSHOVER_ENDPOINT = get_environ_variable_or_exit("PUSHOVER_ENDPOINT")
