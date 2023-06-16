import os.path
import time
import subprocess
import paramiko

pull_config = {
    "idx1": ["下载数据: robot_diagnostic", "pull_data", "/data/testing_data/robot_assembly_qc_ot3"],
    "idx2": ["下载数据且删除: robot_diagnostic", "pull_data_del", "/data/testing_data/robot_assembly_qc_ot3"],
    "idx3": ["删除数据: robot_diagnostic", "del_data", "/data/testing_data/robot_assembly_qc_ot3"],
    "idx4": ["下载数据: pipette_lifetime", "pull_data", "/opt/test"],
    "idx5": ["下载数据且删除: pipette_lifetime", "pull_data_del", "/data/testing_data/tip-pick-up-lifetime-test"],
    "idx6": ["删除数据: pipette_lifetime", "del_data", "/data/testing_data/tip-pick-up-lifetime-test"],
    "idx7": ["下载数据: gripper_diagnostic", "pull_data", "/data/testing_data/gripper-assembly-qc-ot3"],
    "idx8": ["下载数据且删除: gripper_diagnostic", "pull_data_del", "/data/testing_data/gripper-assembly-qc-ot3"],
    "idx9": ["删除数据: gripper_diagnostic", "del_data", "/data/testing_data/gripper-assembly-qc-ot3"]
}

password = "None"


class PullData:

    def __init__(self, ip, clear_flag, pull_flag):
        self.clear_flag = clear_flag
        self.pull_flag = pull_flag
        self.ip = ip
        self.data_path = './'
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def init_data_path(self):
        """
        初始化保存路径
        :return:
        """
        save_path = "DVT_TEST_DATA"
        time_str = time.strftime("%Y%m%d")
        save_path = save_path + " - " + time_str
        if os.path.exists(save_path):
            pass
        else:
            os.mkdir(save_path)
        self.data_path = save_path
        return save_path

    def connect(self):
        """
        connect ip and create obj
        :return:
        """
        try:
            ssh_cmd = f"ssh-keygen -R {self.ip}"
            subprocess.getoutput(ssh_cmd)
            self.client.connect(hostname=self.ip, username="root", password=password, timeout=60)
            print("connected!!")
            return True
        except Exception as e:
            print("unreached ip", e)
            return False

    def scp_file(self, ip, target_path, save_path, user_name="root", password=password):
        """
        scp
        :param ip:
        :param target_path:
        :param save_path:
        :param user_name:
        :param password:
        :return:
        """
        time_str = time.strftime("%Y%m%d-%H-%M-%S")
        save_path = save_path + '/' + f"pull_data-{time_str}"
        scp_cmd = f"scp -r \"{user_name}@{ip}:{target_path}\" \"{save_path}\""
        if password is None or password == "None":
            res = subprocess.getoutput(scp_cmd)
            print(res)
        else:
            pass

    def rm_file(self, target):
        """
        rm
        :param target:
        :return:
        """
        cmd = f"rm -rf {target}"
        std_in, std_out, std_err = self.client.exec_command(cmd, bufsize=-1)
        print(std_out.read().decode('utf-8'))

    def run(self, target_path):
        self.init_data_path()

        if self.pull_flag:
            print("开始拉取文件...")
            try:
                self.scp_file(self.ip, target_path, self.data_path)
                print("download -> " + self.data_path)
            except ConnectionError as e:
                print(e)
        if self.clear_flag:
            # login
            res = self.connect()
            if not res:
                return
            confirm_del = input(f"delete {target_path} ?(y/n)")
            if confirm_del.upper() == "Y":
                # 删除文件
                try:
                    print("开始清除文件...")
                    self.rm_file(target_path + "/*")
                except Exception as e:
                    print("清除文件失败...")
                    print(e)
        print("操作成功...")
