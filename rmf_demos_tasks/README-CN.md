# Task
增加对pickup和dropoff两种脚本的支持  
添加了运行脚本的入口点  
增加了全场景，机器人对pickup和dropoff任务的支持  
增加了fleet adapters task_capabilities pickup和dropoff

增加了PICKUP和DROPOFF的task type
增加了PICKUP和DROPOFF的msg 

增加了rmf panel对pickup和dropoff的支持

增加pickup和dropoff topic

TODO: FleetUpdateHandle增加解析pickup

TODO:rmf_panel 添加对 pickup和dropoff的支持

# 测试命令

## Test pickup
```bash
# 测试pickup一个东西
ros2 run rmf_demos_tasks dispatch_pickup -p pantry -ph coke_dispenser --use_sim_time

# 测试pickup一个东西，并增加取的货物名称和数量
ros2 run rmf_demos_tasks dispatch_pickup -p pantry -ph coke_dispenser -pp code,1 --use_sim_time

# 测试pickup多个东西，并增加取的货物名称和数量
ros2 run rmf_demos_tasks dispatch_pickup -p pantry pantry -ph coke_dispenser coke_dispenser_2 -pp coke,1 coke,1 --use_sim_time

# 测试错误，有pickup信息
ros2 run rmf_demos_tasks dispatch_pickup -p pantry -ph coke_dispenser -d hardware_2 -dh coke_ingestor --use_sim_time

# 测试错误，有pickup信息
ros2 run rmf_demos_tasks dispatch_pickup -p pantry pantry -ph coke_dispenser coke_dispenser_2 -d hardware_2 coe -dh coke_ingestor coke_ingestor_2 -pp coke,1 coke,1 -dp coke,1 coke,1 --use_sim_time
```

## Test Dropoff
```bash
# 测试dropoff一个东西
ros2 run rmf_demos_tasks dispatch_dropoff -d hardware_2 -dh coke_ingestor --use_sim_time

# 测试dropoff一个东西，并增加取的货物名称和数量
ros2 run rmf_demos_tasks dispatch_dropoff -d hardware_2 -dh coke_ingestor -dp code,1 --use_sim_time

# 测试dropoff多个东西，并增加取的货物名称和数量
ros2 run rmf_demos_tasks dispatch_dropoff -d hardware_2 coe -dh coke_ingestor coke_ingestor_2 -dp coke,1 coke,1 --use_sim_time

# 测试错误，有dropoff信息
ros2 run rmf_demos_tasks dispatch_dropoff -p pantry -ph coke_dispenser -d hardware_2 -dh coke_ingestor --use_sim_time

# 测试错误，有dropoff信息
ros2 run rmf_demos_tasks dispatch_dropoff -p pantry pantry -ph coke_dispenser coke_dispenser_2 -d hardware_2 coe -dh coke_ingestor coke_ingestor_2 -pp coke,1 coke,1 -dp coke,1 coke,1 --use_sim_time
```


