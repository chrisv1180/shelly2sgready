import logging
import sys

import yaml

LOG = logging.getLogger("cfg")

class Config:
    def __init__(self, data) -> None:
        try:
            self.use_all_4_states = data['shelly2sgready'].get('use_all_4_states', False)

            self.shelly_state_2_3_ip = data['shelly2sgready']['shelly_state_2_3']['ip']  # type: str
            self.shelly_state_2_3_port = data['shelly2sgready']['shelly_state_2_3'].get('port', 80)  # type: int
            self.shelly_state_2_3_relay = data['shelly2sgready']['shelly_state_2_3'].get('relay', 0)  # type: int
            self.shelly_state_2_3_user = data['shelly2sgready']['shelly_state_2_3'].get('username', None)  # type: str
            self.shelly_state_2_3_pw = data['shelly2sgready']['shelly_state_2_3'].get('password', None)  # type: str

            self.shelly_optional_states_ip = data['shelly2sgready']['shelly_optional_states'].get('ip', None)  # type: str
            self.shelly_optional_states_port = data['shelly2sgready']['shelly_optional_states'].get('port', 80)  # type: int
            self.shelly_optional_states_relay = data['shelly2sgready']['shelly_optional_states'].get('relay', 0)  # type: int
            self.shelly_optional_states_user = data['shelly2sgready']['shelly_optional_states'].get('username', None)  # type: str
            self.shelly_optional_states_pw = data['shelly2sgready']['shelly_optional_states'].get('password', None)  # type: str




        except KeyError as e:
            LOG.error("Missing required config key: %s", e.args[0])
            sys.exit(1)


def load_config(path: str):
    LOG.info("Loading config: %s", path)
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)

    return Config(data)
