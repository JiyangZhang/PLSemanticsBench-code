from experiment_args import ExperimentArgs
from prompts import PROMPT_STRATEGY
from gpt_experiment import GPTRunner, GPT_MODEL_ENUM
from macros import Macros


def gpt_4o_exps():
    print("Running gpt-4o on PEP standard semantics")
    model_name = "gpt-4o"
    exp_args = ExperimentArgs(
        task="pcp",
        setup_name="uk",
        expr_name="IMP-SOS",
        model_name=model_name,
        prompt_strategy=PROMPT_STRATEGY.DA,
    )
    gpt_runner = GPTRunner(
        model_config_file=Macros.model_config_dir
        / exp_args.task
        / exp_args.setup_name
        / exp_args.expr_name.lower()
        / f"config-{model_name}.yaml",
        gpt_model=GPT_MODEL_ENUM.GPT_4o,
        args=exp_args,
    )
    gpt_runner.do_experiment()
    
    print("Running gpt-4o on PEP nonstandard semantics")
    exp_args = ExperimentArgs(
        task="pcp",
        setup_name="mk",
        expr_name="IMP-SOS",
        model_name=model_name,
        prompt_strategy=PROMPT_STRATEGY.DA,
    )
    gpt_runner = GPTRunner(
        model_config_file=Macros.model_config_dir
        / exp_args.task
        / exp_args.setup_name
        / exp_args.expr_name.lower()
        / f"config-{model_name}.yaml",
        gpt_model=GPT_MODEL_ENUM.GPT_4o,
        args=exp_args,
    )
    gpt_runner.do_experiment()

    print("Running gpt-4o on POP standard semantics")
    exp_args = ExperimentArgs(
        task="op",
        setup_name="uk",
        expr_name="IMP-SOS",
        model_name=model_name,
        prompt_strategy=PROMPT_STRATEGY.DA,
    )
    gpt_runner = GPTRunner(
        model_config_file=Macros.model_config_dir
        / exp_args.task
        / exp_args.setup_name
        / exp_args.expr_name.lower()
        / f"config-{model_name}.yaml",
        gpt_model=GPT_MODEL_ENUM.GPT_4o,
        args=exp_args,
    )
    gpt_runner.do_experiment()

    print("Running gpt-4o on POP nonstandard semantics")
    exp_args = ExperimentArgs(
        task="op",
        setup_name="mk",
        expr_name="IMP-SOS",
        model_name=model_name,
        prompt_strategy=PROMPT_STRATEGY.DA,
    )
    gpt_runner = GPTRunner(
        model_config_file=Macros.model_config_dir
        / exp_args.task
        / exp_args.setup_name
        / exp_args.expr_name.lower()
        / f"config-{model_name}.yaml",
        gpt_model=GPT_MODEL_ENUM.GPT_4o,
        args=exp_args,
    )
    gpt_runner.do_experiment()

    print("Running gpt-4o on SRP standard semantics")
    exp_args = ExperimentArgs(
        task="srp",
        setup_name="uk",
        expr_name="IMP-SOS",
        model_name=model_name,
        prompt_strategy=PROMPT_STRATEGY.DA,
    )

    gpt_runner = GPTRunner(
        model_config_file=Macros.model_config_dir
        / exp_args.task
        / exp_args.setup_name
        / exp_args.expr_name.lower()
        / f"config-{model_name}.yaml",
        gpt_model=GPT_MODEL_ENUM.GPT_4o,
        args=exp_args,
    )
    gpt_runner.do_experiment()

    print("Running gpt-4o on SRP nonstandard semantics")
    exp_args = ExperimentArgs(
        task="srp",
        setup_name="mk",
        expr_name="IMP-SOS",
        model_name=model_name,
        prompt_strategy=PROMPT_STRATEGY.DA,
    )
    gpt_runner = GPTRunner(
        model_config_file=Macros.model_config_dir
        / exp_args.task
        / exp_args.setup_name
        / exp_args.expr_name.lower()
        / f"config-{model_name}.yaml",
        gpt_model=GPT_MODEL_ENUM.GPT_4o,
        args=exp_args,
    )
    gpt_runner.do_experiment()

    print("Running gpt-4o on ETP standard semantics with COT")
    exp_args = ExperimentArgs(
        task="etp",
        setup_name="uk",
        expr_name="IMP-SOS",
        model_name=model_name,
        prompt_strategy=PROMPT_STRATEGY.COT,
    )
    gpt_runner = GPTRunner(
        model_config_file=Macros.model_config_dir
        / exp_args.task
        / exp_args.setup_name
        / exp_args.expr_name.lower()
        / f"config-{model_name}.yaml",
        gpt_model=GPT_MODEL_ENUM.GPT_4o,
        args=exp_args,
    )
    gpt_runner.do_experiment()

    print("Running gpt-4o on ETP nonstandard semantics with COT")
    exp_args = ExperimentArgs(
        task="etp",
        setup_name="mk",
        expr_name="IMP-SOS",
        model_name=model_name,
        prompt_strategy=PROMPT_STRATEGY.COT,
    )
    gpt_runner = GPTRunner(
        model_config_file=Macros.model_config_dir
        / exp_args.task
        / exp_args.setup_name
        / exp_args.expr_name.lower()
        / f"config-{model_name}.yaml",
        gpt_model=GPT_MODEL_ENUM.GPT_4o,
        args=exp_args,
    )
    gpt_runner.do_experiment()

if __name__ == "__main__":
    gpt_4o_exps()
