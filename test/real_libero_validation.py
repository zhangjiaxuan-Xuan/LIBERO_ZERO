#!/usr/bin/env python3
"""
正确的 LIBERO Goal New 环境验证脚本
使用 ControlEnv 包装器来创建和渲染环境
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import sys

# 添加 LIBERO 路径
sys.path.insert(0, '/home/x/anaconda3/envs/openvla-oft/LIBERO')

try:
    # 导入 LIBERO
    from libero.libero.benchmark import get_benchmark
    from libero.libero.envs.env_wrapper import ControlEnv
    
    print("✅ LIBERO 导入成功")
    
    # 获取我们创建的 benchmark
    print("🔧 正在加载 libero_goal_new benchmark...")
    benchmark_class = get_benchmark("libero_goal_new")
    benchmark = benchmark_class()
    
    print(f"📋 找到任务数量: {len(benchmark.get_task_names())}")
    print(f"📝 任务列表: {benchmark.get_task_names()}")
    
    # 选择第一个任务进行测试
    task_index = 0
    task_name = benchmark.get_task_names()[task_index]
    bddl_file_path = benchmark.get_task_bddl_file_path(task_index)
    
    print(f"🎯 测试任务: {task_name}")
    print(f"📄 BDDL 文件: {bddl_file_path}")
    
    # 验证 BDDL 文件存在
    if not os.path.exists(bddl_file_path):
        print(f"❌ BDDL 文件不存在: {bddl_file_path}")
        sys.exit(1)
    
    # 创建环境
    print("🏗️ 正在创建 LIBERO ControlEnv...")
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
    
    print("🎬 正在重置环境...")
    obs = env.reset()
    
    print("📸 正在渲染初始状态...")
    # 渲染初始状态
    initial_image = env.env.render(mode='rgb_array', camera_name='frontview', height=512, width=512)
    
    print("🤖 正在执行12步仿真...")
    # 执行12步
    for step in range(12):
        # 随机动作 (7维: 3D位置 + 4D四元数)
        action = np.random.uniform(-1, 1, 7)
        obs, reward, done, info = env.step(action)
        print(f"   步骤 {step+1}: reward={reward:.3f}, done={done}")
        if done:
            print(f"   任务在第{step+1}步完成")
            break
    
    print("📸 正在渲染12步后状态...")
    # 渲染12步后的状态
    final_image = env.env.render(mode='rgb_array', camera_name='frontview', height=512, width=512)
    
    # 旋转180度校正
    print("🔄 正在应用180度旋转...")
    final_image_rotated = np.rot90(final_image, 2)
    initial_image_rotated = np.rot90(initial_image, 2)
    
    # 保存图片
    print("💾 正在保存图片...")
    
    # 保存初始状态
    plt.figure(figsize=(10, 8))
    plt.imshow(initial_image_rotated)
    plt.title(f'LIBERO Goal New - 初始状态\n任务: {task_name}\n环境: {env.problem_name}', fontsize=12, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('libero_goal_new_real_initial.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 保存12步后状态
    plt.figure(figsize=(10, 8))
    plt.imshow(final_image_rotated)
    plt.title(f'LIBERO Goal New - 12步后状态\n任务: {task_name}\n环境: {env.problem_name}', fontsize=12, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('libero_goal_new_real_final.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 创建对比图
    plt.figure(figsize=(16, 8))
    
    plt.subplot(1, 2, 1)
    plt.imshow(initial_image_rotated)
    plt.title(f'初始状态\n{env.problem_name}', fontsize=12)
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(final_image_rotated)
    plt.title(f'12步后状态\n{env.problem_name}', fontsize=12)
    plt.axis('off')
    
    plt.suptitle(f'LIBERO Goal New 环境真实验证\n任务: {task_name}', fontsize=14)
    plt.tight_layout()
    plt.savefig('libero_goal_new_real_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✅ 验证完成!")
    print(f"📸 已生成图片:")
    print(f"   - libero_goal_new_real_initial.png")
    print(f"   - libero_goal_new_real_final.png") 
    print(f"   - libero_goal_new_real_comparison.png")
    
    # 输出环境信息
    print(f"\n🔍 环境信息:")
    print(f"   问题名称: {env.problem_name}")
    print(f"   领域名称: {env.domain_name}")
    print(f"   语言指令: {env.language_instruction}")
    print(f"   兴趣对象: {env.obj_of_interest}")
    
    print("🎉 LIBERO Goal New 环境真实验证成功!")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
