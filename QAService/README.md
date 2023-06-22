# Ewwww, thats disgusting!

**[Customer]**  It is, isn't it. Imagine, a professional software company actually wrote that! 
And, they charged us money for it. If I had been here during at the time when this was
written, I would have canceled the contract on the spot!

**[You]** It never ceases to amaze me, the number of coders out there that don't care about neither
quality nor the aesthetics of their code. But don't worry, we gotcha back! We will have
this refactored in no time!

**[Customer]** Alright. Let me know when you're done!

Good thing **"we"** didn't write that code in the first place, or we would have been in trouble! <br>
Now, let's clean up this mess! <br><br>

**[Step 1]**
Do a code analysis and document your findings.<br>
The first step in a refactoring job is to get a high-level overview of what the code is doing, and<br>
how it's doing it.<br>
<br>
What type of objects are present?<br>
Which layering strategy has been chosen if any?<br>
How well is the code separated?<br>
Does the code follow the principals of SOLID?<br><br>
Make a list of at least 5 shortcomings<br>
Make a note on how you would go about fixing the issue<br><br> 

**[Issues]**
1) Everything in one file<br>
2) Unnecessary documentation<br>
3) Poor naming of constants<br>
4) Try-catch outside the program scope?<br>
5) Poorly named functions<br>
6) What the function does, do not correspond with the name<br>
7) Code repetition, if-else<br>
8) Throwing HTTPException from within business logic<br>
9) Missing documentation on the API<br>
10) Does not follow any best practices whatsoever!<br><br>


**[Step 2]**
I have started by creating some project structure in the **src** directory. I have also created a few <br> 
sceleton classes for you to finish. To save some time I took it upon myself to write the **FAISS index** stuff. <br>
You can treat the **SearchIndexLocator** as a dict to lookup the right search index for a given partition like so: <br>

```python
locator = SearchIndexLocator(
            index_loader=self._load_index,
            embedding_column="answer_embedding",
            partition=["partition_id"],
            labels_columns=["partition_id", "row_id"]
        )

partition_key = .....
search_index = locator[partition_key]

matches = search_index.find_closest(embedding_vector, k=result_count)
```
<br>

To test the code, start the server by running **skillup_app.py**. Make sure to start it from the **src** directory.<br>
Then run the **test_app.py**. Make sure to start it from the **test** directory<br><br>

**[Step 2]**<br>
**Global Variables**<br>
Refactor the code and implement Design Patterns where i makes sense.<br>
Start with getting rid of the global variables<br><br>

**Factories**<br>
The embedding services now exist as both a local version for development, and a remote version for prod.<br>
Does the Factory Design Pattern fit anywhere?<br><br>

### See you in 20 min. Good Luck!






