#!/usr/bin/env python3

import sys
import os

# Add LIBERO path
sys.path.append('./LIBERO')

def test_bddl_parsing():
    """测试 BDDL 文件解析"""
    try:
        from libero.libero.benchmark import get_benchmark
        from bddl import get_parsed_problem
        
        # 获取 benchmark 实例
        benchmark_class = get_benchmark('libero_goal_new')
        benchmark = benchmark_class()
        
        # 获取第一个任务的 BDDL 文件路径
        task_bddl_file = benchmark.get_task_bddl_file_path(0)
        print(f"Task BDDL file: {task_bddl_file}")
        
        # 尝试解析 BDDL 文件
        parsed_problem = get_parsed_problem(task_bddl_file)
        print("✓ BDDL file parsed successfully")
        
        # 检查解析后的 fixtures
        print("Fixtures:", parsed_problem['fixtures'])
        print("Objects:", parsed_problem['objects'])
        
        return True
        
    except Exception as e:
        print(f"Error parsing BDDL: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_bddl_parsing()
