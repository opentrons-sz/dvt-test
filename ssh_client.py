"""
@description: ssh 登录远程服务器 driver
@author: andy-hu
@date: 20230404
"""
import os.path
import paramiko
from paramiko import SSHClient
from typing import List, Callable, Union

SSH_TIMEOUT = 60
multi_cmd: Callable[[List[str]], str] = lambda x: "\n ".join(x)


class SSH(SSHClient):
    def __init__(self, ip: str, port=22, user_name="root", pwd="None"):
        super().__init__()
        self.host_name = ip
        self.port = port
        self.user_name = user_name
        self.password = pwd
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.transport = None
        self.ftp = None

    def login(self):
        """
        login
        :return:
        """
        try:
            self.client.connect(hostname=self.host_name, port=self.port, username=self.user_name, password=self.password)
        except TimeoutError as e:
            print("connect timeout...", e)

    def write_cmd(self, cmd: str) -> str:
        """
        write cmd, 一次性发送一个指令
        :param cmd:
        :return: read result
        """
        std_in, std_out, std_err = self.client.exec_command(cmd, bufsize=-1)
        code = std_out.channel.recv_exit_status()
        return std_out.read().decode('utf-8')

    def line_buffered(self, f):
        line_buf = ""
        while not f.channel.exit_status_ready():
            line_buf += f.read(1)
            if line_buf.endswith('\
    '):
                yield line_buf
                line_buf = ''

    def run(self, command):
        stdin, stdout, stderr = self.client.exec_command(command, bufsize=1)
        for l in self.line_buffered(stdout):
            print(l)

        return stdin, stdout, stderr

    def close_ssh(self):
        """
        close client connect
        :return:
        """
        self.client.close()

    def init_ftp(self) -> None:
        """
        初始化ftp登录连接
        :return:
        """
        if self.ftp is not None:
            return
        try:
            self.transport = paramiko.Transport(self.host_name, self.port)
            self.transport.connect(username=self.user_name, password=self.password)
            self.ftp = paramiko.SFTPClient.from_transport(self.transport)
        except ConnectionError as e:
            print(e)

    def ftp_put_file(self, local_file_name: str, target_file_name: str):
        """
        将本地文件推到服务器
        :param local_file_name:
        :param target_file_name:
        :return:
        """
        if self.ftp is not None:
            self.ftp.put(local_file_name, target_file_name)

    def ftp_get_file(self, target_file_name: str, local_file_name: str):
        """
        下载远程服务器文件
        :param target_file_name:
        :param local_file_name:
        :return:
        """
        if self.ftp is not None:
            self.ftp.get(target_file_name, local_file_name)

    def ftp_get_multi_files(self, target_path: str, local_path: str):
        """
        下载文件夹所有文件
        :param target_path:
        :param local_path:
        :return:
        """
        files = self.ftp_list_file(target_path)
        for file in files:
            print(f"downloading...{os.path.join(target_path, file)}")
            try:
                self.ftp_get_file(os.path.join(target_path, file), os.path.join(local_path, file))
                print("succeed!")
            except FileNotFoundError as e:
                print(e)

    def ftp_cd(self, target_path: str) -> Union[str, None]:
        """
        cd 服务器路径
        :param target_path:
        :return:
        """
        if self.ftp is None:
            return None
        else:
            self.ftp.chidr(target_path)
            return self.ftp.getcwd()

    def ftp_list_file(self, target_path: str) -> Union[List, None]:
        """
        list 出当前路径文件
        :return:
        """
        if self.ftp is None:
            return None
        files: List = self.ftp.listdir(target_path)
        return files

    def ftp_remove_dir(self, target_path: str):
        """
        删除目录
        :param target_path:
        :return:
        """
        if self.ftp is None:
            return
        self.ftp.rmdir(target_path)

    def ftp_remove_file(self, target_file: str):
        """
        rm file
        :param target_file:
        :return:
        """
        if self.ftp is None:
            return
        self.ftp.remove(target_file)

    def close_ftp(self):
        """
        关闭ftp
        :return:
        """
        if self.transport is None:
            return
        self.transport.close()
        self.transport = None
        self.ftp = None


if __name__ == '__main__':
    s_obj = SSH("192.168.6.100")
    s_obj.login()
    s_obj.write_cmd("df -h")

