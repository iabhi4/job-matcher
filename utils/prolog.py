from pyswip import Prolog
from utils.logging_config import get_logger
import os

logger = get_logger(__name__)

def prolog_matching(rules, extracted_info):
    """
    Perform Prolog matching using rules and extracted information from GPT.

    Args:
        rules (dict): Dictionary of rules from the database which were created by the user.
        extracted_info (dict): Dictionary of extracted information.

    Returns:
        dict: Matching results, including matched rules and a score.
    """
    logger.info("Initializing Prolog for matching.")
    prolog = Prolog()


    logger.info("Consulting Prolog file: matching.pl")
    prolog.consult('matching.pl')

    logger.info("Asserting rules into Prolog.")
    for category, rule_value in rules.items():
        if rule_value:
            logger.debug(f"Asserting rule: rule('{category}', '{rule_value}')")
            prolog.assertz(f"rule('{category}', '{rule_value}')")

    logger.info("Asserting extracted information into Prolog.")
    for category, extracted_value in extracted_info.items():
        if extracted_value:
            logger.debug(f"Asserting extracted: extracted('{category}', '{extracted_value}')")
            prolog.assertz(f"extracted('{category}', '{extracted_value}')")

    logger.info("Querying Prolog for match count.")
    match_count = list(prolog.query("match_count(Count)"))[0]["Count"]
    logger.debug(f"Match count: {match_count}")

    logger.info("Querying Prolog for matched rules.")
    matched_rules = list(prolog.query("matched_rules(List)"))[0]["List"]
    logger.debug(f"Matched rules: {matched_rules}")

    result = {
        "score": match_count * 10,  # Scoring idea: 10 points per match
        "matched_rules": matched_rules,
    }
    logger.info(f"Matching results: {result}")
    return result