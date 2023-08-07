# Python_project

This is a query retrieval web app, that uses the tf-idf concept of NLP. Built in python and deployed on Heroku.

[Check webApp](https://dsm-answer-s-voice-web.herokuapp.com/)
![Home Page](https://user-images.githubusercontent.com/47668949/154901789-d1f59167-1648-4f82-a3e3-23aaf3a053bf.png)

## Code Directory

**corpus**: This is our database. The model will try to search the query response from this corpus. We are using a very small corpus in our project, but this can be expanded. Just the initial runtime will increase, later it will use the stored dictionary for query retireval.

**compute.py**: This has main logic of our model.

compute_idfs(documents): Given a dictionary of `documents` that maps names of documents to a list of words, return a dictionary that maps words to their IDF values.

main(ques): This has two functions
- First create the dictionary, that maps word to their idf values. and store in a file using pickle.
- and find top files using TF-IDF and then top sentences using query density and returns top matching sentence.

**speechWeb.py**: This has the logic to convert the audio query into text query.

**views.py**: This has the form required to upload query.

## How to Run Code Locally

Make sure you have all the required packages. `pip install -r requirements.txt`

`python manage.py runserver`

This will start the webapp in your localhost, you can access on http://127.0.0.1:8000/.

## Branches

I have created few braches with each few feature or method:
- answer: no voice feature
- answer_voice: voice feature using pyAudio
- answer_voice_web: voice feature using web recorder.js

Thanks to [addpipe](https://github.com/addpipe) for the web audio recorder code and nice [blog post](https://blog.addpipe.com/using-recorder-js-to-capture-wav-audio-in-your-html5-web-site/).