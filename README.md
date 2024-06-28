## Inspiration
Tabluar data analysis is a crucial need in various time when we need to deal with a large amount of data.  I have built the tool due to professional needs, personal interest in data analysis, recognizing market demand, desire for innovation, educational purposes, problem-solving drive, efficiency concerns.

## What it does
It can create, run, delete, update tables in real time. Tables can be directly uploaded as a CSV file. Images of tables and handwritten tables can also be uploaded for analysis. It can analyse tons of data and find statistical information in a very short time. It can also automatically reference the desired table based on queries.  It can relate more than one table and answer complex queries asked.

## How we built it
I have built the chatbot using Python, Gemini API, and SQL database. It is a Python based ML + Web application hosted on google cloud services. It comes with an user friendly UI/UX with various options.

## Challenges we ran into
Challenges that I ran into include:
Integration of Gemini API with SQL database. Also, there are no previous solutions which I could refer to. Secondly, challenges were faced during prompting the Gemini API to give the best results.

## Accomplishments that we're proud of
1. Tables can directly be fed into the website as CSV format files
2. It is able to analyse handwritten table or printed table images efficiently.
3. It can reference to more than one table at a time to answer queries that involve multiple table schema. The queries can be related to Creation, reading, updating, deleting and even analysing a table from the database.
4. It has history mechanism included with it, helping it understand the contextual references.
5. The chatbot I built has multilingual support.
6. The Tabular Data Analysis tool has user friendly UI/ UX combined with a dark mode toggle button.
7. The chatbot is made responsive, so it can  be used in mobiles, tablets as well as desktops.


## What we learned
1. Integrating Gemini API with SQL helped me learn more about Gemini about how powerful it is, how efficiently it can work with different types of data and the fact that it can do wonders!
2. I came to know about Google cloud services and its features. I learnt about the libraries that can enable me to easily create and manage resources. 
3. I learnt how to effectively use Prompt engineering to gather relevant data from LLM models like gemini api.

## What's next for TabularDataAnalyser
1. My future endeavors include graphical analysis of tabular data as a feature.
2. I also aim to integrate voice recognition along with the other features
3. We can provide table schema as input so that co-relation between tables can be handled more efficiently.


# Setting up locally
1. Install python (skip, if already present)
2. For Windows: 
    myenv\Scripts\activate
   For Linux/Mac:
    source myenv/bin/activate
3. pip install -r requirements.txt
