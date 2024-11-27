# The-boy-who-lived
Welcome to the Harry Potter Chatbot repository! This project features an interactive chatbot designed to bring the iconic character Harry Potter to life. Through advanced natural language processing techniques, this chatbot emulates the personality, knowledge, and charm of Harry Potter himself.

This repository includes the API and backend logic for the chatbot, along with the language model integration. The frontend for this project will be hosted in a separate repository to maintain a clear separation of concerns.
<br><br>
![A pic for harry potter](images/harry.jpg)


## Requirements

- Python 3.8 or later

#### Install Python using MiniConda

1) Download and install MiniConda from [Here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
3) Activate the environment:
```bash
$ conda activate mini-rag
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

- update `.env` with your credentials.

## Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```

- update `.env` with your credentials.



```bash
$ cd docker
$ sudo docker compose up -d
```

## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## 📘 Resources:
- mini-rag-app playlist by Eng/Abu Bakr Soliman. [Here](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj)

