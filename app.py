from airthings_classes import waveplus
from datetime import datetime
import time, json

SerialNumber = 2930053850
SamplePeriod = 60

_TOPIC_NAME = '/devices/{}/events'.format('airthings_wave')


import paho.mqtt.client as mqtt



def main():

    try:
        #---- Initialize ----#
        waveplus = waveplus.WavePlus(SerialNumber)
        mqtt_client = mqtt.Client()
        mqtt_client.connect(host='localhost')

        mqtt_client.loop_start()
        while True:
            
            waveplus.connect()
            
            # read values
            sensors = waveplus.read()

            data = {
                'timestamp': datetime.now().isoformat(),
                'measurement': 'airquality',
                'measures': sensors.getAllValues(),
                'tags': {
                    'sensor_name': 'airthings'
                }
            }
            
            waveplus.disconnect()
            mqtt_client.publish(_TOPIC_NAME, payload = json.dumps(data))
            
            time.sleep(SamplePeriod)

    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        waveplus.disconnect()


if __name__ == '__main__':
    main()
