"""
检查银行名称和ID是否在数据表中的示例用法
"""

import pandas as pd
import numpy as np
from SystemicRiskSimulator.tools.data_tools import check_bank_names_in_list, check_bank_id_in_list


def example_check_bank_functions():
    """
    演示如何使用 check_bank_names_in_list 和 check_bank_id_in_list 函数
    """
    
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
    print("\n" + "="*50 + "\n")
    
    # 使用自定义列名的示例
    # 假设我们有一个不同的数据结构
    custom_data = {
        'bank_code': ['ICBC', 'CCB', 'ABC'],
        'bank_name': ['工商银行', '建设银行', '农业银行'],
        'assets': [1000000, 900000, 800000]
    }
    
    df_custom = pd.DataFrame(custom_data)
    
    print("自定义数据表:")
    print(df_custom)
    print("\n" + "="*50 + "\n")
    
    # 使用自定义列名进行检查
    result_custom_names = check_bank_names_in_list(
        ['工商银行', '招商银行'], 
        df_custom, 
        name_column='bank_name'
    )
    
    print("使用自定义列名检查银行名称结果:")
    print(f"找到的银行名称: {result_custom_names['found']}")
    print(f"未找到的银行名称: {result_custom_names['not_found']}")
    print(f"是否全部找到: {result_custom_names['all_found']}")
    
    result_custom_ids = check_bank_id_in_list(
        ['ICBC', 'CMB'], 
        df_custom, 
        id_column='bank_code'
    )
    
    print("\n使用自定义列名检查银行ID结果:")
    print(f"找到的银行ID: {result_custom_ids['found']}")
    print(f"未找到的银行ID: {result_custom_ids['not_found']}")
    print(f"是否全部找到: {result_custom_ids['all_found']}")


if __name__ == '__main__':
    example_check_bank_functions()