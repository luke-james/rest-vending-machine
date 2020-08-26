FROM python:3

WORKDIR /docs

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["make html"]

CMD ["sphinx-autobuild", "--host", "0.0.0.0", "--port", "1000", ".", "./_build/html"]
