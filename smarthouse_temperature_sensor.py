import logging
import threading
import time
import math
import requests

from messaging import SensorMeasurement
import common


class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement('0.0')

    def simulator(self):

        logging.info(f"Sensor {self.did} starting")

        while True:

            temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)

            logging.info(f"Sensor {self.did}: {temp}")
            self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Sensor Client {self.did} starting")
    def client(self):
      
        while True:
            try:
                url = f"{self.cloud_url}/smarthouse/sensor/{self.device_id}"
                payload = {"value": self.temperature}
                response = requests.put(url, json=payload)
                if response.status_code == 200:
                    logging.info(f"Client: Sent temperature for Sensor [{self.device_id}] - {self.temperature}°C")
                else:
                    logging.error(f"Client: Failed to send temperature for Sensor [{self.device_id}]. "
                                  f"Status code: {response.status_code}")
            except requests.RequestException as e:
                logging.error(f"Client: Error while sending temperature for Sensor [{self.device_id}]: {e}")
            time.sleep(10)  # Send temperature every 10 seconds

        logging.info(f"Client {self.did} finishing")


    def run(self):

        pass
        threading.Thread(target=self.simulator, daemon=True).start()
        threading.Thread(target=self.client, daemon=True).start()

