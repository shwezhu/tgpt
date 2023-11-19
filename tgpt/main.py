import gpt
import config


def main():
    conf = config.load_config("config.yaml")
    gpt.start_talk(conf)


if __name__ == "__main__":
    main()
