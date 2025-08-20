#!/usr/bin/env python3
"""
LIBERO Spatial Orange 全任务验证脚本
为所有10个任务生成12步后的检测图像
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import sys

# Dynamically detect repo root and add to sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

def validate_all_orange_tasks():
    """验证所有 libero_spatial_orange 任务并保存第12步渲染图像"""
    try:
        # 导入 LIBERO（延迟导入以避免在模块导入时出错）
        from libero.libero.benchmark import get_benchmark
        from libero.libero.envs.env_wrapper import ControlEnv

        print("✅ LIBERO 导入成功")

        # 获取我们创建的 benchmark
        print("🔧 正在加载 libero_spatial_orange benchmark...")
        benchmark_class = get_benchmark("libero_spatial_orange")
        benchmark = benchmark_class()

        task_names = benchmark.get_task_names()
        total_tasks = len(task_names)

        print(f"📋 找到任务数量: {total_tasks}")
        print(f"📝 任务列表: {task_names}")

        # 创建输出目录
        output_dir = os.path.join(REPO_ROOT, 'test', 'libero_spatial_orange_all_tasks')
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 输出目录: {output_dir}")

        successful_tasks = []
        failed_tasks = []

        # 遍历所有任务
        for task_index in range(total_tasks):
            task_name = task_names[task_index]
            bddl_file_path = benchmark.get_task_bddl_file_path(task_index)

            print(f"\n🎯 处理任务 {task_index + 1}/{total_tasks}: {task_name}")
            print(f"📄 BDDL 文件: {bddl_file_path}")

            try:
                # 创建环境
                print("🏗️ 正在创建环境...")
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
                    control_freq=20,
                )

                print("🎬 重置环境...")
                obs = env.reset()

                print("🤖 执行12步仿真...")
                # 执行12步
                for step in range(12):
                    action = np.random.uniform(-1, 1, 7)  # Panda机器人7自由度
                    obs, reward, done, info = env.step(action)
                    if done:
                        print(f"   任务在第{step+1}步完成!")
                        break

                print("📸 渲染12步后状态...")
                final_image = env.env.sim.render(height=512, width=512, camera_name='frontview')

                # 180度旋转校正
                final_image_rotated = np.rot90(final_image, 2)

                # 保存图片
                safe_task_name = task_name.replace(' ', '_').replace('/', '_')[:50]
                output_path = os.path.join(output_dir, f"{safe_task_name}_step12_180deg.png")

                plt.figure(figsize=(10, 8))
                plt.imshow(final_image_rotated)
                plt.title(f'Task {task_index+1}: {task_name}\n12 Steps Later (180° Rotated)', fontsize=11, pad=15)
                plt.axis('off')
                plt.tight_layout()
                plt.savefig(output_path, dpi=150, bbox_inches='tight')
                plt.close()

                print(f"✅ 成功保存: {output_path}")
                successful_tasks.append({
                    'id': task_index + 1,
                    'name': task_name,
                    'image': output_path,
                })

                # 关闭环境
                env.close()

            except Exception as e:
                print(f"❌ 任务 {task_index + 1} 失败: {e}")
                failed_tasks.append({
                    'id': task_index + 1,
                    'name': task_name,
                    'error': str(e),
                })

        # 生成总结报告
        print(f"\n🎉 libero_spatial_orange 验证完成!")
        print(f"✅ 成功任务: {len(successful_tasks)}/{total_tasks}")
        print(f"❌ 失败任务: {len(failed_tasks)}/{total_tasks}")

        if successful_tasks:
            print(f"\n📁 成功生成的图片:")
            for task in successful_tasks:
                print(f"  {task['id']}. {task['name'][:50]}...")

        if failed_tasks:
            print(f"\n❌ 失败的任务:")
            for task in failed_tasks:
                print(f"  {task['id']}. {task['name']}: {task['error']}")

        return successful_tasks, failed_tasks

    except Exception as e:
        print(f"❌ libero_spatial_orange 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return [], []

if __name__ == "__main__":
    successful, failed = validate_all_orange_tasks()
    
    if len(successful) == 10:
        print(f"\n🎉 所有 libero_spatial_orange 任务验证成功!")
    elif len(successful) > 0:
        print(f"\n✅ 部分 libero_spatial_orange 任务验证成功!")
    else:
        print(f"\n❌ libero_spatial_orange 验证失败!")
