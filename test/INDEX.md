# Test Directory Index

## Main Documentation
- `README_MAIN.md` - Complete project documentation with technical details
- `PROJECT_UPDATES.md` - Executive summary of all changes made
- `VALIDATION_REPORT.md` - Detailed validation results

## Validation Scripts
- `validate_all_tasks.py` - **MAIN SCRIPT** - Validates all 10 tasks
- `final_real_libero_validation.py` - Single task validation
- `test_render_methods.py` - Rendering method testing

## Generated Images

### Individual Task Validation
- `libero_goal_new_final_initial.png` - Single task initial state
- `libero_goal_new_final_after12.png` - Single task after 12 steps  
- `libero_goal_new_final_comparison.png` - Single task comparison

### Complete Task Suite
`libero_goal_new_all_tasks/` directory contains:
- 30 individual task images (initial, after12, comparison for each task)
- 2 overview images showing all tasks at once

## Debugging & Development Scripts
- `check_objects.py` - Object registration verification
- `test_bddl.py` - BDDL file parsing test
- `debug_env.py` - Environment creation debugging
- Additional development utilities

## Quick Start
1. Review `PROJECT_UPDATES.md` for high-level overview
2. Check `README_MAIN.md` for detailed implementation
3. Run `python validate_all_tasks.py` to reproduce results
4. View images in `libero_goal_new_all_tasks/` for visual verification

## Validation Status: ✅ COMPLETE
All 10 tasks successfully validated with visual proof.
