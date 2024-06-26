
# **************************************************************************
#   SCHC PROJECT
# **************************************************************************
#   AUTHOR: CRISTIAN AUGUSTO WüLFING
#   EMAIL: cris_wulfing@hotmail.com
#   CITY: Santa Maria - Rio Grande do Sul - Brasil
#   COMPANY: Fox IoT
# **************************************************************************
#   Copyright(c) 2023 Fox IoT.
# **************************************************************************

import paho.mqtt.client as mqtt
import json, codecs
import logging

class MQTTconn:

    mqttc = None

    def __init__(self, server, port, username, password, AppID, devices_list, on_message_callback):

        try:
            self.AppID          = AppID
            self.devices_list   = devices_list

            self.mqttc = mqtt.Client()
            self.mqttc.on_connect=self.on_connect
            # self.mqttc.on_disconnect=self.on_disconnect
            self.mqttc.on_message=on_message_callback

            self.mqttc.username_pw_set(username, password)
            self.mqttc.connect(server, port, 60)
            self.mqttc.loop_start()

        except:

            self.mqttc.disconnect()
            logging.info(f"[MQTT] Client disconnected")

    class DownlinkMessage:
        def __init__(self, port, payload, confirmed=False, priority=None):
            self.f_port = port
            self.frm_payload = payload
            self.priority = priority
            self.confirmed = confirmed

        def obj2json(self):
            return self.__dict__

    def on_connect(self, mqttc, mosq, obj, rc):
        logging.info(f"[MQTT] Connected with result code: {rc}")

        for device in self.devices_list:
            DevEUI = self.devices_list[device]["DevEUI"].lower()
            sub_topic  = "v3/{}/devices/eui-{}/up".format(self.AppID, DevEUI)
            mqttc.subscribe(sub_topic)
            logging.info(f"[MQTT] Subscribing on DevEUI {DevEUI.upper()}")

    # def on_disconnect(self, client, userdata, rc):
    #     logging.info(f"[MQTT] Client disconnected")

    def on_subscribe(self, mosq, obj, mid, granted_qos):
        logging.info(f"[MQTT] Subscribed: {mid} {granted_qos}")

    def obj_dict(self, obj):
        return obj.__dict__

    def send_socket(self, payload: bytes, port: int, DevEUI: str) -> None:

        logging.info(f"[MQTT] Sending to device {DevEUI} on port {port}: {payload.hex()}")

        ttnFormatMsg = {"downlinks":[]}

        b64 = codecs.encode(payload, 'base64').decode().replace("\n", "")
        msg = self.DownlinkMessage(port=port, payload=b64, confirmed=False, priority="HIGHEST")
        ttnFormatMsg["downlinks"].append(msg.obj2json())

        pub_topic  = "v3/{}/devices/eui-{}/down/replace".format(self.AppID, DevEUI) # push | replace
        self.mqttc.publish(pub_topic, payload=json.dumps(ttnFormatMsg), qos=0, retain=False)
