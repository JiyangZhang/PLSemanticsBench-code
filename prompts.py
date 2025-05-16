from enum import StrEnum

class PROMPT_STRATEGY(StrEnum):
    COT = "cot"
    FEW_SHOT_COT = "few-shot-cot"
    DA = "da"
    FEW_SHOT_DA = "few-shot-da"


system_prompt = """You are an expert in Programming Language and Formal Methods."""

concise_reason_prompt = """Keep the reasoning concise and to the point"""


# Task descriptions prompts
pcp_task_desc = """
TASK: predict if the given program can execute under the given semantics or not.
- If you think the program can execute successfully, answer with the special word '##success##':

    <ans> ##success## </ans>

- If you believe the program cannot execute due to semantically invalid statements, answer with the special word '##error##' with the rule that prevents execution:

    <ans> ##error## </ans>
    <rule> [Rule causing halting due to semantically invalid statement] </rule>

Only write the answer. Note that you **MUST** wrap your prediction with `<ans>` tags and the violated rule with `<rule>` tags if any.
"""
pcp_task_cot_desc = """
TASK: predict if the given program can execute under the given semantics or not.
- If you think the program can execute successfully, answer with the special word '##success##':

    <ans> ##success## </ans>

- If you believe the program cannot execute due to semantically invalid statements, answer with the special word '##error##' with the reason and the rule that prevents execution:

    <ans> ##error## </ans>
    <rule> [Rule causing halting due to semantically invalid statement] </rule>

Explain your reasoning step-by-step **before** answering. Wrap your reasoning in `<reason>` tags.
Note that you **MUST** wrap your reasoning steps with `<reason>` tags, the prediction with `<ans>` tags, and the violated rule with `<rule>` tags if any.
"""

op_task_desc = """
TASK: predict the value of the variable `ans` after executing the above program.
- If you think the program will never terminate, answer with the special word '##timeout##':

    <ans> ##timeout## </ans>

- If you believe the program has runtime error or undefined behavior, answer with the special word '##error##':

    <ans> ##error## </ans>

- Otherwise, provide the predicted value of ans in the following format:

    <ans> [Your answer] </ans>

Only write the answer. You **MUST** wrap your prediction with `<ans>` tags.
"""

op_task_cot_desc = """
TASK: predict the value of the variable `ans` after reasoning abou the execution of the above program.
- If you think the program will never terminate, answer with the special word '##timeout##':

    <ans> ##timeout## </ans>

- If you believe the program has runtime error or undefined behavior, answer with the special word '##error##':

    <ans> ##error## </ans>

- Otherwise, provide the predicted value of ans in the following format:

    <ans> [Your answer] </ans>

Explain your reasoning step-by-step **before** answering. Wrap your reasoning in `<reason>` tags.
Note that you **MUST** wrap your reasoning steps with `<reason>` tags and the prediction with `<ans>` tags.
"""

