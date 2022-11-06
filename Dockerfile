# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./auth /code/auth

# # 
# COPY ./5ab9cc34711e.json /code/5ab9cc34711e.json

# # 
# COPY /.env /code/.env

# 
COPY ./main.py /code/main.py

# 
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD exec uvicorn main:app --host 0.0.0.0 --port 8080 --workers 2
