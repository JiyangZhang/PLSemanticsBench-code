import seutil as su
import dataclasses
import enum
from openai import OpenAI

from base_experiment import BaseRunner

logger = su.log.get_logger(__name__, su.log.INFO)


@dataclasses.dataclass(frozen=True)
class GPT_MODEL:
    name: str = ""
    reasoning: bool = False
    from_openai: bool = False
    api_base: str = None


class GPT_MODEL_ENUM(enum.Enum):
    GPT_4o = GPT_MODEL(name="gpt-4o", reasoning=False, from_openai=True, api_base=None)
    O3_MINI = GPT_MODEL(name="o3-mini", reasoning=True, from_openai=True, api_base=None)


class GPTRunner(BaseRunner):
    def __init__(self, model_config_file: str, gpt_model: GPT_MODEL_ENUM, **kwargs):
        super().__init__(**kwargs)
        # load model's config
        self.model_config = su.io.load(model_config_file)
        self.gpt_model = gpt_model
        self.setup_client()

    # fed

    def setup_client(self):
        api_key = os.environ["OPENAI_API_KEY"]  # specify your OPENAI api key here
        self.client = OpenAI(
            api_key=api_key,
        )

    def _query(
        self,
        chat: list[dict],
        stop: list[str] = [],
    ) -> list[str]:
        try:
            completion_kwargs = {
                "model": self.gpt_model.value.name,
                "messages": chat,
                "stop": stop,
            }
            if self.gpt_model.value.reasoning and self.gpt_model.value.from_openai:
                completion_kwargs["max_completion_tokens"] = self.model_config.get(
                    "max_completion_tokens", 16000
                )
            else:
                completion_kwargs["max_completion_tokens"] = self.model_config.get(
                    "max_completion_tokens", 2048
                )
                completion_kwargs["temperature"] = self.model_config.get(
                    "temperature", 0
                )
            response = self.client.chat.completions.create(**completion_kwargs)
            return [c.message.content for c in response.choices]
        except Exception as e:
            # raise ModelRunnerException(
            logger.warning(
                f"Error while running query with model {self.args.model_name} : {e}"
            )
            return []
        # yrt

    # fed


# ssalc
