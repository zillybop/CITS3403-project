# CITS3403-project


## Purpose, Design, and Use:
### Purpose
The purpose of this application is to provide a web-based image processing tool that allows users to upload images, apply various image processing techniques, and share the results with others. The application is designed to be user-friendly and accessible, making it easy for anyone to perform image processing tasks without needing extensive technical knowledge.
### Design
The logical layout of the website is as follows:
- Navigation bar and log-in/out button present on every page.
- Introductory page ("introductory" view)
    - First page the user sees (acts as index).
    - Explains the purpose of the website.
    - Explains how to use the website.
        - Describes the different tools.
    - Encourages the user to make an account.
- Collection page ("upload data" view)
    - Must be logged in to use.
    - Displays a collection of the users images.
    - Allows the user to upload new images to their collection.
    - Allows the user to delete images from their collection.
    - User can download an image from their collection.
- Image Analyis Tools page ("visualise data" view)
    - If they're not logged in this page allows the user to upload a single image.
    - Otherwise it allows users to pick an image from their collection.
    - Lets the user perform all the different image analysis, alteration, and other manipulations on their chosen image.
        - Convert to black and white.
        - Edge detection.
        - Connected components.
        - Colour Histogram.
        - Display EXIF data.
        - etc.
    - After performing their analysis the user can download the new image or, if logged in, can save it to their collection.
- Share page ("share data" view)
    - User can post images from their collection to a linear feed.
    - User can remove their images from this feed.
    - This feed also contains images that the users friends have shared on their feed.
- Account page
    - Allows the user to add and remove friends.
    - Allows the user to delete their account and all associated data.
    - Allows the user to change their password.
### Use

## Group Members
| UWA ID | Name | Github Username |
|--------|------|-----------------|
| 23815348 | Aaron Barneveld Labbe | Attempt-27 |
| 23804015 | Alec Hassell | zillybop |
| 24265974 | Audrey Tan | aud-tan |
| 23476285 | Ryan Allagapen | teylan3007 |

## Instructions for Launch
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
Some dummy accounts have been created for testing purposes. The credentials are as follows:
|username|password|
|--------|-------|
|admin  |password|
|admin2  |password2|
|admin3  |password3|
|admin4  |password4|
|admin5  |password5|
