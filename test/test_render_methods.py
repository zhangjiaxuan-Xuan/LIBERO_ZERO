#!/usr/bin/env python3
"""
测试 LIBERO 环境的渲染方法
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# 添加 LIBERO 路径
sys.path.insert(0, '/home/x/anaconda3/envs/openvla-oft/LIBERO')

try:
    from libero.libero.benchmark import get_benchmark
    from libero.libero.envs.env_wrapper import ControlEnv
    
    print("✅ LIBERO 导入成功")
    
    # 获取 benchmark
    benchmark_class = get_benchmark("libero_goal_new")
    benchmark = benchmark_class()
    
    # 选择第一个任务
    task_index = 0
    task_name = benchmark.get_task_names()[task_index]
    bddl_file_path = benchmark.get_task_bddl_file_path(task_index)
    
    print(f"🎯 测试任务: {task_name}")
    
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
    
    print("🔍 查看环境属性...")
    print(f"env.env 类型: {type(env.env)}")
    print(f"可用方法: {[method for method in dir(env.env) if 'render' in method.lower()]}")
    
    # 测试不同的渲染方法
    print("📸 测试渲染方法...")
    
    try:
        # 方法1: 不带 mode 参数
        image1 = env.env.render(camera_name='frontview', height=512, width=512)
        print(f"✅ 方法1成功: 形状 {image1.shape}")
        
        # 保存图片
        plt.figure(figsize=(8, 8))
        plt.imshow(image1)
        plt.title(f'LIBERO Goal New 真实环境\n{task_name}\n{env.problem_name}')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('libero_goal_new_test_render.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✅ 图片已保存: libero_goal_new_test_render.png")
        
    except Exception as e1:
        print(f"❌ 方法1失败: {e1}")
        
        try:
            # 方法2: 使用 sim.render
            image2 = env.env.sim.render(height=512, width=512, camera_name='frontview')
            print(f"✅ 方法2成功: 形状 {image2.shape}")
            
            # 保存图片
            plt.figure(figsize=(8, 8))
            plt.imshow(image2)
            plt.title(f'LIBERO Goal New 真实环境 (sim.render)\n{task_name}\n{env.problem_name}')
            plt.axis('off')
            plt.tight_layout()
            plt.savefig('libero_goal_new_test_render_sim.png', dpi=150, bbox_inches='tight')
            plt.close()
            
            print("✅ 图片已保存: libero_goal_new_test_render_sim.png")
            
        except Exception as e2:
            print(f"❌ 方法2失败: {e2}")
            
            try:
                # 方法3: 直接调用 render()
                image3 = env.env.render()
                print(f"✅ 方法3成功: 形状 {image3.shape if image3 is not None else 'None'}")
                
                if image3 is not None:
                    plt.figure(figsize=(8, 8))
                    plt.imshow(image3)
                    plt.title(f'LIBERO Goal New 真实环境 (直接render)\n{task_name}\n{env.problem_name}')
                    plt.axis('off')
                    plt.tight_layout()
                    plt.savefig('libero_goal_new_test_render_direct.png', dpi=150, bbox_inches='tight')
                    plt.close()
                    
                    print("✅ 图片已保存: libero_goal_new_test_render_direct.png")
                    
            except Exception as e3:
                print(f"❌ 方法3失败: {e3}")
                print("🔍 尝试查看 render 方法签名...")
                import inspect
                try:
                    sig = inspect.signature(env.env.render)
                    print(f"render 方法签名: {sig}")
                except:
                    print("无法获取 render 方法签名")
    
    print(f"\n🔍 环境信息:")
    print(f"   问题名称: {env.problem_name}")
    print(f"   领域名称: {env.domain_name}")
    print(f"   语言指令: {env.language_instruction}")
    
except Exception as e:
    print(f"❌ 总错误: {e}")
    import traceback
    traceback.print_exc()