srp_zero_shot_task_desc = """## TASK:
For each question below, you'll be given:
1. A specific statement from the program with its line number
2. The program state (variable values) before executing that statement

You must:
- Identify ALL semantic rules needed to execute the statement completely
- List them in the correct order of application

Here is one example:
** Statement:**
line 4:while ({NOT_OP}(n {LTEQ_OP} 0)) {{

**Program state before execution:**
{{'n': 100, 'sum': 0}}


This is a `while` loop with a condition `{NOT_OP}(n {LTEQ_OP} 0)`. First, we need to evaluate the boolean condition.
1. The outermost boolean expression is `!b` where `b = (n {LTEQ_OP} 0)`. This triggers **Rule 28** or **29**, depending on the evaluation result.
2. To evaluate `b = (n {LTEQ_OP} 0)`, this is a relational comparison and uses **Rule 12** or **13** depending on whether it is true or false.
3. To compute `n {LTEQ_OP} 0`, we need to evaluate both `n` and `0`, which are arithmetic expressions. We use **Rule 2** to evaluate `n` (since `n` is a variable), and **Rule 1** to evaluate `0`.
4. After evaluating both sides to values, we determine `100 {LTEQ_OP} 0`, which is false, so we use **Rule 13** to reduce to `false`.
5. Now we have `{NOT_OP}(false)` → `true`, which is handled by **Rule 29**.
6. Finally, the `while` condition is true, so we apply **Rule 34** to transform the loop into `S1;while(...)`.

Therefore, the final answer is:
<ans>
  <answer id="1">
    <rule>2</rule>
    <rule>1</rule>
    <rule>13</rule>
    <rule>29</rule>
    <rule>34</rule>
  </answer>
</ans>


## Questions:
{questions}

## Response Format:
Respond with an XML block structured as follows:

<ans>
  <answer id="1">
    <rule>1</rule>
    <rule>2</rule>
    ...
  </answer>
  <answer id="2">
    <rule>1</rule>
    <rule>2</rule>
    ...
  </answer>
  ...
</ans>

### Notes:
- Each `<answer id="N">` element corresponds to the N-th question.
- Inside each `<answer>` block, list each semantic rule in the correct order using `<rule>` tags.

## Important Notes:
- The **order** of rules matters and should reflect the evaluation sequence.
- A single rule may be applied multiple times during evaluation.
- You must include **all** semantic rules required for complete execution.
- Base your analysis solely on the provided semantics, not on general programming knowledge.

Only output the `<ans>` XML block. Do not include any other content.
"""

srp_zero_shot_cot_task_desc = """## TASK:
For each question below, you'll be given:
1. A specific statement from the program with its line number
2. The program state (variable values) before executing that statement

You must:
- Identify ALL semantic rules needed to execute the statement completely
- List them in the correct order of application

Here is one example:
** Statement:**
line 4:while (!(n <= 0)) {{

**Program state before execution:**
{{'n': 100, 'sum': 0}}


This is a `while` loop with a condition `!(n <= 0)`. First, we need to evaluate the boolean condition.
1. The outermost boolean expression is `!b` where `b = (n <= 0)`. This triggers **Rule 28** or **29**, depending on the evaluation result.
2. To evaluate `b = (n <= 0)`, this is a relational comparison and uses **Rule 12** or **13** depending on whether it is true or false.
3. To compute `n <= 0`, we need to evaluate both `n` and `0`, which are arithmetic expressions. We use **Rule 2** to evaluate `n` (since `n` is a variable), and **Rule 1** to evaluate `0`.
4. After evaluating both sides to values, we determine `100 <= 0`, which is false, so we use **Rule 13** to reduce to `false`.
5. Now we have `!(false)` → `true`, which is handled by **Rule 29**.
6. Finally, the `while` condition is true, so we apply **Rule 34** to transform the loop into `S1;while(...)`.

Therefore, the final answer is:
<ans>
  <answer id="1">
    <rule>2</rule>
    <rule>1</rule>
    <rule>13</rule>
    <rule>29</rule>
    <rule>34</rule>
  </answer>
</ans>

## Questions:
{questions}

## Response Format:
Respond with an XML block structured as follows:

<ans>
  <answer id="1">
    <rule>1</rule>
    <rule>2</rule>
    ...
  </answer>
  <answer id="2">
    <rule>1</rule>
    <rule>2</rule>
    ...
  </answer>
  ...
</ans>

### Notes:
- Each `<answer id="N">` element corresponds to the N-th question.
- Inside each `<answer>` block, list each semantic rule in the correct order using `<rule>` tags.

## Important Notes:
- The **order** of rules matters and should reflect the evaluation sequence.
- A single rule may be applied multiple times during evaluation.
- You must include **all** semantic rules required for complete execution.
- Base your analysis solely on the provided semantics, not on general programming knowledge.

Explain your reasoning step-by-step **before** answering. Wrap your reasoning in `<reason>` tags.
"""

