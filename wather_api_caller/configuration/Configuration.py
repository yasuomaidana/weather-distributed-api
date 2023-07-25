import yaml


class Configuration:
    def __init__(self, yaml_name: str):
        with open(yaml_name + ".yml", "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        f.close()

    def get_database(self) -> dict:
        self.config['database']['connection_string'] = self.config['database']['connection_string'].format(
            user=self.config['database']['user'],
            password=self.config['database']['password']
        )
        return self.config["database"]

