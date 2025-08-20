#!/usr/bin/env python3
"""
Orange Bowl 纹理图片精细颜色处理脚本
保留原有花纹和线条，只改变色调为橙色系
"""

import numpy as np
from PIL import Image
import cv2
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def process_orange_bowl_texture_refined():
    """精细处理 orange bowl 的纹理图片，保留纹理细节"""

    # 输入和输出路径（使用相对仓库路径）
    assets_dir = os.path.join(REPO_ROOT, 'libero', 'libero', 'assets', 'stable_scanned_objects', 'orange_bowl')
    input_path = os.path.join(assets_dir, 'texture_original_backup.png')
    output_path = os.path.join(assets_dir, 'texture.png')
    
    print(f"🎨 开始精细处理 Orange Bowl 纹理图片...")
    print(f"📁 输入文件: {input_path}")
    
    # 检查备份文件是否存在
    if not os.path.exists(input_path):
        print(f"❌ 错误: 备份文件不存在 {input_path}")
        return False
    
    try:
        # 读取原始备份图片
        print("📖 读取原始备份纹理图片...")
        img = Image.open(input_path)
        img_array = np.array(img).astype(np.float32)
        
        print(f"📏 图片尺寸: {img_array.shape}")
        print(f"🎨 图片模式: {img.mode}")
        
        # 转换为HSV色彩空间以便更好地控制色调
        print("🔄 转换色彩空间到HSV...")
        img_bgr = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_RGB2BGR)
        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # 分离HSV通道
        h, s, v = cv2.split(img_hsv)
        
        print("🎨 开始精细颜色转换...")
        
        # 创建掩码：排除纯黑色像素 (0,0,0)
        mask = ~((img_array[:,:,0] == 0) & (img_array[:,:,1] == 0) & (img_array[:,:,2] == 0))
        
        # 橙色在HSV中的色调值约为15-25（OpenCV中H值范围0-179）
        orange_hue = 15  # 橙色色调
        
        # 对非黑色像素应用橙色色调
        h[mask] = orange_hue
        
        # 增强饱和度，但保持原有的变化
        # 将饱和度提升到橙色范围，但保留原有的明暗变化
        s[mask] = np.clip(s[mask] * 1.2 + 30, 0, 255)  # 适度增加饱和度
        
        # 保持原有的亮度变化，这样可以保留纹理细节
        # 对于很暗的区域，稍微提亮一点以显示橙色
        v[mask] = np.clip(v[mask] * 1.1 + 10, 0, 255)
        
        # 重新合并HSV通道
        img_hsv_processed = cv2.merge([h, s, v])
        
        # 转换回RGB
        print("🔄 转换回RGB色彩空间...")
        img_bgr_processed = cv2.cvtColor(img_hsv_processed.astype(np.uint8), cv2.COLOR_HSV2BGR)
        img_rgb_processed = cv2.cvtColor(img_bgr_processed, cv2.COLOR_BGR2RGB)
        
        # 对于原本是纯黑色的像素，保持不变
        final_img = img_rgb_processed.copy()
        black_mask = ~mask
        final_img[black_mask] = img_array[black_mask].astype(np.uint8)
        
        print("✅ 颜色转换完成!")
        
        # 保存处理后的图片
        print("💾 保存精细处理后的纹理图片...")
        processed_img = Image.fromarray(final_img.astype(np.uint8))
        processed_img.save(output_path)
        
        print(f"✅ 新纹理已保存至: {output_path}")
        
        # 生成对比预览图片
        print("🖼️ 生成对比预览图片...")
        
        # 创建对比图片
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # 原始图片（缩放显示）
        original_resized = np.array(img.resize((512, 512), Image.LANCZOS))
        axes[0].imshow(original_resized)
        axes[0].set_title('Original Texture\n(Before Processing)', fontsize=12)
        axes[0].axis('off')
        
        # 处理后图片（缩放显示）
        processed_resized = np.array(processed_img.resize((512, 512), Image.LANCZOS))
        axes[1].imshow(processed_resized)
        axes[1].set_title('Orange Texture\n(After Processing)', fontsize=12)
        axes[1].axis('off')
        
        # 差异图片
        diff = np.abs(original_resized.astype(np.float32) - processed_resized.astype(np.float32))
        diff_normalized = (diff / diff.max() * 255).astype(np.uint8)
        axes[2].imshow(diff_normalized)
        axes[2].set_title('Difference Map\n(Shows Changes)', fontsize=12)
        axes[2].axis('off')
        
        plt.suptitle('Orange Bowl Texture Processing Comparison\n(Preserving Original Details)', fontsize=14, y=0.98)
        plt.tight_layout()
        
        preview_path = "/home/x/anaconda3/envs/openvla-oft/LIBERO/test/orange_bowl_texture_comparison.png"
        plt.savefig(preview_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"🖼️ 对比预览已保存至: {preview_path}")
        
        # 保存单独的处理后预览图片
        processed_preview_path = "/home/x/anaconda3/envs/openvla-oft/LIBERO/test/orange_bowl_texture_refined.png"
        processed_resized_img = Image.fromarray(processed_resized)
        processed_resized_img.save(processed_preview_path)
        print(f"🖼️ 精细处理预览已保存至: {processed_preview_path}")
        
        # 显示处理统计
        non_black_pixels = np.sum(mask)
        total_pixels = mask.size
        black_pixels = total_pixels - non_black_pixels
        
        print(f"\n📊 处理统计:")
        print(f"   - 总像素数: {total_pixels:,}")
        print(f"   - 处理像素数: {non_black_pixels:,} ({non_black_pixels/total_pixels*100:.1f}%)")
        print(f"   - 背景像素数: {black_pixels:,} ({black_pixels/total_pixels*100:.1f}%)")
        print(f"   - 处理方法: HSV色彩空间色调转换")
        print(f"   - 橙色色调值: {orange_hue}")
        print(f"   - 保留细节: ✅ 原有花纹和线条")
        
        return True
        
    except Exception as e:
        print(f"❌ 处理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = process_orange_bowl_texture_refined()
    
    if success:
        print(f"\n🎉 Orange Bowl 精细纹理处理成功!")
        print(f"🎨 保留了原有花纹和线条，只改变了色调为橙色")
        print(f"🔄 建议重新运行环境验证以查看效果")
    else:
        print(f"\n❌ Orange Bowl 精细纹理处理失败!")
