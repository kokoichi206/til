-module(pastebeam).
% -export([start/0, loop/1]).
-export([start/0, accepter/1, session/2]).

% TODO: use prefix challenge instead of suffix

% loop(X) when X =< 0 ->
%     ok;
% loop(X) ->
%     io:format("~w\n", [X]),
%     loop(X-1).

start() ->
    % active false?
    {ok, LSock} = gen_tcp:listen(5016, [binary, {packet, line}, {active, false}, {reuseaddr, true}]),
    % run esparate threads)
    Pid = spawn(?MODULE, accepter, [LSock]),
    gen_tcp:controlling_process(LSock, Pid),
    Pid.

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

fail_session(Sock, Reason) ->
    io:format("ERROR: session failed: ~w\n", [Reason]),
    gen_tcp:close(Sock),
    ok.

-spec session(State, Sock) -> ok when
      State :: command |
                {challenge, binary()} |
                {accepted, binary(), binary()} |
                {post, binary()} |
                {get, unicode:chardata()},
      Sock :: gen_tcp:socket().
session(command, Sock) ->
    case gen_tcp:recv(Sock, 0) of
        {ok, <<"POST\r\n">>} ->
            session({post, <<"">>}, Sock);
        {ok, <<"GET ", Id/binary>>} ->
            session({get, string:trim(Id)}, Sock);
        {ok, _} ->
            gen_tcp:send(Sock, "INVALID COMMAND\r\n"),
            gen_tcp:close(Sock),
            ok;
        {error, Reason} ->
            fail_session(Sock, Reason)
    end;
session({post, Lines}, Sock) ->
    case gen_tcp:recv(Sock, 0) of
        {ok, <<"SUBMIT\r\n">>} ->
            io:format("submit"),
            session({challenge, Lines}, Sock);
        {ok, Line} ->
            session({post, <<Lines/binary, Line/binary>>}, Sock);
        {error, Reason} ->
            fail_session(Sock, Reason)
    end;
session({challenge, Lines}, Sock) ->
    Challenge = binary:encode_hex(crypto:strong_rand_bytes(32)),
    gen_tcp:send(Sock, [<<"CHALLENGE ">>, Challenge, <<"\r\n">>]),
    session({accepted, Lines, Challenge}, Sock);
session({accepted, Lines, Challenge}, Sock) ->
    case gen_tcp:recv(Sock, 0) of
        {ok, <<"ACCEPTED ", Suffix/binary>>} -> 
            Blob = <<Lines/binary, Challenge/binary, <<"\r\n">>/binary, Suffix/binary>>,
            case binary:encode_hex(crypto:hash(sha256, Blob)) of
                <<"00000", _/binary>> ->
                    Id = binary:encode_hex(crypto:strong_rand_bytes(32)),
                    file:write_file(Id, Lines),
                    gen_tcp:send(Sock, [<<"SENT ">>, Id, <<"\r\n">>]),
                    gen_tcp:close(Sock),
                    ok;
                _ ->
                    gen_tcp:send(Sock, <<"CHALLENGED FAILED\r\n">>),
                    gen_tcp:close(Sock),
                    ok
            end;
        {ok, _} -> 
            gen_tcp:send(Sock, "INVALID COMMAND\r\n"),
            gen_tcp:close(Sock),
            ok;
        {error, Reason} ->
            fail_session(Sock, Reason)
    end;
session({get, Id}, Sock) ->
    io:format("TODO: GET MODE~s\n", [Id]),
    gen_tcp:close(Sock),
    ok.

accepter(LSock) ->
    {ok, Sock} = gen_tcp:accept(LSock),
    spawn(?MODULE, session, [command, Sock]),
    accepter(LSock).
