# 02. Context Engineering

Context engineering is the discipline of choosing, ordering, compressing, and labeling the information a model sees. Long prompts are only one tool.

## Mental Model

Good context is structured and intentional:

- System policy tells the model how to behave.
- User request defines the task.
- Retrieved context supplies facts.
- Conversation state supplies relevant history.
- Tool state supplies machine-readable results.
- Truncation policy decides what is lost when the budget is tight.

## Key Tradeoffs

- More context can improve recall but increase latency and distract the model.
- High-priority policy and fresh retrieved facts should survive truncation.
- Context blocks need source labels so answers can cite and attribute evidence.

## Practice

- Run `python labs/02_context_engineering/run.py`.
- Change the token budget and observe which context blocks are dropped.
- Add a low-priority noisy block and verify it does not displace critical facts.

## Mastery Checklist

- You can separate prompt instructions from contextual evidence.
- You can describe a context packing policy.
- You can explain how stale or irrelevant context causes hallucinations.
- You can design a test for truncation behavior.
