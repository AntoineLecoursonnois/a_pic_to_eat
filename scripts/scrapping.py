import requests
from bs4 import BeautifulSoup
import pandas as pd


def build_soup(input):
    '''
    Return a soup from a list of ingredients found out by our model.
    '''

    # Is the input a list of strings
    try:
        assert isinstance(input, list)
        assert all(list(map(lambda string: isinstance(string, str),
                            input)))
    except AssertionError:
        print('-------------------------------------------------------', '\n',
              'Be aware that i only eat a single list of strings !', '\n',
              '-------------------------------------------------------')

    # Create a finding text for each ingredient
    text_url = "-".join(input)

    # Request marmiton.org and catch the Soup
    response = requests.get(
        f'https://www.marmiton.org/recettes/recherche.aspx?aqt={text_url}')
    soup = BeautifulSoup(response.content, "html.parser")

    return soup


def parse_recipes(soup):
    '''
    Use soup from build_soup function to scrap the recipes.
    Retrieve recipes with a blurred image.
    Generate and return a dataframe containing all the informations to display on Streamlit
    (A dataframe is the format needed by Streamlit).
    '''
    # Instanciate the lists needed to store the informations for each recipe
    url_recipe = []
    title = []
    img_url = []
    star_recipe = []
    review_nbr = []

    # Scrap all recipes items from first page
    # If the url given does not work anymore, just rough scrap a recipe of crepes
    for card in soup.find_all(
            'a',
        {'class': 'SearchResultsstyle__SearchCardResult-sc-1gofnyi-2 gQpFpv'}):

        # Url recipe
        try:
            url_recipe.append('https://www.marmiton.org' + card.get("href"))
        except:
            url_recipe.append(
                'https://www.marmiton.org/recettes/recette_crepes-faciles-a-faire-avec-les-enfants_45187.aspx'
            )

        # Title recipe
        try:
            title.append(card.find('h4').string)
        except:
            title.append('Crepes faciles')

        # Url picture
        try:
            img_url.append(card.find('img').get('src'))
        except:
            img_url.append(
                'https://assets.afcdn.com/recipe/20170404/63020_w768h583c1cx2217cy1478.webp'
            )

        # Recipe global score :  0-5 (float)
        try:
            star_recipe.append(float(card.find('span').text.replace('/5', '')))
        except:
            star_recipe.append(1)

        # Number of reviews (int)
        # If there is no review, set the number of reviews to 1
        try:
            rev_result = card.find('div', {
                'class':
                'RecipeCardResultstyle__RatingNumber-sc-30rwkm-3 jIDOia'
            }).text
            review_nbr.append(
                [int(value) for value in rev_result if value.isdigit()][0])
        except:
            review_nbr.append(1)

    # Generate the DataFrame and fill in the columns with the informations just scrapped
    recipe_df = pd.DataFrame({
        'url_recipe': url_recipe,
        'title': title,
        'img_url': img_url,
        'star_recipe': star_recipe,
        'review_nbr': review_nbr
    })

    # Compute a new score for each recipe considering the number of reviews
    recipe_df['score_review'] = round(
        (recipe_df['star_recipe'] + (0.3 * recipe_df['review_nbr'])) / 1.3, 1)

    # Sort the recipes by this new score in a descending way
    recipe_df = recipe_df.sort_values(by=['score_review'], ascending=False)

    # Delete the recipes with a blurred image
    recipe_df = recipe_df[~recipe_df['img_url'].str.contains("blurred")]

    # Set a new index to the dataframe
    recipe_df = recipe_df.reset_index(drop=True)

    # Return the clean dataframe sorted by our computed score
    return recipe_df


def scrap_marmiton(input_ingredients):
    '''
    Use build_soup and parse_recipes functions to generate a dataframe
    from the ingredients detected by our model.
    The dataframe will be used by Streamlit to display the recipes and
    their informations to the user.
    '''
    # Generate a soup from the ingredients detected by our model
    soup = build_soup(input_ingredients)

    # Store the informations found in the soup into a dataframe
    df_recipes = parse_recipes(soup)

    return df_recipes
