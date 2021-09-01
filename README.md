A Pic To Eat

Reduce food waste with a single picture of your fridge.

=> What :

We have noticed that we are getting "greener" to reduce our environmental impact and control the quality of what we eat.
This way, we often find ourselves with various fruits and vegetables rotting at the bottom of our fridge becausse of a lack of cooking knowledge.

Artificial intelligence can help us fight this situation, but how?

The process imagined and deployed on heroku is as follows :
- Take a picture of your fridge
- Load it on our app
- The IA will:  - Crop it in patches
                - Detect all the fruits and vegetables present
                - Live scrap Marmiton.org (a famous french cooking recipes website) in order to find all the recipes that contains the detected products
                - Suggest you a top 3 of the best recipes regarding the reviews

- You now have the keys to act against food waste, bon appétit.

=> Why :

This project was carried out during the last two weeks of the developer training in artificial intelligence provided by Le Wagon.
The aim of this exercise was to use some of the techniques acquired during this program.
Aware of the environmental issues, we wanted to help reduce food waste.

=> Who :

Arnaud Taillard

Jérémy Hidalgo

Antoine Lecoursonnois

=> How :

The techniques used are:

- Cropping.
- Deep learning model (CNN) to detect 15 fruits and vegetables.
- Transfer learning (VGG16) to optimize our results (Precision score : 95.9%).
- Live scrapping of the Marmiton website from the detected products.
- Production on heroku.

=> See the presentation :

If you are interested to see our presentation, a video will be available in September 2021 on the Youtube account Le Wagon Nantes - batch data 667 (2nd group).
