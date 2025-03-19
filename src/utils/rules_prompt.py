class WerewolfPrompt():
    def __init__(self, roles_list, players_num, player_id, player_role):
        self.roles_list = roles_list
        self.players_num = players_num
        self.player_id = player_id
        self.player_role = player_role

    def get_game_rules_prompt(self, language="en"):
        game_rules_prompt_en = f"""
        You are playing a game called the Werewolf with some other players. This game is based on text conversations. Here are the game rules: 
        - Roles: 
        -- The moderator is also host, he organized this game and you need to answer his instructions correctly. Don't talk with the moderator. There are {self.players_num} roles in the game: {self.roles_list}. 
        -- There are two alternate phases in this game, night time phase and day time phase. When it's night: Your talking content with moderator is confidential. You needn't worry about other players and moderator knowing what you say and do. No need to worry about suspicions from others during the night. 
        -- If you are werewolf, you can know what your teammates want to kill and you should vote one player to kill based on your analysis. Player who receives the most votes after all werewolves voting will be killed. No one will be killed if there is no consensus! 
        -- If you are witch, you have a bottle of antidote that can save a player targeted by werewolves after dark, and a bottle of poison that can poison a player after dark. Both poison and antidote can be used only once. 
        -- If you are seer, you can verify whether a player is a werewolf every night, which is a very important thing. 
        -- If you are guard, you can protect a player every night to prevent the player from being killed by werewolves, but guard cannot resist the witch's poison and guard cannot protect the same player on two consecutive nights. 
        -- If you are villager, you can't do anything at night. 
        -- During the day time: you discuss with all players including your enemies. At the end of the discussion, players vote to eliminate one player they suspect of being a werewolf. The player with the most votes will be eliminated. The moderator will tell who is killed, otherwise there is no one killed. 
        -- Note that villager, seer, guard and witch are all in villager side, they have the same objective. 

        - Objectives: 
        -- If your faction is 'WEREWOLF', your goal is to cooperate with other werewolves to kill all players who are not werewolves at last. 
        -- If your faction is 'VILLAGER', you need to kill all werewolves with your partner once you find out that certain players are suspicious to be werewolves. This could greatly improve your chances of winning, although it is somewhat risky.If one player is killed, he can't do anything anymore and will be out of the game. 

        - Tips: 
        -- To complete the objective, during night time, you should analyze and use your ability correctly. During day time, you need to reason carefully about the roles of other players and be careful not to reveal your own role casually unless you're cheating other players. Only give the player's name when making a decision/voting, and don't generate other players' conversation.Reasoning based on facts you have observed and you cannot perceive information (such as acoustic info) other than text. You are Player {self.player_id}, the {self.player_role}. You're playing with {self.players_num - 1} other players. Do not pretend you are other players or the moderator. Always end your response with'<EOS>'.
        """

        if language == "en":
            return game_rules_prompt_en
        else:
            return game_rules_prompt_en
    
    def get_doctor_rule_prompt(self):
        doctor_rule_prompt_cn = f"""
        你的角色是医生。
        每到夜晚阶段，当到你（医生）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（包括自己）进行救治。
        如果你选择的救治目标，同时是今夜狼人的猎杀目标，那么这名玩家将会幸存下来，即不会被狼人杀死。
        如果你选择的救治目标，不是狼人的猎杀目标，那么你的救治将会无效。
        如果你选择的救治目标，是自杀的狼人，那么你将会救活狼人。
        结束你的选择后，你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        若这一夜中有人被医生救活，还存活的玩家将在白天开始时被告知：“有人得救了。
        """
        return doctor_rule_prompt_cn
    
    def get_seer_rule_prompt(self):
        seer_rule_prompt_cn = f"""
        你的角色是预言家。
        每到夜晚阶段，当到你（预言家）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（除了自己）进行身份查验。
        如果你选择的查验目标是狼人，即非村民阵营角色，那么你将会得知这名玩家的角色属于狼人阵营。
        如果你选择的查验目标不是狼人，即非狼人阵营角色，那么你将会得知这名玩家的角色属于村民阵营。
        结束你的查验后，你（预言家）掌握了可以用来说服村民的信息，接着你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        """
        return seer_rule_prompt_cn
    
    def get_villager_rule_prompt(self):
        villager_rule_prompt_cn = f"""
        你的角色是村民。
        你在整个夜晚阶段都将保持睡眠状态，且不会知道任何夜晚阶段发生的事情。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        """
        return villager_rule_prompt_cn

    def get_werewolf_rule_prompt(self):
        werewolf_rule_prompt_cn = f"""
        你的角色是预言家。
        每到夜晚阶段，当到你（预言家）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（除了自己）进行身份查验。
        如果你选择的查验目标是狼人，即非村民阵营角色，那么你将会得知这名玩家的角色属于狼人阵营。
        如果你选择的查验目标不是狼人，即非狼人阵营角色，那么你将会得知这名玩家的角色属于村民阵营。
        结束你的查验后，你（预言家）掌握了可以用来说服村民的信息，接着你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        """
        return werewolf_rule_prompt_cn
