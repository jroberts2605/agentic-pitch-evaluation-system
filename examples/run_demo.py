import asyncio

from examples.pitches import EXAMPLE_PITCHES
from src.pipeline import run_pitch_pipeline


async def main():
    """Run each example pitch through the evaluation pipeline."""

    for pitch_name, pitch_text in EXAMPLE_PITCHES.items():
        result = await run_pitch_pipeline(
            pitch_text=pitch_text,
            pitch_id=pitch_name,
        )

        evaluation = result["evaluation"]

        print("\n" + "=" * 70)
        print(f"{pitch_name} — FINAL RESULT")
        print("=" * 70)

        print(f"Pitch type: {result['pitch_type']}")
        print(f"Iterations: {result['iterations']}")
        print(f"Passed: {evaluation.passes}")

        print("\nFinal draft:\n")
        print(result["final_draft"])

        print("\nFinal evaluation:")
        print(evaluation.summary)

        print("\nRubric feedback:")
        for index, feedback in enumerate(
            evaluation.per_criterion_feedback,
            start=1,
        ):
            print(f"{index}. {feedback}")


if __name__ == "__main__":
    asyncio.run(main())