#!bin/bash
import os
import time
import argparse
from create_ec2_instance import create_ec2_instances
from ssh_worker import ssh_worker
from utils.utils import load_cmdconfig, load_instances_ip, load_aws_config
from s3_service import s3_service

bucket_name = "hanxiong"
instances_number = 4


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='provide ImageId to be created')
	parser.add_argument('--ImageId', '-i', help='give ImageId', required = True)
	args = vars(parser.parse_args())

	if os.path.exists("./tmp/instances_info.json"):
		os.remove("./tmp/instances_info.json")
	

	## upload tasksconfig.json to s3
	s3 = s3_service()
	if s3.put_file(bucket_name = bucket_name, path = "./config/tasksconfig.json", key = "tasksconfig.json"):
		print("successfully upload tasksconfig.json to s3")
	else:
		print("fail to upload tasksconfig.json to s3")
		raise
	

	ImageId = args['ImageId']
	### create n instances
	# aws_config = load_aws_config()
	# instances = create_ec2_instances(aws_access_key_id = aws_config["aws_access_key_id"],
	# 								aws_secret_access_key = aws_config["aws_secret_access_key"],
	# 								region_name = aws_config["region_name"],
	# 								ImageId = ImageId, 
	# 								MaxCount = 2, 
	# 								MinCount = 1, 
	# 								InstanceType = 'm4.xlarge')


	user_data = '''#!/bin/bash
				cd /home/ubuntu/yintech/ddpg_model/model/src
				chmod a+x aws_task_run.py
				chmod a+x aws_test_run.py
				sudo -u ubuntu ./aws_task_run.py
				'''	
	for i in range(instances_number):
		try:
			instances = create_ec2_instances(ImageId = ImageId, 
											MaxCount = 1, 
											MinCount = 1, 
											InstanceType = 'm4.xlarge',
											user_data = user_data)
			time.sleep(5)
		except Exception as error:
			print(error)
		# print(instances.get_instance_public_ip())
		# print(instances.get_instance_id())

























	### start tasks, using ssh to control the behaviour ###
	# instances_ip = load_instances_ip()
	# cmd_list = load_cmdconfig()
	# for i, ins_ip in enumerate(instances_ip):
	# 	time.sleep(5)
	# 	for j in range(3):
	# 		try:
	# 			time.sleep(2)
	# 			worker = ssh_worker(key_path = "yintech.pem", 
	# 								instance_ip = ins_ip, 
	# 								cmd_list = cmd_list)
	# 			worker.establish_connect()
	# 			worker.run_cmd()
	# 			print("run the ", i, "th task")
	# 			worker.close_connection()
	# 			break
	# 		except Exception as error:
	# 			print("error happens at ", j, "th try on instance ", ins_ip)






























### download list file from s3

### assign tasks to n instance

# instances_ip = load_instances_ip()
# cmd_list = load_cmdconfig()
# for i, ins_ip in enumerate(instances_ip):
# 	worker = ssh_worker(key_path = "yintech.pem", 
# 						instance_ip = ins_ip, 
# 						cmd_list = cmd_list)
# 	worker.establish_connect()
# 	print("run the ", i, "th cmd")
# 	worker.run_cmd()
# 	worker.close_connection()

# running_task_num = len(instances_ip)
# while running_task_num:
# 	for i, ins_ip in enumerate(instances_ip):
# 		worker = ssh_worker(key_path = "yintech.pem", 
# 							instance_ip = ins_ip, 
# 							cmd_list = cmd_list)
# 		worker.establish_connect()
# 		status = worker.run_single_cmd("ps -A | grep -v grep | grep aws_test_run.py")
# 		if not worker.run_single_cmd("ps -A | grep -v grep | grep aws_test_run.py"):
# 			print("finish work on ", i)
# 			running_task_num -= 1
# 		else:
# 			print("on ", i, " ", status)
# 		worker.close_connection()
# 		print("running_task_num is ", running_task_num)
# 	time.sleep(5)
# print("finish all the works")




### finish works and saves all tasks to s3