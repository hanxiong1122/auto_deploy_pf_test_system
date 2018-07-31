import boto3
import time

# def create_instance()

class create_ec2_instances(object):
	def __init__(self, ImageId = 'ami-d87877a7', MaxCount = 1, MinCount = 1, InstanceType = 't2.micro', time_out = 30):
		self.ec2 = boto3.resource('ec2')
		self.ImageId = ImageId
		self.MaxCount = MaxCount
		self.MinCount = MinCount
		self.InstanceType = InstanceType
		self.time_out = time_out
		self.public_ip_address_list, self.id_list = self.create_running_instance()

	def create_running_instance(self):
		instances = self.ec2.create_instances(ImageId = self.ImageId,
												MinCount = self.MinCount,
												MaxCount = self.MaxCount,
												InstanceType= self.InstanceType)

		running_instance_num = 0
		id_list = [ins.id for ins in instances]
		created_instance_num = len(id_list)
		print("created ", created_instance_num," instances ids, they are ", id_list)

		# a collection of instances with id_list
		instance_collection = self.ec2.instances.filter(InstanceIds = id_list)
		# filter criterion, need find running instance
		filter = [{'Name': 'instance-state-name', 'Values': ['running']}]

		start_time = time.time()
		while (running_instance_num != created_instance_num): 
			filtered_collection = instance_collection.filter(Filters = filter)
			filtered_instances = [_ for _ in filtered_collection]
			running_instance_num = len(filtered_instances)
			print("running_instance_num is ", running_instance_num)
			time.sleep(5)
			end_time = time.time()
			if ((end_time - start_time) > self.time_out * 5): 
				break

		print("We created ", running_instance_num, "running instances")

		for instance in filtered_instances:
			print(instance.id, "public_ip_address is ", instance.public_ip_address)
		return [instance.public_ip_address for instance in filtered_instances], [instance.id for instance in filtered_instances]

	def terminate(self):
		if (self.id_list == []):
			print("no ec2 instance to be terminated")
			return

		for instance_id in self.id_list:
			instance = self.ec2.Instance(instance_id)
			response = instance.terminate()
			print(response)
		self.id_list = []
		print("close all created running instance")
		return

if __name__=="__main__":
	ImageId = 'ami-d87877a7'
	instances = create_ec2_instances(ImageId = ImageId, MaxCount = 1, MinCount = 1)
	# time.sleep(10)
	# print("now we close all running instance")
	# instances.terminate()

