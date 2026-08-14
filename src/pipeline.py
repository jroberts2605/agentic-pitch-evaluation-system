from agents import Agent, Runner
from agents.mcp import MCPServerStdio

from src.pitch_agents import (
    classifier_agent,
    consumer_coach,
    b2b_saas_coach,
    deep_tech_coach,
    optimizer_agent,
)
from src.schemas import PitchEvaluation


MAX_ITERATIONS = 3

PITCH_TYPE_LABELS = {
    "consumer": "Consumer",
    "b2b_saas": "B2B SaaS",
    "deep_tech": "Deep Tech",
}


EVALUATOR_INSTRUCTIONS = """
You are a startup pitch evaluator.

Evaluate the pitch using the rubric that corresponds to its pitch type.
Use the get_rubric tool provided by the MCP server to retrieve the
appropriate evaluation criteria.

Evaluate each criterion individually and provide specific feedback.

The pitch passes only if it satisfies all criteria in the rubric.

Do not assume or invent information that is not present in the pitch.
"""


async def run_pitch_pipeline(pitch_text: str, pitch_id: str = "Pitch") -> dict:
    """
    Classify, coach, evaluate, and iteratively improve a startup pitch.

    Args:
        pitch_text: The founder's original startup pitch.
        pitch_id: Optional label used when displaying pipeline progress.

    Returns:
        A dictionary containing the pitch type, final draft,
        final evaluation, and number of iterations.
    """

    # Classify the pitch
    classification_result = await Runner.run(classifier_agent, pitch_text)
    classification = classification_result.final_output
    pitch_type = classification.pitch_type

    print(
        f"\n=== {pitch_id}: "
        f"classified as {PITCH_TYPE_LABELS[pitch_type]} ==="
    )
    print(f"Reasoning: {classification.reasoning}\n")

    # Connect to the MCP rubric server
    server = MCPServerStdio(
        params={
            "command": "python",
            "args": ["mcp/rubric_server.py"],
        },
        client_session_timeout_seconds=60,
    )

    async with server:
        evaluator_agent = Agent(
            name="Pitch Evaluator",
            instructions=EVALUATOR_INSTRUCTIONS,
            model="gpt-4.1",
            output_type=PitchEvaluation,
            mcp_servers=[server],
        )

        # Route the pitch to the appropriate specialized coach
        if pitch_type == "consumer":
            coach = consumer_coach
        elif pitch_type == "b2b_saas":
            coach = b2b_saas_coach
        else:
            coach = deep_tech_coach

        # Generate the initial coached draft
        coach_result = await Runner.run(coach, pitch_text)
        current_draft = coach_result.final_output

        evaluation = None

        # Evaluator-optimizer loop
        for iteration in range(1, MAX_ITERATIONS + 1):
            evaluation_input = f"""
Pitch type: {pitch_type}

Pitch:
{current_draft}
"""

            evaluation_result = await Runner.run(
                evaluator_agent,
                evaluation_input,
            )
            evaluation = evaluation_result.final_output

            print(f"Iteration {iteration}: {evaluation.summary}")

            # Stop once all rubric criteria are satisfied
            if evaluation.passes:
                break

            optimizer_input = f"""
Current pitch:
{current_draft}

Evaluator feedback:
{chr(10).join(evaluation.per_criterion_feedback)}
"""

            optimizer_result = await Runner.run(
                optimizer_agent,
                optimizer_input,
            )
            current_draft = optimizer_result.final_output

    return {
        "pitch_type": pitch_type,
        "final_draft": current_draft,
        "evaluation": evaluation,
        "iterations": iteration,
    }