import dataclasses

from prompts import PROMPT_STRATEGY


@dataclasses.dataclass
class ExperimentArgs:
    task: str = ""
    setup_name: str = ""
    expr_name: str = ""
    model_name: str = ""
    prompt_strategy: PROMPT_STRATEGY = PROMPT_STRATEGY.DA

    def __str__(self):
        lines = []
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            lines.append(value)
        return "-".join(lines).replace("/", "-")
