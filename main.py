#!bin/bash
import time
import argparse
from create_ec2_instance import create_ec2_instances
from ssh_worker import ssh_worker
from utils.utils import load_cmdconfig, load_instances_ip, load_aws_config


ImageId = 'ami-05fcb5dcc02e13d8c11111111111111'

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='provide ImageId to be created')
	parser.add_argument('--ImageId', '-i', help='give ImageId', required = False)
	args = vars(parser.parse_args())

	if args['ImageId']:
		print(args['ImageId'])
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

	instances = create_ec2_instances(ImageId = ImageId, 
									MaxCount = 4, 
									MinCount = 1, 
									InstanceType = 'm4.xlarge')

	print(instances.get_instance_public_ip())
	print(instances.get_instance_id())

	### start tasks ###
	instances_ip = load_instances_ip()
	cmd_list = load_cmdconfig()
	for i, ins_ip in enumerate(instances_ip):
		time.sleep(2)
		for j in range(3):
			try:
				time.sleep(0.5)
				worker = ssh_worker(key_path = "yintech.pem", 
									instance_ip = ins_ip, 
									cmd_list = cmd_list)
				worker.establish_connect()
				print("run the ", i, "th task")
				worker.run_cmd()
				worker.close_connection()
				break
			except Exception as error:
				print("error happens at ", j, " th try on instance ", ins_ip)






























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