import re
from src.utils.config import LANGUAGE, PLAYER_NUMS
from src.utils.game_enum import GameRole, GamePhase


class GameRulePrompt:
    def __init__(self, players_num=PLAYER_NUMS, roles_list=['werewolf', 'werewolf', 'doctor', 'seer', 'villager', 'villager'], language=LANGUAGE):
        self.players_num = players_num
        self.roles_list = roles_list
        self.language = language

    def get_game_rules_prompt(self):
        game_rules_prompt_en = f""" """
        game_rules_prompt_cn = f"""你是一位擅长玩名为"狼人杀"的社交推理游戏的专家，你正在与其他{self.players_num - 1}名玩家一起玩这个游戏。这个游戏基于文字对话。以下是游戏规则：
- 游戏中有{self.players_num}个角色：{self.roles_list}。- 系统同时也是主持人，他组织了这个游戏，你需要正确回应他的指示。不要与系统交谈。游戏开始时，每位玩家会被分配一个隐藏身份，分为狼人阵营和村民阵营（预言家、医生、普通村民）。游戏中有两个回合："夜晚"回合和"白天"回合。游戏按夜晚回合与白天回合交替进行，直至一方获胜。-- 当是夜晚时：你与主持人的对话内容是保密的。你无需担心其他玩家知道你说什么和做什么。在夜晚，不用担心来自他人的怀疑。-- 在白天回合：你与所有玩家讨论，包括你的敌人。在讨论结束时，玩家们投票淘汰一名他们怀疑是狼人的玩家。得票最多的玩家将被淘汰。如果一名玩家被杀死，他将不能再做任何事情并退出游戏。
- 角色：-- 狼人，互相知道队友的身份，同时可以了解他的队友想要杀死谁。狼人们应该基于分析投票选择一名玩家杀死。在所有狼人投票后，获得最多票数的玩家将被杀死。如果没有达成共识，则没有人会被杀死！-- 医生，可以选择任何一位活着的玩家（包括医生自己）进行治疗。如果医生的治疗目标也是狼人今晚的攻击目标，被击杀玩家将存活下来。如果医生的治疗目标不是狼人的攻击目标，那医生的治疗将不会有效果。如果医生的治疗目标是一个自杀的狼人，医生的治疗会使这名狼人复活。-- 预言家，可以每晚验证一名玩家是否为狼人，这是非常重要的。-- 村民，在夜晚不能做任何事情。
- 目标：-- 如果玩家的阵营是"狼人"，他的目标是与其他狼人合作，最终杀死所有非狼人玩家。注意狼人都属于狼人阵营，他们有相同的目标。-- 如果玩家的阵营是"村民"，村民阵营玩家需要一起杀死所有狼人。注意村民、预言家和医生都属于村民阵营，他们有相同的目标。
- 提示：-- 为了完成目标，在夜晚回合，每位玩家应该分析并正确使用角色的能力。在白天回合，玩家需要仔细推理其他玩家的角色，除非是在欺骗其他玩家，否则不要随意透露自己的角色。做决定/投票时只给出玩家ID，不要生成其他玩家的对话。基于观察到的事实进行推理，玩家不能感知文本以外的其他任何信息（如声音信息）。-- 玩家可以假装为其他角色（Role），但不可以假装为其他玩家（Player）或主持人（Host）。"""

        if self.language == "en":
            return game_rules_prompt_en
        else:
            return game_rules_prompt_cn

    def get_role_prompt(self, player_id, role):
        game_rule_prompt = self.get_game_rules_prompt()
        if role == GameRole.WEREWOLF:
            role_prompt = WerewolfRolePrompt(
                player_id).get_werewolf_rule_prompt()
        elif role == GameRole.DOCTOR:
            role_prompt = WerewolfRolePrompt(
                player_id).get_doctor_rule_prompt()
        elif role == GameRole.SEER:
            role_prompt = WerewolfRolePrompt(player_id).get_seer_rule_prompt()
        elif role == GameRole.VILLAGER:
            role_prompt = WerewolfRolePrompt(
                player_id).get_villager_rule_prompt()
        else:
            raise ValueError(f"Unknown role: {role}")

        prompt = f"""全局游戏规则提示：{game_rule_prompt}\n角色游戏规则提示：{role_prompt}\n"""

        return prompt

    def get_night_action_prompt(self, role, day_count, player_id, werewolf_partners=None):
        if role == GameRole.WEREWOLF:
            action = "kill"
            if werewolf_partners is not None:
                prompt_en = f""" """
                prompt_cn = f"""现在是第{day_count}天的夜晚回合，你（和你的队友）应该选择一名玩家进行{action}。你的狼人同伙是玩家{werewolf_partners}。作为玩家{player_id}和一名{role.value}，你应该先分析当前局势，然后执行一个动作。\n{self.get_response_format_prompt(GameRole.WEREWOLF)}"""
            elif werewolf_partners is None:
                prompt_en = f""" """
                prompt_cn = f"""现在是第{day_count}天的夜晚回合，你应该选择一名玩家进行{action}。作为玩家{player_id}和一名{role.value}，你应该先分析当前局势，然后执行一个动作。\n{self.get_response_format_prompt(GameRole.WEREWOLF)}"""
        elif role == GameRole.DOCTOR:
            action = "save"
            prompt_en = f""" """
            prompt_cn = f"""现在是第{day_count}天的夜晚回合，你应该选择一名玩家进行{action}。作为玩家{player_id}和一名{role.value}，你应该先分析当前局势，然后执行一个动作。\n{self.get_response_format_prompt(GameRole.DOCTOR)}"""
        elif role == GameRole.SEER:
            action = "see"
            prompt_en = f""" """
            prompt_cn = f"""现在是第{day_count}天的夜晚回合，你应该选择一名玩家进行{action}。作为玩家{player_id}和一名{role.value}，你应该先分析当前局势，然后执行一个动作。\n{self.get_response_format_prompt(GameRole.SEER)}"""

        if self.language == "en":
            return prompt_en
        else:
            return prompt_cn

    def get_last_night_info_prompt(self, current_day, killed_player, alive_players_id):
        if killed_player is None:
            last_night_info_prompt_cn = f"""\n当前是第{current_day}天白天回合，昨夜没有人被杀死。存活玩家有{len(alive_players_id)}名，分别是：{alive_players_id}"""
        else:
            last_night_info_prompt_cn = f"""\n当前是第{current_day}天白天回合，昨夜被杀死的玩家是：{killed_player}。目前存活玩家有{len(alive_players_id)}名，分别是：{alive_players_id}"""
        return last_night_info_prompt_cn

    def get_phase_prompt(self, day_count, phase, alive_players):
        if self.language == "cn":
            if phase == GamePhase.NIGHT:
                current_phase = "'夜晚'阶段"
            elif phase == GamePhase.DAY:
                current_phase = "'白天'阶段"
            elif phase == GamePhase.VOTE:
                current_phase = "'投票'阶段"
        elif self.language == "en":
            if phase == GamePhase.NIGHT:
                current_phase = "'Night' phase"
            elif phase == GamePhase.DAY:
                current_phase = "'Day' phase"
            elif phase == GamePhase.VOTE:
                current_phase = "'Vote' phase"

        phase_prompt_cn = f"""现在是游戏的第{day_count}天，当前游戏阶段是{current_phase}, 当前存活玩家有{len(alive_players)}名，分别是：{alive_players}"""
        phase_prompt_en = f"""It's day {day_count} of the game, the current game phase is {current_phase}, and there are {len(alive_players)} players still alive: {alive_players}."""
        if self.language == "en":
            return phase_prompt_en
        elif self.language == "cn":
            return phase_prompt_cn

    def get_response_format_prompt(self, role):
        if role == GameRole.WEREWOLF:
            action = "kill"
        elif role == GameRole.DOCTOR:
            action = "save"
        elif role == GameRole.SEER:
            action = "see"
        else:
            raise ValueError(f"Unknown role: {role}")

        response_format_prompt_cn = f"""你应该只以下面描述的JSON格式回应。回应格式：
{{
    "reasoning": "对当前局势的分析",
    "action": "{action}",
    "target": "ID_X"
}}
确保回应可以被Python的json.loads解析。"""

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

    def get_day_discuss_prompt(self, day, id, role):
        prompt = f"""现在是第{day}天的白天（DAY）讨论阶段，轮到你发言。作为玩家{id}且身份是{role}，在向其他玩家发言前，你应当先自行分析当前局势，然后向所有其他玩家发表意见。请严格按以下 JSON 格式回应:
{{
"reasoning": "仅对自己分析的当前局势推理", 
"statement": "向所有其他玩家发表的言论"
}}
确保回应可以被Python的json.loads解析。"""
        return prompt

    def get_vote_prompt(self, day, id, role):
        prompt = f"""现在是第{day}天投票(VOTE)阶段。你应该投票给一名玩家,或者不投票,以最大化狼人的利益(对于狼人阵营（WEREWOLVES）来说)/你应该投票给最有可能是狼人的一名玩家,或者不投票(对于村民阵营(VILLAGERS)来说)。作为玩家{id}且身份是{role}，你应当先分析当前局势，然后选择一个动作：'no vote'/'vote'。请严格按以下JSON 格式回应:
{{
"reasoning": "对当前局势的推理", 
""action":": "vote / no vote",
"target": "ID_X / None"
}}
确保回应可以被Python的json.loads解析。
"""
        return prompt


