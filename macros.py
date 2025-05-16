import os
from pathlib import Path


class Macros:
    papers: list[str] = ["neurips25"]
    main_dir = Path(os.path.realpath(__file__)).parent.resolve()
    model_config_dir = main_dir / "model_configs"    
    data_dir = main_dir / "data"
    results_dir = main_dir / "results"
    tmp_dir = main_dir / ".tmp"


