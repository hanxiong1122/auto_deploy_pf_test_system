import boto3
import botocore
import paramiko

# key = paramiko.RSAKey.from_private_key_file("yintech.pem")
# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# instances_ip = ["54.161.211.36","52.90.137.110"]

# for instance_ip in instances_ip:
# 	# Connect/ssh to an instance
# 	try:
# 	    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
# 	    client.connect(hostname=instance_ip, username="ubuntu", pkey=key)

# 	    # Execute a command(cmd) after connecting/ssh to an instance
# 	    stdin, stdout, stderr = client.exec_command("touch ~/helloWorld.txt")
# 	    print(stdout.read())
# 	    # close the client connection once the job is done
# 	    client.close()

# 	except Exception as e:
# 	    print(e)

cmd_list = ["touch ~/helloWorld.txt","touch ~/helloWorld1.txt"]
class ssh_worker(object):
	def __init__(self, key_path, instance_ip, cmd_list, username = "ubuntu"):
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
	
	def close_connection(self):
		self.client.close()

if __name__=="__main__":
	instances_ip = ["54.161.211.36","52.90.137.110"]
	print(cmd_list)
	for instance_ip in instances_ip:
		worker = ssh_worker(key_path = "yintech.pem", 
							instance_ip = instance_ip, 
							cmd_list = cmd_list)
		worker.establish_connect()
		worker.run_cmd()
		worker.close_connection()

