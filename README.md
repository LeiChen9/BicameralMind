<!--
 * @Author: LeiChen9 chenlei9691@gmail.com
 * @Date: 2024-07-01 10:08:41
 * @LastEditors: LeiChen9 chenlei9691@gmail.com
 * @LastEditTime: 2024-07-03 17:21:53
 * @FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/README.md
 * @Description: 
 * 
 * Copyright (c) 2024 by Riceball, All Rights Reserved. 
-->
# BicameralMind

一个多agent协同系统

## Work
### TODO
- 增加单元测试，在每个function实现后增加测试功能

### 7.3
- 调试了PubMedQA做测试
### 6.30
- 重构manager代码
- 增加多轮反思功能
- 增加logger文件记录
- 解决api报错问题
### 6.28
- agent manager需要填上register/unregister功能 
- 实现agent基类 
- 增加IO的数据结构 
- 对agent的状态用enum做约束 
### 6.27
- 初始化agent package 
- 增加全局config 
- 实现单例模式annotation 

## Design
用户只需要manager一个入口就好了。内部的executor和mentor的交互可以作为内部状态做转移和记录，不需要对外暴露<br>
executor和mentor的多轮交互的终止条件：收敛<br>
agent的属性：自己的名字，自己的角色。<br>
manager需要管理的是agent的角色。名字不重要
~~agent自身的属性应该是role，obj。role是自身的核心属性，决定接下来的行为。<br>~~
~~manager 通过 name来识别和使用agent，所以name应该是manager要维护的。~~

## Eval
注意所有eval数据集都在datasets里面。文件结构见下一节。
### PubMedQA
#### Git
git@github.com:pubmedqa/pubmedqa.git
#### Thoughts
pubmedqa是可以分为train/dev/test的。如果只用test感觉有点亏。但是可以先试一下链路

## File Structure
in case gitignore hide some FS
.
├── README.md
├── agents
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   ├── agent.cpython-38.pyc
│   │   ├── agent_enum.cpython-38.pyc
│   │   ├── agent_manager.cpython-38.pyc
│   │   └── agent_model.cpython-38.pyc
│   ├── agent.py
│   ├── agent_enum.py
│   ├── agent_manager.py
│   └── agent_model.py
├── api.py
├── config.toml
├── custom_key.toml
├── data_structures
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   └── io_object.cpython-38.pyc
│   └── io_object.py
├── datasets
│   └── pubmedqa
│       ├── LICENSE
│       ├── README.md
│       ├── data
│       │   ├── ori_pqal.json
│       │   └── test_ground_truth.json
│       ├── evaluation.py
│       ├── get_human_performance.py
│       └── preprocess
│           └── split_dataset.py
├── eval.py
├── log_config.toml
├── main.py
├── medical_dialog.py
└── utils
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-38.pyc
    │   └── singleton.cpython-38.pyc
    ├── singleton.py
    └── tools.py

## Reference Work
- Nori, H., Lee, Y. T., Zhang, S., Carignan, D., Edgar, R., Fusi, N., King, N., Larson, J., Li, Y., Liu, W., Luo, R., McKinney, S. M., Ness, R. O., Poon, H., Qin, T., Usuyama, N., White, C., & Horvitz, E. (2023). Can Generalist Foundation Models Outcompete Special-Purpose Tuning? Case Study in Medicine. *arXiv eprint: 2311.16452*.