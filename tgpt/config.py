import yaml


def load_config(config_file: str) -> dict:
    try:
        # print("Absolute path:", os.path.abspath(config_file))
        with open(config_file) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(f"No config file found:{config_file}")
        exit()
    return config
