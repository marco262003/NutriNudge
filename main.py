import json

# food swaps
healthy_swaps = {
    "white rice": "brown rice","pork": "tofu","soy sauce": "calamansi juice","pasta": "sweet potato noodles",
    "cream": "coconut milk","singkamas": "carrots","talong": "zucchini","mani": "edamame","munggo": "lentils",
    "bataw": "green beans","patani": "chickpeas","kundol": "daikon radish","patola": "okra","upo": "chayote",
    "kalabasa": "sweet potato","labanos": "turnip","mustasa": "kangkong","sibuyas": "leeks","kamatis": "bell pepper",
    "bawang": "shallots","luya": "turmeric","linga": "chia seeds","sigarilyas": "asparagus"
}

# Basic ingredient prices
prices = {
    "brown rice": 15.00, "munggo": 20.00, "malunggay": 10.00, "calamansi juice": 10.00,
    "tofu": 30.00, "kangkong": 15.00, "kamatis": 20.00, "sibuyas": 15.00,
    "sweet potato": 20.00, "coconut milk": 25.00, "kalabasa": 15.00, "talong": 15.00,
    "tilapia": 50.00, "sigarilyas": 20.00, "bawang": 10.00, "luya": 10.00,
    "banana": 10.00, "avocado": 30.00, "sweet potato noodles": 25.00, "bagoong": 15.00,
    "pandan": 10.00, "tamarind": 15.00, "chili pepper": 10.00, "singkamas": 15.00,
    "mani": 20.00, "bataw": 20.00, "patani": 20.00, "kundol": 15.00, "patola": 20.00,
    "upo": 15.00, "labanos": 15.00, "mustasa": 15.00, "linga": 30.00, "ampalaya": 20.00,
    "gabi": 15.00, "kabute": 25.00, "kamote tops": 10.00, "langka": 25.00, "mais": 15.00,
    "flour": 30.00, "pechay": 15.00, "pipino": 15.00, "repolyo": 20.00, "sayote": 15.00,
    "gluten-free soy sauce": 35.00
}

# List to store meal plans
meals = []

def load_recipes():
    """Load recipes from JSON file"""
    try:
        with open("recipes.json", "r") as file:
            return json.load(file)
    except:
        print("Error loading recipes file!")
        return []

def load_meals():
    """Load saved meals from file"""
    try:
        with open("saved_meals.json", "r") as file:
            return json.load(file)
    except:
        print("No saved meals found. Starting with empty list.")
        return []

def save_meals():
    """Save meals to file"""
    with open("saved_meals.json", "w") as file:
        json.dump(meals, file, indent=4)

def calculate_match_score(pantry_items, recipe_ingredients):
    """Calculate how many ingredients match between pantry and recipe"""
    # Clean up the pantry items
    pantry_items = [item.lower().strip() for item in pantry_items]

    # Count matching ingredients
    matching = []
    for ingredient in recipe_ingredients:
        ingredient = ingredient.lower().strip()
        if ingredient in pantry_items:
            matching.append(ingredient)

    # Calculate score as percentage
    if len(recipe_ingredients) == 0:
        return 0, []

    score = (len(matching) / len(recipe_ingredients)) * 100
    return score, matching


def find_recipes(pantry_items, recipes, dietary_choice="none"):
    """Find recipes that match pantry items"""
    matching_recipes = []

    # Filter recipes by dietary preference
    if dietary_choice.lower() != "none":
        filtered_recipes = []
        for recipe in recipes:
            if recipe["dietary"].get(dietary_choice.lower(), False):
                filtered_recipes.append(recipe)
    else:
        filtered_recipes = recipes

    # Find matching recipes
    for recipe in filtered_recipes:
        score, matched = calculate_match_score(pantry_items, recipe["ingredients"])

        # Only include recipes with at least 75% match
        if score >= 75:
            matching_recipes.append({
                "recipe": recipe,
                "match_score": score,
                "matched_ingredients": matched
            })

    return matching_recipes

def display_recipe(recipe_match):
    """Display a recipe with details"""
    recipe = recipe_match["recipe"]
    score = recipe_match["match_score"]
    matched = recipe_match["matched_ingredients"]

    print(f"\n==== {recipe['name']} ====")
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(f"  - {ingredient}")

    print("\nNutrition:")
    for key, value in recipe["nutrition"].items():
        print(f"  {key}: {value}")

    print(f"\nPrice: ₱{recipe['price']:.2f}")
    print(f"Match Score: {score:.1f}%")

    # Show missing ingredients
    if score < 100:
        print("\nMissing Ingredients:")
        missing = [ing for ing in recipe["ingredients"] if ing not in matched]
        missing_cost = 0
        for ing in missing:
            cost = prices.get(ing, 0)
            missing_cost += cost
            print(f"  - {ing} (₱{cost:.2f})")
        print(f"Total cost for missing ingredients: ₱{missing_cost:.2f}")

    # Show instructions
    print("\nCooking Instructions:")
    instructions = recipe.get("instructions", [])
    if isinstance(instructions, str):
        instructions = [step.strip() for step in instructions.split(".") if step.strip()]

    for i, step in enumerate(instructions, 1):
        print(f"  Step {i}: {step}")

    # Add to meals list
    meals.append({
        "name": recipe["name"],
        "match_score": score
    })

def main():
    """Main program function"""
    # Load data
    recipes = load_recipes()
    global meals
    meals = load_meals()

    print("=== Welcome to NutriNudge! ===")

    # Get user input
    pantry_input = input("Enter your pantry ingredients (comma-separated ex: sitaw, bawang, calamansi juice, soy sauce): ")
    pantry_items = [item.strip() for item in pantry_input.split(",")]

    dietary = input("Dietary preference (vegan/vegetarian/gluten-free/none): ").lower()
    if dietary not in ["vegan", "vegetarian", "gluten-free", "none"]:
        print("Invalid choice. Using 'none' as default.")
        dietary = "none"

    # Find matching recipes
    matches = find_recipes(pantry_items, recipes, dietary)

    if not matches:
        print("Sorry, no matching recipes found!")
    else:
        # Sort by match score (highest first)
        matches.sort(key=lambda x: x["match_score"], reverse=True)

        # Display matching recipes
        print(f"\nFound {len(matches)} matching recipes:")
        for match in matches:
            display_recipe(match)

    # Show meal plan
    print("\n=== Meal Plan Summary ===")
    if not meals:
        print("No meals saved yet.")
    else:
        for meal in meals:
            print(f"  - {meal['name']} (Match: {meal['match_score']:.1f}%)")

    # Save meals
    save_meals()

if __name__ == "__main__":
    main()