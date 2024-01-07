import logging
from enum import Enum
import ShellyPy

from shelly2sgready.config import load_config

class SGReadyStates(Enum):
    """
    the 4 possible SGReady states
    """
    state1_block = "state1_block"
    state2_normal = "state2_normal"
    state3_go = "state3_go"
    state4_force = "state4_force"

class SGReadyControl():
    def __init__(self, path_to_config: str):
        """

        :param path_to_config: path to a YamlConfig file containing at least shelly2sgready paragraph (see config.yaml)
        """

        conf = load_config(path_to_config)

        self.conf = conf
        self.last_state = None
        self.actual_state = None
        self.last_changed = None
        self.use_all_states = conf.use_all_4_states

        # shelly one (non-optional)
        if conf.shelly_state_2_3_user is not None and conf.shelly_state_2_3_pw is not None:
            self.shelly_state_2_3 = ShellyPy.Shelly(conf.shelly_state_2_3_ip, conf.shelly_state_2_3_port,
                                                    login={"username": conf.shelly_state_2_3_user,
                                                     "password": conf.shelly_state_2_3_pw})
        else:
            self.shelly_state_2_3 = ShellyPy.Shelly(conf.shelly_state_2_3_ip, conf.shelly_state_2_3_port)

        # shelly two (optional)
        if self.use_all_states:
            if conf.shelly_optional_states_user is not None and conf.shelly_optional_states_pw is not None:
                self.shelly_optional = ShellyPy.Shelly(conf.shelly_optional_states_ip, conf.shelly_optional_states_port,
                                                       login={"username": conf.shelly_optional_states_user,
                                                         "password": conf.shelly_optional_states_pw})
            else:
                self.shelly_optional = ShellyPy.Shelly(conf.shelly_optional_states_ip, conf.shelly_optional_states_port)
        else:
            self.shelly_optional = None

    def getState(self) -> SGReadyStates:
        """ reads the state of the configured (in init) shelly relays and translates it to a SGReadyState

        :return: corresponding shelly2sgready.sgready.SGReadyStates
        """

        shelly1_state = self.shelly_state_2_3.relay(self.conf.shelly_state_2_3_relay)
        bit1 = shelly1_state["output"]

        if self.use_all_states:
            shelly2_state = self.shelly_optional.relay(self.conf.shelly_optional_states_relay)
            bit2 = shelly2_state["output"]
        else:
            bit2 = False

        if bit1 and bit2:
            state = SGReadyStates.state4_force
        elif bit1 and not bit2:
            state = SGReadyStates.state3_go
        elif not bit1 and bit2:
            state = SGReadyStates.state1_block
        else:
            state = SGReadyStates.state2_normal

        return state

    def setState(self, state: SGReadyStates):
        """ switches the configured (in init) shelly relays according to given shelly2sgready.sgready.SGReadyStates

        :param state: shelly2sgready.sgready.SGReadyStates
        """

        if not self.use_all_states and (state == SGReadyStates.state1_block or state == SGReadyStates.state4_force):
            logging.warning(f"trying to set state {state.value} but only states 2 and 3 allowed; fallback to this states")
            if state == SGReadyStates.state1_block:
                state = SGReadyStates.state2_normal
            if state == SGReadyStates.state4_force:
                state = SGReadyStates.state3_go

        self.last_state = self.getState()
        self.actual_state = state

        if state == SGReadyStates.state1_block:
            self.shelly_optional.relay(self.conf.shelly_optional_states_relay, turn=True)
            self.shelly_state_2_3.relay(self.conf.shelly_state_2_3_relay, turn=False)
        elif state == SGReadyStates.state2_normal:
            if self.use_all_states:
                self.shelly_optional.relay(self.conf.shelly_optional_states_relay, turn=False)
            self.shelly_state_2_3.relay(self.conf.shelly_state_2_3_relay, turn=False)
        elif state == SGReadyStates.state3_go:
            if self.use_all_states:
                self.shelly_optional.relay(self.conf.shelly_optional_states_relay, turn=False)
            self.shelly_state_2_3.relay(self.conf.shelly_state_2_3_relay, turn=True)
        elif state == SGReadyStates.state4_force:
            self.shelly_optional.relay(self.conf.shelly_optional_states_relay, turn=True)
            self.shelly_state_2_3.relay(self.conf.shelly_state_2_3_relay, turn=True)
        else:
            raise ValueError(f"State {state} not supported!")


