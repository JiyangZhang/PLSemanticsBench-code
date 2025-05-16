from typing import List

from experiment_args import ExperimentArgs
from prompts import PROMPT_STRATEGY
from prompts import (
    pcp_with_semantics_sos_prompt,
    pcp_with_semantics_sos_cot_prompt,
    op_with_semantics_sos_prompt,
    op_with_semantics_sos_cot_prompt,
    op_no_semantics_prompt,
    op_no_semantics_cot_prompt,
    srp_stmt_prompt,
    srp_zero_shot_sos_prompt,
    srp_zero_shot_sos_cot_prompt,
    etp_imp_sos_prompt,
    etp_imp_sos_cot_prompt,
)


SEMANTICS_MUTATIONS = {
    "addSub_mulDiv_negateRelation": {
        "ADD_OP": "-",
        "SUB_OP": "+",
        "MUL_OP": "/",
        "DIV_OP": "*",
        "LT_OP": ">",
        "GT_OP": "<",
        "LTEQ_OP": ">=",
        "GTEQ_OP": "<=",
        "EQ_OP": "!=",
        "NEQ_OP": "==",
        "AND_OP": "||",
        "OR_OP": "&&",
    },
    "unseen": {
        "ADD_OP": "𐕐",
        "SUB_OP": "𐕙",
        "MUL_OP": "𐕊",
        "DIV_OP": "𐕏",
        "MOD_OP": "𐕖",
        "ASSIGN_OP": "𐕂",
        "LT_OP": "𐔳",
        "GT_OP": "𐕃",
        "LTEQ_OP": "𐔷",
        "GTEQ_OP": "𐕛",
        "EQ_OP": "𐕟",
        "NEQ_OP": "𐕀",
        "AND_OP": "𐕜",
        "OR_OP": "𐔻",
        "NOT_OP": "𐔰",
        "BREAK": "𐔾",
        "IF": "𐔸",
        "ELSE": "𐕎",
        "WHILE": "𐕕",
        "HALT": "𐔱",
        "CONTINUE": "𐔲",
    },
}

def make_pcp_prompt(args: ExperimentArgs, dt: dict) -> List[dict]:
    program = dt["program"] if args.setup_name != "mk" else dt["mutated-program"]
    if args.prompt_strategy == PROMPT_STRATEGY.DA and "SOS" in args.expr_name:
        prompt_template = pcp_with_semantics_sos_prompt
    elif args.prompt_strategy == PROMPT_STRATEGY.COT and "SOS" in args.expr_name:
        prompt_template = pcp_with_semantics_sos_cot_prompt
    #
    prompt = prompt_template.format(
        language=dt["language"],
        syntax=dt["syntax"],
        semantics=dt["semantics"],
        program=program,
    )
    chat = [{"role": "user", "content": prompt}]
    return chat


def make_op_prompt(args: ExperimentArgs, dt: dict) -> List[dict]:
    program = dt["program"] if args.setup_name != "mk" else dt["mutated-program"]
    if args.setup_name != "nk":
        if args.prompt_strategy == PROMPT_STRATEGY.DA and "SOS" in args.expr_name:
            prompt_template = op_with_semantics_sos_prompt
        elif args.prompt_strategy == PROMPT_STRATEGY.COT and "SOS" in args.expr_name:
            prompt_template = op_with_semantics_sos_cot_prompt
    elif args.setup_name == "nk":
        if args.prompt_strategy == PROMPT_STRATEGY.DA and "SOS" in args.expr_name:
            prompt_template = op_no_semantics_prompt
        elif args.prompt_strategy == PROMPT_STRATEGY.COT and "SOS" in args.expr_name:
            prompt_template = op_no_semantics_cot_prompt
    #
    prompt = prompt_template.format(
        language=dt["language"],
        syntax=dt["syntax"],
        semantics=dt["semantics"],
        program=program,
    )
    chat = [{"role": "user", "content": prompt}]
    return chat


def make_srp_prompt(args: ExperimentArgs, dt: dict) -> List[dict]:
    """
    Prepare the prompt for the SRP task of a given program.
    """
    program = dt["program"] if args.setup_name != "mk" else dt["mutated-program"]
    if args.prompt_strategy == PROMPT_STRATEGY.DA and "SOS" in args.expr_name:
        prompt_template = srp_zero_shot_sos_prompt
    elif args.prompt_strategy == PROMPT_STRATEGY.COT and "SOS" in args.expr_name:
        prompt_template = srp_zero_shot_sos_cot_prompt
    #
    if args.setup_name == "mk" and "negateRelation" in dt["mutation-pattern"]:
        prompt = prompt_template.format(
            language=dt["language"],
            syntax=dt["syntax"],
            semantics=dt["semantics"],
            program=program,
            questions=_prepare_srp_questions(dt, program),
            LTEQ_OP=SEMANTICS_MUTATIONS[
                "addSub_mulDiv_negateRelation"
            ]["LTEQ_OP"],
            NOT_OP="!",
        )
    elif args.setup_name == "mk" and "unseen" in dt["mutation-pattern"]:
        prompt = prompt_template.format(
            language=dt["language"],
            syntax=dt["syntax"],
            semantics=dt["semantics"],
            program=program,
            questions=_prepare_srp_questions(dt, program),
            LTEQ_OP=SEMANTICS_MUTATIONS["unseen"]["LTEQ_OP"],
            NOT_OP=SEMANTICS_MUTATIONS["unseen"]["NOT_OP"],
        )
    else:
        prompt = prompt_template.format(
            language=dt["language"],
            syntax=dt["syntax"],
            semantics=dt["semantics"],
            program=program,
            questions=_prepare_srp_questions(dt, program),
            LTEQ_OP="<=",
            NOT_OP="!",
        )
    #
    chat = [{"role": "user", "content": prompt}]
    return chat


def make_etp_prompt(args: ExperimentArgs, dt: dict) -> List[dict]:
    program = dt["program"] if args.setup_name != "mk" else dt["mutated-program"]
    if args.prompt_strategy == PROMPT_STRATEGY.DA and "SOS" in args.expr_name:
        prompt_template = etp_imp_sos_prompt
    elif args.prompt_strategy == PROMPT_STRATEGY.COT and "SOS" in args.expr_name:
        prompt_template = etp_imp_sos_cot_prompt
    #
    prompt = prompt_template.format(
        language=dt["language"],
        syntax=dt["syntax"],
        semantics=dt["semantics"],
        program=_add_linenum_to_program(program),
    )
    chat = [{"role": "user", "content": prompt}]
    return chat


###
# Helper functions
###


def _prepare_srp_questions(dt: dict, program: str) -> str:
    """Prepare the prompt for the SRP task of a given program."""
    srp_data = dt["sampled-statements"]
    program_lines = program.split("\n")
    question_prompt = ""
    for i, srp_dt in enumerate(srp_data):
        question_prompt += srp_stmt_prompt.format(
            index=i + 1,
            line_number=int(srp_dt["line_number"]),
            program_state=srp_dt["prior_state"],
            statement=program_lines[int(srp_dt["line_number"]) - 1],
        )
        question_prompt += "\n\n"
    #
    return question_prompt


def _add_linenum_to_program(program: str) -> str:
    """Add line numbers to the program."""
    lines = program.strip().split("\n")
    numbered_lines = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
    return "\n".join(numbered_lines)
