"""
@description: for dvt test
@auth: andy-hu
@date: 20230615
"""
from pull_data import pull_config
from pull_data import PullData


class TestTools:
    def __init__(self):
        self.robot_ip = None

    def get_input_menu1(self):
        get_input = input("type 1 pull data(输入1开始拉取数据)\n"
                          "type 2 to jog(输入2开始移动robot)\n"
                          "type 3 to require firmware(输入3开始查询firmware)\n"
                          ">")
        self.menu1_handel(get_input)

    def pull_data_menu(self):
        for k, v in pull_config.items():
            print(f"type {k[3]} to {v[0]}")
        get_input = input(">")
        return get_input

    def pull_data_handel(self, pull_description, pull_tag, pull_target):
        """
        pull data
        :param pull_description:
        :param pull_tag:
        :param pull_target:
        :return:
        """
        print("start " + pull_description)
        if pull_tag == "pull_data":
            clear_flag = False
            pull_flag = True
        elif pull_tag == "pull_data_del":
            clear_flag = True
            pull_flag = True
        elif pull_tag == "del_data":
            clear_flag = True
            pull_flag = False
        else:
            raise ValueError("PULL DATA ERR")
        pull = PullData(self.robot_ip, clear_flag, pull_flag)
        pull.run(pull_target)

    def menu1_handel(self, menu1_answer: str):
        """
        一级菜单
        :param menu1_answer:
        :return:
        """
        if menu1_answer == "1":
            pull_data_selection = self.pull_data_menu()
            target = pull_config[f"idx{pull_data_selection}"]
            pull_description = target[0]
            pull_tag = target[1]
            pull_target = target[2]
            self.pull_data_handel(pull_description, pull_tag, pull_target)
        elif menu1_answer == "2":
            pass
        elif menu1_answer == "3":
            pass
        else:
            print("Press Err")

    def get_robot_ip(self):
        get_ip = input("=====================\n"
                       "DVT Robot Test\n\n"
                       "robot ip(输入ip)\n"
                       ">")
        self.robot_ip = get_ip.strip()
        return get_ip

    def test_loop(self):
        self.get_robot_ip()
        self.get_input_menu1()
        return input("press any key to continue, press 'q' quit (q键退出，其它按键继续...)\n"
                     ">")


if __name__ == '__main__':
    t = TestTools()
    while True:
        ret = t.test_loop()
        if ret.upper() == 'Q':
            break
