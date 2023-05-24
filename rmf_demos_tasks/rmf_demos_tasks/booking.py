#!/usr/bin/env python3

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

# TODO: 优化内存回收
# TODO: 优化多线程支持
# TODO: 集成到rmf_demos中
task_count = 0
task_queue = {}
class Booking(Node):
    def __init__(self):
        super().__init__('task_requester')
        # TODO: websocket 定时任务
        # TODO: websocket 请求格式
        # 任务队列
        self.responses = {}

        # websocket

        self.transient_qos = QoSProfile(
            history=History.KEEP_LAST,
            depth=1,
            reliability=Reliability.RELIABLE,
            durability=Durability.TRANSIENT_LOCAL)

        self.pub = self.create_publisher(
          ApiRequest, 'task_api_requests', self.transient_qos)

    def request_cb(self,time,request,task_id):
        # TODO: 检查Request有效性


        # 将任务加入到task 队列中
        print("Recv a Booking Task:\t",time)
        print("Task ID:\t" + task_id)
        print("Request:\t")
        print(request)
        task = schedule.every().day.at(time).do(self.job,time=time,task_id=task_id,request=request)
        global task_queue
        task_queue[task_id] = task
        print("Task Queue")
        print(task_queue)
        # TODO: 返回response
        return task_id

    def job(self,time,task_id,request): # TODO: 增加time和request
        print("Start Booking Task:\t" + time)
        print("Task ID:\t" + task_id)
        print("Request:\t")
        print(request)

        # Construct task
        msg = ApiRequest()
        msg.request_id = "delivery_" + str(uuid.uuid4())
        print("Request ID:\t" + msg.request_id)
        msg.json_msg = request

        # 接收响应
        self.responses[msg.request_id] = asyncio.Future()
        def receive_response(response_msg: ApiResponse):
            if response_msg.request_id == msg.request_id:
                print(response_msg.json_msg)
                self.responses[msg.request_id].set_result(json.loads(response_msg.json_msg))

        self.sub = self.create_subscription(
            ApiResponse, 'task_api_responses', receive_response, 10
        )

        # 发送任务
        # WARN: 发送任务必须在订阅之后
        self.pub.publish(msg)

        rclpy.spin_until_future_complete(
            self, self.responses[msg.request_id], timeout_sec=5.0)

        # TODO: 检查response 
        if self.responses[msg.request_id].done():
            print(f'Got response:\n{self.responses[msg.request_id].result()}')
        else:
            print('Did not get a response')
        # TODO: 处理异常情况

    def cancel_cb(self,task_id):
        # TODO: task_id有效性

        # 按照task_id从任务队列中取出任务，然后取消该任务
        print("Cancel Task:\t" + task_id)
        global task_queue
        task = task_queue.pop(task_id,None)
        if (task):
            schedule.cancel_job(task)
            print("Find Task:\t" + task_id)
            print("Current Task Queue Size:\t")
            print(task_queue)
            return True
        else: 
            print("Task has been dispatched")
            return False

        # TODO: 返回response

    def update():
        # 上报任务信息
        print()  

async def add(task_count):
    return task_count + 1

async def Server(websocket, path):
    global task_count
    booking = Booking()
    while True:
        schedule.run_pending()
        try:
            msg = await websocket.recv()
            print("Websocket Recv msg:\t")
            print(msg)

            json_msg = json.loads(msg)

            msg_type = json_msg["type"]
            if (msg_type == "booking"):
                time = json_msg["time"]
                request = json_msg["request"]
                # 生成task_id
                task_id = "delivery.booking-" + str(task_count)
                task_count = await add(task_count)
                print(task_count)
                task_id =  booking.request_cb(time,request,task_id)
                print(task_id)
                all_jobs = schedule.get_jobs()
                print("Current Booking Job")
                print(all_jobs)
                await websocket.send(task_id)
            elif (msg_type == "cancel"):
                task_id = json_msg["task_id"]
                success = booking.cancel_cb(task_id)
                all_jobs = schedule.get_jobs()
                print("Current Booking Job")
                print(all_jobs)
                await websocket.send(str(success))
            else:
                print("Unspport Websocket Request Type")
        except websockets.ConnectionClosedOK:
            pass
        
       
async def main(argv=sys.argv):
    rclpy.init(args=sys.argv)
    args_without_ros = rclpy.utilities.remove_ros_args(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('-su', '--server_url',
                          type=str, nargs='+',
                            help="Websocket server address")
    parser.add_argument('-sp', '--server_port',
                            type=int, nargs='+',
                            help="Websocket server port")
    args = parser.parse_args(args_without_ros[1:])

    server_url = args.server_url[0]
    server_port = args.server_port[0]

    async with websockets.serve(Server,server_url,server_port):
    # async with websockets.serve(Server,"localhost", 8765):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main(sys.argv))
