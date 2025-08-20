#!/usr/bin/env python3

import sys
import os

# Add LIBERO path
sys.path.append('/home/x/anaconda3/envs/openvla-oft/LIBERO')

def test_simple():
    """简单测试"""
    try:
        from libero.libero.envs.bddl_base_domain import TASK_MAPPING
        from libero.libero.envs.base_object import OBJECTS_DICT
        
        print("Task mapping keys:", list(TASK_MAPPING.keys()))
        print("Object dict keys:", list(OBJECTS_DICT.keys()))
        
        # 检查新注册的对象
        if 'blue_bottle' in OBJECTS_DICT:
            print("✓ blue_bottle found in OBJECTS_DICT")
        else:
            print("✗ blue_bottle not found in OBJECTS_DICT")
            
        if 'white_cabinet' in OBJECTS_DICT:
            print("✓ white_cabinet found in OBJECTS_DICT")
        else:
            print("✗ white_cabinet not found in OBJECTS_DICT")
            
        if 'white_bowl' in OBJECTS_DICT:
            print("✓ white_bowl found in OBJECTS_DICT")
        else:
            print("✗ white_bowl not found in OBJECTS_DICT")
            
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple()