srp_task_desc = """
## TASK:
For each question below, you'll be given:
1. A specific statement from the program with its line number
2. The program state (variable values) before executing that statement

You must:
- Identify ALL semantic rules needed to execute the statement completely
- List them in the correct order of application

## Questions:
{questions}

## Response Format:
Respond with an XML block structured as follows:

<ans>
  <answer id="1">
    <rule>1</rule>
    <rule>2</rule>
    ...
  </answer>
  <answer id="2">
    <rule>1</rule>
    <rule>2</rule>
    ...
  </answer>
  ...
</ans>

### Notes:
- Each `<answer id="N">` element corresponds to the N-th question.
- Inside each `<answer>` block, list each semantic rule in the correct order using `<rule>` tags.

## Important Notes:
- The **order** of rules matters and should reflect the evaluation sequence.
- A single rule may be applied multiple times during evaluation.
- You must include **all** semantic rules required for complete execution.
- Base your analysis solely on the provided semantics, not on general programming knowledge.

Only output the `<ans>` XML block. Do not include any other content.
"""

srp_task_cot_desc = """
## TASK:
For each question below, you'll be given:
1. A specific statement from the program with its line number
2. The program state (variable values) before executing that statement

You must:
- Identify ALL semantic rules needed to execute the statement completely
- List them in the correct order of application

## Questions:
{questions}

## Response Format:
Respond with an XML block structured as follows:

<reason>
Your reasoning steps here, explaining how you arrived at the rules needed for each question.
</reason>

<ans>
  <answer id="1">
    <rule>1</rule>
    <rule>2</rule>
    ...
  </answer>
  <answer id="2">
    <rule>1</rule>
    <rule>2</rule>
    ...
  </answer>
  ...
</ans>

### Notes:
- Each `<answer id="N">` element corresponds to the N-th question.
- Inside each `<answer>` block, list each semantic rule in the correct order using `<rule>` tags.

## Important Notes:
- The **order** of rules matters and should reflect the evaluation sequence.
- A single rule may be applied multiple times during evaluation.
- You must include **all** semantic rules required for complete execution.
- Base your analysis solely on the provided semantics, not on general programming knowledge.

Explain your reasoning step-by-step **before** answering. Wrap your reasoning in `<reason>` tags.
"""


etp_task_desc = """## TASK:
Given a program and its semantics, predict the execution trace. Your goal is to simulate execution step by step and output the exact sequence of executed statements and the program state after the execution of each statement.

## Response Format:
Respond with an XML block structured as follows:

<answer>
  <step>
    <linenumber>1</linenumber>
    <program_state>
        <n>0</n>
        <sum>0</sum>
    </program_state>
  </step>
  <step>
    <linenumber>2</linenumber>
    <program_state>
      <n>100</n>
      <sum>0</sum>
    </program_state>
  </step>
  ...
</answer>

## Notes:
- Each `<step>` must correspond to **exactly one executed statement**.
- The `<linenumber>` must indicate the line number of the statement that was just executed.
- The `<program_state>` must represent the **entire program state immediately after** the execution of that statement.
- The program state must list **all variables currently in scope**, using the variable names as XML tags and their current values as tag content.
- Include variables even if they did not change.
- You must include **every executed statement** as a separate `<step>`, in the **exact order** they are executed.
- Do not skip any step or merge multiple steps into one.

Only output the `<answer>` XML block. Do not include explanations, comments, or any other text.
"""

etp_task_cot_desc = """## TASK:
Given a program and its semantics, predict the execution trace. Your goal is to simulate execution step by step and output the exact sequence of executed statements and the program state after the execution of each statement.

## Response Format:
Respond with an XML block structured as follows:

<answer>
  <step>
    <linenumber>1</linenumber>
    <program_state>
        <n>0</n>
        <sum>0</sum>
    </program_state>
  </step>
  <step>
    <linenumber>2</linenumber>
    <program_state>
      <n>100</n>
      <sum>0</sum>
    </program_state>
  </step>
  ...
</answer>

## Notes:
- Each `<step>` must correspond to **exactly one executed statement**.
- The `<linenumber>` must indicate the line number of the statement that was just executed.
- The `<program_state>` must represent the **entire program state immediately after** the execution of that statement.
- The program state must list **all variables currently in scope**, using the variable names as XML tags and their current values as tag content.
- Include variables even if they did not change.
- You must include **every executed statement** as a separate `<step>`, in the **exact order** they are executed.
- Do not skip any step or merge multiple steps into one.

Explain your reasoning step-by-step **before** answering. Wrap your reasoning in `<reason>` tags.
Note that you **MUST** wrap your reasoning steps with `<reason>` tags, the prediction with `<answer>` tags.
"""


