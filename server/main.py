"""FastAPI server for chord keyboard → text conversion."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from groq_client import convert_ipa
from semantic_client import expand_semantic

app = FastAPI(title="Chord Keyboard Engine")

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


class ExpandRequest(BaseModel):
    tokens: list[str]  # e.g. ["CREATE", "FUNCTION", "ASYNC"]


class ExpandResponse(BaseModel):
    text: str  # e.g. "Create an async function."


@app.post("/convert", response_model=ConvertResponse)
async def convert(req: ConvertRequest):
    """Convert raw IPA phoneme stream to formatted text."""
    text = convert_ipa(req.ipa, lang=req.lang)
    return ConvertResponse(text=text)


@app.post("/expand", response_model=ExpandResponse)
async def expand(req: ExpandRequest):
    """Expand semantic tokens to natural language."""
    text = expand_semantic(req.tokens)
    return ExpandResponse(text=text)


@app.get("/health")
async def health():
    return {"status": "ok"}
