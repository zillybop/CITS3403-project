# Overview
For this project you are required to build a data analytics application, which allows users to upload private data, view automated analysis of their data and then selectively share the results with other users. You may interpret the concept of "data" and "analysis"  _very_ _flexibly_. For example, the application could be:

-   An exercise tracking application, where users track their exercise habits, can view stats about their habits, and share information about their achievements with their friends on the system.
-   A statistical analysis tool, allowing users to upload certain types of datasets (e.g. timeseries, tabular data), and then run standard statistical analysis algorithms (e.g. regression, clustering, outlier detection) on them, and share their findings and datasets with their colleagues.
-   A course-selector tool, allowing users to upload details (e.g. times, duration, credit hours) of courses they are interested in taking, and then run scheduling algorithms to generate a plausible selection of units, and allowing users to share suggested schedules with their classmates.
-   A tournament management system, where users can input results of sports/board games tournaments, see player stats, and then share results with other users.
-   An infectious disease monitoring system where users can upload datasets of infections, and the application will plot them on a map and you can share areas with high outbreaks to other users.
-   A news sentiment analysis tool, allowing users to upload or input news content, and then analyse the text using NLP algorithms (e.g., sentiment scoring) to determine overall sentiment, and share the analysed data with their colleagues.
Any method of data entry is fine. For example data could be manually entered by the user, or uploaded in batches in a suitable file format, or automatically sourced from other devices and services (e.g. fitness trackers, smart watches, publicly available feeds and datasets).

Please think carefully about the design of the application. It should be:

-   _Engaging_, so that it looks good and focuses the user on important elements of the application.
-   _Effective_, so it produces value for the user, by providing information, entertainment or community.
-   _Intuitive_, so that it is easy for a user to use.

# Requirements
- _Upload_ - "upload private data"
- _Analyse_ - "view automated analysis of their data"
- _Share_ - "selectively share the results with other users"

# Ideas
### Dungeons and Dragons Character Sheet
- _Upload_:
	- User inputs their character details the first time they use the site as part of the character creation process.
	- User is able to download their character as a file (`.JSON`?) and re-upload it next time they use the site.
	- Character is also stored on the server under the users account.
- _Analyse_:
	- Calculate stats like ability modifiers, armour-class, etc. for each character.
	- Provide info like user's favorite species, class, etc. based on all the characters they've got on their account.
- _Share_:
	- Allow other users to see your characters.
- Pros:
	- Cool format to upload.
- Cons:
	- Only one of us would be familiar with the D&D part of the project.

### Club Manager
- _Upload_:
	- Initial list of club members and their details.
	- Ability to add new members.
	- Financial data.
	- Slightly worried about the "private" part. - Aaron
- _Analyse_:
	- Membership over time.
	- Finances. 
- _Share_:
	- Share club membership and finance info with club members.
- Pros:
	- Clubs on campus.
- Cons:
	- Ignorance of club operations.

### Shortcut Racer
- _Upload_:
	- Users complete the shortcut excersises and data is gathered on that users performance.
- _Analyse_:
	- Speed, % of people who can solve it, (% who used command).
- _Share_:
	- Share perfomance data with other users.
- Pros:
	- Computer science (we're all familiar with it).
- Cons:
	- Analysis is a bit drawn out.

### Music Analyser
- _Upload_:
	- Specific chord, progression, melody, etc.
- _Analyse_:
	- Music theory analysis of whatever info -- what chord it makes, parts of it, modes.
- _Share_:
	- Can share musical elements with other users.
- Pros:
	- Shouldn't be to hard if we can do the music theory.
- Cons:
	- Music theory.

### Youtube to Sheet Music:
- _Upload_:
	- User supplies the website with a link to a song on Youtube.
- _Analyse_:
	- User selects whether they want chords, melody, etc.
	- Using some sort of already made pitch detection package or software the website transcribes the song as playable sheet music (need to see if something like this exists that we could use).
- _Share_:
 	- Share transcribed songs with other users.
- Pros:
	- Very practical.
 	- Simple front end.
- Cons:
	- Don't yet know if there is any sort of packages that we could use.
	- How much work are we doing and how much are we outsourcing.
	- Copyright issues?
    
### Probability Visualiser
- _Upload_:
	- Your own dataset.
- _Analyse_:
	- Normal distributions, binomial theorem.
- _Share_:
	- Share your analysis and datasets with other users.
- Pros:
	- Very data science.
- Cons:
	- Probably hard.
 	- Kind of boring. - Aaron
