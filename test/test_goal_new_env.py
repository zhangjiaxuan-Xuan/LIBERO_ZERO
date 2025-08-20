#!/usr/bin/env python3

import sys
import os

# Add LIBERO path
sys.path.append('./LIBERO')

def test_benchmark_registration():
    """测试新环境是否正确注册"""
    print("=== Testing Benchmark Registration ===")
    try:
        from libero.libero.benchmark import get_benchmark_dict, get_benchmark
        
        # 获取所有可用的 benchmark
        benchmark_dict = get_benchmark_dict()
        print(f"Available benchmarks: {list(benchmark_dict.keys())}")
        
        # 检查新环境是否注册
        if 'libero_goal_new' in benchmark_dict:
            print("✓ LIBERO_GOAL_NEW benchmark successfully registered!")
            
            # 尝试创建 benchmark 实例
            benchmark_class = get_benchmark('libero_goal_new')
            benchmark = benchmark_class()
            
            print(f"✓ Benchmark created successfully with {benchmark.get_num_tasks()} tasks")
            print(f"Task names: {benchmark.get_task_names()}")
            
            return benchmark
        else:
            print("✗ LIBERO_GOAL_NEW benchmark not found in registry")
            return None
            
    except Exception as e:
        print(f"✗ Error testing benchmark registration: {e}")
        return None

def test_object_registration():
    """测试对象注册是否正确"""
    print("\n=== Testing Object Registration ===")
    try:
        from libero.libero.envs.objects.turbosquid_objects import BlueBottle
        from libero.libero.envs.objects.articulated_objects import WhiteCabinet
        from libero.libero.envs.objects.google_scanned_objects import WhiteBowl
        
        # 测试创建对象实例
        blue_bottle = BlueBottle()
        white_cabinet = WhiteCabinet()
        white_bowl = WhiteBowl()
        
        print("✓ BlueBottle object created successfully")
        print("✓ WhiteCabinet object created successfully") 
        print("✓ WhiteBowl object created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing object registration: {e}")
        return False

def test_environment_creation():
    """测试环境创建"""
    print("\n=== Testing Environment Creation ===")
    try:
        from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation
        from libero.libero.benchmark import get_benchmark
        
        # 获取 benchmark 实例
        benchmark_class = get_benchmark('libero_goal_new')
        benchmark = benchmark_class()
        
        # 获取第一个任务的 BDDL 文件路径
        task_bddl_file = benchmark.get_task_bddl_file_path(0)
        print(f"Task BDDL file: {task_bddl_file}")
        
        # 创建环境
        env = Libero_Tabletop_Manipulation(
            bddl_file_name=task_bddl_file,
            robots=['FETCH'],  # 使用 FETCH 机器人
            has_renderer=False,  # 不渲染以避免 GUI 问题
            has_offscreen_renderer=False,
            render_camera="frontview",
            horizon=200,
            control_freq=20,
        )
        print("✓ Environment created successfully")
        
        # 获取观察空间信息
        obs = env.reset()
        print(f"✓ Environment reset successful")
        print(f"Observation keys: {list(obs.keys())}")
        
        # 测试一个简单的动作
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        print(f"✓ Environment step successful")
        print(f"Reward: {reward}, Done: {done}")
        
        env.close()
        return True
        
    except Exception as e:
        print(f"✗ Error testing environment creation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Testing LIBERO_GOAL_NEW Environment Setup")
    print("=" * 50)
    
    # 测试 benchmark 注册
    benchmark = test_benchmark_registration()
    if not benchmark:
        print("❌ Benchmark registration failed, stopping tests")
        return
    
    # 测试对象注册
    objects_ok = test_object_registration()
    if not objects_ok:
        print("❌ Object registration failed, stopping tests")
        return
    
    # 测试环境创建
    env_ok = test_environment_creation()
    
    if env_ok:
        print("\n🎉 All tests passed! LIBERO_GOAL_NEW environment is ready to use!")
        print("\nExample usage:")
        print('import libero.libero as libero')
        print('env = libero.make("libero_goal_new", task_id=0)')
        print('obs = env.reset()')
    else:
        print("\n❌ Some tests failed")

if __name__ == "__main__":
    main()
