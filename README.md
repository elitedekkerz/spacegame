# description #
this project is intended to make a game server with a minimal user interface.  

# requirements #
python3  
pip3  

# start server #
```
pip3 install -r requirements.txt
./server.py
```  
  
# connect to server #
just connect to a socket. for example with netcat:  
`nc <address> 1961`
  
# todo #
- rename clientHandler to simulation
- create separate mainloop for simulation, handleClients should be called from
- ship commands as separate modules
- user input should be automatically lowercased when received
