import json
import os

DB_FILE = "recipes.json"

#function that loads the database into memory
def load_db():
    if not os.path.exists(DB_FILE):
        return {"recipes": []}
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
#function that writes new data to the json file
def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

#function that allows us to add new recipes to our database wothout manually editing the file
def add_recipe(name, url, source=None, category=None, tags=None):
    db = load_db()

    #loop to prevent duplicate recipes
    for recipe in db["recipes"]:
        if recipe["url"] == url:
            return False
        
    db["recipes"].append({
        "name": name,
        "url": url,
        "source": source,
        "category": category,
        "tags": tags or []
    })

    save_db(db)
    return True

#function to grab a random recipe from the database
def get_random_recipe():
    db = load_db()
    if not db["recipes"]:
        return None
    
    import random
    return random.choice(db["recipes"])

#function to search for a recipe based on keywords
def search_recipes(keyword):
    db = load_db()
    keyword = keyword.lower()

    return [
        r for r in db["recipes"]
        if keyword in r["name"].lower()
        or keyword in " ".join(r["tags"]).lower()
    ]

