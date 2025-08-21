这个数据环境是为了实现完全的zero-shot学习的测试，放入环境的物体其中包括一些特殊的意义指代物：
- moutai 对应原本的winebottle
- blue white porcelain bowl 对应原本的black bowl
- butter 对应原本的 cream cheese
- saucer 对应原本的 plate
- white cabinet 对应原本的 wooden cabinet

这个环境以goal为基础，只检测在图像识别上的zeroshot能力，因此只需要将目标物体进行替换，配置和init文件一并照搬即可
但是注意要更新好bddl文件中的所有相关内容

新环境名称：libero_0