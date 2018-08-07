import boto3
import os
import shutil



class s3_service(object):
	def __init__(self, 
				aws_access_key_id = None, 
				aws_secret_access_key = None, 
				region_name = None):
		try: 
			if not aws_access_key_id and not aws_secret_access_key and not region_name:
				self.session = boto3.Session(aws_access_key_id = aws_access_key_id,
											  aws_secret_access_key = aws_secret_access_key,
											  region_name = region_name)
			else:
				self.session = boto3.Session()
			self.s3 = self.session.resource('s3')
		except Exception as error:
			print("can not connect to s3")
			raise

	def show_s3_list(self):
		for bucket in self.s3.buckets.all():
			print(bucket.name)
			print("---")
			for item in bucket.objects.all():
				print("\t", item.key)

	def create_bucket(self, bucket_name):
		try:
			response = self.s3.create_bucket(Bucket = bucket_name)
			print(response)
		except Exception as error:
			print(error)

	def put_file(self, bucket_name, path, key):
		try:
			bucket = self.s3.Bucket(bucket_name)
			with open(path, 'rb') as data:
				bucket.put_object(Key = key, Body = data)
		except Exception as error:
			print(error)

	def uploadDirectory(self, bucket_name, path):
		bucket = self.s3.Bucket(bucket_name)
		for subdir, dirs, files in os.walk(path):
			for file in files:
				full_path = os.path.join(subdir, file)
				print(full_path)
				with open(full_path, 'rb') as data:
						bucket.put_object(Key=full_path[len(path)+1:], Body=data)

	def download_and_del_file(self, bucket_name, key, filename):
		try:
			self.s3.Bucket(bucket_name).download_file(key, filename)
			self.s3.Object(bucket_name, key).delete()
			print("successfully download and delete file in s3")
			return True
		except Exception as error:
			print(error)
			return False


class s3_service(object):
	def __init__(self):
		self.s3 = boto3.resource('s3')

	def show_s3_list(self):
		for bucket in self.s3.buckets.all():
			print(bucket.name)
			print("---")
			for item in bucket.objects.all():
				print("\t", item.key)

	def create_bucket(self, bucket_name):
		try:
			response = self.s3.create_bucket(Bucket = bucket_name)
			print(response)
		except Exception as error:
			print(error)

	def put_file(self, bucket_name, object_name):
		try:
			response = self.s3.objects(bucket_name, object_name).put(Body = open(object_name, 'rb'))
			print(response)
		except Exception as error:
			print(error)

	def uploadDirectory(self, bucket_name, path):
		bucket = self.s3.Bucket(bucket_name)
		for subdir, dirs, files in os.walk(path):
			for file in files:
				full_path = os.path.join(subdir, file)
				print(full_path)
				with open(full_path, 'rb') as data:
						bucket.put_object(Key=full_path[len(path)+1:], Body=data)



