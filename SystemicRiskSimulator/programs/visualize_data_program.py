from SystemicRiskSimulator.external_packages import sys, pickle, base64
from SystemicRiskSimulator.core.functions.fun_visualize_data import visualize_data_program


def main():
    # 从命令行参数获取配置字典
    sgv_base64 = sys.argv[1]
    sgv_pkl = base64.b64decode(sgv_base64)
    sgv = pickle.loads(sgv_pkl)
    # config_json = sys.argv[1]
    # sgv = json.loads(config_json)

    # 调用函数
    visualize_data_program(sgv)

    # #DEBUG
    # print(np.random.rand(5))
    # print('模拟器版本号：' + sgv['simulator_version'])
    # print("测试运行可视化数据程序！已经运行！")


if __name__ == '__main__':
    main()
