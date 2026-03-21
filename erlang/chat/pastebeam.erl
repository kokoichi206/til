-module(pastebeam).
% -export([start/0, loop/1]).
-export([start/0, accepter/2, server/1]).

% loop(X) when X =< 0 ->
%     ok;
% loop(X) ->
%     io:format("~w\n", [X]),
%     loop(X-1).

start() ->
    {ok, LSock} = gen_tcp:listen(5016, [binary, {packet, 0}, {reuseaddr, true}]),
    % run esparate threads)
    Sink = spawn(pastebeam, server, ["Hello"]),
    spawn(pastebeam, accepter, [LSock, Sink]),
    Sink.

     % gen_tcp:send(Sock,
     %             ["======\n"
     %             Message, "\n"
     %             "======\n"]),
   % gen_tcp:close(Sock),

server(Message) ->
    receive
        {connected, Sock} ->
            gen_tcp:send(Sock, ["================\n",
                                Message, "\n",
                                "================\n"]),
            gen_tcp:close(Sock),
            server(Message);
        {message, NewMessage} ->
            server(NewMessage)
    end.

accepter(LSock, Sink) ->
    {ok, Sock} = gen_tcp:accept(LSock),
    Sink ! {connected, Sock},
    accepter(LSock, Sink).

