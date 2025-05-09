import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:

            logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Actuator Client {self.did} starting")

        while True:
            try:
                url = f"{self.cloud_url}/smarthouse/actuator/{self.device_id}"
                response = requests.get(url)
                if response.status_code == 200:
                    self.state = response.json().get("state", "Off")
                    logging.info(f"Client: Retrieved state for Lightbulb [{self.device_id}] - {self.state}")
                else:
                    logging.error(f"Client: Failed to retrieve state for Lightbulb [{self.device_id}]. "
                                  f"Status code: {response.status_code}")
            except requests.RequestException as e:
                logging.error(f"Client: Error while retrieving state for Lightbulb [{self.device_id}]: {e}")
            time.sleep(10)  
        logging.info(f"Client    {self.did} finishing")


    def run(self):
        pass
        # start thread simulating physical light bulb
        threading.Thread(target=self.simulator, daemon=True).start()
        # start thread simulating client
        threading.Thread(target=self.client, daemon=True).start()


