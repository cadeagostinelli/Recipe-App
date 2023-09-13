import random
import streamlit as st
from yt_extractor import extract_info
import database_service as dbs
from yt_extractor import get_duration_text
from youtube_dl.utils import ExtractorError

st.title("Recipe APP")

menu_options = ("Today's recipe", "All recipes", "Add recipe", "Find recipes")
selection = st.sidebar.selectbox("Menu", menu_options)

if selection == "All recipes":
    st.markdown(f'## All recipes')
    recipes = dbs.get_all_recipe()
    if not recipes:
        st.text("No recipes in database!")
    else:
        for re in recipes:
            url = "https://youtu.be/" + re["video_id"]
            st.text(re["title"])
            st.text(f"{re['channel']} - {get_duration_text(re['duration'])}")
            deletion = st.button('Delete recipe', key=re["video_id"])
            if deletion:
                dbs.delete_recipe(re["video_id"])
                st.experimental_rerun()
            st.video(url)

elif selection == 'Add recipe':
    st.markdown(f'## Add recipe')
    url = st.text_input('Please enter the video url')
    if st.button("Add recipe"):
        if url:
            recipe_data = extract_info(url)
            if recipe_data is None:
                st.text("Could not find video, please try another.")
            else:
                st.text(recipe_data['title'])
                st.text(recipe_data['channel'])
                st.video(url)
                dbs.insert_recipe(recipe_data)
                st.text("Added recipe!")

elif selection == "Today's recipe":
    st.markdown(f"## Today's recipe")
    recipes = dbs.get_all_recipe()
    if not recipes:
        st.text("No recipes in Database")
    else:
        to = dbs.get_recipe_today()
        if not to:
            recipes = dbs.get_all_recipe()
            n = len(recipes)
            index = random.randint(0, n - 1)
            to = recipes[index]
            dbs.update_recipe_today(to)
        else:
            to = to[0]
            st.text("Try inserting additional recipes!")

        if st.button("Choose another recipe"):
            recipes = dbs.get_all_recipe()
            n = len(recipes)
            if n > 1:
                index = random.randint(0, n - 1)
                to_new = recipes[index]
                while True:
                    index = random.randint(0, n - 1)
                    to_new = recipes[index]
                    if to_new['video_id'] != to['video_id']:
                        break
                to = to_new
                dbs.update_recipe_today(to)

            url = "https://youtu.be/" + to["video_id"]
            st.text(to["title"])
            st.text(f"{to['channel']} - {get_duration_text(to['duration'])}")
            st.video(url)

elif selection == "Find recipes":
    st.markdown(f'## Find recipes')
    st.text("Let's find a recipe just for you!")

    keyword = st.text_input('Please enter an ingredient, dish, or other interest you would like to find!')

    if keyword:
        url = "https://www.youtube.com/results?search_query=" + keyword

        # Extract recipe data only if URL is not empty
        if url != '':
            recipe_data = extract_info(url)

            if recipe_data is not None:
                st.text(recipe_data["title"])
                st.text(f"{recipe_data['channel']} - {get_duration_text(recipe_data['duration'])}")
                st.video(url)

                st.text("Would you like to add this recipe?")
                if st.button("Add recipe"):
                    dbs.insert_recipe(recipe_data)
                    st.text("Added recipe!")
    else:
        st.text("For best results, be specific!")
