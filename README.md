# YouScan

## 1. Are you a good detective?<br />
  Task located in "Task 1" folder.<br />
  There are images of viualisations, PDF file with conclusions and Jupiter Notebook.<br /><br />

  Requirements for Jupiter Notebook:<br />
  libraries:<br />
    &emsp;pandas: 1.3.5<br />
    &emsp;numpy: 1.21.2<br />
    &emsp;matplotlib: 3.5.2<br />
    &emsp;seaborn: 0.11.1<br />
    &emsp;scikit-learn: 0.24.2<br /><br />

## 2. Are you a good hacker?<br />
  Task located in "Task 2" folder.<br />
  There are "main" app script, database initiation script, templates of pages in "templates" folder.<br /><br />

  Requirements for app:<br />
  libraries:<br />
    &emsp;flask: 2.0.2<br />
    &emsp;psycopg2: 2.9.3<br />
    &emsp;groq: 0.1.0<br />
    &emsp;re: 2.7.1<br />
    &emsp;requests: 2.25.1<br /><br />

### Description:<br />
Storage - I am using local PostgreSQL with 2 main tables - users for authentication and notes itself. You can find a scheme in the “Task 2” folder.<br /><br /> 

LLM - I stopped on open-source LLM model llama3-70b-8192 powered by groq.com. It has such limitations: requests per minute = 30, requests per day =14400, tokens per minute = 6000 and context window 8192 tokens (6000 words). https://console.groq.com/settings/limits<br /><br />

App - Main app created using Flask.<br /><br />

Architecture - we have a database setup on pgadmin4, an app that connects to it for note extraction and save and an LLM model that receives questions with notes and gives answers based on the question.<br /><br />

Live demo will be sent to you personally.

