#!/usr/bin/env python3

import sys
import os

# Add LIBERO path
sys.path.append('./LIBERO')

def test_direct_env():
    """直接测试环境创建"""
    try:
        from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation
        from libero.libero.benchmark import get_benchmark
        
        # 获取 benchmark 实例
        benchmark_class = get_benchmark('libero_goal_new')
        benchmark = benchmark_class()
        
        # 尝试第2个任务（put_the_bowl_on_the_stove），这个任务可能更简单
        task_id = 1
        task_bddl_file = benchmark.get_task_bddl_file_path(task_id)
        print(f"Task BDDL file: {task_bddl_file}")
        print(f"Task name: {benchmark.get_task_names()[task_id]}")
        
        # 检查文件是否存在
        if not os.path.exists(task_bddl_file):
            print(f"✗ BDDL file does not exist: {task_bddl_file}")
            return False
            
        print("✓ BDDL file exists")
        
        # 尝试创建环境
        try:
            env = Libero_Tabletop_Manipulation(
                bddl_file_name=task_bddl_file,
                robots=['Panda'],  # 改用 Panda 机器人
                has_renderer=False,
                has_offscreen_renderer=False,
                horizon=200,
                control_freq=20,
                hard_reset=False,  # 添加这个参数
            )
            print("✓ Environment created successfully")
            
            # 尝试重置环境
            obs = env.reset()
            print("✓ Environment reset successful")
            print(f"Observation keys: {list(obs.keys())}")
            
            env.close()
            return True
            
        except Exception as env_error:
            print(f"✗ Environment creation error: {env_error}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"✗ General error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Direct Environment Creation")
    print("=" * 40)
    test_direct_env()
