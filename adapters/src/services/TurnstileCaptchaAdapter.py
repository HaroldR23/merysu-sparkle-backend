import httpx

from domain.src.ports.CaptchaService import CaptchaService
from settings.env_variables import TURNSTILE_SECRET_KEY


class TurnstileCaptchaAdapter(CaptchaService):
    async def verify(self, token: str) -> dict:

        payload = {
            "secret": TURNSTILE_SECRET_KEY,
            "response": token
        }

        client = httpx.AsyncClient(timeout=5)
        r = await client.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data=payload
        )
        await client.aclose()

        data = r.json()

        return data
