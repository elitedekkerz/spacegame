#!/bin/bash
#help
[ -z $1 ] && echo "usage: $0 <server> [<ship>]" && exit 1

(
   #set name
   echo config name $USER
   #join ship if name provided
   [ ! -z $2 ] \
      && sleep 0.1\
      && echo config ship join $2
   #read user input and pass it forward
   while read input; do echo $input; done <&0
) | nc $1 1961 #join given server at default port
