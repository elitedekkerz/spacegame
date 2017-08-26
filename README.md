# description #
a parser based space ship simulator server

# requirements #
python3  
pip3  

# start server #
```
pip3 install -r requirements.txt
./server.py
```  
  
# connect to server #
just connect to the game socket socket. for example with netcat:  
`nc <address> 1961`
  
# todo #
- rename clientHandler to simulation
- create separate mainloop for simulation, handleClients should be called from
- user input should be automatically lowercased when received
- allow players to join other ships
- help command
