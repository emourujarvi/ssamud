# ssamud
Space Station Adventure XII MUD
Spent a weekend while hacking this.

To run use python3:

`python3 mud.py`

To connect use telnet, server opens to port 7777:

`telnet localhost 7777`

For now, player can pick any name.

## What works
- Moving between rooms
- Seeing other players
- Highlighting Objects Of Interest (OOI)
- Removing idle connections
- Basic commands

## Commands
- ` ' `  or  ` say `         broadcast msg to players in the same room
- ` &dash; `  or  ` com `    broadcast msg to every player
- ` n ` ` e ` ` s ` ` w `    shorthands for ` north `, ` east `, ` south `, and ` west ` move commands
- ` l `  or  ` look `        prints room description
- ` exits `                  prints out room exits
- ` where `                  prints out room id
- ` quit `                   disconnects from the server

## Needs
- Interacting with OOI
- Opening locked doors
- Story
- Containers / Chests
- Game mechanics (Combat?)
