from typing import Dict, List
import re
import seutil as su
from abc import ABC
from tqdm import tqdm
from datetime import datetime

from prompt_maker import (
    make_srp_prompt,
    make_pcp_prompt,
    make_op_prompt,
    make_etp_prompt,
)
from experiment_args import ExperimentArgs
from macros import Macros
from prompts import system_prompt


logger = su.log.get_logger(__name__, su.log.INFO)


class BaseRunner(ABC):
    def __init__(self, args: ExperimentArgs):
        self.args = args
        self._system: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": system_prompt,
            },
        ]
        logger.info(f"Querying model: {args.model_name}")

    def do_experiment(self):
        results_file_path = Macros.results_dir / f"results-{str(self.args)}.jsonl"
        dataset = self.load_dataset()
        results = self.run(dataset)
        su.io.dump(results_file_path, results)

    def load_dataset(self) -> List:
        logger.info(
            f"Loading dataset for task {self.args.task}, under setup {self.args.setup_name} on {self.args.expr_name} ...."
        )
        data_file_path = (
            Macros.data_dir
            / f"dataset-{self.args.task}-{self.args.setup_name}-{self.args.expr_name}.jsonl"
        )
        dataset = su.io.load(data_file_path)
        return dataset

    def run(self, dataset: List) -> List:
        """
        Run the experiments on the provided dataset
        """
        logger.info(f"Start running experiments: {str(self.args)} ...")
        # temp = 0.0
        results = []
        for p in tqdm(dataset, total=len(dataset)):
            # Save intermediate results periodically
            if len(results) % 128 == 0:
                su.io.dump(
                    Macros.tmp_dir / f"ckpt-{str(self.args)}-{datetime.now()}.jsonl",
                    results,
                )
            #
            chat_prompt = self._prepare_prompt(p)
            result = self.query_llm(p, chat_prompt=chat_prompt)
            results.append(result)
        return results

    def query_llm(self, dt: Dict, chat_prompt: List[dict]) -> Dict:
        """
        Query LLM with the **single** data.
        """
        res = {}
        res.update(
            {
                key: value
                for key, value in dt.items()
                if key not in {"syntax", "semantics"}
            }
        )
        # query llm
        chat = self._assemble_chat(chat_prompt)
        model_responses = self._query(chat)
        # res["model-input"] = chat
        if model_responses:
            res["model-prediction"] = model_responses[0]
        else:
            res["model-prediction"] = ""
        return res

    def _assemble_chat(self, chat_prompt: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Create the chat format for LLMs."""
        if "deepseek" in self.args.model_name:
            # remove system prompt according to the deepseek model card
            chat = chat_prompt
        else:
            chat = self._system + chat_prompt

        return chat

    def _prepare_prompt(self, dt: Dict) -> List[dict]:
        """
        Return the prompt string given the one data.
        """
        chat = []
        if self.args.task == "pcp":
            chat = make_pcp_prompt(self.args, dt)
        elif self.args.task == "op":
            chat = make_op_prompt(self.args, dt)
        elif self.args.task == "srp":
            chat = make_srp_prompt(self.args, dt)
        elif self.args.task == "etp":
            chat = make_etp_prompt(self.args, dt)
        else:
            raise NotImplementedError(
                f"Prompt for {str(self.args)} is not implemented yet."
            )

        return chat

    # -----------------
    # helper functions
    # -----------------

    def _extract_code(self, res: str):
        code_match = re.search(
            r"```(\w*)\n([\s\S]*?)```",
            res,
            flags=re.MULTILINE,
        )
        if code_match is not None:
            return code_match.group(2)
        else:
            return ""

    def extract_content_between_tags(self, text: str, tag: str) -> str:
        """Regular expression to match content between <tag> and </tag>"""
        pattern = f"<{tag}>(.*?)</{tag}>"
        matches = re.findall(
            pattern, text, re.DOTALL
        )  # re.DOTALL allows matching across newlines
        return matches[0]

    def add_linenum_to_program(self, program: str) -> str:
        """Add line numbers to the program."""
        lines = program.strip().split("\n")
        numbered_lines = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
        return "\n".join(numbered_lines)
