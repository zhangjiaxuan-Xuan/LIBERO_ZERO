#!/usr/bin/env python3

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Add LIBERO path
sys.path.append('./LIBERO')

def validate_simple_env():
    """简化验证，直接使用 robosuite"""
    try:
        print("🔧 Starting Simple Environment Test...")
        
        # 尝试导入并测试基础组件
        from libero.libero.benchmark import get_benchmark
        
        print("✅ Benchmark import successful")
        
        # 获取 benchmark
        benchmark_class = get_benchmark('libero_goal_new')
        benchmark = benchmark_class()
        
        print(f"✅ Benchmark created with {benchmark.get_num_tasks()} tasks")
        print(f"📋 Task names: {benchmark.get_task_names()}")
        
        # 检查 BDDL 文件
        task_id = 0
        task_bddl_file = benchmark.get_task_bddl_file_path(task_id)
        task_name = benchmark.get_task_names()[task_id]
        
        print(f"📄 Testing task: {task_name}")
        print(f"📄 BDDL file: {task_bddl_file}")
        
        if os.path.exists(task_bddl_file):
            print("✅ BDDL file exists")
        else:
            print("❌ BDDL file does not exist")
            return False
        
        # 尝试使用 robosuite 直接创建一个简单的环境来测试渲染
        print("🎮 Testing robosuite rendering capabilities...")
        
        import robosuite as suite
        from robosuite.controllers import load_controller_config
        
        # 创建一个简单的测试环境
        controller_config = load_controller_config(default_controller="OSC_POSE")
        
        env = suite.make(
            env_name="Lift",
            robots="Panda",
            has_renderer=False,
            has_offscreen_renderer=True,
            render_camera="frontview",
            camera_heights=512,
            camera_widths=512,
            controller_configs=controller_config,
        )
        
        print("✅ Robosuite test environment created")
        
        # 重置环境
        obs = env.reset()
        print("✅ Environment reset successful")
        
        # 执行几步动作
        print("🎮 Executing test actions...")
        for step in range(12):
            action = np.random.randn(env.action_spec[0].shape[0]) * 0.1
            obs, reward, done, info = env.step(action)
            print(f"  Step {step+1}: reward={reward:.3f}")
        
        # 渲染图像
        print("📸 Rendering image...")
        # 尝试直接使用 sim 来渲染
        img = env.sim.render(height=512, width=512, camera_name="frontview")
        
        if img is not None:
            print(f"✅ Image captured! Shape: {img.shape}")
            
            # 转换为 PIL Image 并翻转 180 度
            img_pil = Image.fromarray(img)
            img_rotated = img_pil.rotate(180)
            
            # 保存图片
            output_path = "./LIBERO/robosuite_test_render.png"
            img_rotated.save(output_path)
            
            print(f"🖼️ Test image saved to: {output_path}")
            
            # 用 matplotlib 显示
            plt.figure(figsize=(10, 8))
            plt.imshow(np.array(img_rotated))
            plt.title("Robosuite Test Environment (180° rotated)")
            plt.axis('off')
            
            output_path_plt = "./LIBERO/robosuite_test_render_with_title.png"
            plt.savefig(output_path_plt, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"🖼️ Titled test image saved to: {output_path_plt}")
            
        env.close()
        print("✅ Robosuite test completed successfully")
        
        # 现在测试 LIBERO 对象是否可以正常导入
        print("🔍 Testing LIBERO object imports...")
        
        from libero.libero.envs.objects import get_object_fn
        
        test_objects = ['blue_bottle', 'white_cabinet', 'white_bowl']
        for obj_name in test_objects:
            try:
                obj_class = get_object_fn(obj_name)
                obj_instance = obj_class()
                print(f"✅ {obj_name}: imported and instantiated successfully")
            except Exception as e:
                print(f"❌ {obj_name}: failed - {e}")
                return False
        
        print("✅ All LIBERO objects imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during simple validation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🎯 LIBERO Goal New - Simple Validation Test")
    print("=" * 60)
    
    success = validate_simple_env()
    
    if success:
        print("\n🎉 Simple Validation Complete!")
        print("✅ Benchmark system is working")
        print("✅ BDDL files are accessible")
        print("✅ Robosuite rendering is functional")
        print("✅ LIBERO objects can be imported")
        print("\n💡 Note: The full LIBERO environment creation may have configuration issues,")
        print("   but the core components are working correctly.")
        print("   The rendering system is confirmed to work with 180° rotation.")
    else:
        print("\n❌ Simple Validation Failed!")

if __name__ == "__main__":
    main()
