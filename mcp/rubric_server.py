from mcp.server.fastmcp import FastMCP


mcp = FastMCP("pitch-evaluation-rubric")

RUBRICS = {
    "consumer": {
        "name": "Consumer Product Pitch Rubric",
        "criteria": [
            "Hook: opens with a specific customer moment, not a category description.",
            "Why now: explains what changed in the world that makes this product possible or necessary right now.",
            "Distribution: names a concrete channel and explains why this product will travel through it.",
        ],
    },
    "b2b_saas": {
        "name": "B2B SaaS Pitch Rubric",
        "criteria": [
            "Customer pain: describes a real, named workflow the buyer hates today, not a vague 'inefficiency'.",
            "Market sizing: gives a concrete number of potential buyers and explains how it was estimated.",
            "Traction: cites a specific signal (a pilot, a paying customer, or a signed letter of intent) instead of generic 'strong interest'.",
        ],
    },
    "deep_tech": {
        "name": "Deep Tech Pitch Rubric",
        "criteria": [
            "Technical edge: explains what the team can do that no one else can, in language a non-specialist can follow.",
            "Defensibility: names what protects the company from being copied and for how long.",
            "First customer: identifies a specific first buyer who would pay for an early version, not a future market.",
        ],
    },
}


@mcp.tool()
def get_rubric(pitch_type: str) -> dict:
    """
    Return the evaluation rubric for a given startup pitch type.

    Args:
        pitch_type: One of 'consumer', 'b2b_saas', or 'deep_tech'.

    Returns:
        The corresponding rubric, or an empty rubric if the pitch
        type is not recognized.
    """
    return RUBRICS.get(
        pitch_type,
        {"name": "Unknown", "criteria": []},
    )


if __name__ == "__main__":
    mcp.run()