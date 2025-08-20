#!/usr/bin/env python3

import sys
import os

# Add LIBERO path
sys.path.append('./LIBERO')

def check_missing_objects():
    """检查 BDDL 文件中引用的对象"""
    try:
        from libero.libero.envs.base_object import OBJECTS_DICT
        
        # 这些是在 BDDL 文件中引用的对象类别
        referenced_objects = [
            'white_cabinet',
            'flat_stove', 
            'wine_rack',
            'white_bowl',
            'cream_cheese',
            'blue_bottle',
            'plate'
        ]
        
        print("Checking referenced objects in OBJECTS_DICT...")
        missing_objects = []
        
        for obj in referenced_objects:
            if obj in OBJECTS_DICT:
                print(f"✓ {obj} found")
            else:
                print(f"✗ {obj} NOT found")
                missing_objects.append(obj)
                
        if missing_objects:
            print(f"\nMissing objects: {missing_objects}")
            print("Available objects:", list(OBJECTS_DICT.keys()))
        else:
            print("\n✓ All referenced objects found!")
            
        return len(missing_objects) == 0
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_missing_objects()
