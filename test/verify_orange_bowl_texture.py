#!/usr/bin/env python3
"""
验证更新后的 Orange Bowl 纹理效果
创建环境并渲染图片以查看新的橙色纹理
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import sys

# Dynamically detect repo root and add to sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

def test_orange_bowl_texture():
    """测试更新后的 orange bowl 纹理效果"""
    
    print("🎨 验证更新后的 Orange Bowl 纹理效果...")
    
    try:
        # 导入 LIBERO
        from libero.libero.benchmark import get_benchmark
        from libero.libero.envs.env_wrapper import ControlEnv
        
        print("✅ LIBERO 导入成功")
        
        # 获取 orange 环境
        print("🔧 正在加载 libero_spatial_orange benchmark...")
        benchmark_class = get_benchmark("libero_spatial_orange")
        benchmark = benchmark_class()
        
        # 选择一个任务进行测试
        task_index = 0
        task_name = benchmark.get_task_names()[task_index]
        bddl_file_path = benchmark.get_task_bddl_file_path(task_index)
        
        print(f"🎯 测试任务: {task_name}")
        print(f"📄 BDDL 文件: {bddl_file_path}")
        
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
            control_freq=20
        )
        
        print("🎬 重置环境...")
        obs = env.reset()
        
        # 渲染初始状态
        print("📸 渲染初始状态...")
        initial_image = env.env.sim.render(height=512, width=512, camera_name='frontview')
        
        # 执行几步以便更好地观察对象
        print("🤖 执行5步仿真以获得更好的视角...")
        for step in range(5):
            action = np.random.uniform(-0.5, 0.5, 7)  # 较小的动作幅度
            obs, reward, done, info = env.step(action)
        
        # 渲染5步后状态
        print("📸 渲染5步后状态...")
        step5_image = env.env.sim.render(height=512, width=512, camera_name='frontview')
        
        # 执行更多步骤
        print("🤖 继续执行到12步...")
        for step in range(7):  # 继续执行7步，总共12步
            action = np.random.uniform(-0.5, 0.5, 7)
            obs, reward, done, info = env.step(action)
        
        # 渲染12步后状态
        print("📸 渲染12步后状态...")
        final_image = env.env.sim.render(height=512, width=512, camera_name='frontview')
        
        # 180度旋转校正
        initial_image_rotated = np.rot90(initial_image, 2)
        step5_image_rotated = np.rot90(step5_image, 2)
        final_image_rotated = np.rot90(final_image, 2)
        
        # 创建比较图片
        print("🖼️ 创建对比图片...")
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        axes[0].imshow(initial_image_rotated)
        axes[0].set_title('Initial State\n(Orange Bowl with New Texture)', fontsize=12)
        axes[0].axis('off')
        
        axes[1].imshow(step5_image_rotated)
        axes[1].set_title('After 5 Steps\n(Better View of Orange Bowl)', fontsize=12)
        axes[1].axis('off')
        
        axes[2].imshow(final_image_rotated)
        axes[2].set_title('After 12 Steps\n(Final State)', fontsize=12)
        axes[2].axis('off')
        
        plt.suptitle(f'Orange Bowl Texture Verification\nTask: {task_name}', fontsize=14, y=0.98)
        plt.tight_layout()
        
    # 保存比较图片
    output_dir = os.path.join(REPO_ROOT, 'test')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'orange_bowl_texture_verification.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✅ 验证图片已保存至: {output_path}")

    # 单独保存每个状态的图片
    initial_path = os.path.join(output_dir, 'orange_bowl_initial_state.png')
    step5_path = os.path.join(output_dir, 'orange_bowl_step5_state.png')
    final_path = os.path.join(output_dir, 'orange_bowl_final_state.png')

    Image.fromarray(initial_image_rotated).save(initial_path)
    Image.fromarray(step5_image_rotated).save(step5_path)
    Image.fromarray(final_image_rotated).save(final_path)

    print(f"📁 单独图片已保存:")
    print(f"   - 初始状态: {initial_path}")
    print(f"   - 5步后状态: {step5_path}")
    print(f"   - 12步后状态: {final_path}")

    # 关闭环境
    env.close()

    return True
        
    except Exception as e:
        print(f"❌ 验证过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_orange_bowl_texture()
    
    if success:
        print(f"\n🎉 Orange Bowl 纹理效果验证成功!")
        print(f"🎨 新的橙色纹理已应用到环境中")
        print(f"📸 请查看生成的验证图片以确认效果")
    else:
        print(f"\n❌ Orange Bowl 纹理效果验证失败!")
