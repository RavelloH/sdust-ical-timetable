import pandas as pd
import os
import glob

# 查找所有xls文件
xls_files = glob.glob("*.xls") + glob.glob("*.xlsx")
print(f"找到的Excel文件: {xls_files}")

if xls_files:
    # 读取第一个xls文件
    file_path = xls_files[0]
    print(f"\n正在分析文件: {file_path}")
    
    try:
        # 尝试读取所有工作表
        excel_file = pd.ExcelFile(file_path)
        print(f"工作表名称: {excel_file.sheet_names}")
        
        # 读取第一个工作表
        df = pd.read_excel(file_path, sheet_name=0)
        print(f"\n数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        
        print("\n前几行数据:")
        print(df.head(10))
        
        print("\n完整数据:")
        print(df.to_string())
        
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        # 尝试其他编码
        try:
            df = pd.read_excel(file_path, sheet_name=0, engine='xlrd')
            print("\n使用xlrd引擎重新读取:")
            print(df.to_string())
        except Exception as e2:
            print(f"使用xlrd引擎也失败: {e2}")
