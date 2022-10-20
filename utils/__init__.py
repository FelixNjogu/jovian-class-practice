#some statistical utilities

def probability(matching_outcomes, total_outcomes):
    """compute probabilty of an event when all outcomes are given"""
    return matching_outcomes/total_outcomes
def union_probability(p_a,p_b,p_intersection):
    """compute probability of P(A or B) given P(A), P(B)"""
    return p_a+p_b-p_intersection