import asyncio
from typing import Optional

class DeploymentService:
    async def deploy(self, target: str, code: str) -> Optional[str]:
        await asyncio.sleep(0.3)
        return f"https://{target}.example.com/mvp"
