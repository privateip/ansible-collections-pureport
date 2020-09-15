# Connection

The ```pureport.network.connection``` role provides an abstraction for 
creating connections from a Pureport Multicloud Fabric to another cloud by
implementing a common abstraction layer.  

## Usage

This role can add a new connection (`state=present`) or remove an existing
connection (`state=absent`) from a Pureport Mutlicloud Fabric.  If the 
fabric doesn't already exist, it will be created.

- [Adding a connection to Pureport](docs/add_connection.md)
- [Removing a connection from Pureport](docs/remove_connection.md)

## Requirements

- Ansible 2.9 or later
- Pureport client 1.0.7 or later
- One ore more cloud libraries depending on connection type.  See connection
  type role for more details on required libraries.

### requirements.txt

```
ansible 
pureport-client
```

