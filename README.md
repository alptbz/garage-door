# Demo project - Garage Door Monitoring Service

Minimal script to monitor a garage door state and send notification using [Pushover](https://pushover.net/) if garage door is open for too long.

This project is part of [Das Garagentor](https://gitlab.com/ch-tbz-wb/Stud/FAAS/-/tree/main/2_Unterrichtsressourcen/B/Uebungen/Vorlagen/MQTTHTTP?ref_type=heads).
(If the link is no longer valid try [FAAS](https://gitlab.com/ch-tbz-wb/Stud/FAAS) and navigate to the folder 
containing the exercise)

## Components
 - Docker / [Podman](https://podman.io/)
 - [MQTT (paho-mqtt)](https://pypi.org/project/paho-mqtt/)
 - [HTTP API (flask)](https://flask.palletsprojects.com/)
 - [Logging (logging)](https://docs.python.org/3/howto/logging.html)
 - [Pushover](https://pushover.net/)

## Preparations
 - To run the project some ENVIRONMENT variables are required. Create a `.env` file with the following structure:
```bash
PUSHOVER_ENDPOINT=https://api.pushover.net/1/messages.json
PUSHOVER_API_TOKEN=
PUSHOVER_USER_ID=
GARAGE_DOOR_TOPIC=
MQTT_HOST=
MQTT_PORT=
```

## Useful commands

 - Build container image
```bash
podman build -t garage-door
```
 - Run container image
```bash
podman run -p 5000:5000 --env-file .env --rm garage-door
```
 - Build container and run the container
```powershell
podman build -t garage-door . ; podman run -p 5000:5000 --env-file .env --rm garage-door
```