> navegar hasta la carpta aa_lambda/python/
> python3 -m venv venv
> venv\Scripts\activate
> echo %VIRTUAL_ENV%
> (venv) pip install spacy
> (venv) pip install spacy es_dep_news_trf
python -m spacy download es_dep_news_trf
python -m spacy download es_core_news_lg
python -m spacy download es_core_news_md
python -m spacy download es_core_news_sm

pip install spacy es_dep_news_trf; pip install spacy es_core_news_lg; pip install spacy es_core_news_md; pip install spacy es_core_news_sm

pip install flask; pip install flask_cors; pip install flask_socketio; pip install spacy; pip install unidecode; pip install matplotlib; pip install networkx

--------------------------------------------
PowerShell> cd aa_lambda\python
PowerShell> Compress-Archive -Force -Path  .\* -DestinationPath lambda_function.zip
