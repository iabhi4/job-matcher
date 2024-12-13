% Define user-defined rules
:- dynamic rule/2.

% Define extracted information
:- dynamic extracted/2.

% Matching logic: Match extracted information with user-defined rules
match(Category, Value) :-
    rule(Category, Value),
    extracted(Category, Value).

% Count total matches
match_count(Count) :-
    findall(_, match(_, _), Matches),
    length(Matches, Count).

% List all matched rules
matched_rules(List) :-
    findall((Category, Value), match(Category, Value), List).