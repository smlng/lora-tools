#!/usr/bin/env python3
import argparse
import json
import logging
import time
import ttn

from cayennelpp import LppFrame


OUT_JSON = False


def uplink_callback(msg):
    """
    MQTT receive callback
    """
    logging.info("Uplink message")
    logging.info("  FROM: %s", str(msg.dev_id))
    logging.info("  TIME: %s", str(msg.metadata.time))
    logging.info("   RAW: %s", str(msg.payload_raw))
    frame = LppFrame.from_base64(msg.payload_raw)

    if OUT_JSON:
        out = []
        for item in frame.data:
            out.append({'channel': item.channel, 'type': item.type, 'value': item.value})
        print(json.dumps(out))
    else:
        print(frame)


def main():
    """
    The main loop
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('app', help='The TTN application name.',
                        type=str)
    parser.add_argument('key', help='The TTN application (secret) key.',
                        type=str)
    parser.add_argument('--json', help='Set output format to JSON.',
                        action='store_true')
    args = parser.parse_args()

    logging.debug("APP ID:  %s", args.app)
    logging.debug("APP KEY: %s", args.key)
    logging.debug("OUTJSON: %s", str(args.json))
    global OUT_JSON
    OUT_JSON = args.json

    ttncli = ttn.HandlerClient(args.app, args.key)

    mqttcli = ttncli.data()
    mqttcli.set_uplink_callback(uplink_callback)
    mqttcli.connect()

    while 1:
        time.sleep(10)


if __name__ == "__main__":
    main()
