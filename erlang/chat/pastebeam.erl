-module(pastebeam).
% -export([start/0, loop/1]).
-export([start/0, accepter/1, session/2]).

% loop(X) when X =< 0 ->
%     ok;
% loop(X) ->
%     io:format("~w\n", [X]),
%     loop(X-1).

start() ->
    % active false?
    {ok, LSock} = gen_tcp:listen(5016, [binary, {packet, 0}, {active, false}, {reuseaddr, true}]),
    % run esparate threads)
    spawn(?MODULE, accepter, [LSock]).

% server(Message) ->
%     receive
%         {connected, Sock} ->
%             gen_tcp:send(Sock, ["================\n",
%                                 Message, "\n",
%                                 "================\n"]),
%             gen_tcp:close(Sock),
%             server(Message);
%         {message, NewMessage} ->
%             server(NewMessage)
%     end.

-spec session(State, Sock) -> ok when
      State :: command | {challenge, list(binary())} | {post, list(binary())} | {get, unicode:chardata()},
      Sock :: gen_tcp:socket().
session(command, Sock) ->
    case gen_tcp:recv(Sock, 0) of
        {ok, <<"POST\r\n">>} ->
            session({post, []}, Sock);
        {ok, <<"GET ", Id/binary>>} ->
            session({get, string:trim(Id)}, Sock);
        {ok, _} ->
            gen_tcp:send(Sock, "INVALID COMMAND\r\n"),
            gen_tcp:close(Sock),
            ok;
        {error, Reason} ->
            io:format("ERROR: session failed: ~w\n", [Reason]),
            gen_tcp:close(Sock),
            ok
    end;
session({post, Lines}, Sock) ->
    case gen_tcp:recv(Sock, 0) of
        {ok, <<"SUBMIT\r\n">>} ->
            session({challenge, Lines}, Sock);
        {ok, Line} ->
            session({post, [Line|Lines]}, Sock);
        {error, Reason} ->
            io:format("ERROR: session failed: ~w\n", [Reason]),
            gen_tcp:close(Sock),
            ok
    end;
session({get, Id}, Sock) ->
    io:format("TODO: GET MODE~s\n", [Id]),
    gen_tcp:close(Sock),
    ok;
session({challenge, Lines}, Sock) ->
    io:format("TODO: CHALLENGE: ~w\n", [Lines]),
    gen_tcp:close(Sock),
    ok.

accepter(LSock) ->
    {ok, Sock} = gen_tcp:accept(LSock),
    spawn(?MODULE, session, [command, Sock]),
    accepter(LSock).
