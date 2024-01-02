from SystemicRiskSimulator.external_packages import sys, pickle, base64
from SystemicRiskSimulator.core.functions.fun_visualize_data import visualize_data_program
from SystemicRiskSimulator.core.functions.fun_visualize_data import fun_visualize_data


def main():
    # 从命令行参数获取配置字典
    sgv_base64 = sys.argv[1]
    sgv_pkl = base64.b64decode(sgv_base64)
    sgv = pickle.loads(sgv_pkl)

    fun_visualize_data(sgv)

if __name__ == '__main__':
    main()
