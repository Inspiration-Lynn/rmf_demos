import re
import sys
from urllib import request
import uuid
import argparse
import json
import asyncio

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import qos_profile_system_default
from rclpy.qos import QoSProfile
from rclpy.qos import QoSHistoryPolicy as History
from rclpy.qos import QoSDurabilityPolicy as Durability
from rclpy.qos import QoSReliabilityPolicy as Reliability

from rmf_task_msgs.msg import ApiRequest, ApiResponse
import schedule
import time
import asyncio

import websockets

async def main(argv=sys.argv):
    rclpy.init(args=sys.argv)
    args_without_ros = rclpy.utilities.remove_ros_args(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('-su', '--server_url',required=True,
                          type=str, nargs='+', default="",
                            help="Websocket Server Address")
    parser.add_argument('-t', '--type',required=True,
                          type=str, nargs='+', default="",
                            help="Type of booking task")
    parser.add_argument('-tm', '--time',required=True,
                          type=str, nargs='+', default="",
                            help="Time for booking task")
    parser.add_argument('-r', '--request',required=True,
                          type=str, nargs='+', default="",
                            help="Request for booking task")
    parser.add_argument('-ti', '--task_id',required=True,
                          type=str, nargs='+', default="",
                            help="Task Id for cancel")
    # TODO: 验证request合法性
    args = parser.parse_args(args_without_ros[1:])

    print("Server URL:\t",str(args.server_url[0]))

    payload = {}

    payload["type"] = args.type[0]
    payload["time"] = args.time[0]
    payload["request"] = args.request[0]
    payload["task_id"] = args.task_id[0]

    print(payload)
    
    msg = json.dumps(payload)

    async with websockets.connect(args.server_url[0]) as websocket:
        await websocket.send(msg)
        msg = await websocket.recv()
        print(msg)
        # await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main(sys.argv))