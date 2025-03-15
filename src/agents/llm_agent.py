from .base_agent import BaseAgent
import random

class LLMAgent(BaseAgent):
    def __init__(self, player_id, role, api_client):
        """初始化基于LLM的智能体
        
        Args:
            player_id: 玩家ID
            role: 角色对象(Werewolf, Villager等)
            api_client: LLMClient实例
        """
        super().__init__(player_id, role)
        self.api_client = api_client
        self.chat_history = []  # 存储与其他玩家的对话历史
        self.knowledge = {
            "suspects": [],      # 怀疑是狼人的玩家
            "trusted": [],       # 认为是好人的玩家
            "observed_deaths": [] # 观察到的死亡情况
        }
        
    def generate_response(self, from_player, message, game_state):
        """生成对特定玩家消息的回复
        
        Args:
            from_player: 发送消息的玩家ID
            message: 接收到的消息内容
            game_state: 当前游戏状态
            
        Returns:
            str: 生成的回复内容
        """
        # 记录对话
        self.chat_history.append({
            "from": from_player,
            "to": self.player_id,
            "content": message,
            "day": game_state.day_count
        })
        
        # 构建完整的提示词
        system_prompt = self._build_system_prompt(game_state)
        
        # 构建消息历史(最近5条)以保持上下文
        recent_history = self._format_recent_chat_history(from_player)
        
        # 构建消息请求
        messages = [
            {"role": "system", "content": system_prompt},
            *recent_history,
            {"role": "user", "content": message}
        ]
        
        # 调用LLM生成回复
        response = self.api_client.get_response(messages)
        if response["success"]:
            # 记录自己的回复
            self.chat_history.append({
                "from": self.player_id,
                "to": from_player,
                "content": response["content"],
                "day": game_state.day_count
            })
            return response["content"]
        else:
            # 出错时返回简单回复
            return "抱歉，我暂时无法回复。"
    
    def _build_system_prompt(self, game_state):
        """根据游戏状态构建系统提示词
        
        Args:
            game_state: 当前游戏状态
            
        Returns:
            str: 完整的系统提示词
        """
        # 获取基础角色提示词
        base_prompt = self.api_client.get_role_prompt(self.role.role_type)
        
        # 添加游戏状态信息
        game_info = f"""
当前是第{game_state.day_count}天的{game_state.phase}阶段。
存活玩家: {[p for p in game_state.players if p.is_alive]}
你所知道的信息:
- 你的角色: {self.role.name}
- 你怀疑的玩家: {self.knowledge['suspects']}
- 你信任的玩家: {self.knowledge['trusted']}
"""
        
        # 为不同角色添加特定信息
        role_specific = ""
        if self.role.role_type == "werewolf":
            # 狼人知道其他狼人
            werewolves = [p.player_id for p in game_state.players 
                          if p.role.team == "werewolf" and p.is_alive and p.player_id != self.player_id]
            role_specific = f"你的狼人同伴: {werewolves}\n"
        elif self.role.role_type == "seer":
            # 预言家知道查验结果
            role_specific = "你的查验结果:\n"
            for event in game_state.history:
                if event["type"] == "check" and event["source"] == self.player_id:
                    role_specific += f"- 玩家{event['target']}是{'狼人' if event['result'] == 'werewolf' else '好人'}\n"
        
        # 组合完整提示词
        return f"{base_prompt}\n\n{game_info}\n{role_specific}\n请根据你的角色和身份来回应其他玩家的消息。"
    
    def _format_recent_chat_history(self, target_player, max_history=5):
        """格式化与特定玩家的最近对话
        
        Args:
            target_player: 目标玩家ID
            max_history: 最大历史消息数
            
        Returns:
            list: 格式化的消息历史
        """
        # 筛选与目标玩家的对话
        relevant_chats = [chat for chat in self.chat_history 
                          if (chat["from"] == target_player and chat["to"] == self.player_id) or
                             (chat["from"] == self.player_id and chat["to"] == target_player)]
        
        # 取最近的几条
        recent_chats = relevant_chats[-max_history:] if len(relevant_chats) > max_history else relevant_chats
        
        # 格式化为LLM API需要的格式
        formatted = []
        for chat in recent_chats:
            if chat["from"] == self.player_id:
                formatted.append({"role": "assistant", "content": chat["content"]})
            else:
                formatted.append({"role": "user", "content": chat["content"]})
                
        return formatted
    
    def update_knowledge(self, game_state):
        """根据游戏状态更新智能体的知识
        
        Args:
            game_state: 当前游戏状态
        """
        # 实现根据游戏事件更新智能体的知识
        # 例如更新怀疑名单、更新信任名单等
        pass
        
    def act(self, valid_actions, game_state):
        """决策行动，例如投票或使用能力
        
        Args:
            valid_actions: 有效行动列表
            game_state: 当前游戏状态
            
        Returns:
            dict: 选择的行动
        """
        if game_state.phase == "night":
            # 夜晚决策使用角色能力
            return self._night_action(valid_actions, game_state)
        elif game_state.phase == "vote":
            # 投票决策
            return self._vote_action(valid_actions, game_state)
        else:
            # 讨论阶段无需特殊行动
            return None
    
    def _night_action(self, valid_actions, game_state):
        """夜晚行动决策
        
        Args:
            valid_actions: 有效行动列表
            game_state: 当前游戏状态
            
        Returns:
            dict: 选择的行动
        """
        # 简单实现：为不同角色提供基础的夜间行为逻辑
        if self.role.role_type == "werewolf":
            # 狼人选择袭击目标(非狼人)
            targets = [p.player_id for p in game_state.players 
                       if p.is_alive and p.role.team != "werewolf"]
            if targets:
                target = random.choice(targets)  # 简单起见随机选择，后续可接入LLM决策
                return {"type": "kill", "target": target}
                
        elif self.role.role_type == "doctor":
            # 医生选择救人
            alive_players = [p.player_id for p in game_state.players if p.is_alive]
            if alive_players:
                # 简单起见随机选择，后续可接入LLM决策
                target = random.choice(alive_players)
                return {"type": "save", "target": target}
                
        elif self.role.role_type == "seer":
            # 预言家选择查验目标
            unknown_players = [p.player_id for p in game_state.players 
                             if p.is_alive and p.player_id != self.player_id]
            if unknown_players:
                target = random.choice(unknown_players)  # 简单起见随机选择
                return {"type": "check", "target": target}
                
        return None
    
    def _vote_action(self, valid_actions, game_state):
        """投票行动决策
        
        Args:
            valid_actions: 有效行动列表
            game_state: 当前游戏状态
            
        Returns:
            dict: 选择的行动
        """
        # 简单实现：随机投票
        # 后续可改为基于LLM的决策或更复杂的逻辑
        alive_players = [p.player_id for p in game_state.players 
                         if p.is_alive and p.player_id != self.player_id]
        if alive_players:
            target = random.choice(alive_players)
            return {"type": "vote", "target": target}
        return None