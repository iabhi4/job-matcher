% matching_rules.pl

% Load the similarity facts
:- [similarity_facts].

% Rule to determine if a category matches
category_matches(Category) :-
    category_similarity(Category, SimilarityScore, match),
    SimilarityScore >= 0.75.

% Collect all matched categories
matched_categories(Categories) :-
    findall(Category, category_matches(Category), Categories).

% Calculate the match percentage
match_percentage(Percentage) :-
    findall(Category, category_similarity(Category, _, _), AllCategories),
    length(AllCategories, TotalCategories),
    matched_categories(MatchedCategories),
    length(MatchedCategories, MatchedCount),
    Percentage is (MatchedCount / TotalCategories) * 100.
