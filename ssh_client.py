import paramiko
import os

host = 'ec2-13-48-1-143.eu-north-1.compute.amazonaws.com'
user = 'new_user'
secret = '123456'
port = 22
file_name='minecraft.db'
path = os.path.dirname(os.path.abspath(__file__))+'/'

def send():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=secret, port=port)
        ftp_client = client.open_sftp()
        ftp_client.put(path+file_name,file_name)
        ftp_client.close()
        client.close()
    except Exception as e:
        get()

def get():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    ftp_client = client.open_sftp()

    ftp_client.get(file_name,path+file_name)
    ftp_client.close()
    client.close()

if __name__ == '__main__':
    get()
