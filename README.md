# The-boy-who-lived
Welcome to the Harry Potter Chatbot repository! This project features an interactive chatbot designed to bring the iconic character Harry Potter to life. Through advanced natural language processing techniques, this chatbot emulates the personality, knowledge, and charm of Harry Potter himself.

This repository includes the API and backend logic for the chatbot, along with the language model integration. The frontend for this project will be hosted in a separate repository to maintain a clear separation of concerns.
<br><br>
![A pic for harry potter](images/harry.jpg)


## Requirements

#### Install Python using MiniConda

1) Download and install MiniConda from [Here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n harry python=3.10
```
3) Activate the environment:
```bash
$ conda activate harry
```

## Installation

### Install the required packages

```bash
$ cd src
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cd src
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
$ cd src
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Demo 🎥

Watch a video demonstration of the app in action:

[Watch the Demo Video](https://drive.google.com/file/d/16FPqJ4xmzbkRiD4cdAYRgy1qhZmWw8dZ/view)

## 📘 Resources:
- mini-rag-app playlist by Eng/Abu Bakr Soliman. [Here](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj)
- langgraph documentation. [Here](https://langchain-ai.github.io/langgraph/tutorials/introduction/)

