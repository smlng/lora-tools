#!/usr/bin/env python3
import argparse
import json
import logging
import os
import time
import ttn

from cayennelpp import LppFrame


out_json = False


def uplink_callback(msg, client):
    logging.info("Uplink message")
    logging.info("  FROM: ", msg.dev_id)
    logging.info("  TIME: ", msg.metadata.time)
    logging.info("   RAW: ", msg.payload_raw)
    frame = LppFrame.from_base64(msg.payload_raw)

    if out_json:
        out = []
        for d in frame.data:
            out.append({'channel': d.channel, 'type': d.type, 'value': d.value})
        print(json.dumps(out))
    else:
        print(frame)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('app',      help='The TTN application name.', type=str)
    parser.add_argument('key',      help='The TTN application (secret) key.', type=str)
    parser.add_argument('--json',   help='Set output format to JSON.', action='store_true')
    args = parser.parse_args()

    logging.debug("APP ID:  ", args.app)
    logging.debug("APP KEY: ", args.key)
    logging.debug("OUTJSON: ", str(args.json))
    global out_json
    out_json = args.json
    
    ttncli = ttn.HandlerClient(args.app, args.key)

    mqttcli = ttncli.data()
    mqttcli.set_uplink_callback(uplink_callback)
    mqttcli.connect()

    while 1:
        time.sleep(10)


if __name__ == "__main__":
    main()
