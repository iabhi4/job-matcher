from utils.db import get_db
from utils.logging_config import get_logger
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pyswip import Prolog

logger = get_logger(__name__)
db = get_db()

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_categories():
    logger.info("Fetching categories from the database")
    category_collection = db['categories']
    categories = category_collection.find({}, {"_id": 0})
    logger.info(f"Fetched {len(list(categories))} categories")
    return list(categories)


def get_category_rule(category_name):
    logger.info(f"Fetching rule for category: {category_name}")
    category_rules_collection = db['categories']
    rule = category_rules_collection.find_one({"category": category_name}, {"_id": 0, "rule": 1})
    if rule:
        logger.info(f"Rule for category {category_name}: {rule['rule']}")
        return rule['rule'].split(',')
    else:
        logger.warning(f"No rule found for category: {category_name}")
        return None

def get_category_rules_dict():
    logger.info("Fetching category rules from the database")
    category_rules_collection = db['categories']
    category_rules = category_rules_collection.find({}, {"_id": 0})
    
    category_rules_dict = {}
    for rule in category_rules:
        category_name = rule['category']
        rule_value = rule['rule']
        if category_name in category_rules_dict:
            category_rules_dict[category_name].append(rule_value)
        else:
            category_rules_dict[category_name] = [rule_value]
    
    logger.info(f"Fetched rules for {len(category_rules_dict)} categories")
    return category_rules_dict


def compute_similarity(list1, list2, threshold=0.8):
    logger.info(f"Calculating similarity between lists with threshold {threshold}")
    embeddings1 = model.encode(list1)
    embeddings2 = model.encode(list2)

    logger.info("Embeddings generated for both lists")

    cosine_scores = cosine_similarity(embeddings1, embeddings2)
    logger.debug(f"Cosine similarity scores: {cosine_scores}")

    max_similarities = np.max(cosine_scores, axis=1)
    average_similarity = np.mean(max_similarities)
    logger.info(f"Average similarity: {average_similarity}")

    return average_similarity

def string_matching_rules(category_rules_dict, extracted_info):
    logger.info("Processing string matching rules")
    matched_categories = {}
    for category, rules in extracted_info.items():
        for rule in rules:
            if rule in extracted_info.get(category, []):
                matched_categories.append(category)
                break
    logger.info(f"Matched categories: {matched_categories}")
    return matched_categories

"""def prepare_prolog_facts(similarity_results, threshold):
    logger.info("Preparing Prolog facts")
    prolog_facts = []
    for category, similarity_score in similarity_results.items():
        category_prolog = category.replace(' ', '_').lower()
        match_status = 'match' if similarity_score >= threshold else 'no_match'
        fact = f"category_similarity('{category_prolog}', {similarity_score}, {match_status})."
        prolog_facts.append(fact)
    logger.info(f"Prepared {len(prolog_facts)} Prolog facts")
    return prolog_facts

def write_prolog_facts(facts, filename='similarity_facts.pl'):
    logger.info(f"Writing Prolog facts to {filename}")
    with open(filename, 'w') as file:
        for fact in facts:
            file.write(fact + '\n')
    logger.info("Prolog facts written successfully")

def run_prolog_reasoning():
    logger.info("Running Prolog reasoning")
    prolog = Prolog()
    prolog.consult('matching_rules.pl')
    percentage_result = list(prolog.query('match_percentage(Percentage)'))
    if percentage_result:
        match_percentage = percentage_result[0]['Percentage']
    else:
        match_percentage = 0.0
    matched_categories_result = list(prolog.query('matched_categories(Categories)'))
    if matched_categories_result:
        matched_categories = matched_categories_result[0]['Categories']
        matched_categories = [str(cat) for cat in matched_categories]
    else:
        matched_categories = []
    logger.info(f"Prolog reasoning completed with match percentage: {match_percentage} and matched categories: {matched_categories}")
    return match_percentage, matched_categories

def process_matching(extracted_info, category_rules_dict, categories, threshold=0.75):
    logger.info("Processing matching")
    similarity_results = {}
    for category in categories:
        extracted_values = extracted_info.get(category, [])
        user_values = category_rules_dict.get(category, [])
        similarity_score = compute_similarity(extracted_values, user_values)
        similarity_results[category] = similarity_score
    logger.info(f"Similarity results: {similarity_results}")
    prolog_facts = prepare_prolog_facts(similarity_results, threshold)
    write_prolog_facts(prolog_facts)

    match_percentage, matched_categories = run_prolog_reasoning()
    logger.info(f"Matching process completed with match percentage: {match_percentage}")
    return match_percentage, matched_categories, similarity_results
"""