#!/usr/bin/env python3
"""
批量创建 LIBERO_0 的所有初始化文件
基于 libero_goal 的 init 文件，使用相同的任务映射关系
"""

import os
import shutil

def create_libero_0_init_files():
    """创建所有 LIBERO_0 初始化文件"""
    
    # 原始和目标目录
    goal_init_dir = "/home/x/anaconda3/envs/openvla-oft/LIBERO/libero/libero/init_files/libero_goal"
    libero_0_init_dir = "/home/x/anaconda3/envs/openvla-oft/LIBERO/libero/libero/init_files/libero_0"
    
    # 创建目标目录（如果不存在）
    os.makedirs(libero_0_init_dir, exist_ok=True)
    
    # 任务映射关系 (原始任务名 -> 新任务名)
    task_mappings = {
        'open_the_middle_drawer_of_the_cabinet.pruned_init': 'open_the_middle_drawer_of_the_white_cabinet.pruned_init',
        'open_the_top_drawer_and_put_the_bowl_inside.pruned_init': 'open_the_top_drawer_and_put_the_blue_white_porcelain_bowl_inside.pruned_init',
        'push_the_plate_to_the_front_of_the_stove.pruned_init': 'push_the_saucer_to_the_front_of_the_stove.pruned_init',
        'put_the_bowl_on_the_plate.pruned_init': 'put_the_blue_white_porcelain_bowl_on_the_saucer.pruned_init',
        'put_the_bowl_on_the_stove.pruned_init': 'put_the_blue_white_porcelain_bowl_on_the_stove.pruned_init',
        'put_the_bowl_on_top_of_the_cabinet.pruned_init': 'put_the_blue_white_porcelain_bowl_on_top_of_the_white_cabinet.pruned_init',
        'put_the_cream_cheese_in_the_bowl.pruned_init': 'put_the_butter_in_the_blue_white_porcelain_bowl.pruned_init',
        'put_the_wine_bottle_on_the_rack.pruned_init': 'put_the_moutai_on_the_rack.pruned_init',
        'put_the_wine_bottle_on_top_of_the_cabinet.pruned_init': 'put_the_moutai_on_top_of_the_white_cabinet.pruned_init',
        'turn_on_the_stove.pruned_init': 'turn_on_the_stove.pruned_init'
    }
    
    print("🚀 开始创建 LIBERO_0 的所有10个初始化文件...")
    
    # 处理每个初始化文件
    for original_init, new_init in task_mappings.items():
        original_path = os.path.join(goal_init_dir, original_init)
        new_path = os.path.join(libero_0_init_dir, new_init)
        
        if not os.path.exists(original_path):
            print(f"❌ 原始初始化文件不存在: {original_path}")
            continue
            
        print(f"📝 复制初始化文件: {original_init} -> {new_init}")
        
        # 复制文件
        shutil.copy2(original_path, new_path)
        
        print(f"✅ 已创建: {new_init}")
    
    print(f"\n🎉 成功创建了 {len(task_mappings)} 个 LIBERO_0 初始化文件!")

if __name__ == "__main__":
    create_libero_0_init_files()
    print("\\n🎯 LIBERO_0 初始化文件创建完成！")
