The goal: create a chat bot that can answer questions from a given PDF.

Initial plan
- Extract text from the PDF
- Create embeddings from the extracted text
- Store the embeddings in a vectorized DB
- Create a script that can answer questions via the DB

Step one:
Extract text from the PDF, using langchain's pypdfloader. For the PDF I'm using an old manual I had lying around in my document's folder.

Step two:
Store the extracted text in ChromaDB using OpenAI's embedding model

Step three:
Write a script for querying the DB using argparser and langchain

Step four:
Asses the model.

First I try asking something directly from the text:
"While some of the equipment mentioned in this manual (such as the Alertor) is not in use at this time"

python query.py --query "what equipment is not in use at this time"

NOTE: While some of the equipment mentioned 
in this manual (such as the Alertor) is not 
in use at this time at the Western Pacific 
Railroad Museum, it is provided in its 
original content in this manual. 


---

             
           
              
          
              


---

      

       
          
            

  
         
           
   
  
           
            
          
             
        
           
           
           
         
            
          
          
       
         
            
          
           
          
             



---

Answer this question based on the above context: what equipment mentioned is not in use at this time?

CLEARLY something went awry, it was able to extract some text and answer my question, however, there are a large number of odd characters. Debugging this further led me to find out it's happening at the document extraction page and is actually a problem with the PDF text itself. The note about the alerter can be copied and pasted but all other text leads to unknown symbols. 

Since the decision to use this data source was arbitrary, let's switch to another document. And this time let's use one that I actually have some legal authority to share, my resume.

After replacing the file, we stop seeing the nonsense characters we were seeing before:

 python query.py --query "what does Kyle Lare do"
Number of requested results 3 is greater than number of elements in index 1, updating n_results = 1
Human: 
Answer the question based only on the following context:

Kyle Lare
713-444-8889   ●   Dallas, TX   ●   kylelare98@gmail.com
EXPERIENCE
Computational Engineer Nov 2021 – Present
Railspire | Dallas, TX
Hired on as the third software engineer at a fast-paced pre-revenue startup with large ambitions 
of automating the rail industry. Working directly under one of the two cofounders and wearing 
many hats along the way including, but not limited to, data scientist, software engineer, and 
systems integration tester. 
    Key Accomplishments:
●Pitched and implemented an ETL data pipeline for analyzing and storing system data to 
provide proactive customer support, software error detection, and queryable results using 
JSON, Python, and MongoDB
●Significantly reduced engineering software testing hours by co-developing a batch-
processing simulation tool using Flask, Docker, Python and RabbitMQ
●Designed, developed and maintained several software applications using Python and QT for 
testing and debugging safety-critical locomotive systems
●Led a push for increased documentation efforts, converted all existing documentation to 
LaTeX and developed a pipeline for automating the document review process
●Collaborated with cross-functional teams to design and analyze a series of experiments for 
quantifying noise in a GPS-RTK system
Student Researcher May 2020 – June 2021
Rice University | Houston, TX
●Developed a polymer model for a protein network interaction with DNA using Python and 
GROMACS in the Center for Theoretical Biological Physics at Rice
●Analyzed simulation trajectories and created informative visuals using Numpy, Matplotlib 
and Seaborn
●Presented results to the Onuchic-Wolynes research groups at Rice University (Oct 2020) 
and at the University of Houston’s 2020 and 2021 Undergraduate Research Day events
Undergraduate Researcher June 2018 - May 2020
University of Houston | Houston, TX
●Debugged Dr. Greg Morrison’s patent sorting machine learning algorithm via analysis of 
large text files (~10 million lines) of unstructured data.
●Worked under Dr. Mini Das on improvement of x-ray technology via digital filter processing 
in Python
EDUCATION
University of Houston  | Bachelor of Science in Physics, Minor in Mathematics May 2021
SKILLS
Python | Data Science | Machine Learning | ETL | LaTeX | Git | Linux | SQL | PostgreSQL |
MongoDB | Pandas | NumPy | PyQt |

---

Answer this question based on the above context: what does Kyle Lare do

Response: content='Kyle Lare is a Computational Engineer who works at Railspire in Dallas, TX. He is responsible for developing software applications, analyzing system data, testing safety-critical locomotive systems, and collaborating with cross-functional teams. He has experience in Python, data science, machine learning, ETL, LaTeX, Git, Linux, SQL, PostgreSQL, MongoDB, Pandas, NumPy, and PyQt.' response_metadata={'token_usage': {'completion_tokens': 81, 'prompt_tokens': 557, 'total_tokens': 638}, 'model_name': 'gpt-3.5-turbo', 'system_fingerprint': 'fp_3bc1b5746c', 'finish_reason': 'stop', 'logprobs': None}
Sources: ['/home/kylelare/Documents/rag_data/ResumeSpring2024.pdf']

Amazing, but let's try a more advanced question. And this time I'll spare you and condense the output.

Answer this question based on the above context: who did Kyle Lare study under?

Response: content='Kyle Lare studied under Dr. Mini Das at the University of Houston.'

We've successfully met our goal and answered questions using RAG from a given PDF. But let's make some more improvements before we call this a day.

Some additional improvements
After playing around with some open source alternatives, I've switched the embedding function to HuggingFaceEmbeddings, as well as changing the model to a locally ran llama2-uncensored via ollama. I have some natural suspicions about Open AI's use of user data, and although I do think their model's are better, I'm fine getting slightly worse results at the cost of some battery life.
