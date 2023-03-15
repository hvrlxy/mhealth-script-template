import paramiko
from scp import SCPClient
import os
import configparser

class AutoSCP:
    def __init__(self, project_id):
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../'
        self.khoury_id, self.ppk_password, self.hostname = self.get_credentials()
        self.ppk_path = self.ROOT_DIR + 'shh/id_ed25519.ppk'
        self.data_path = os.path.dirname(os.path.abspath(__file__)) + '/../data/raw/'
        self.project_id = project_id
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.hostname,
                            username=self.khoury_id,
                            password=self.ppk_password,
                            key_filename=self.ppk_path)
        
    def get_credentials(self):
        # get the credentials in the config file
        config_path = self.ROOT_DIR + 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_path)
        # get the section server-psw
        credentials = config['server-psw']
        return credentials['USERNAME'], credentials['PASSWORD'], credentials['HOSTNAME']

    def get_logs_watch(self, subject_id, date):
        scp = SCPClient(self.ssh.get_transport())

        # check if the destination folder exists
        if not os.path.exists(f"{self.data_path}{subject_id}@{self.project_id}/logs-watch/"):
            os.makedirs(f"{self.data_path}{subject_id}@{self.project_id}/logs-watch/")

        scp.get(f"/opt/sci_jitai/{subject_id}@{self.project_id}/logs-watch/{date}", 
                f"{self.data_path}{subject_id}@{self.project_id}/logs-watch", 
                recursive=True)

        scp.close()

    def get_logs(self, subject_id, date):
        scp = SCPClient(self.ssh.get_transport())

        # check if the destination folder exists
        if not os.path.exists(f"{self.data_path}{subject_id}@{self.project_id}/logs/"):
            os.makedirs(f"{self.data_path}{subject_id}@{self.project_id}/logs/")

        scp.get(f"/opt/sci_jitai/{subject_id}@{self.project_id}/logs/{date}", 
                f"{self.data_path}{subject_id}@{self.project_id}/logs", 
                recursive=True)
        scp.close()

    def get_data(self, subject_id, date):
        scp = SCPClient(self.ssh.get_transport())

        # check if the destination folder exists
        if not os.path.exists(f"{self.data_path}{subject_id}@{self.project_id}/data/"):
            os.makedirs(f"{self.data_path}{subject_id}@{self.project_id}/data/")

        scp.get(f"/opt/sci_jitai/{subject_id}@{self.project_id}/data/{date}", 
                f"{self.data_path}{subject_id}@{self.project_id}/data", 
                recursive=True)
        scp.close()

    def get_data_watch(self, subject_id, date):
        scp = SCPClient(self.ssh.get_transport())

        # check if the destination folder exists
        if not os.path.exists(f"{self.data_path}{subject_id}@{self.project_id}/data-watch/"):
            os.makedirs(f"{self.data_path}{subject_id}@{self.project_id}/data-watch/")

        scp.get(f"/opt/sci_jitai/{subject_id}@{self.project_id}/data-watch/{date}", 
                f"{self.data_path}{subject_id}@{self.project_id}/data-watch", 
                recursive=True)
        scp.close()
