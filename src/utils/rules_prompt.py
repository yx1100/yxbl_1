class WerewolfRolePrompt:
    def __init__(self, player_id, language='cn'):
        self.player_id = player_id
        self.language = language

    def _get_player_id_prompt(self):
        if self.language == "en":
            return f"""Your player id is {self.player_id}, """
        else:
            return f"""你是玩家 {self.player_id}，"""

    def get_doctor_rule_prompt(self):
        base_prompt = self._get_player_id_prompt()
        doctor_rule_prompt_cn = base_prompt + f"""你的角色是医生。
每到夜晚阶段，当到你（医生）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（包括自己）进行救治。
如果你选择的救治目标，同时是今夜狼人的猎杀目标，那么这名玩家将会幸存下来，即不会被狼人杀死。
如果你选择的救治目标，不是狼人的猎杀目标，那么你的救治将会无效。
如果你选择的救治目标，是自杀的狼人，那么你将会救活狼人。
结束你的选择后，你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
等待天亮后，你将会被唤醒，接着你可以参与讨论。
若这一夜中有人被医生救活，还存活的玩家将在白天开始时被告知：“有人得救了。"""
        doctor_rule_prompt_en = base_prompt + f"""Your role is Doctor.
Every night, when it's your turn, you will be awakened. Then you can choose any living player (including yourself) to heal.
If your healing target is also the werewolves' attack target tonight, he will survive, i.e., not be killed by the werewolves.
If your healing target is not the werewolves' attack target, your healing will have no effect.
If your healing target is a werewolf who committed suicide, you will revive them.
After you make your choice, your turn ends and you will fall asleep again, waiting for dawn.
When morning comes, you will be awakened and can participate in discussions.
If someone was saved by the doctor during the night, all living players will be informed at the beginning of the day: "Someone was saved." """
        if self.language == "en":
            return doctor_rule_prompt_en
        else:
            return doctor_rule_prompt_cn

    def get_seer_rule_prompt(self):
        base_prompt = self._get_player_id_prompt()
        seer_rule_prompt_cn = base_prompt + f"""你的角色是预言家。
每到夜晚阶段，当到你（预言家）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（除了自己）进行身份查验。
如果你选择的查验目标是狼人，即非村民阵营角色，那么你将会得知这名玩家的角色属于狼人阵营。
如果你选择的查验目标不是狼人，即非狼人阵营角色，那么你将会得知这名玩家的角色属于村民阵营。
结束你的查验后，你（预言家）掌握了可以用来说服村民的信息，接着你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
等待天亮后，你将会被唤醒，接着你可以参与讨论。"""
        seer_rule_prompt_en = base_prompt + f"""Your role is Seer.
Every night, when it's your turn, you will be awakened. Then you can choose any living player (except yourself) to verify their identity.
If your verification target is a werewolf, i.e., not in the villager faction, you will learn that this player belongs to the werewolf faction.
If your verification target is not a werewolf, i.e., not in the werewolf faction, you will learn that this player belongs to the villager faction.
After your verification, you (the Seer) have information that can be used to convince villagers. Then your turn ends and you will fall asleep again, waiting for dawn.
When morning comes, you will be awakened and can participate in discussions."""
        if self.language == "en":
            return seer_rule_prompt_en
        else:
            return seer_rule_prompt_cn

    def get_villager_rule_prompt(self):
        base_prompt = self._get_player_id_prompt()
        villager_rule_prompt_cn = base_prompt + f"""你的角色是村民。
你在整个夜晚阶段都将保持睡眠状态，且不会知道任何夜晚阶段发生的事情。
等待天亮后，你将会被唤醒，接着你可以参与讨论。"""
        villager_rule_prompt_en = base_prompt + f"""Your role is Villager.
You will remain asleep throughout the night phase and won't know about anything that happens during that time.
When morning comes, you will be awakened and can participate in discussions."""
        if self.language == "en":
            return villager_rule_prompt_en
        else:
            return villager_rule_prompt_cn

    def get_werewolf_rule_prompt(self):
        base_prompt = self._get_player_id_prompt()
        werewolf_rule_prompt_cn = base_prompt + f"""你的角色是狼人。
每到夜晚阶段，当到你（狼人）的回合时，在场还存活着的狼人将被唤醒，接着狼人们可以达成共识选择杀害任意一名还存活的玩家（包括狼人自己）。
如果在场仅剩下一名狼人，这名狼人是你的话，那么你（狼人）将选择杀害任意一名还存活的玩家（包括你自己）。
当狼人阵营选定受害者后，接着你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
等待天亮后，你将会被唤醒，接着你可以参与讨论。
夜晚阶段被杀害的玩家将会被宣布。"""
        werewolf_rule_prompt_en = base_prompt + f"""Your role is Werewolf.
Every night, when it's your turn, all surviving werewolves will be awakened. Then the werewolves can reach a consensus to kill any living player (including werewolves themselves).
If there is only one werewolf left in the game and it's you, then you (the Werewolf) will choose to kill any surviving player (including yourself).
After the werewolf faction selects a victim, your turn ends and you will fall asleep again, waiting for dawn.
When morning comes, you will be awakened and can participate in discussions.
Players killed during the night phase will be announced."""
        if self.language == "en":
            return werewolf_rule_prompt_en
        else:
            return werewolf_rule_prompt_cn


