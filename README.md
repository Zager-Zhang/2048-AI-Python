# 2048

## 整体结构

> 2048-AI：Minimax搜索并使用Alpha Beta剪枝进行优化

![image](https://github.com/Zager-Zhang/2048-AI-Python/blob/master/images/%E6%95%B4%E4%BD%93%E7%BB%93%E6%9E%84.png)

## 程序使用说明

0. 配置python环境，安装pygame模块

1. 运行play.py

2. 出现游戏界面后用鼠标选择Classic模式或者Auto模式，游戏默认为Classic模式

3. Classic模式可以通过“W” “S” “A” “D”或方向键“↑” “↓” “←” “→”进行操作，并且可以点击Tip随时给予提示或关闭提示。当游戏结束时，会在界面提示“Game Over！”并播放音效。点击“New”即可开始新的一局

4. 点击Auto，进入AI模式，游戏开始自动运行，直到游戏结束。结束后点击“New”可以选择开启下一局

5. 如果想要退出游戏，则可以直接点击右上角的×号

6. 在游戏过程中，如果出现错误操作，则会出现提示音效


## AI性能

> 共做了125次测试

```
1024 -> 100%
2048 -> 89%
4096 -> 38%
8192 -> 3%
```

[![image](https://github.com/Zager-Zhang/2048-AI-Python/blob/master/images/%E7%BB%9F%E8%AE%A1%E6%95%B0%E6%8D%AE.png)]