#######################
# Prompts for each task
#######################
pcp_with_semantics_sos_cot_prompt1 = """You are an interpreter for a programming language called {language}. You will be provided with:
1. The syntax of {language} written in EBNF.
2. The semantics of {language} written using small-step operational semantics.
3. A {language} program.

Your task is to predict whether the given program can execute without encountering semantic errors, following only the rules in the provided semantics.

We will follow these steps to reach the final answer:

### Step 1: Understand the Rules
- Read and internalize the rules of the language semantics.
- Pay attention to any rules that lead to `HALT` without using the `HALT` statement. These represent semantically invalid behavior.

### Step 2: Understand the Program
- Read the program line-by-line and understand its structure based on the syntax.

### Step 3: Simulate Execution Step-by-Step
- Start from the initial configuration and apply the semantic rules to simulate each step.
- At each step, identify the rule used and update the program state accordingly.

### Step 4: Check for Invalid Behavior
- If during the execution any rule leads to `HALT` without an explicit `HALT` statement, stop and mark the program as semantically invalid.
- Otherwise, continue until no further steps can be taken.

### Step 5: Output the Result
- If the program executes successfully using only valid rules, answer with:

  <ans> ##success## </ans>

- If the program halts due to a semantic error, answer with:

  <ans> ##error## </ans>
  <reason> [Explain what went wrong and why the program cannot continue] </reason>
  <rule> [Name the specific rule that caused HALT or error] </rule>

Assume that:
- The syntax and semantics provided are correct.
- You must only reason using the semantics and rules explicitly given.

Here is the syntax of {language} in EBNF:
```
{syntax}
```

Here is the small-step operational semantics of {language}:
```
{semantics}
```

Here is the program to evaluate:
```
{program}
```

Now follow Steps 1-5 and output your prediction.
"""

pcp_with_semantics_sos_cot_prompt = (
    """You are an interpreter for my language called {language}. I will describe the syntax for {language} in EBNF form and I will describe the semantics for {language} using small-step operational semantics. All the rules that lead to HALT without using the HALT statement are describing semantically invalid statements. If the execution of a {language} program requires such rules then that program is not executable. Your task is to check if the given {language} program can execute or not. You will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give are correct.
    Here is the syntax of {language} in EBNF form
    ```
    {syntax}
    ```

    Here is the semantics of {language}
    ```
    {semantics}
    ```

    Here is the {language} program
    ```
    {program}
    ```
    """
    + pcp_task_cot_desc
)


pcp_with_semantics_sos_prompt = (
    """You are an interpreter for my language called {language}. I will describe the syntax for {language} in EBNF form and I will describe the semantics for {language} using small-step operational semantics. All the rules that lead to HALT without using the HALT statement are describing semantically invalid statements. If the execution of a {language} program requires such rules then that program is not executable. Your task is to check if the given {language} program can execute or not. You will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give are correct.
Here is the syntax of {language} in EBNF form
```
{syntax}
```

Here is the semantics of {language}
```
{semantics}
```

Here is the {language} program
```
{program}
```
"""
    + pcp_task_desc
)


op_with_semantics_sos_prompt = (
    """You are an interpreter for my language called {language}. I will describe the syntax for {language} in EBNF form and I will describe the semantics for {language} using small-step operational semantics. You will use this to execute a {language} program. You will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give are correct. Here is the syntax of {language} in EBNF form
```
{syntax}
```

Here is the semantics of {language}
```
{semantics}
```

Here is the {language} program
```
{program}
```
"""
    + op_task_desc
)

