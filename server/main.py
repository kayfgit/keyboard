"""FastAPI server for IPA chord keyboard → text conversion."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from groq_client import convert_ipa

app = FastAPI(title="IPA Chord Keyboard Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConvertRequest(BaseModel):
    ipa: str   # e.g. "ðəkætsætɒnðəmæt"
    lang: str = "en"  # "en" or "pt"


class ConvertResponse(BaseModel):
    text: str  # e.g. "The cat sat on the mat."


@app.post("/convert", response_model=ConvertResponse)
async def convert(req: ConvertRequest):
    """Convert raw IPA phoneme stream to formatted text."""
    text = convert_ipa(req.ipa, lang=req.lang)
    return ConvertResponse(text=text)


@app.get("/health")
async def health():
    return {"status": "ok"}
