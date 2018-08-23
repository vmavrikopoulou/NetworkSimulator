# NetworkSimulator
Python simulator for Crownstone Mesh Network

Use python3 to run this.

## Installation

We use pip to install the dependencies.

```
pip3 install -r requirements.txt
```

## Running Examples

In the example folder run:

```
python3 test.py
```

## How it works

The simulator is made up from 4 parts.
- SimulationCore (Simulator in the API)
- Interaction Module (optional)
- Crownstone Classes
- Broadcaster Classes

When the simulator is instantiated, the time is 0.

Before running a simulation, it has to be set up first. You do this by loading the modules into the simulator.

### Step 1. The Interaction Module

The interaction module is meant to be like a user. It has a tick() function which gives it the time. You can decide to send mesh messages to
the Crownstones with instructions at certain intervals. You can init it with a name.

#### Available Methods:

> ##### tick(time: float)
> time is the simulation time in seconds. This is called every step of the simulation.


> ##### sendMessage(data: any)
> Use this method to send a mesh message. The format of the message is:
>
>```{"sender": < name >, "payload": < data >}```


### Step 2. The Crownstone Classes

Your simulation will act like Crownstones in a room, but you'll have to define their behaviour. You can create classes that inherit from the CrownstoneCore class to define
your behaviour.

#### Available Methods:

> ##### tick(time: float)
> time is the simulation time in seconds. This is called before every step of the simulation.


> ##### sendMessage(data: any)
> Use this method to send a mesh message. The format of the message is:
>
>```{"sender": < id >, "payload": < data >}```


> ##### receiveMessage(data: any, rssi: number)
> When mesh messages are received, this method is called. You can overload it to use it.
 The format of the message is:
>
>```{"sender": < id or interaction module name >, "payload": < data >}```


> ##### newMeasurement(data: any, rssi: int)
> When broadcasters reach this Crownstone, this method is calld. The format of the incoming data is:
>
>```{"address": < address of broadcaster >, "payload": < data >}```


### Step 3. The Broadcaster Classes

Broadcasters are IBeacons, phones etc. Everything that sends advertisements. They are different from advertisements for the mesh.
Custom Broadcasters inherit the BroadcasterCore class.


#### Mandatory Methods:

> ##### setBroadcastParameters(intervalMs, payload)
> This should be set before you start the simulation. It is the advertising interval in milliseconds and the default payload. This payload will be repeated unless you change it later using the changePayload method.
> IBeacons for instance will never change their payload.

> ##### getRssiToCrownstone(targetCrownstoneId: string)
> The simulator will ask your broadcaster to generate a message for this CrownstoneId. The simulator will take your advertising interval into account so you don't have to worry about that.
>
> If you do not want to send a message to that Crownstone, just return ```None```, else return the rssi.

#### Available Methods:

> ##### changePayload(payload: any)
> the payload you set here will be broadcast on the next broadcast interval.


> ##### tick(time: float)
> time is the simulation time in seconds. This is called before every step of the simulation. You can use this to change the payload if you want to.


### Step 4. Starting the simulation.

When you have set everything up you load your custom classes into the simulator:
```python
# create a simulator
mySimulation = Simulator()

# setup simulation
mySimulation.loadInteractionModule(interactionModule)
mySimulation.loadCrownstones(crownstones)
mySimulation.loadBroadcasters(beacons)
```

After which you start the simulation:
```python
mySimulation.start(10, timeStep=0.01)
```

Methods:

#### Available Methods:

> ##### loadInteractionModule(module: InteractionCore)
> Load your interaction module. This is not required. If you choose to provide one, it must inherit from InteractionCore.


> ##### loadCrownstones(crownstones: [ CrownstoneCore ])
> Load your custom Crownstone classes into the simulator. You must provide a list of classes that inherit the CrownstoneCore.


> ##### loadBroadcasters(broadcasters: [ BroadcasterCore ] )
> Load your custom Broadcaster classes into the simulator. You must provide a list of classes that inherit the BroadcasterCore.


> ##### start(duration: float: timeStep: float)
> Duration is the total time of the simulation. Timestep is the step of each tick in seconds.


## Advanced Usage

The simulator handles the sending and receiving of messages. If you want to add delays or failures or artifacts you can overload this method of the simulator. See the /examples/advanced folder for an example of this.