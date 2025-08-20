#!/usr/bin/env python3
"""
验证 init_files 设置是否正确
"""

import os
import sys
sys.path.insert(0, '/home/x/anaconda3/envs/openvla-oft/LIBERO')

from libero.libero.benchmark import get_benchmark

def verify_init_files():
    print("🔍 验证 init_files 设置...")
    
    # 测试 libero_goal_new
    print("\n📋 检查 libero_goal_new:")
    try:
        benchmark_class = get_benchmark("libero_goal_new")
        benchmark = benchmark_class()
        
        for i, task_name in enumerate(benchmark.get_task_names()):
            bddl_file_path = benchmark.get_task_bddl_file_path(i)
            task = benchmark.get_task(i)
            
            # 构建 init_states 路径
            from libero.libero.utils import get_libero_path
            init_states_path = os.path.join(
                get_libero_path("init_states"),
                task.problem_folder,
                task.init_states_file,
            )
            
            exists = os.path.exists(init_states_path)
            status = "✅" if exists else "❌"
            print(f"  {status} Task {i+1}: {task_name}")
            print(f"     Init file: {task.init_states_file}")
            print(f"     Path: {init_states_path}")
            print(f"     Exists: {exists}")
            
            if not exists:
                print(f"     Expected path: {init_states_path}")
        
        print(f"\n✅ libero_goal_new benchmark 验证完成")
        
    except Exception as e:
        print(f"❌ libero_goal_new 验证失败: {e}")
    
    # 测试 libero_spatial_orange
    print("\n📋 检查 libero_spatial_orange:")
    try:
        benchmark_class = get_benchmark("libero_spatial_orange")
        benchmark = benchmark_class()
        
        missing_files = []
        for i, task_name in enumerate(benchmark.get_task_names()[:3]):  # 只检查前3个
            task = benchmark.get_task(i)
            
            from libero.libero.utils import get_libero_path
            init_states_path = os.path.join(
                get_libero_path("init_states"),
                task.problem_folder,
                task.init_states_file,
            )
            
            exists = os.path.exists(init_states_path)
            status = "✅" if exists else "❌"
            print(f"  {status} Task {i+1}: {task_name}")
            print(f"     Init file: {task.init_states_file}")
            print(f"     Exists: {exists}")
            
            if not exists:
                missing_files.append(init_states_path)
        
        if missing_files:
            print(f"\n❌ 缺少 {len(missing_files)} 个文件")
        else:
            print(f"\n✅ libero_spatial_orange benchmark 验证完成")
        
    except Exception as e:
        print(f"❌ libero_spatial_orange 验证失败: {e}")

if __name__ == "__main__":
    verify_init_files()
