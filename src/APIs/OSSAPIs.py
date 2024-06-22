import oss2
from oss2 import ObjectIterator
import os

# TODO 放入环境变量
# 加载 .env 文件
load_dotenv()

access_key_id = os.getenv('ACCESS_KEY_ID')
access_key_secret = os.getenv('ACCESS_KEY_SECRET')
endpoint = os.getenv('ENDPOINT')
bucket_name = 'bucket-feishu'


class OSSManager:
    def __init__(self, access_key_id, access_key_secret, endpoint, bucket_name):
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)

    def upload_file(self, local_file_path, oss_key_prefix):
        """上传本地文件到OSS，文件路径为local_file_path，OSS上的路径前缀为oss_key_prefix"""
        # 获取文件名
        filename = os.path.basename(local_file_path)
        # 完整的OSS对象键（key）
        oss_key = '{}{}'.format(oss_key_prefix, filename)
        # 打开文件并上传
        with open(local_file_path, 'rb') as file:
            result = self.bucket.put_object(oss_key, file)
            print("打开文件并上传的结果：", result)
        return result.status

    def list_files(self, oss_key_prefix):
        """列举OSS上指定前缀的文件"""
        objects = oss2.ObjectIterator(self.bucket, prefix=oss_key_prefix)
        for obj in objects:
            print(obj.key)
# 使用示例
if __name__ == "__main__":
    # 阿里云账号的Access Key ID和Access Key Secret

    # 创建OSSManager实例
    oss_manager = OSSManager(access_key_id, access_key_secret, endpoint, bucket_name)

    # 上传文件的本地路径
    local_file_path = '../../file_v3_00c3_b15c6ace-a38e-4713-9833-ece20cce7ecg.mp4'
    # OSS上的目录前缀
    oss_key_prefix = 'video/'

    # 上传文件
    oss_manager.upload_file(local_file_path, oss_key_prefix)

    # 列举OSS上prefix为'picture/'的文件
    oss_manager.list_files(oss_key_prefix)
