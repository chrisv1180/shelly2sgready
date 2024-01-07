# shelly2sgready
A simple wrapper for SG-Ready devices (e.g. a heatpump)that allows controlling it with help from  one or two Shelly devices.

This wrapper allows to set one of four SG-Ready states and to read the current state.
```python
state1_block = "state1_block"
state2_normal = "state2_normal"
state3_go = "state3_go"
state4_force = "state4_force"
```

## Dependencies
This project uses [ShellyPy](https://github.com/Jan200101/ShellyPy) in version 0.3.0 to communicate with the Shelly devices via HTTP Api.

For configuring the wrapper [PyYAML](https://github.com/yaml/pyyaml) is used.

## Example
### Config file
config.yaml
```yaml
# Config file

# configuration for switching sgready device with one or two Shelly devices
shelly2sgready:
  use_all_4_states: false      # if true also set shelly_optional_states

  shelly_state_2_3:
    ip: 192.168.178.73          # required
    port: 80                    # optional
    relay: 0                    # optional
    #username: admin             # optional
    #password: geheim            # optional

  # this shelly is optional; set use_all_4_states: false if second shelly is not used
  shelly_optional_states:
    ip: 192.168.178.74          # required
    port: 80                    # optional
    relay: 0                    # optional
    #username: admin             # optional
    #password: geheim            # optional
```

### Usage
```python
import argparse
from shelly2sgready.sgready import SGReadyControl, SGReadyStates

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cfg_path")
    args = parser.parse_args()

    heatpump = SGReadyControl(path_to_config=args.cfg_path)
    heatpump.setState(SGReadyStates.state3_go)
    state = heatpump.getState()
    heatpump.setState(SGReadyStates.state2_normal)


if __name__ == '__main__':
    main()
```

## License
This project is licensed under the [MIT License](LICENSE)  