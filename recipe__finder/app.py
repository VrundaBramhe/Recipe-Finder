from flask import Flask, request, render_template
import requests

api_key = "a0377c80b7ca4d57ae4d85675494f7eb"
params ={"apiKey" : api_key,"instructionsRequired":True,"addRecipeInstructions" : True,"number":12}
base_url = "https://api.spoonacular.com/recipes/complexSearch"

app = Flask(__name__)


@app.route('/')
def show_home_page():
	return render_template('homepage.html')


@app.route('/searching_page', methods=['GET', 'POST'])
def find_recipes():

    if request.method == 'POST':
        ingredient = request.form['ingredient']

        query_params = params.copy()
        query_params['includeIngredients'] = ingredient

        response = requests.get(base_url, params=query_params)
        recipes = response.json()
        recipes_list = recipes.get("results", [])
        print("Ingredient:", ingredient)
        print("API URL:", response.url)
        print("Response JSON:", recipes)

        return render_template('results.html',recipes_list=recipes_list,ingredient=ingredient)

    else:
        return render_template('searching_page.html')






@app.route('/show_specific_recipe', methods=['POST'])
def show_specific_recipe():
    recipe_id = request.form['recipe_id']
    recipe_name = request.form['recipe_name']
    recipe_image = request.form['recipe_image']



    # ingredients
    ingredients_list_response = requests.get(f"https://api.spoonacular.com/recipes/{recipe_id}/ingredientWidget.json",
                                             params={"apiKey": api_key})
    ingredients_list = ingredients_list_response.json()
    ingredients_array = []
    for ele in ingredients_list["ingredients"]:
        ingredients_array.append(ele["name"])

    # steps
    step_response = requests.get(f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions",
                                 params={"apiKey": api_key})
    steps = step_response.json()
    recipe_steps = steps[0]["steps"]  # array
    steps_array = []
    for ele in recipe_steps:
        steps_array.append(ele["step"])


    return render_template('specific_recipe.html' , recipe_name=recipe_name,recipe_ingredients=ingredients_array,recipe_steps=steps_array,dish_img=recipe_image)

# @app route(/'specific_recipe',methods=['GET', 'POST'])
# def show_specific_recipe(recipeid):
#     # print("Steps : ")
#     step_response = requests.get(f"https://api.spoonacular.com/recipes/{recipeid}/analyzedInstructions",
#                                  params=params)
#     steps = step_response.json()
#     recipe_steps = steps[0]["steps"]  # array
#     steps_list = []
#     for ele in recipe_steps:
#         steps_list.append(ele["step"])







if __name__ == "__main__":
    app.run(debug=True)
