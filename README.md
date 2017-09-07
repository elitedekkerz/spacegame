!["ingame" screenshot](art/screenshot.png?raw=True)
# description #
a parser based space ship simulator server

# requirements #
python3  
python3-pip  

# start server #
```
pip3 install -r requirements.txt
./server.py
```  
  
# connect to server #
just connect to the game socket socket. for example with netcat:  
`nc <address> 1961`

# recommended tools for better experience #
to improve the experience we recommend building your own clients for parsing the I/O.  
alternatively, you can try a combination of these:
- [https://github.com/Swordfish90/cool-retro-term]
- [https://github.com/zevv/bucklespring]
  
# todo #
- rename clientHandler to simulation
- create separate mainloop for simulation, handleClients should be called from
- user input should be automatically lowercased when received
