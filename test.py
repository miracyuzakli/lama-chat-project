from lama_model.query_handler import qa_chain


query1 = "حد اقل واریز حساب ها چقدر است ؟"
result = qa_chain.invoke({"query": query1})
print(result)