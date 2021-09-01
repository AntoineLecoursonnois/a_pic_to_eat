from scripts.cropping import *
from scripts.scrapping import *
from scripts.predictions import *
import streamlit as st
import numpy as np
import cv2


def main():
    '''
    Full script read by streamlit to run the app.
    Present and describe the app, load an image, convert it to cv2 object,
    crop it into patches, use those patches to detect products,
    display the results, let the user choose the products he/she wants to cook,
    live scrap marmiton.org using the detected products
    and display a top 3 recipes from a score considering
    the global score of each recipes and the number of rates.
    '''
    # Set the main title
    st.title('📷 A Pic To Eat :yum:')

    # Set a description of project objectives
    st.write("**Reduce food waste with a single picture of your fridge.**")

    # Upload the image of a fridge
    image_file = st.file_uploader("Upload image",
                                  type=['jpeg', 'png', 'jpg', 'webp'])

    # Once it is loaded convert it to a cv2 object
    if image_file is not None:
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)

        # Display the image
        st.image(opencv_image, channels="RGB")

        # Once the user confirm it is the right image launch the process
        if st.checkbox("It's my fridge, process !"):
            # Crop the image into patches
            patch_list = cropping_image(image=opencv_image)

            # Convert patches into numpy array in order to detect products
            patch_array = np.array(patch_list)

            # Detect products
            prediction_dict = predict(patch_array)

            # Insert the results into a list and sort them
            predicted_ingredients = sorted(list(prediction_dict['prediction']))

            # Inform the user that he has detected products
            st.write("These are the products I have detected.")

            # Display them into 2 columns
            predicted_ingredients = sorted(predicted_ingredients)
            col_1, col_2, = st.columns(2)

            # Insert a checkbox for each product
            option_a = col_1.checkbox(predicted_ingredients[0])
            known_variables = [option_a]

            # Display as many checkboxes as detected products (8 max)
            if len(predicted_ingredients)>1:
                option_b = col_2.checkbox(predicted_ingredients[1])
                known_variables = [option_a, option_b]
                if len(predicted_ingredients)>2:
                    option_c = col_1.checkbox(predicted_ingredients[2])
                    known_variables = [option_a, option_b, option_c]
                    if len(predicted_ingredients)>3:
                        option_d = col_2.checkbox(predicted_ingredients[3])
                        known_variables = [
                            option_a, option_b, option_c, option_d]
                        if len(predicted_ingredients)>4:
                            option_e = col_1.checkbox(predicted_ingredients[4])
                            known_variables = [
                                option_a, option_b, option_c, option_d, option_e
                            ]
                            if len(predicted_ingredients)>5:
                                option_f = col_2.checkbox(predicted_ingredients[5])
                                known_variables = [
                                    option_a, option_b, option_c, option_d,
                                    option_e, option_f
                                ]
                                if len(predicted_ingredients)>6:
                                    option_g = col_1.checkbox(predicted_ingredients[6])
                                    known_variables = [
                                        option_a, option_b, option_c, option_d,
                                        option_e, option_f, option_g
                                    ]
                                    if len(predicted_ingredients)>7:
                                        option_h = col_2.checkbox(predicted_ingredients[7])
                                        known_variables = [
                                            option_a, option_b, option_c, option_d, option_e, option_f,
                                            option_g, option_h
                                        ]

            # Instanciate a list of product choosent by the user
            final_products = []
            counter = 0
            for option in known_variables:
                if option == 1:
                    final_products.append(predicted_ingredients[counter])
                    counter += 1
                else:
                    counter += 1

            # Inform the user that he can choose the products he/she wants to cook
            # Each time the user clic on a checkbox, the full script is re-run
            # considering this new information
            st.write("If you have preferences, please select the products you would like to cook.")
            # Tune the text (center, bold, raise text size and change color to green)
            st.markdown("<center><b><span style='font-size: 180%; color: green'>Top 3 recipes Marmiton from all of these products.</span></b></center>",
                unsafe_allow_html=True)

            # If no product has been selected, use the original list of predictions for scrapping
            # Otherwise, only use the selected products
            if len(final_products) == 0:
                recipes = scrap_marmiton(predicted_ingredients)
            else:
                recipes = scrap_marmiton(final_products)

            # Display the recipe title
            col1, col2, col3 = st.columns(3)
            col1.subheader(recipes['title'][0])
            col2.subheader(recipes['title'][1])
            col3.subheader(recipes['title'][2])

            # Insert the image of each recipe with its url into a variable
            html0=f"<a href={recipes['url_recipe'][0]} target='_blank'><img src={recipes['img_url'][0]}></a>"
            html1=f"<a href={recipes['url_recipe'][1]} target='_blank'><img src={recipes['img_url'][1]}></a>"
            html2=f"<a href={recipes['url_recipe'][2]} target='_blank'><img src={recipes['img_url'][2]}></a>"
            # Display it and let the user click on it to access to the link on marmiton
            col1, col2, col3 = st.columns(3)
            col1.markdown(html0, unsafe_allow_html=True)
            col2.markdown(html1, unsafe_allow_html=True)
            col3.markdown(html2, unsafe_allow_html=True)

            # Display the recipe score
            col1, col2, col3 = st.columns(3)
            col1.metric('Score', recipes['score_review'][0])
            col2.metric('Score', recipes['score_review'][1])
            col3.metric('Score', recipes['score_review'][2])


if __name__ == "__main__":
    main()
