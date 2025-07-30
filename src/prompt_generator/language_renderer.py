import os
from typing import Dict, Optional

# 导入新架构的组件
from src.prompt_generator.action_space import ActionIntent
from src.utils.llm_client import LLMClient
from src.utils.game_enum import GameRole

# 意图到自然语言指令的映射
INTENT_TO_INSTRUCTION: Dict[ActionIntent, str] = {
    # 发言类
    ActionIntent.CLAIM_SEER: "宣称自己是预言家",
    ActionIntent.CLAIM_DOCTOR: "宣称自己是医生",
    ActionIntent.CLAIM_VILLAGER: "宣称自己是村民",
    ActionIntent.CLAIM_WEREWOLF: "（用一种令人信服的方式）宣称自己是狼人以混淆视听",
    ActionIntent.ACCUSE_PLAYER: "指控目标玩家是狼人",
    ActionIntent.DEFEND_PLAYER: "为目标玩家辩护，声称其是好人",
    ActionIntent.QUESTION_PLAYER: "质疑目标玩家的发言或行为",
    ActionIntent.SHARE_INFO: "分享一个关键信息（比如查验结果）",
    ActionIntent.STAY_NEUTRAL: "发表一段中立、划水的言论以隐藏自己的真实想法",
    # 投票和夜晚行动意图通常不会直接生成发言，但可以保留用于其他目的
    ActionIntent.VOTE_PLAYER: "准备投票给目标玩家",
    ActionIntent.NIGHT_ACTION_KILL: "夜晚行动：击杀目标玩家",
    ActionIntent.NIGHT_ACTION_HEAL: "夜晚行动：治疗目标玩家",
    ActionIntent.NIGHT_ACTION_CHECK: "夜晚行动：查验目标玩家",
}


def generate_utterance(
    game_history: str,
    persona: str,
    intent: ActionIntent,
    target_player_id: Optional[int] = None,
    style: str = "自然且符合角色的",
    api_key: Optional[str] = None,
    model: str = "qwen-max"
) -> str:
    """
    语言渲染器：接收小模型输出的“动作-意图”，调用云端大模型API，生成自然语言发言。

    Args:
        game_history (str): 游戏到目前为止的完整历史记录。
        persona (str): 对大模型扮演角色的详细描述 (e.g., "你是一个正在隐藏身份的狼人...")。
        intent (ActionIntent): 小模型选择的决策意图。
        target_player_id (Optional[int]): 意图所指向的目标玩家ID。
        style (str): 对发言风格的要求 (e.g., "强硬且自信的", "旁敲侧击的")。
        api_key (Optional[str]): API密钥，如果为None，则从环境变量读取。
        model (str): 使用的大模型名称。

    Returns:
        str: 大模型生成的自然语言发言。
    """
    # 1. 初始化LLM客户端
    client = LLMClient(api_key=api_key, model=model)

    # 2. 构建决策意图指令
    intent_instruction = INTENT_TO_INSTRUCTION.get(intent, "执行一个未知动作")
    if target_player_id is not None:
        intent_instruction = intent_instruction.replace("目标玩家", f"玩家{target_player_id}")

    # 3. 构建系统消息 (System Prompt)，融合角色、意图和风格
    system_prompt = f"""
你是一个狼人杀游戏的顶级玩家，请严格按照以下指令进行角色扮演。

# 你的角色和任务 (Persona):
{persona}

# 你的核心策略意图 (Strategic Intent):
你的下一个发言需要达成的核心策略意图是：**{intent_instruction}**。

# 你的发言风格 (Style):
你的语气和风格必须是**{style}**。

请直接生成你的发言内容，不要包含任何解释、分析或如 "好的，这是我的发言：" 等额外文本。
"""

    # 4. 构建用户消息 (User Prompt)，提供上下文
    user_prompt = f"""
这是到目前为止的游戏历史记录，请仔细阅读以了解上下文：
---
{game_history}
---

现在，基于你的角色、策略意图和风格要求，生成你接下来要说的下一段话。
"""

    # 5. 构造消息列表并调用API
    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_prompt.strip()}
    ]

    response = client.get_response(messages)

    if response["success"]:
        return response["content"].strip()
    else:
        print(f"调用大模型API时发生错误: {response['error']}")
        # 在真实应用中，这里可以返回一个备用发言或抛出异常
        return f"（出现错误，无法生成发言。意图：{intent_instruction}）"


# --- 示例用法 ---
if __name__ == '__main__':
    # 假设的游戏场景
    sample_history = """
第一天白天：
玩家1发言：我觉得大家可以先报一下身份，我是个村民，希望能找到狼人。
玩家2发言：我是预言家，昨晚查了3号，他是好人。
玩家3发言：2号说得对，我是个好人，我觉得4号发言很奇怪。
...
第一天投票：玩家4被投票出局。
第一夜：无人死亡。
第二天白天：
玩家2发言：我昨晚查了6号，他是狼人！大家今天一定要投他！
"""
    
    # 场景1: 玩家6（狼人）需要反击
    print("--- 场景1: 狼人反击 ---")
    persona_werewolf = "你是一个正在隐藏身份的狼人（玩家6），你的队友昨晚被查杀，现在情况非常危急。你需要说服大家相信真正的预言家是假的。"
    generated_speech_1 = generate_utterance(
        game_history=sample_history,
        persona=persona_werewolf,
        intent=ActionIntent.ACCUSE_PLAYER,
        target_player_id=2,
        style="坚定且带有煽动性的"
    )
    print(f"玩家6（狼人）的发言: {generated_speech_1}\n")

    # 场景2: 玩家5（村民）感到困惑
    print("--- 场景2: 村民划水 ---")
    persona_villager = "你是一个普通村民（玩家5），你对场上局势感到困惑，不确定谁是真正的预言家。"
    generated_speech_2 = generate_utterance(
        game_history=sample_history,
        persona=persona_villager,
        intent=ActionIntent.STAY_NEUTRAL,
        style="犹豫且寻求信息的"
    )
    print(f"玩家5（村民）的发言: {generated_speech_2}\n")
    
    # 场景3: 玩家3（被验证过的好人）支持预言家
    print("--- 场景3: 好人辩护 ---")
    persona_good_guy = "你是玩家3，一个已经被预言家验证过身份的好人。你需要站出来支持预言家。"
    generated_speech_3 = generate_utterance(
        game_history=sample_history,
        persona=persona_good_guy,
        intent=ActionIntent.DEFEND_PLAYER,
        target_player_id=2,
        style="逻辑清晰且充满信心的"
    )
    print(f"玩家3（好人）的发言: {generated_speech_3}\n")
