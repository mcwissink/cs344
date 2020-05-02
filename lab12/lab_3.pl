sameweight(duck, woman).

witch(X) :-
    wood(X).

wood(X) :-
    floats(X).

floats(X) :-
    sameweight(duck, X).
