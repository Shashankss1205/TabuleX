## Deployed Link
🔗 [https://chatbot-ypewq27giq-et.a.run.app/](https://chatbot-ypewq27giq-et.a.run.app/)



## Inspiration
Tabluar data analysis is a crucial need in various time when we need to deal with a large amount of data.  We have built the tool due to professional needs, personal interest in data analysis, recognizing market demand, desire for innovation, educational purposes, problem-solving drive, efficiency concerns.

## What it does
It can create, run, delete, update tables in real time. Tables can be directly uploaded as a CSV file. Images of tables and handwritten tables can also be uploaded for analysis. It can analyse tons of data and find statistical information in a very short time. It can also automatically reference the desired table based on queries.  It can relate more than one table and answer complex queries asked.

## How we built it
We have built the chatbot using Python, Gemini API, and SQL database. It is a Python based ML + Web application hosted on google cloud services. It comes with an user friendly UI/UX with various options.
The graph plotter is built similarly, the only difference being the LLM model translates the users query to a Python query instead of SQL Query.

## Challenges we ran into
Challenges that we ran into include:
Integration of Gemini API with SQL database. Also, there are no previous solutions which I could refer to. Secondly, challenges were faced during prompting the Gemini API to give the best results.

## Accomplishments that we're proud of
1. Tables can directly be fed into the website as CSV format files
2. It is able to analyse handwritten table or printed table images efficiently.
3. It can reference to more than one table at a time to answer queries that involve multiple table schema. The queries can be related to Creation, reading, updating, deleting and even analysing a table from the database.
4. It has history mechanism included with it, helping it understand the contextual references.
5. Message can also be input by users using their voice.
6. The chatbot we built has multilingual support.
7. Sample questions are listed to assist users with a feature to copy them.
8. The Tabular Data Analysis tool has user friendly UI/ UX combined with a dark mode toggle button.
9. The chatbot is made responsive, so it can  be used in mobiles, tablets as well as desktops.
10. The Graph Plotter can easily plot any types of graph making large data visualisation easy.
11. A similar graph guide is provided to assist users for the types of graphs.



## What we learned
1. Integrating Gemini API with SQL helped me learn more about Gemini about how powerful it is, how efficiently it can work with different types of data and the fact that it can do wonders!
2. Gained knowledge about Google Cloud Services and its features, along with libraries that facilitate resource management. 
3. Learned effective prompt engineering to gather relevant data from LLM models like the Gemini API.

## What's next for TabularDataAnalyser
Our future endeavors include adding various new functionalities based on user needs.



# Setting up locally
1. Install python (skip, if already present)
2. pip install virtualenv => virtualenv myenv
3. For Windows: 
    myenv\Scripts\activate
   For Linux/Mac:
    source myenv/bin/activate
4. pip install -r requirements.txt
5. python app.py.

(Steps 2 and 3 can be skipped if you choose not to create a virtual environment)
