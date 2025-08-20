#!/usr/bin/env python3

import sys
import os

# Add LIBERO path
sys.path.append('./LIBERO')

def debug_env_creation():
    """调试环境创建过程"""
    try:
        # 先测试一个原始的 libero_goal 任务
        print("=== Testing Original libero_goal ===")
        from libero.libero.benchmark import get_benchmark
        
        benchmark_class = get_benchmark('libero_goal')
        benchmark_original = benchmark_class()
        
        # 获取原始任务的 BDDL 文件
        original_task_file = benchmark_original.get_task_bddl_file_path(1)  # put_the_bowl_on_the_stove
        print(f"Original task file: {original_task_file}")
        
        # 尝试创建原始环境
        from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation
        
        try:
            env_original = Libero_Tabletop_Manipulation(
                bddl_file_name=original_task_file,
                robots=['Panda'],
                has_renderer=False,
                has_offscreen_renderer=False,
                horizon=200,
                control_freq=20,
                hard_reset=False,
            )
            print("✓ Original environment created successfully")
            env_original.close()
        except Exception as e:
            print(f"✗ Original environment creation failed: {e}")
            return False
        
        # 现在测试新的环境
        print("\n=== Testing New libero_goal_new ===")
        benchmark_class = get_benchmark('libero_goal_new')
        benchmark_new = benchmark_class()
        
        new_task_file = benchmark_new.get_task_bddl_file_path(1)
        print(f"New task file: {new_task_file}")
        
        try:
            env_new = Libero_Tabletop_Manipulation(
                bddl_file_name=new_task_file,
                robots=['Panda'],
                has_renderer=False,
                has_offscreen_renderer=False,
                horizon=200,
                control_freq=20,
                hard_reset=False,
            )
            print("✓ New environment created successfully")
            env_new.close()
            return True
        except Exception as e:
            print(f"✗ New environment creation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"✗ General error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_env_creation()
