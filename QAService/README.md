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
Then run the **test_app.py**. Make sure to start it from the **test** directory

### See you in 30 min. Good Luck!