class GameRulePrompt:
    def __init__(self, players_num=6, roles_list=['werewolf', 'werewolf', 'doctor', 'seer', 'villager', 'villager'], language="cn"):
        self.players_num = players_num
        self.roles_list = roles_list
        self.language = language

    def get_game_rules_prompt(self):
        game_rules_prompt_en = f"""You are playing a game called Werewolf with other players. This game is based on text conversations. Here are the game rules:
- There are {self.players_num} roles in the game: {self.roles_list}. You are playing with {self.players_num - 1} other players.
- The System is also the host, organizing the game. You need to respond to its instructions correctly. Do not talk to the System.
- The game alternates between two phases: "Night" phase and "Day" phase.
-- During the Night phase: Your conversations with the host are private. You do not need to worry about other players knowing what you say or do. There is no suspicion from others during the night.
-- During the Day phase: You discuss with all players, including your enemies. At the end of the discussion, players vote to eliminate one player they suspect of being a werewolf. The player with the most votes will be eliminated. The host will announce who was eliminated, or if no one was eliminated.

- Roles:
-- Werewolf: You know the identities of your fellow werewolves and can discuss with them whom to eliminate. Werewolves should vote to kill one player based on analysis. The player with the most votes among the werewolves' choices will be eliminated. If there is no consensus, no one will be eliminated.
-- Doctor: You can choose any living player (including yourself) to heal. If your healing target is also the werewolves' attack target for the night, that player will survive. If your healing target is not the werewolves' attack target, your healing will have no effect. If your healing target is a werewolf who committed suicide, you will revive them.
-- Seer: You can verify whether a player is a werewolf each night. This is a critical ability for the game.
-- Villager: You cannot take any actions during the night.

- Objectives:
-- If you belong to the "Werewolf" faction, your goal is to cooperate with other werewolves to eliminate all players who are not werewolves. Note that all werewolves share the same objective.
-- If you belong to the "Villager" faction, your goal is to work with other villagers to eliminate all werewolves. Villagers, Seers, and Doctors all belong to the Villager faction and share the same objective.

- Tips:
-- To achieve your objective, during the Night phase, analyze the situation and use your abilities wisely. During the Day phase, reason carefully about the roles of other players. Unless you are trying to deceive others, avoid revealing your role casually. When making decisions or voting, only provide the player's ID and do not generate conversations for other players. Base your reasoning on observed facts, and do not perceive information beyond the text (e.g., auditory information).
-- You may pretend to be another role, but you cannot pretend to be another player or the host.
-- Always end your response with "<EOS>."
    """

        game_rules_prompt_cn = f"""你正在玩一个叫做狼人杀的游戏，与其他玩家一起。这个游戏基于文字对话。以下是游戏规则：
- 游戏中有{self.players_num}个角色：{self.roles_list}。你与其他{self.players_num - 1}名玩家一起游戏。
- 系统同时也是主持人，他组织了这个游戏，你需要正确回应他的指示。不要与系统交谈。
- 游戏中有两个交替的回合，"夜晚"回合和"白天"回合。
-- 当是夜晚时：你与主持人的对话内容是保密的。你无需担心其他玩家知道你说什么和做什么。在夜晚，不用担心来自他人的怀疑。
-- 在白天回合：你与所有玩家讨论，包括你的敌人。在讨论结束时，玩家们投票淘汰一名他们怀疑是狼人的玩家。得票最多的玩家将被淘汰。主持人会告知谁被杀死，否则就是没有人被杀死。
-- 如果一名玩家被杀死，他将不能再做任何事情并退出游戏。

- 角色：
-- 狼人，互相知道队友的身份，同时可以了解他的队友想要杀死谁。狼人们应该基于分析投票选择一名玩家杀死。在所有狼人投票后，获得最多票数的玩家将被杀死。如果没有达成共识，则没有人会被杀死！
-- 医生，可以选择任何一位活着的玩家（包括医生自己）进行治疗。如果医生的治疗目标也是狼人今晚的攻击目标，被杀害玩家将存活下来。如果医生的治疗目标不是狼人的攻击目标，那医生的治疗将不会有效果。如果医生的治疗目标是一个自杀的狼人，医生的治疗会使这名狼人复活。
-- 言家，可以每晚验证一名玩家是否为狼人，这是非常重要的。
-- 村民，在夜晚不能做任何事情。

- 目标：
-- 如果玩家的阵营是"狼人"，他的目标是与其他狼人合作，最终杀死所有非狼人玩家。注意狼人都属于狼人阵营，他们有相同的目标。
-- 如果玩家的阵营是"村民"，村民阵营玩家需要一起杀死所有狼人。注意村民、预言家和医生都属于村民阵营，他们有相同的目标。

- 提示：
-- 为了完成目标，在夜晚回合，每位玩家应该分析并正确使用角色的能力。在白天回合，玩家需要仔细推理其他玩家的角色，除非是在欺骗其他玩家，否则不要随意透露自己的角色。做决定/投票时只给出玩家ID，不要生成其他玩家的对话。基于观察到的事实进行推理，玩家不能感知文本以外的信息（如声音信息）。
-- 玩家可以假装为其他玩家角色，但不可以假装为其他玩家或主持人。"""

        if self.language == "en":
            return game_rules_prompt_en
        else:
            return game_rules_prompt_cn

    def get_night_action_prompt(self, role, day_count, player_id):
        action = ""
        if role == "Werewolf":
            action = "kill"
        elif role == "Doctor":
            action = "save"
        elif role == "Seer":
            action = "see"

        prompt_en = f"""Now it is the night round on the {day_count}th day, you (and your teammate) should choose one player to {action}. As player {player_id} and a {role}, you should first reason about the current situation, then perform an action."""
        prompt_cn = f"""现在是第{day_count}天的夜晚回合，你（和你的队友）应该选择一名玩家进行{action}。作为玩家{player_id}和一名{role}，你应该先分析当前局势，然后执行一个动作。"""

        if self.language == "en":
            return prompt_en
        else:
            return prompt_cn

    def get_phase_prompt(self, day_count, phase, alive_players):
        if self.language == "cn":
            if phase == "NIGHT":
                current_phase = "'夜晚'阶段"
            elif phase == "DAY":
                current_phase = "'白天'阶段"
            elif phase == "VOTE":
                current_phase = "'投票'阶段"
        elif self.language == "en":
            if phase == "NIGHT":
                current_phase = "'Night' phase"
            elif phase == "DAY":
                current_phase = "'Day' phase"
            elif phase == "VOTE":
                current_phase = "'Vote' phase"

        phase_prompt_cn = f"""现在是游戏的第{day_count}天，当前游戏阶段是{current_phase}, 当前存活玩家有{len(alive_players)}名，分别是：{alive_players}"""
        phase_prompt_en = f"""It's day {day_count} of the game, the current game phase is {current_phase}, and there are {len(alive_players)} players still alive: {alive_players}."""
        if self.language == "en":
            return phase_prompt_en
        elif self.language == "cn":
            return phase_prompt_cn

    def get_response_format_prompt(self, role):
        if role == "werewolf":
            action = "kill"
        elif role == "doctor":
            action = "save"
        elif role == "seer":
            action = "see"
        else:
            action = None

        response_format_prompt_cn = f"""你应该只以下面描述的JSON格式回应。回应格式：
{{
    "reasoning": "对当前局势的分析",
    "action": "{action}",
    "target": "ID_X"
}}
确保回应可以被Python的json.loads解析"""
        response_format_prompt_en = f"""You should only respond in JSON format as described below.
Response Format:
{{
"reasoning": "reason about the current situation",
"action": "{action}",
"target": "ID_X"
}}
Ensure the response can be parsed by Python json.loads"""

        if self.language == "en":
            return response_format_prompt_en
        else:
            return response_format_prompt_cn
