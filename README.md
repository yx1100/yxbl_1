# yxbl_1
The code repository for the first paper during the doctoral period.


狼人杀项目/
├── src/
│   ├── environment/
│   │   ├── __init__.py
│   │   ├── werewolf_env.py      # 狼人杀游戏环境（MDP实现）
│   │   ├── game_state.py        # 游戏状态管理
│   │   ├── game_logic.py        # 游戏规则与逻辑
│   │   ├── game_manager.py      # 游戏阶段管理(夜晚、白天等)
│   │   ├── reward.py            # 奖励函数
│   │   └── action_space.py      # 行动空间定义
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py        # 基础智能体接口
│   │   ├── rule_agent.py        # 基于规则的智能体
│   │   └── learning_agent.py    # 强化学习智能体
│   ├── roles/
│   │   ├── __init__.py
│   │   ├── role.py              # 角色基类
│   │   ├── villager.py          # 村民角色
│   │   ├── werewolf.py          # 狼人角色
│   │   ├── doctor.py            # 医生角色
│   │   └── seer.py              # 预言家角色
│   ├── RL/
│   │   ├── __init__.py
│   │   ├── models.py            # 神经网络模型定义
│   │   ├── memory.py            # 经验回放缓冲区
│   │   └── algorithms/
│   │       ├── __init__.py
│   │       ├── dqn.py           # DQN算法实现
│   │       ├── ppo.py           # PPO算法实现
│   │       └── a2c.py           # A2C算法实现
│   └── utils/
│       └── __init__.py
├── train.py                     # 训练脚本
├── evaluate.py                  # 评估脚本
├── config.py                    # 配置文件
└── main.py                      # 主程序入口

