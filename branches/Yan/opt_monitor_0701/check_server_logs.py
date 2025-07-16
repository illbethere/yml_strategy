#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def check_server_status():
    """检查服务器状态"""
    print("=== 检查服务器状态 ===")
    
    try:
        # 检查日志
        response = requests.get('http://localhost:5000/api/logs', timeout=10)
        if response.status_code == 200:
            logs = response.json()
            print(f"服务器日志条数: {len(logs)}")
            print("最新日志:")
            for log in logs[-5:]:  # 显示最后5条日志
                print(f"  {log.get('time', '')}: {log.get('msg', '')}")
        else:
            print("无法获取日志")
            
    except Exception as e:
        print(f"检查服务器状态失败: {e}")

def test_option_data_directly():
    """直接测试期权数据"""
    print("\n=== 直接测试期权数据 ===")
    
    try:
        # 导入服务器模块
        import sys
        sys.path.append('.')
        
        from server_fixed import DataService
        
        # 创建数据服务实例
        ds = DataService()
        
        print(f"期权静态数据行数: {len(ds.option_static_df)}")
        print(f"期权表格数据行数: {len(ds.option_table)}")
        
        if not ds.option_static_df.empty:
            print("期权静态数据示例:")
            print(ds.option_static_df.head())
            
        if not ds.option_table.empty:
            print("期权表格数据示例:")
            print(ds.option_table.head())
        else:
            print("期权表格数据为空")
            
    except Exception as e:
        print(f"直接测试失败: {e}")

def force_update_option():
    """强制更新期权数据"""
    print("\n=== 强制更新期权数据 ===")
    
    try:
        import sys
        sys.path.append('.')
        
        from server_fixed import DataService
        
        ds = DataService()
        
        # 强制调用更新
        ds.update_option()
        
        print(f"更新后期权表格数据行数: {len(ds.option_table)}")
        
        if not ds.option_table.empty:
            print("更新后期权数据示例:")
            print(ds.option_table.head())
            
            # 测试API返回
            df = ds.option_table
            if not df.empty:
                df_sorted = df.sort_values(
                    by=["option_code", "gain_loss"], ascending=[True, False]
                )
                result = df_sorted.to_dict(orient="records")
                print(f"API应返回 {len(result)} 条数据")
                if result:
                    print("第一条数据:")
                    print(json.dumps(result[0], indent=2, ensure_ascii=False))
        else:
            print("更新后期权表格数据仍为空")
            
    except Exception as e:
        print(f"强制更新失败: {e}")

if __name__ == "__main__":
    check_server_status()
    test_option_data_directly()
    force_update_option() 