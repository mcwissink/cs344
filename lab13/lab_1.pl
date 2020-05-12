%% a.
%% Exercise 3.2
directlyIn(olga, katarina).
directlyIn(natasha, olga).
directlyIn(irina, natasha).
in(X, Y) :- directlyIn(X, Y).
in(X, Z) :-
    directlyIn(Y, Z),
    in(X, Y).

in(irina, olga). %% true
in(katarina, natasha). %% false 

%% Exercise 4.5
tran(eins,one).
tran(zwei,two).
tran(drei,three).
tran(vier,four).
tran(fuenf,five).
tran(sechs,six).
tran(sieben,seven).
tran(acht,eight).
tran(neun,nine). 

listtran([],[]).
listtran([X|TX], [Y|TY]) :- tran(X, Y), listtran(TX, TY).

%% b.
p(a) :- q(b).
q(b).

%% P(X) returns X = a
