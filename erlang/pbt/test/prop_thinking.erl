-module(prop_thinking).
-include_lib("proper/include/proper.hrl").

%%%%%%%%%%%%%%%%%%
%%% Properties %%%
%%%%%%%%%%%%%%%%%%
prop_test() ->
    ?FORALL(List, non_empty(list(integer())),
        begin
            thinking:biggest(List) =:= model_biggest(List)
        end).

prop_sort() ->
    ?FORALL(List, list(term()),
            is_orderd(lists:sort(List))).
% 不変条件を列挙。
prop_sort_same_size() ->
    ?FORALL(L, list(number()),
            length(L) =:= length(lists:sort(L))).
prop_sort_no_added() ->
    ?FORALL(L, list(number()),
        begin
            Sorted = lists:sort(L),
            lists:all(fun(Element) -> lists:member(Element, L) end, Sorted)
        end).


prop_count() ->
    ?FORALL(String, non_empty(string()),
        thinking:count(String) =:= alt_word_count(String)
    ).

%%%%%%%%%%%%%%%
%%% Helpers %%%
%%%%%%%%%%%%%%%
model_biggest(List) ->
    lists:last(lists:sort(List)).

is_orderd([A, B|T]) ->
    A =< B andalso is_orderd([B|T]);
is_orderd(_) ->
    true.

alt_word_count(String) -> space(String).
space([]) -> 0;
space([$\s|Str]) -> space(Str);
space(Str) -> word(Str).
word([]) -> 1;
word([$\s|Str]) -> 1+space(Str);
word([_|Str]) -> word(Str).

%%%%%%%%%%%%%%%%%%
%%% Generators %%%
%%%%%%%%%%%%%%%%%%
mytype() -> term().
