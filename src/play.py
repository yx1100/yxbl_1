import random
from agents.llm_agent import LLMAgent
from agents.human_agent import HumanAgent


def setup_game(player_count=6):
    # 设置游戏环境和玩家
    # 计算村民数量
    villagers_count = player_count - 4  # 1 doctor, 2 werewolves, 1 seer
    if villagers_count < 0:
        raise ValueError(
            "Player count must be at least 4 to have all required roles")

    # 创建角色列表
    player_role_list = ['doctor'] + ['werewolf'] * \
        2 + ['seer'] + ['villager'] * villagers_count
    # 随机打乱角色列表
    random.shuffle(player_role_list)

    # 创建玩家ID列表,格式为"ID_X"。
    player_id_list = [f"ID_{i}" for i in range(1, player_count + 1)]

    # 随机选择一个ID作为人类玩家
    human_player_id = random.choice(player_id_list)

    # 创建玩家代理
    agents = []
    for player_id, role in zip(player_id_list, player_role_list):
        # 根据角色确定阵营
        faction = "WEREWOLVES" if role == "werewolf" else "VILLAGERS"

        # 根据ID创建人类或AI代理
        if player_id == human_player_id:
            # agent = HumanAgent(player_id=player_id, role=role, faction=faction)
            agent = LLMAgent(player_id=player_id, role=role, faction=faction)
        else:
            agent = LLMAgent(player_id=player_id, role=role, faction=faction)
        agents.append(agent)

    return player_role_list, player_id_list, human_player_id, agents


def main():
    a, b, c, agents = setup_game()

    for agent in agents:
        print(
            f"Player ID: {agent.player_id}, Role: {agent.role}, Faction: {agent.faction}, Human/AI: {agent.human_or_ai}")
        if agent.human_or_ai == "AI":
            agent_prompt = agent.client.messages
            print(agent_prompt)
            response = agent.client.get_response(input_messages=agent_prompt)
            if response["success"]:
                print(response["content"],'\n')
            else:
                print(response["error"])


if __name__ == "__main__":
    main()
