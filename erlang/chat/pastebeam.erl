-module(pastebeam).
% -export([start/0, loop/1]).
-export([start/0, accepter/1]).

% loop(X) when X =< 0 ->
%     ok;
% loop(X) ->
%     io:format("~w\n", [X]),
%     loop(X-1).

start() ->
    {ok, LSock} = gen_tcp:listen(5016, [binary, {packet, 0}, {reuseaddr, true}]),
    % run esparate threads)
    spawn(pastebeam, accepter, [LSock]).

accepter(LSock) ->
    {ok, Sock} = gen_tcp:accept(LSock),
    gen_tcp:send(Sock,
                 "======\n"
                 "Hello\n"
                 "======\n"),
    gen_tcp:close(Sock),
    accepter(LSock).

