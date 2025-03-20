class WerewolfPrompt():
    def __init__(self, roles_list, players_num, player_id, language='cn'):
        self.roles_list = roles_list
        self.players_num = players_num
        self.player_id = player_id
        self.language = language

    def get_game_rules_prompt(self):
        game_rules_prompt_en = f"""
        You are playing a game called the Werewolf with some other players. This game is based on text conversations. Here are the game rules: 
        - There are {self.players_num} roles in the game: {self.roles_list}. You're playing with {self.players_num - 1} other players.
        - The System is also host, he organized this game and you need to answer his instructions correctly. Don't talk with the System. 
        - There are two alternate rounds in this game, "Night" round and "Day" round. 
        -- When it's night: Your talking content with System is confidential. You needn't worry about other players and System knowing what you say and do. No need to worry about suspicions from others during the night.
        -- During the Day round: you discuss with all players including your enemies. At the end of the discussion, players vote to eliminate one player they suspect of being a werewolf. The player with the most votes will be eliminated. The System will tell who is killed, otherwise there is no one killed. 

        - Roles: 
        -- If you are werewolf, you can know what your teammates want to kill and you should vote one player to kill based on your analysis. Player who receives the most votes after all werewolves voting will be killed. No one will be killed if there is no consensus! 
        -- If you are doctor, you can choose any living player (including yourself) to heal. If your healing target is also the werewolves' attack target tonight, he will survive. If your healing target is not the werewolves' attack target, your healing will have no effect. If your healing target is a werewolf who committed suicide, you will revive them. 
        -- If you are seer, you can verify whether a player is a werewolf every night, which is a very important thing. 
        -- If you are villager, you can't do anything at night. 

        - Objectives: 
        -- If your faction is 'WEREWOLF', your goal is to cooperate with other werewolves to kill all players who are not werewolves at last. Note that werewolf are all in WEREWOLF side, they have the same objective. 
        -- If your faction is 'VILLAGER', you need to kill all werewolves with your partner once you find out that certain players are suspicious to be werewolves. This could greatly improve your chances of winning, although it is somewhat risky.If one player is killed, he can't do anything anymore and will be out of the game. Note that villager, seer and doctor are all in VILLAGER side, they have the same objective. 

        - Tips: 
        -- To complete the objective, during Night round, you should analyze and use your ability correctly. During Day round, you need to reason carefully about the roles of other players and be careful not to reveal your own role casually unless you're cheating other players. Only give the player's ID when making a decision/voting, and don't generate other players' conversation.Reasoning based on facts you have observed and you cannot perceive information (such as acoustic info) other than text. Do not pretend you are other players or the System. Always end your response with'<EOS>'.

        """

        game_rules_prompt_cn = f"""
        你正在玩一个叫做狼人杀的游戏，与其他玩家一起。这个游戏基于文字对话。以下是游戏规则：
        - 游戏中有{self.players_num}个角色：{self.roles_list}。你与其他{self.players_num - 1}名玩家一起游戏。
        - 系统同时也是主持人，他组织了这个游戏，你需要正确回应他的指示。不要与系统交谈。
        - 游戏中有两个交替的回合，"夜晚"回合和"白天"回合。
        -- 当是夜晚时：你与系统的对话内容是保密的。你无需担心其他玩家和系统知道你说什么和做什么。在夜晚，不用担心来自他人的怀疑。
        -- 在白天回合：你与所有玩家讨论，包括你的敌人。在讨论结束时，玩家们投票淘汰一名他们怀疑是狼人的玩家。得票最多的玩家将被淘汰。系统会告知谁被杀死，否则就是没有人被杀死。

        - 角色：
        -- 如果你是狼人，你可以了解你的队友想要杀死谁，并且你应该基于你的分析投票选择一名玩家杀死。在所有狼人投票后，获得最多票数的玩家将被杀死。如果没有达成共识，则没有人会被杀死！
        -- 如果你是医生，你可以选择任何一位活着的玩家（包括你自己）进行治疗。如果你的治疗目标也是狼人今晚的攻击目标，他将存活下来。如果你的治疗目标不是狼人的攻击目标，你的治疗将不会有效果。如果你的治疗目标是一个自杀的狼人，你会使他复活。
        -- 如果你是预言家，你可以每晚验证一名玩家是否为狼人，这是非常重要的。
        -- 如果你是村民，你在夜晚不能做任何事情。

        - 目标：
        -- 如果你的阵营是"狼人"，你的目标是与其他狼人合作，最终杀死所有非狼人玩家。注意狼人都属于狼人阵营，他们有相同的目标。
        -- 如果你的阵营是"村民"，你需要与你的伙伴一起杀死所有狼人，一旦你发现某些玩家可疑是狼人。这将大大提高你获胜的机会，尽管这有些风险。如果一名玩家被杀死，他将不能再做任何事情并退出游戏。注意村民、预言家和医生都属于村民阵营，他们有相同的目标。

        - 提示：
        -- 为了完成目标，在夜晚回合，你应该分析并正确使用你的能力。在白天回合，你需要仔细推理其他玩家的角色，除非你是在欺骗其他玩家，否则不要随意透露自己的角色。做决定/投票时只给出玩家ID，不要生成其他玩家的对话。基于你观察到的事实进行推理，你不能感知文本以外的信息（如声音信息）。不要假装你是其他玩家或系统。始终以"<EOS>"结束你的回应。
        """

        if self.language == "en":
            return game_rules_prompt_en
        else:
            return game_rules_prompt_cn

    def _get_player_id_prompt(self):
        if self.language == "en":
            return f"""Your player id is {self.player_id}, """
        else:
            return f"""你是玩家 {self.player_id}，"""

    def get_doctor_rule_prompt(self):
        base_prompt = self._get_player_id_prompt
        doctor_rule_prompt_cn = base_prompt + f"""
        你的角色是医生。
        每到夜晚阶段，当到你（医生）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（包括自己）进行救治。
        如果你选择的救治目标，同时是今夜狼人的猎杀目标，那么这名玩家将会幸存下来，即不会被狼人杀死。
        如果你选择的救治目标，不是狼人的猎杀目标，那么你的救治将会无效。
        如果你选择的救治目标，是自杀的狼人，那么你将会救活狼人。
        结束你的选择后，你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        若这一夜中有人被医生救活，还存活的玩家将在白天开始时被告知：“有人得救了。
        """
        doctor_rule_prompt_en = base_prompt + f"""
        Your role is Doctor.
        Every night, when it's your turn, you will be awakened. Then you can choose any living player (including yourself) to heal.
        If your healing target is also the werewolves' attack target tonight, he will survive, i.e., not be killed by the werewolves.
        If your healing target is not the werewolves' attack target, your healing will have no effect.
        If your healing target is a werewolf who committed suicide, you will revive them.
        After you make your choice, your turn ends and you will fall asleep again, waiting for dawn.
        When morning comes, you will be awakened and can participate in discussions.
        If someone was saved by the doctor during the night, all living players will be informed at the beginning of the day: "Someone was saved."
        """
        if self.language == "en":
            return doctor_rule_prompt_en
        else:
            return doctor_rule_prompt_cn

    def get_seer_rule_prompt(self):
        base_prompt = self._get_player_id_prompt
        seer_rule_prompt_cn = base_prompt + f"""
        你的角色是预言家。
        每到夜晚阶段，当到你（预言家）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（除了自己）进行身份查验。
        如果你选择的查验目标是狼人，即非村民阵营角色，那么你将会得知这名玩家的角色属于狼人阵营。
        如果你选择的查验目标不是狼人，即非狼人阵营角色，那么你将会得知这名玩家的角色属于村民阵营。
        结束你的查验后，你（预言家）掌握了可以用来说服村民的信息，接着你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        """
        seer_rule_prompt_en = base_prompt + f"""
        Your role is Seer.
        Every night, when it's your turn, you will be awakened. Then you can choose any living player (except yourself) to verify their identity.
        If your verification target is a werewolf, i.e., not in the villager faction, you will learn that this player belongs to the werewolf faction.
        If your verification target is not a werewolf, i.e., not in the werewolf faction, you will learn that this player belongs to the villager faction.
        After your verification, you (the Seer) have information that can be used to convince villagers. Then your turn ends and you will fall asleep again, waiting for dawn.
        When morning comes, you will be awakened and can participate in discussions.
        """
        if self.language == "en":
            return seer_rule_prompt_en
        else:
            return seer_rule_prompt_cn

    def get_villager_rule_prompt(self):
        base_prompt = self._get_player_id_prompt()  # 注意这里添加了()调用函数
        villager_rule_prompt_cn = base_prompt + f"""
        你的角色是村民。
        你在整个夜晚阶段都将保持睡眠状态，且不会知道任何夜晚阶段发生的事情。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        """
        villager_rule_prompt_en = base_prompt + f"""
        Your role is Villager.
        You will remain asleep throughout the night phase and won't know about anything that happens during that time.
        When morning comes, you will be awakened and can participate in discussions.
        """
        if self.language == "en":
            return villager_rule_prompt_en
        else:
            return villager_rule_prompt_cn

    def get_werewolf_rule_prompt(self):
        base_prompt = self._get_player_id_prompt()  # 注意这里添加了()调用函数
        werewolf_rule_prompt_cn = base_prompt + f"""
        你的角色是狼人。
        每到夜晚阶段，当到你（狼人）的回合时，在场还存活着的狼人将被唤醒，接着狼人们可以达成共识选择杀害任意一名还存活的玩家（包括狼人自己）。
        如果在场仅剩下一名狼人，这名狼人是你的话，那么你（狼人）将选择杀害任意一名还存活的玩家（包括你自己）。
        当狼人阵营选定受害者后，接着你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        夜晚阶段被杀害的玩家将会被宣布。
        """
        werewolf_rule_prompt_en = base_prompt + f"""
        Your role is Werewolf.
        Every night, when it's your turn, all surviving werewolves will be awakened. Then the werewolves can reach a consensus to kill any living player (including werewolves themselves).
        If there is only one werewolf left in the game and it's you, then you (the Werewolf) will choose to kill any surviving player (including yourself).
        After the werewolf faction selects a victim, your turn ends and you will fall asleep again, waiting for dawn.
        When morning comes, you will be awakened and can participate in discussions.
        Players killed during the night phase will be announced.
        """
        if self.language == "en":
            return werewolf_rule_prompt_en
        else:
            return werewolf_rule_prompt_cn
