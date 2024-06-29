# BicameralMind

一个多agent协同系统

## Work
### TODO
- debug
- 增加单元测试，在每个function实现后增加测试功能
### 6.28
- agent manager需要填上register/unregister功能 ✅
- 实现agent基类 ✅
- 增加IO的数据结构 ✅
- 对agent的状态用enum做约束 ✅
### 6.27
- 初始化agent package ✅
- 增加全局config ✅
- 实现单例模式annotation ✅

## Design
agent自身的属性应该是role，obj。role是自身的核心属性，决定接下来的行为。<br>
manager 通过 name来识别和使用agent，所以name应该是manager要维护的。