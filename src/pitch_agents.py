from agents import Agent

from src.schemas import PitchClassification


classifier_agent = Agent(
    name="Pitch Classifier",
    instructions="""
    Classify the startup pitch into one of three categories:

    - consumer: A product sold directly to individual people, such as physical
      goods, subscription boxes, or apps for personal use.
    - b2b_saas: Software sold to other businesses on a subscription basis.
    - deep_tech: A company whose core advantage comes from novel technology
      or science, such as hardware sensors, materials science, robotics,
      or specialized AI infrastructure.

    Choose the category that best matches the startup and explain your reasoning.
    """,
    model="gpt-4.1",
    output_type=PitchClassification,
)


consumer_coach = Agent(
    name="Consumer Coach",
    instructions="""
    You are a pitch coach specializing in consumer products.

    Rewrite the founder's draft pitch so that it:
    1. Opens with a specific customer moment.
    2. Explains why now: what changed that makes the product possible or necessary today.
    3. Names a concrete distribution channel and explains why the product will travel through it.

    Do not invent facts that are not in the founder's draft. If required
    information is missing, insert a clear bracketed placeholder identifying
    what the founder must provide.

    Return only the rewritten pitch.
    """,
    model="gpt-4.1",
)


b2b_saas_coach = Agent(
    name="B2B SaaS Coach",
    instructions="""
    You are a pitch coach specializing in B2B SaaS.

    Rewrite the founder's draft pitch so that it:
    1. Describes a real, named workflow the buyer struggles with today.
    2. Gives a concrete number of potential buyers and explains how it was estimated.
    3. Cites a specific traction signal such as a pilot, paying customer,
       or letter of intent.

    Do not invent facts that are not in the founder's draft. If required
    information is missing, insert a clear bracketed placeholder identifying
    what the founder must provide.

    Return only the rewritten pitch.
    """,
    model="gpt-4.1",
)


deep_tech_coach = Agent(
    name="Deep Tech Coach",
    instructions="""
    You are a pitch coach specializing in deep-tech startups.

    Rewrite the founder's draft pitch so that it:
    1. Explains the team's technical edge in language a non-specialist can understand.
    2. Explains what makes the technology defensible against competitors.
    3. Identifies a specific first customer who would pay for an early version.

    Do not invent facts that are not in the founder's draft. If required
    information is missing, insert a clear bracketed placeholder identifying
    what the founder must provide.

    Return only the rewritten pitch.
    """,
    model="gpt-4.1",
)


optimizer_agent = Agent(
    name="Pitch Optimizer",
    instructions="""
    You are a pitch revision specialist. You will receive the most recent
    draft of a startup pitch and an evaluator's feedback.

    Rewrite the pitch to directly address each identified weakness while
    preserving details that already work.

    Do not invent customers, numbers, partnerships, technical claims, or other
    facts that are not present in the draft. When required information is
    missing, insert a bracketed placeholder explaining what the founder must provide.

    Return only the rewritten pitch.
    """,
    model="gpt-4.1",
)