#!/usr/bin/env python3
"""
验证 libero_spatial_orange 环境的创建和渲染
"""

import os
import sys
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Dynamically detect repo root and add to sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

def test_orange_environment():
    """测试 libero_spatial_orange 环境"""
    print("🧪 开始测试 libero_spatial_orange 环境...")
    
    try:
        # 导入必要的模块
        from libero.libero.benchmark import get_benchmark
        from libero.libero.envs.env_wrapper import ControlEnv
        
        # 获取 benchmark
        print("📋 获取 benchmark...")
        benchmark = get_benchmark("libero_spatial_orange")()
        task_names = benchmark.get_task_names()
        print(f"✅ 成功获取 {len(task_names)} 个任务")
        
        # 测试前3个任务
        test_tasks = task_names[:3]
        results = []
        
        for i, task_name in enumerate(test_tasks):
            print(f"\n🎯 测试任务 {i+1}: {task_name}")
            
            try:
                # 获取任务 BDDL 文件路径
                bddl_file_path = benchmark.get_task_bddl_file_path(i)
                print(f"✅ 成功获取 BDDL 文件: {bddl_file_path}")
                
                # 创建环境 - 使用 LIBERO 的 ControlEnv
                env = ControlEnv(
                    bddl_file_name=bddl_file_path,
                    robots=["Panda"],
                    controller="OSC_POSE",
                    has_renderer=False,
                    has_offscreen_renderer=True,
                    render_camera="frontview",
                    camera_names=["frontview", "agentview"],
                    camera_heights=512,
                    camera_widths=512,
                    horizon=1000,
                    control_freq=20
                )
                print(f"✅ 成功创建环境")
                
                # 重置环境
                obs = env.reset()
                print(f"✅ 成功重置环境")
                
                # 执行12步
                for step in range(12):
                    action = np.random.uniform(-1, 1, 7)  # Panda机器人7自由度
                    obs, reward, done, info = env.step(action)
                
                # 渲染图片
                img = env.env.sim.render(
                    width=512, 
                    height=512, 
                    camera_name="frontview"
                )
                
                # 翻转180度
                img_flipped = np.rot90(img, 2)
                
                # 保存图片
                img_pil = Image.fromarray(img_flipped)
                output_dir = os.path.join(REPO_ROOT, 'test')
                os.makedirs(output_dir, exist_ok=True)
                safe_name = ''.join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in task_name[:50])
                output_path = os.path.join(output_dir, f"libero_spatial_orange_task_{i+1}_{safe_name}_step12_180deg.png")
                img_pil.save(output_path)
                
                results.append({
                    'task_id': i,
                    'task_name': task_name,
                    'status': 'success',
                    'image_path': output_path
                })
                
                print(f"✅ 成功渲染并保存图片: {output_path}")
                
                # 关闭环境
                env.close()
                
            except Exception as e:
                print(f"❌ 任务 {i+1} 失败: {e}")
                results.append({
                    'task_id': i,
                    'task_name': task_name,
                    'status': 'failed',
                    'error': str(e)
                })
        
        # 生成报告
        print(f"\n📊 libero_spatial_orange 环境测试完成:")
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"✅ 成功: {success_count}/{len(test_tasks)}")
        print(f"❌ 失败: {len(test_tasks) - success_count}/{len(test_tasks)}")
        
        print(f"\n📁 生成的图片:")
        for result in results:
            if result['status'] == 'success':
                print(f"  - {result['image_path']}")
        
        return results
        
    except Exception as e:
        print(f"❌ libero_spatial_orange 环境测试失败: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    results = test_orange_environment()
    
    if results:
        success_count = sum(1 for r in results if r['status'] == 'success')
        if success_count > 0:
            print(f"\n🎉 libero_spatial_orange 环境验证成功! ({success_count} 个任务通过测试)")
        else:
            print(f"\n❌ libero_spatial_orange 环境验证失败!")
    else:
        print(f"\n❌ libero_spatial_orange 环境验证失败!")
