import harperdb

# for reference use streamlit run app.py to run
# Instance
db = harperdb.HarperDB(url="https://cloud-1-recipe.harperdbcloud.com", 
                        username="pasta",
                        password="guy")

SCHEMA = "recipe_repo"
TABLE = "recipes"
TABLE_TODAY = "recipe_today"

# create table if not exists
table_definition = {
    "hash_attribute": "video_id",
    "schema": SCHEMA,
    "table": TABLE,
    "attributes": [
        {"name": "video_id", "type": "string"},
        {"name": "title", "type": "string"},
        {"name": "channel", "type": "string"},
        {"name": "view_count", "type": "number"},
        #{"name": "like_count", "type": "number"},
        {"name": "channel_id", "type": "string"},
        {"name": "duration", "type": "number"},
        #{"name": "categories", "type": "string"},
        #{"name": "tags", "type": "string"}
    ]
}

# insert recipe data
def insert_recipe(info):
    recipe_data = {
        "video_id": info['video_id'],
        "title": info['title'],
        "channel": info['channel'],
        "view_count": info['view_count'],
        #"like_count": info['like_count'],
        "channel_id": info['channel_id'],
        "duration": info['duration'],
        #"captions": info['captions']
        #"categories": info['categories'],
        #"tags": info['tags']
    }
    return db.insert(SCHEMA, TABLE, [recipe_data])

# get all recipes
def get_all_recipe():
    sql_query = f"SELECT * FROM {SCHEMA}.{TABLE}"
    results = db.sql(sql_query)
    return results

def get_recipe_today():
    return db.sql(f"select * from {SCHEMA}.{TABLE_TODAY} where id = 0")

def delete_recipe(recipe_data):
    return db.delete(SCHEMA, TABLE, [recipe_data])

def update_recipe_today(recipe_data, insert=False):
    recipe_data['id'] = 0
    if insert:
        return db.insert(SCHEMA, TABLE_TODAY, [recipe_data])
    return db.update(SCHEMA, TABLE_TODAY, [recipe_data])