from airthings_classes import waveplus
from datetime import datetime
import time, json
import paho.mqtt.client as mqtt
from os import environ


# Waveplus
_SerialNumber = int(environ.get('WAVE_SN'))
_SamplePeriod = int(environ.get('WAVE_SAMPLE_PERIOD', 60))

# MQTT
_MQTT_HOST = environ.get('MQTT_HOSTNAME','localhost')
_TOPIC_NAME = '/devices/{}/events'.format('airthings_wave')


def main():

    mqtt_client = mqtt.Client()
    mqtt_client.connect(host=_MQTT_HOST)
    mqtt_client.loop_start()

    waveplus = waveplus.WavePlus(_SerialNumber)
    try:
        while True:
            waveplus.connect()
            
            # read values
            sensors = waveplus.read()

            data = {
                'time': datetime.now().isoformat(),
                'measurement': 'airquality',
                'fields': sensors.getAllValues(),
                'tags': {
                    'sensor_name': 'airthings',
                    'sender': 'me'
                }
            }
            
            waveplus.disconnect()
            mqtt_client.publish(_TOPIC_NAME, payload = json.dumps(data))
            
            time.sleep(_SamplePeriod)
    except Exception as e:
        print("Something went wrong")
        print(str(e))
        raise e
    finally:
        waveplus.disconnect()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


if __name__ == '__main__':
    main()
