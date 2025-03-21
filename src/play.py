from src.environment.game_manager import GameManager


def main():
    game_manager = GameManager()
    game_manager.setup_game()

    agents = game_manager.game_agents

    for agent in agents:
        print(
            f"Player ID: {agent.player_id}, Role: {agent.role}, Faction: {agent.faction}, Human/AI: {agent.human_or_ai}")
        if agent.human_or_ai == "AI":
            agent_prompt = agent.client.messages
            print(agent_prompt)
            response = agent.client.get_response(input_messages=agent_prompt)
            if response["success"]:
                print(response["content"], '\n')
            else:
                print(response["error"])


if __name__ == "__main__":
    main()
