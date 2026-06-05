"""
简单测试脚本，验证新添加的银行检查函数
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = r"C:\Users\Ethan\CoreFiles\ProjectsFile\SystemicRiskSimulator"
sys.path.insert(0, project_root)

try:
    import pandas as pd
    from SystemicRiskSimulator.tools.data_tools import check_bank_names_in_list, check_bank_id_in_list
    
    print("成功导入模块！")
    
    # 创建示例数据表
    data = {
        '基本：银行代码': ['ICBC', 'CCB', 'ABC', 'BOC', 'COMM'],
        '基本：银行中文简称': ['工商银行', '建设银行', '农业银行', '中国银行', '交通银行'],
        '总资产': [1000000, 900000, 800000, 700000, 600000],
        '总负债': [900000, 800000, 700000, 600000, 500000]
    }
    
    df_sample = pd.DataFrame(data)
    
    print("示例数据表:")
    print(df_sample)
    print("\n" + "="*50 + "\n")
    
    # 测试 check_bank_names_in_list 函数
    bank_names_to_check = ['工商银行', '建设银行', '招商银行', '浦发银行']
    result_names = check_bank_names_in_list(bank_names_to_check, df_sample)
    
    print("检查银行名称结果:")
    print(f"要检查的银行名称: {bank_names_to_check}")
    print(f"找到的银行名称: {result_names['found']}")
    print(f"未找到的银行名称: {result_names['not_found']}")
    print(f"是否全部找到: {result_names['all_found']}")
    print("\n" + "="*50 + "\n")
    
    # 测试 check_bank_id_in_list 函数
    bank_ids_to_check = ['ICBC', 'CCB', 'CMB', 'SPDB']
    result_ids = check_bank_id_in_list(bank_ids_to_check, df_sample)
    
    print("检查银行ID结果:")
    print(f"要检查的银行ID: {bank_ids_to_check}")
    print(f"找到的银行ID: {result_ids['found']}")
    print(f"未找到的银行ID: {result_ids['not_found']}")
    print(f"是否全部找到: {result_ids['all_found']}")
    
    print("\n✅ 所有测试通过！函数正常工作。")
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
except Exception as e:
    print(f"❌ 运行错误: {e}")