#!/usr/bin/env python3

import sys
import os

# Add LIBERO path
sys.path.append('./LIBERO')

def debug_get_object_fn():
    """调试 get_object_fn 函数"""
    try:
        from libero.libero.envs.objects import get_object_fn, OBJECTS_DICT
        
        print("OBJECTS_DICT contents:")
        for key, value in OBJECTS_DICT.items():
            print(f"  {key}: {value}")
        
        print("\nTesting get_object_fn for common objects:")
        test_objects = ['wine_bottle', 'akita_black_bowl', 'wooden_cabinet', 'plate']
        
        for obj_name in test_objects:
            try:
                obj_fn = get_object_fn(obj_name)
                print(f"✓ {obj_name}: {obj_fn}")
                
                # 尝试创建实例
                instance = obj_fn()
                print(f"  ✓ Instance created: {instance}")
                
            except Exception as e:
                print(f"✗ {obj_name}: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_get_object_fn()
