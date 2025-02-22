from fastapi import FastAPI, File, UploadFile, HTTPException
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)

app = FastAPI()

