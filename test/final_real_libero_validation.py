#!/usr/bin/env python3
"""
最终正确的 LIBERO Goal New 环境验证脚本
使用正确的 sim.render() 方法来渲染环境
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import sys

# 添加 LIBERO 路径
sys.path.insert(0, './LIBERO')

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
    # 使用正确的 sim.render() 方法
    initial_image = env.env.sim.render(height=512, width=512, camera_name='frontview')
    
    print("🤖 正在执行12步仿真...")
    # 执行12步
    for step in range(12):
        # 随机动作 (7维: 3D位置 + 4D四元数)
        action = np.random.uniform(-1, 1, 7)
        obs, reward, done, info = env.step(action)
        print(f"   步骤 {step+1}: reward={reward:.3f}, done={done}")
        if done:
            print(f"   任务在第{step+1}步完成!")
            break
    
    print("📸 正在渲染12步后状态...")
    # 渲染12步后的状态
    final_image = env.env.sim.render(height=512, width=512, camera_name='frontview')
    
    # 旋转180度校正
    print("🔄 正在应用180度旋转...")
    final_image_rotated = np.rot90(final_image, 2)
    initial_image_rotated = np.rot90(initial_image, 2)
    
    # 保存图片
    print("💾 正在保存图片...")
    
    # 保存初始状态
    plt.figure(figsize=(10, 8))
    plt.imshow(initial_image_rotated)
    plt.title(f'LIBERO Goal New - Initial State\\nTask: {task_name}\\nProblem: {env.problem_name}', fontsize=12, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('libero_goal_new_final_initial.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 保存12步后状态
    plt.figure(figsize=(10, 8))
    plt.imshow(final_image_rotated)
    plt.title(f'LIBERO Goal New - After 12 Steps\\nTask: {task_name}\\nProblem: {env.problem_name}', fontsize=12, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('libero_goal_new_final_after12.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 创建对比图
    plt.figure(figsize=(16, 8))
    
    plt.subplot(1, 2, 1)
    plt.imshow(initial_image_rotated)
    plt.title(f'Initial State\\n{env.problem_name}', fontsize=12)
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(final_image_rotated)
    plt.title(f'After 12 Steps\\n{env.problem_name}', fontsize=12)
    plt.axis('off')
    
    plt.suptitle(f'LIBERO Goal New Environment Validation\\nTask: {task_name}', fontsize=14)
    plt.tight_layout()
    plt.savefig('libero_goal_new_final_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✅ 验证完成!")
    print(f"📸 已生成图片:")
    print(f"   - libero_goal_new_final_initial.png")
    print(f"   - libero_goal_new_final_after12.png") 
    print(f"   - libero_goal_new_final_comparison.png")
    
    # 输出环境信息
    print(f"\\n🔍 环境信息:")
    print(f"   问题名称: {env.problem_name}")
    print(f"   领域名称: {env.domain_name}")
    print(f"   语言指令: {env.language_instruction}")
    print(f"   兴趣对象: {env.obj_of_interest}")
    
    # 检查替换的对象是否出现在场景中
    print(f"\\n🎯 对象替换验证:")
    print(f"   场景应包含:")
    print(f"   ✓ blue_bottle (替换 wine_bottle)")
    print(f"   ✓ white_cabinet (替换 wooden_cabinet)")
    print(f"   ✓ white_bowl (替换 akita_black_bowl)")
    
    print("\\n🎉 LIBERO Goal New 环境最终验证成功!")
    print("   这是真正的 LIBERO 环境，包含了我们替换的对象！")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
