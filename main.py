import logging
from threading import Thread
import paho.mqtt.client as mqtt
from flask import Flask
from enum import Enum
import schedule
import time
from datetime import datetime, timedelta

import app_config
import app_logger


class GarageDoorState(Enum):
    CLOSED = 1,
    OPEN = 2,
    NEITHER = 3

    def __str__(self):
        if self.value == GarageDoorState.OPEN.value:
            return "Offen"
        if self.value == GarageDoorState.CLOSED.value:
            return "Geschlossen"
        if self.value == GarageDoorState.NEITHER.value:
            return "Wedernoch"


last_state: GarageDoorState = GarageDoorState.NEITHER
last_opened_timestamp = datetime.now()
notification_sent = False


def split_into_axis(raw_sensor_value: str):
    return tuple([float(x.strip()) for x in raw_sensor_value.split(",")])


def eval_garage_door_state(raw_sensor_value: str) -> GarageDoorState:
    x, y, z = split_into_axis(raw_sensor_value)
    if y > 0.8:
        return GarageDoorState.CLOSED
    elif z < -0.8:
        return GarageDoorState.OPEN
    return GarageDoorState.NEITHER


def send_message_to_me(message):
    import requests
    resp = requests.post(app_config.PUSHOVER_ENDPOINT,
                         data={"token": app_config.PUSHOVER_API_TOKEN , "user": app_config.PUSHOVER_USER_ID,
                               "message": message})
    print(resp)


def check_garage_door_state():
    global last_opened_timestamp, notification_sent
    if (last_state == GarageDoorState.OPEN
            and datetime.now() - last_opened_timestamp > timedelta(0, 5)
            and not notification_sent):
        logging.info("garage door is open too long. sending pushover notification")
        send_message_to_me("Schliess das verdammte Garagentor! Wir haben dich Lieb. Deine Mitbewohner.")
        notification_sent = True


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(app_config.GARAGE_DOOR_TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global last_state, notification_sent, last_opened_timestamp
    if msg.topic == app_config.GARAGE_DOOR_TOPIC:
        msg_str = msg.payload.decode("utf-8")
        current_state = eval_garage_door_state(msg_str)
        if current_state != last_state:
            logging.info(f"garage changed to state {current_state.name}")
            last_state = current_state
            if current_state != GarageDoorState.NEITHER:
                last_opened_timestamp = datetime.now()
                notification_sent = False

            print(current_state)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(app_config.MQTT_HOST, app_config.MQTT_PORT, 60)

app = Flask(__name__)


@app.route("/")
def index():
    return f"<p>Die Garage ist {last_state}</p>"


client.loop_start()

schedule.clear()
schedule.every(1).seconds.do(check_garage_door_state)


def schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    logging.info(f"Starting Garage door notification service")
    thread_schedule = Thread(target=schedule_thread, args=())
    thread_schedule.start()
    app.run(host="0.0.0.0")
