import tkinter as tk
from tkinter import ttk
import logging
import requests

from messaging import ActuatorState
import common


def lightbulb_cmd(state, did):

    new_state = state.get()
    logging.info(f"Dashboard: {new_state}")
    url = f"http://localhost:8000/smarthouse/actuator/{did}"
    payload = ActuatorState(state=new_state).to_json()

    try:
        response = requests.put(url, json=payload)

        if response.status_code == 200:
            logging.info(f"Successfully updated lightbulb [{did}] state to {new_state}")
        else:
            logging.error(f"Failed to update lightbulb [{did}] state. "
                          f"Status code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        logging.error(f"Error while updating lightbulb [{did}] state: {e}")

def init_lightbulb(container, did):

    lb_lf = ttk.LabelFrame(container, text=f'LightBulb [{did}]')
    lb_lf.grid(column=0, row=0, padx=20, pady=20, sticky=tk.W)

    # variable used to keep track of lightbulb state
    lightbulb_state_var = tk.StringVar(None, 'Off')

    on_radio = ttk.Radiobutton(lb_lf, text='On', value='On',
                               variable=lightbulb_state_var,
                               command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    on_radio.grid(column=0, row=0, ipadx=10, ipady=10)

    off_radio = ttk.Radiobutton(lb_lf, text='Off', value='Off',
                                variable=lightbulb_state_var,
                                command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    off_radio.grid(column=1, row=0, ipadx=10, ipady=10)
