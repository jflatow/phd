-module(combinator).

-export([factorial/1, x/1, y/1, z/1]).

%% the factorial step function
%% takes a function Self which is the result of fact(Self)
%% (i.e. Self =:= fact(Self))
%% the trick is that Self isn't evaluated until you need it
%% (see step #6 below)
%% when you call the thing returned by the combinator with an argument N
%% Self gets created with the ability to call itself if needed
%% at which point it winds up a stack of references to itself
%% it continues until it gets the argument 0
%% at which point it no longer needs to reference Self
%% so it can unwind, returning the initial value 1

fact(Self) ->
    fun (0) ->
            1;
        (N) ->
            N * Self(N - 1)
    end.

factorial(N) when is_integer(N) ->
    (z(fun fact/1))(N).

%% the classic Y combinator (with more meaningful variable names)

y(Step) ->
    %% n indicates control flow
    %% * indicates a function call
    %% ** an almost recursive call
    %% *** the true recursive call
    %%                                  Self
    %%    2        9*   4**  3           1    7        8*   6*** 5
    (fun (Self) -> Step(Self(Self)) end)(fun (Self) -> Step(Self(Self)) end).

%% the 'refactored' X and Z combinators

recur(X) ->
    X(X).

%% X is just a more compact Y

x(Step) ->
    recur(fun (Self) -> Step(Self(Self)) end).


%% Z is an applicative-order fixed-point combinator (e.g. for Erlang)
%% it wraps Self so that it can reference itself without calling the recursion

z(Step) ->
    recur(fun (Self) -> Step(fun (Y) -> (Self(Self))(Y) end) end).
