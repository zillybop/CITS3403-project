# CITS3403-project

# Rationale - from discussion in meeting on 21/04/2025
- Introductory page
    - Explains the function of the website.
    - Explains each of the pages.
    - Encourages the user to make an account.
    - No functionality, just informational.
    - Could it be better to just load what's currently the visualise page on lauch and have tooltips and other text elements to explain things rather than a whole "redundant" page?
- Upload page
    - User chooses images to upload and store on their account in their collection.
- Share page
    - User can post images from their collection to a linear feed.
    - User can delete images from this feed.
    - Also shows a feed of images from their friends that have been shared.
    - Users outgoing and incoming feeds done side by side on the same page?
- Visualise page
    - Think it should probably be renamed something like "manipulate".
    - If not logged in, allows the user to upload a single image.
    - Otherwise allows the user to pick an image from their collection.
    - Lets the user perform all the different image analysis, alteration, and other manipulations.
    - Once finished the user can download the image or, if logged it, can save it to their collection.
- Collection page
    - We should make a page for the user to view their collection of images.
    - User should be able to download images from the collection too.
    - Should also be able to delete images from their collection.
    - Could this be part of what is currently the upload page?
- Logging in
    - Will need a log-in (or log-out) button built into `base.html`.
    - Will need page for viewing account info including adding and managing friends.
    - Should logging in have its own button somewhere at the top or should it be part of the nav bar?


# Purpose:
a description of the purpose of the application, explaining its design and use.
- The purpose of this application is to provide a web-based image processing tool that allows users to upload images, apply various image processing techniques, and share the results with others. The application is designed to be user-friendly and accessible, making it easy for anyone to perform image processing tasks without needing extensive technical knowledge.
- The application is built using Flask, a lightweight web framework for Python, and utilises various image processing libraries to perform tasks such as black and white conversion, edge detection, and connected components analysis. Users can upload images, apply the desired processing techniques, and then share the processed images with others in some way (TBD)

## Tools
- First: Black and white conversion
- Potential enhancements:
    - Edge detection
    - Connected components



# Members
|UWA ID |  Name | Github Username  |
|-------|-------|------------------|
|23815348| Aaron Barneveld Labbe| Attempt-27 |
|23804015| Alec Hassell | zillybop         |
|24265974| Audrey Tan | aud-tan |
|23476285| Ryan Allagapen | teylan3007 |

# Instructions for Launch
Install requirements from requirements.txt
```bash
pip install -r requirements.txt
```
Active the virtual environment
```bash
source application-env/bin/activate
```

Run the application
```bash
flask run
```

# Instructions for tests

