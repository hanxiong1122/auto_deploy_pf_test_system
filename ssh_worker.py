import boto3
import botocore
import paramiko

from utils.utils import load_cmdconfig, load_instances_ip

# key = paramiko.RSAKey.from_private_key_file("yintech.pem")
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# instances_ip = ["54.147.245.101","52.91.227.23"]


# cmd = "cd /home/ubuntu/yintech/ddpg_model/model/src;chmod a+x aws_test_run.py; ./aws_test_run.py 1>&2 &"
# for i,instance_ip in enumerate(instances_ip):
# 	# Connect/ssh to an instance
# 	try:
# 	    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
# 	    client.connect(hostname=instance_ip, username="ubuntu", pkey=key)

# 	    # Execute a command(cmd) after connecting/ssh to an instance
# 	    print("Execute command on ", i, "th machine")
# 	    stdin, stdout, stderr = client.exec_command(cmd)


# 	    # close the client connection once the job is done
# 	    client.close()

# 	except Exception as e:
# 	    print(e)

# cmd_list = ["touch ~/helloWorld.txt","touch ~/helloWorld1.txt"]




class ssh_worker(object):
	def __init__(self, key_path, instance_ip, cmd_list = None, username = "ubuntu"):
		self.key = paramiko.RSAKey.from_private_key_file(key_path)
		self.instance_ip = instance_ip
		self.cmd_list = cmd_list
		self.username = username
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	def establish_connect(self):
		try:
			self.client.connect(hostname = self.instance_ip, username = self.username, pkey = self.key)
		except Exception as e:
			print(e)

	def run_cmd(self):
		for cmd in self.cmd_list:
			stdin, stdout, stderr = self.client.exec_command(cmd)
	
	def run_single_cmd(self, cmd):
		stdin, stdout, stderr = self.client.exec_command(cmd)
		stdout.channel.recv_exit_status()
		return stdout.readlines()
	
	def close_connection(self):
		self.client.close()




if __name__=="__main__":
	instances_ip = load_instances_ip()
	cmd_list = load_cmdconfig()
	for i, instance_ip in enumerate(instances_ip):
		worker = ssh_worker(key_path = "yintech.pem", 
							instance_ip = instance_ip, 
							cmd_list = cmd_list)
		worker.establish_connect()
		print("run the ", i, "th cmd")
		worker.run_cmd()
		worker.close_connection()

