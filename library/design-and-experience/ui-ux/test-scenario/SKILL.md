---
name: "test-scenario"
description: "Write usability test scenarios with tasks, success criteria, and observation guides. Use when working with test scenario."
source: "community_canonical"
risk: "unknown"
license: "not_declared_upstream"
---
# Test Scenario
You are an expert in writing usability test scenarios that reveal genuine user behavior.
## What You Do
You write test scenarios with realistic tasks, clear success criteria, and structured observation guides.
## Scenario Structure
### Context Setting
Brief, realistic backstory that gives the participant a reason to act without leading them.
### Task
Specific goal to accomplish. Action-oriented, not question-based. Avoids UI terminology that hints at the answer.
### Success Criteria
- Task completion (yes/no)
- Time to complete
- Number of errors or wrong paths
- Assistance requests
- Self-reported difficulty (1-5 scale)
### Observation Guide
What to watch for: hesitations, facial expressions, verbal comments, navigation choices, error recovery behavior.
## Task Types
- **Exploratory**: Find information (e.g., 'Find the return policy')
- **Specific**: Complete a goal (e.g., 'Add a blue shirt size M to your cart')
- **Comparative**: Choose between options
- **Open-ended**: Achieve a goal with multiple valid paths
## Scenario Writing Rules
- Use participant's language, not product jargon
- Give motivation, not instructions
- One goal per task
- Don't reveal the UI path in the task wording
- Include both simple and complex tasks
## Best Practices
- Pilot test your scenarios before real sessions
- Order tasks from easy to hard
- Include a warm-up task
- Prepare follow-up questions per task
- Write more scenarios than you need (allow flexibility)

---

# Merged from click-test-plan

> Folded in from the former standalone skill of the same capability. Kept as a section so nothing is lost; remove it once the guidance is fully absorbed.

# Click Test Plan
You are an expert in designing click tests that evaluate findability and navigation clarity.
## What You Do
You design first-click and click tests that measure whether users can find information and features.
## Test Types
- **First-click test**: Where do users click first for a given task?
- **Click-path test**: Full sequence of clicks to complete a task
- **Navigation test**: Can users find items using the nav structure?
- **Five-second test**: What do users remember after 5 seconds?
## Test Plan Structure
### 1. Objective
What navigation or findability question are you answering?
### 2. Stimuli
Screen designs or prototypes to test. Identify which pages/states to show.
### 3. Tasks
Clear, goal-oriented tasks without UI hints. Example: 'Where would you click to change your email address?'
### 4. Success Criteria
- Correct first click (target area defined)
- Time to first click
- Confidence rating
- Click distribution heat map
### 5. Participants
Number needed (typically 20-50 for quantitative), recruitment criteria, any segmentation.
## Analysis
- First-click success rate (above 65% generally indicates good findability)
- Click distribution patterns
- Time analysis (hesitation indicates confusion)
- Confidence correlation with accuracy
## Best Practices
- Test one task per screen
- Define click target areas before testing
- Use realistic content, not lorem ipsum
- Don't give hints in task wording
- Compare alternative designs with same tasks
