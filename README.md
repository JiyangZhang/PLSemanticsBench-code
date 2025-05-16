# PLSemanticsBench

This benchmark investigates the idea of using LLMs as interpreters for programming languages.

# Environment Setup
## Requirements

1. [Conda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/linux.html)
   is used for managing dependencies and creating virtual environment
   to run the experiments.

## Setup

1. Navigate to the root directory containing `env.yaml` and execute the
   command below to install project dependencies
   ```bash
   conda env create -f env.yaml
   ```

2. In the root directory, execute the below command to start the
   created virtual environment.
   ```bash
   conda activate llm-interpreter
    ```

## Repository Structure

- `data/`: directory contains the raw data in `.jsonl`
- `results/`: models' generated results will be written to this directory
- `model_configs` contains the config files for model inference, including hyper-parameter

# How to run the code
We provide the code to run gpt-4o models on all four tasks in PLSemanticsBench.
The results will be written to the `results/` directory.

```bash
# the default one is gpt-4o
python main.py
```

# Citation & License
Please use the following citations if you found our work to be useful in your work.
```
@inproceedings{plsemanticsbench,
    title={PLSemanticsBench: Large Language Models are Bad Programming Language Interpreters},
    author={Jiyang Zhang and Aditya Thimmaiah and Samuel Yuan and Junyi Jessy Li and Milos Gligoric},
    booktitle={},
    year={2025},
    url={}
}
```
