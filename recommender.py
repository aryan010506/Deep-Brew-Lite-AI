from drinks_db import drinks

def recommend_drink(profile):
    scored_drinks = []

    for drink in drinks:
        score = 0

        if drink["type"] == profile["preferred_type"]:
            score += 5
        

        if drink["milk"] == profile["milk"]:
            score += 3
            

        sweet_diff = abs(drink["sweetness"] - profile["sweetness"])
        score += (5 - sweet_diff)
        
        caffeine_diff = abs(drink["caffeine"] - profile["caffeine"])
        score += (5 - caffeine_diff)

        scored_drinks.append((drink, score))

    scored_drinks.sort(key=lambda x: x[1], reverse=True)
    return scored_drinks[0][0]