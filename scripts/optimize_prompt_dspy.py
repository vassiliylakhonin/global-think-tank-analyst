#!/usr/bin/env python3
"""
DSPy Algorithmic Prompt Optimization for Global Think Tank Analyst.

This script demonstrates how to shift from manual prompt engineering to
programmatic optimization. It defines a metric (Evidence Discipline) and
uses a DSPy teleprompter to optimize the instructions to maximize the score.
"""

import os
import sys

try:
    import dspy
    from dspy.teleprompt import BootstrapFewShot
except ImportError:
    print("DSPy is required. Install via: pip install global-think-tank-analyst[dspy]")
    sys.exit(1)

# Configure LM
if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY is required.")
    sys.exit(1)

lm = dspy.OpenAI(model='gpt-4o-mini', max_tokens=1000)
dspy.settings.configure(lm=lm)

# 1. Define the Signature
class GenerateStrategicMemo(dspy.Signature):
    """Generate a structured strategic-risk memo answering a policy question."""
    
    question = dspy.InputField(desc="The geopolitical or policy question")
    context = dspy.InputField(desc="The raw facts and news data")
    memo = dspy.OutputField(desc="The structured memo with Facts, Assessments, and Watch Indicators")

# 2. Define the Module
class AnalystModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(GenerateStrategicMemo)

    def forward(self, question, context):
        return self.generate(question=question, context=context)

# 3. Define the Validation Metric (Evidence Discipline)
def evidence_metric(example, pred, trace=None):
    """
    Reward memos that correctly separate Facts and Assessments and include provenance tags.
    """
    memo = pred.memo
    score = 0
    
    if "Facts" in memo and "Assessments" in memo:
        score += 0.5
    
    # Check for provenance tags (our core SKILL.md rule)
    if "[primary]" in memo or "[secondary]" in memo:
        score += 0.5
        
    return score == 1.0  # Return boolean success

def main():
    print("Setting up DSPy Optimization Pipeline...")
    
    # 4. Prepare a tiny training set
    trainset = [
        dspy.Example(
            question="What is the impact of EU CBAM on Kazakh steel?",
            context="EU CBAM imposes carbon tax on imports. Kazakhstan relies on coal power for steel production."
        ).with_inputs('question', 'context'),
        dspy.Example(
            question="How will US semiconductor export controls affect Chinese AI startups?",
            context="US banned exports of advanced chips like H100 to China. Startups are seeking alternatives."
        ).with_inputs('question', 'context')
    ]

    # 5. Compile and Optimize
    print("Running BootstrapFewShot optimizer...")
    teleprompter = BootstrapFewShot(metric=evidence_metric, max_bootstrapped_demos=2)
    
    analyst = AnalystModule()
    optimized_analyst = teleprompter.compile(analyst, trainset=trainset)
    
    print("\n--- Optimization Complete ---")
    print("You can now save this optimized module or inspect its internal prompts.")
    
    # Test it
    test_pred = optimized_analyst(
        question="How does the Red Sea shipping crisis affect European supply chains?",
        context="Houthi attacks in the Red Sea forced Maersk to reroute around Africa, adding 10 days to transit."
    )
    
    print("\n--- Optimized Output Sample ---")
    print(test_pred.memo)

if __name__ == "__main__":
    main()
