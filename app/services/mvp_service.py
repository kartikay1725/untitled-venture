import asyncio
from typing import List

class MVPService:
    async def generate_code(self, features: List[str]) -> str:
        await asyncio.sleep(0.2)
        code_lines = [
            "import streamlit as st",
            "",
            "def main():",
            "    st.title('Generated MVP')",
            ""
        ]
        for f in features:
            code_lines.append(f"    st.header('{f}')")
            code_lines.append(f"    st.write('Placeholder for {f}')")
        code_lines.append("")
        code_lines.append("if __name__ == '__main__':")
        code_lines.append("    main()")
        return "\n".join(code_lines)
