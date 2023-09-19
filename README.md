# gRPC HotelReservation + Intel IPU Scripting

Usable scripting for running DeathStarBench's HotelReservation application with Intel's IPU emulator

## Installation

First, ssh into your CloudLab master node with the -A option to cache public keys in your ssh-agent. An example is shown below, but you will need your own CloudLab account and experiment cluster.
```bash
ssh -A edwinlim@ms0415.utah.cloudlab.us
```

Then, go to the /dev/shm directory and clone the repository.
```bash
cd /dev/shm
git clone git@github.com:edwinlim0919/grpc-hotel-ipu.git 
```

Head into the /grpc-hotel-ipu directory and setup some a bash environment.
Press "y" and enter whenever prompted.
You may need to log out of the node and log back in to see env changes take affect.
```bash
cd grpc-hotel-ipu
source ./env.sh
```

Next, install the dependencies needed to run DeathStarBench.
Press "y" and enter whenever prompted.
```bash
source ./setup.sh
```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
