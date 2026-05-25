from pathlib import Path

from dst_factory.llm.client_factory import TextGenerationClient, build_llm_client


class DSTSectionGenerator:
    """Generates one DST section using the configured LLM provider."""

    def __init__(self, llm_client: TextGenerationClient | None = None) -> None:
        self.llm_client = llm_client or build_llm_client()

    def generate_section(
        self,
        dst_id: str,
        source_context: str,
        prompt_path: Path,
    ) -> str:
        template = prompt_path.read_text(encoding="utf-8")

        prompt = (
            template.replace("{{DST_ID}}", dst_id)
            .replace("{{SOURCE_CONTEXT}}", source_context)
        )

        return self.llm_client.generate_text(prompt)
    

