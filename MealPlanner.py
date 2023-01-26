from chatgpt_wrapper import ChatGPT
import re
import json

'''
TODO:
    Implement retry prompt on incorrect formatting

WORKFLOW:
    Input preferences
        Flavor
        Diet
        People
    GPT meal plan, ingredients for meals
    On request, GPT generate recipe for a day of meals
        fancier meals
        more customized meals
    Compile into grocery list
    Input meals liked
    Generate preferences from meals
    Loop
'''
json_regex = r".*(\[(?:.|\s?)*\])"

food_preferences_prompt = "Give me a general description of my food preferences given that I like these meals: {}"

food_recommendation_prompt = "Give me a list of {} meals given that my preferences are: {}"
food_recommendation_formatting = "\nDisplayed as a parsable json list. Continue until the output is complete. The meals should be structured as follows: list(str)"

food_recipe_prompt = "Give me a list of recipes for each of the meals listed: {}"
food_recipe_formatting = "\n Don't give me the unformatted recipe. Continue until the output is complete. Displayed as a parsable json list of recipes. The recipes list should be structured as follows: list({\"Name\": (recipe_name),\"Instructions\":(list(recipe_instructions)),\"Ingredients\":(list(recipe_ingredients))})"

food_grocery_prompt = "Give me a grocery list that will tell me everything I need to purchase for these recipes listed, quantities included: {}"
food_grocery_formatting = "\nContinue until the output is complete. Displayed as a parsable json list. The groceries should be structured as follows: list({\"Item\": (item_name), \"Quantity\": (item_quantity)})"

bot = ChatGPT()

def gen_recommendations(preferences, num_recommendations):
    """return list of recommendations given preferrence string

    Args:
        preference (string): describes a preference description
        num_recommendations (int): number of recommendations to pull

    Returns:
        list: list of recommendations
    """
    prompt = food_recommendation_prompt.format(num_recommendations,preferences)
    formatted_prompt = prompt + food_recommendation_formatting

    recommendation_string = bot.ask(formatted_prompt)
    print(recommendation_string)
    json_string = re.search(json_regex,recommendation_string)[0]
    recommendations = json.loads(json_string)

    return recommendations

def gen_preferences(preferred_items):
    """return text encoding preferences from given preferred items

    Args:
        preferred_items (list): list of preferred items

    Returns:
        string : description of preferrence from prefered items
    """
    items_string = ','.join(preferred_items)
    preference = bot.ask(food_preferences_prompt.format(items_string))
    return preference

def gen_recipes(meals):
    meals_string = ",".join(meals)
    prompt = food_recipe_prompt.format(meals_string)
    formatted_prompt = prompt+food_recipe_formatting

    recipes_string = bot.ask(formatted_prompt)
    print(recipes_string)
    json_string = re.search(json_regex,recipes_string)[0]
    recipes = json.loads(json_string)

    return recipes

def gen_groceries(recipes):
    recipes_string = json.dumps(recipes)
    prompt = food_grocery_prompt.format(recipes_string)
    formatted_prompt = prompt+food_grocery_formatting

    groceries_string = bot.ask(formatted_prompt)
    print(groceries_string)
    json_string = re.search(json_regex,groceries_string)[0]
    groceries = json.loads(json_string)

    return groceries

def main():
    preferences = "Healthy mediterranian home-made meals with portions suitable for 3 people with daily calorie restrictions of: 3000, 2500, 2000"
    meals = gen_recommendations(preferences,2)
    print(meals)
    recipes = gen_recipes(meals)
    print(recipes)
    groceries = gen_groceries(recipes)
    print(groceries)

    return

if __name__ == "__main__":
    main()