class WerewolfRolePrompt:
    def __init__(self, player_id, language=LANGUAGE):
        self.player_id = player_id
        self.language = language

    def _get_player_id_prompt(self):
        """
        返回玩家ID的提示词

        :return: str
        """
        if self.language == "cn":
            return f"""你是玩家 {self.player_id}，"""
        elif self.language == "en":
            return f"""Your player id is {self.player_id}, """
        else:
            raise ValueError(f"Unsupported language: {self.language}")

    def get_doctor_rule_prompt(self):
        """
        返回医生角色的规则提示词
        :return: str
        """
        base_prompt = self._get_player_id_prompt()
        doctor_rule_prompt_cn = base_prompt + f"""你的角色是医生。每到夜晚阶段，当到你（医生）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（包括自己）进行救治。如果你选择的救治目标，同时是今夜狼人的猎杀目标，那么这名玩家将会幸存下来，即不会被狼人杀死。如果你选择的救治目标，不是狼人的猎杀目标，那么你的救治将会无效。如果你选择的救治目标，是自杀的狼人，那么你将会救活狼人。结束你的选择后，你的回合就结束了，你将会再次进入睡眠状态，等待天亮。等待天亮后，你将会被唤醒，接着你可以参与讨论。若这一夜中有人被医生救活，还存活的玩家将在白天开始时被告知：“有人得救了”。"""
        doctor_rule_prompt_en = base_prompt + f""" """
        if self.language == "en":
            return doctor_rule_prompt_en
        else:
            return doctor_rule_prompt_cn

    def get_seer_rule_prompt(self):
        base_prompt = self._get_player_id_prompt()
        seer_rule_prompt_cn = base_prompt + f"""你的角色是预言家。每到夜晚阶段，当到你（预言家）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（除了自己）进行身份查验。如果你选择的查验目标是狼人，即非村民阵营角色，那么你将会得知这名玩家的角色属于狼人阵营。如果你选择的查验目标不是狼人，即非狼人阵营角色，那么你将会得知这名玩家的角色属于村民阵营。结束你的查验后，你（预言家）掌握了可以用来说服村民的信息，接着你的回合就结束了，你将会再次进入睡眠状态，等待天亮。等待天亮后，你将会被唤醒，接着你可以参与讨论。"""
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
        villager_rule_prompt_cn = base_prompt + \
            f"""你的角色是村民。你在整个夜晚阶段都将保持睡眠状态，且不会知道任何夜晚阶段发生的事情。等待天亮后，你将会被唤醒，接着你可以参与讨论。"""
        villager_rule_prompt_en = base_prompt + f"""Your role is Villager.
You will remain asleep throughout the night phase and won't know about anything that happens during that time.
When morning comes, you will be awakened and can participate in discussions."""
        if self.language == "en":
            return villager_rule_prompt_en
        else:
            return villager_rule_prompt_cn

    def get_werewolf_rule_prompt(self):
        base_prompt = self._get_player_id_prompt()
        werewolf_rule_prompt_cn = base_prompt + f"""你的角色是狼人。每到夜晚阶段，当到你（狼人）的回合时，在场还存活着的狼人将被唤醒，接着狼人们可以达成共识选择击杀任意一名还存活的玩家（包括狼人自己）。如果在场仅剩下一名狼人，这名狼人是你的话，那么你（狼人）将选择击杀任意一名还存活的玩家（包括你自己）。当狼人阵营选定受害者后，接着你的回合就结束了，你将会再次进入睡眠状态，等待天亮。等待天亮后，你将会被唤醒，接着你可以参与讨论。夜晚阶段被击杀的玩家将会被宣布。"""
        werewolf_rule_prompt_en = base_prompt + f"""Your role is Werewolf. Every night, when it's your turn, all surviving werewolves will be awakened. Then the werewolves can reach a consensus to kill any living player (including werewolves themselves).
If there is only one werewolf left in the game and it's you, then you (the Werewolf) will choose to kill any surviving player (including yourself). After the werewolf faction selects a victim, your turn ends and you will fall asleep again, waiting for dawn.
When morning comes, you will be awakened and can participate in discussions. Players killed during the night phase will be announced."""
        if self.language == "en":
            return werewolf_rule_prompt_en
        else:
            return werewolf_rule_prompt_cn
