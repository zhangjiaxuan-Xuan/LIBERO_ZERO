#!/usr/bin/env python3
"""
Orange Bowl 纹理图片颜色处理脚本
将白色区域变成橙色，黑色区域变成深橙色
"""

import numpy as np
from PIL import Image
import os

# Detect repo root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def process_orange_bowl_texture():
    """处理 orange bowl 的纹理图片"""
    
    # 输入和输出路径（相对于仓库根）
    assets_dir = os.path.join(REPO_ROOT, 'libero', 'libero', 'assets', 'stable_scanned_objects', 'orange_bowl')
    input_path = os.path.join(assets_dir, 'texture.png')
    backup_path = os.path.join(assets_dir, 'texture_original_backup.png')
    output_path = os.path.join(assets_dir, 'texture.png')
    
    print(f"🎨 开始处理 Orange Bowl 纹理图片...")
    print(f"📁 输入文件: {input_path}")
    
    # 检查文件是否存在
    if not os.path.exists(input_path):
        print(f"❌ 错误: 纹理文件不存在 {input_path}")
        return False
    
    try:
        # 读取图片
        print("📖 读取原始纹理图片...")
        img = Image.open(input_path)
        img_array = np.array(img)
        
        print(f"📏 图片尺寸: {img_array.shape}")
        print(f"🎨 图片模式: {img.mode}")
        
        # 备份原始文件
        print("💾 创建原始文件备份...")
        img.save(backup_path)
        print(f"✅ 备份保存至: {backup_path}")
        
        # 处理图片颜色
        processed_array = img_array.copy()
        
        # 定义橙色调色板
        orange_light = np.array([255, 165, 0])    # 亮橙色 (Orange)
        orange_medium = np.array([255, 140, 0])   # 中橙色 (Dark Orange)
        orange_dark = np.array([255, 69, 0])      # 深橙色 (Orange Red)
        orange_deep = np.array([204, 85, 0])      # 更深橙色
        
        print("🎨 开始颜色转换...")
        
        # 获取图片的高度和宽度
        height, width = img_array.shape[:2]
        total_pixels = height * width
        processed_pixels = 0
        
        # 逐像素处理
        for i in range(height):
            for j in range(width):
                # 获取当前像素的RGB值
                if len(img_array.shape) == 3:  # RGB图片
                    r, g, b = img_array[i, j, :3]
                else:  # 灰度图片
                    r = g = b = img_array[i, j]
                
                # 跳过纯黑色像素 (0,0,0) - 作为背景不处理
                if r == 0 and g == 0 and b == 0:
                    continue
                
                # 计算像素亮度
                brightness = (r + g + b) / 3.0
                
                # 根据亮度分配不同的橙色
                if brightness > 200:  # 很亮的像素 -> 亮橙色
                    new_color = orange_light
                elif brightness > 150:  # 中等亮度 -> 中橙色
                    new_color = orange_medium
                elif brightness > 100:  # 较暗像素 -> 深橙色
                    new_color = orange_dark
                else:  # 很暗的像素 -> 更深橙色
                    new_color = orange_deep
                
                # 应用新颜色，但保持原始的透明度信息（如果有的话）
                if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
                    processed_array[i, j, :3] = new_color
                    # 如果有透明通道，保持不变
                    if img_array.shape[2] == 4:
                        processed_array[i, j, 3] = img_array[i, j, 3]
                else:
                    processed_array[i, j] = np.mean(new_color)  # 转为灰度
                
                processed_pixels += 1
            
            # 显示进度
            if (i + 1) % (height // 10) == 0:
                progress = ((i + 1) / height) * 100
                print(f"   进度: {progress:.1f}%")
        
        print(f"✅ 处理完成! 共处理 {processed_pixels} 个非背景像素")
        
        # 保存处理后的图片
        print("💾 保存处理后的纹理图片...")
        processed_img = Image.fromarray(processed_array.astype(np.uint8))
        processed_img.save(output_path)
        
        print(f"✅ 新纹理已保存至: {output_path}")

        # 生成预览图片到test目录
        preview_dir = os.path.join(REPO_ROOT, 'test')
        os.makedirs(preview_dir, exist_ok=True)
        preview_path = os.path.join(preview_dir, 'orange_bowl_texture_preview.png')
        processed_img.save(preview_path)
        print(f"🖼️ 预览图片已保存至: {preview_path}")

        # 显示颜色转换统计
        print(f"\n🎨 颜色转换完成:")
        print(f"   - 亮橙色 (RGB: {orange_light}): 用于亮色区域")
        print(f"   - 中橙色 (RGB: {orange_medium}): 用于中等亮度区域")
        print(f"   - 深橙色 (RGB: {orange_dark}): 用于较暗区域")
        print(f"   - 更深橙色 (RGB: {orange_deep}): 用于最暗区域")
        print(f"   - 纯黑色像素 (0,0,0): 保持不变作为背景")

        return True

    except Exception as e:
        print(f"❌ 处理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = process_orange_bowl_texture()
    
    if success:
        print(f"\n🎉 Orange Bowl 纹理处理成功!")
        print(f"🔄 建议重新运行环境验证以查看效果")
    else:
        print(f"\n❌ Orange Bowl 纹理处理失败!")