op_with_semantics_sos_cot_prompt = (
    """You are an interpreter for my language called {language}. I will describe the syntax for {language} in EBNF form and I will describe the semantics for {language} using small-step operational semantics. You will use this to execute a {language} program. You will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give are correct. Here is the syntax of {language} in EBNF form
```
{syntax}
```

Here is the semantics of {language}
```
{semantics}
```

Here is the {language} program
```
{program}
```
"""
    + op_task_cot_desc
)


op_no_semantics_prompt = (
    """You are an interpreter for my language called {language}.

Here is the {language} program
```
{program}
```
"""
    + op_task_desc
)

op_no_semantics_cot_prompt = (
    """You are an interpreter for my language called {language}.

Here is the {language} program
```
{program}
```
"""
    + op_task_cot_desc
)

## --
# srp
## --

srp_zero_shot_sos_prompt = (
    """You are an interpreter for my language called {language}. I will describe the syntax for {language} in EBNF form and I will describe the semantics for {language} using small-step operational semantics. You will use this to execute a {language} program. You will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give are correct. Here is the syntax of {language} in EBNF form
```
{syntax}
```

Here is the semantics of {language}
```
{semantics}
```

Here is the {language} program
```
{program}
```
"""
    + srp_zero_shot_task_desc
)

srp_zero_shot_sos_cot_prompt = (
    """You are an interpreter for my language called {language}. I will describe the syntax for {language} in EBNF form and I will describe the semantics for {language} using small-step operational semantics. You will use this to execute a {language} program. You will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give are correct. Here is the syntax of {language} in EBNF form
```
{syntax}
```

Here is the semantics of {language}
```
{semantics}
```

Here is the {language} program
```
{program}
```
"""
    + srp_zero_shot_cot_task_desc
)

srp_sos_prompt = (
    """You are an interpreter for my language called {language}. I will describe the syntax for {language} in EBNF form and I will describe the semantics for {language} using small-step operational semantics. You will use this to execute a {language} program. You will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give are correct. Here is the syntax of {language} in EBNF form
```
{syntax}
```

Here is the semantics of {language}
```
{semantics}
```

Here is the {language} program
```
{program}
```
"""
    + srp_task_desc
)

srp_sos_cot_prompt = (
    """You are an interpreter for my language called {language}. I will describe the syntax for {language} in EBNF form and I will describe the semantics for {language} using small-step operational semantics. You will use this to execute a {language} program. You will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give are correct. Here is the syntax of {language} in EBNF form
```
{syntax}
```

Here is the semantics of {language}
```
{semantics}
```

Here is the {language} program
```
{program}
```
"""
    + srp_task_cot_desc
)

srp_stmt_prompt = """
### Question {index}:
** Statement:**
```
line {line_number}:{statement}
```
**Program state before execution:**
{program_state}"""


# ETP prompts
etp_imp_sos_prompt = (
    """You are an interpreter for my language called {language}. I will describe the syntax for {language} in EBNF form and I will describe the semantics for {language} using small-step operational semantics. You will use this to execute a {language} program. You will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give are correct.
Here is the syntax of {language} in EBNF form
```
{syntax}
```

Here is the semantics of {language}
```
{semantics}
```
Here is the {language} program
```
{program}
```
"""
    + etp_task_desc
)

etp_imp_sos_cot_prompt = (
    """You are an interpreter for my language called {language}. I will describe the syntax for {language} in EBNF form and I will describe the semantics for {language} using small-step operational semantics. You will use this to execute a {language} program. You will only use the rules described in the semantics I provide. Assume all the rules in the semantics I give are correct.
Here is the syntax of {language} in EBNF form
```
{syntax}
```

Here is the semantics of {language}
```
{semantics}
```
Here is the {language} program
```
{program}
```
"""
    + etp_task_cot_desc
)
