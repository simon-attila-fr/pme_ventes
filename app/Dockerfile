FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 6789

# CMD ["python", "main.py"]
CMD [ "gradio", "main.py" ]