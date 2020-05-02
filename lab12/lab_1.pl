%% a.
%% Exercise 1.4
%% 1.
killer(Butch).
%% 2.
married(Mia, Marsellus).
%% 3.
dead(Zed).
%% 4.
kills(Marsellus, X) :-
    footMassage(Mia, X).
%% 5.
loves(Mia, X) :-
    goodDancer(X).
%% 6.
eats(Jules, X) :-
    nutritious(X);
    tasty(X).
/*
I simply converted names atoms, unknowns to variables, and predicates to functors
This seemed to fit Prolog's basic structure well
*/

%% b.
%% Exercise 1.5
%% 1. 
/*
yes
Prolog simply looks at the fact wizard(ron)
*/
%% 2. 
/*
no
Prolog doesn't have the functor witch/1
*/
%% 3. 
/*
no
Prolog doesn't have a variable or atom hermione
*/
%% 4. 
/*
no
Prolog doesn't have a variable or atom hermione
*/
%% 5. 
/*
yes
Prolog infers the head wizard(harry) :- hasBroom(harry), hasWand(harry)
hasBroom(harry) is infered from hasBroom(harry) :- quidditchPlayer(harry)
quidditchPlayer(harry) and hasWand(harry) are both facts
*/
%% 6. 
/*
no
Prolog doesn't have a variable or atom Y
*/
%% 7. 
/*
no
Prolog doesn't have the functor witch/1
Prolog doesn't have a variable or atom Y
*/

%% b.
/*
Prolog doesn't really support propositional logic syntax but from our reading, we found that Prolog uses modus ponens inference to make assertions about a head from a body

foo(X) :- bar(X)

this structure represents modus ponens
so if the body is true: bar(y)
then the head is true: foo(y)
*/

%% c.
/*
The Horn clauses syntax provides a more efficient way of representing propositional logic that makes sense for a programming environment.
*/

%% d.
/*
It seems that Prolog offers this interface through the queries and responses to the knowledge base.
From the terminal, one can ASK the knowledge base for some fact, and the knowledge base TELLS the response.
*/
