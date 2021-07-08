from airthings_classes import waveplus_sensor
from datetime import datetime
import time, json, argparse
import paho.mqtt.client as mqtt
from os import environ



def parse_args():
    parser = argparse.ArgumentParser(description=("Common line arguments"))

    parser.add_argument('--env-file', required=False, help='File to read environment variables from')

    return parser.parse_args()



def main():

    # Waveplus
    _SerialNumber = int(environ.get('WAVE_SN'))
    _SamplePeriod = int(environ.get('WAVE_SAMPLE_PERIOD', 60))

    # MQTT
    _MQTT_HOST = environ.get('MQTT_HOSTNAME','localhost')
    _TOPIC_NAME = '/devices/{}/events'.format(environ['WAVE_DEVICE_ID'])

    mqtt_client = mqtt.Client()
    mqtt_client.connect(host=_MQTT_HOST)
    mqtt_client.loop_start()

    waveplus = waveplus_sensor.WavePlus(_SerialNumber)
    try:
        while True:
            waveplus.connect()
            
            sensors = waveplus.read()

            data = {
                'time': time.time_ns(),
                'measurement': 'airquality',
                'fields': sensors.getAllValues(),
                'tags': {
                    'sensor_name': environ['WAVE_DEVICE_ID']
                }
            }
            
            waveplus.disconnect()
            print("Sending data: {}".format(json.dumps(data)))
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

def set_environment(file_path):
    with open(file_path, 'r') as fh:
        lines = fh.readlines()
        for line in lines:
            parts = line.split('=')
            environ[parts[0].strip()] = parts[1].strip()


if __name__ == '__main__':
    args = parse_args()
    if args.env_file:
        set_environment(args.env_file)
    main()
