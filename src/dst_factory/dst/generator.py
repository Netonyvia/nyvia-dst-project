from pathlib import Path

from dst_factory.dst.assembler import DSTAssembler
from dst_factory.dst.section import DSTSection
from dst_factory.dst.section_generator import DSTSectionGenerator
from dst_factory.sources.extractor import DriveSourceExtractor
from dst_factory.sources.models import SourceDocument


class DSTGenerator:
    """Orchestrates section-by-section DST generation."""

    DEFAULT_SECTION_PROMPTS = [
        "00_metadata_resumen.md",
        "01_explicito.md",
        "02_humano_politico.md",
        "03_metodologico.md",
        "04_estrategico.md",
        "05_metricas.md",
        "06_knowledge_transfer.md",
        "07_indexacion.md",
    ]

    def __init__(
        self,
        source_extractor: DriveSourceExtractor | None = None,
        section_generator: DSTSectionGenerator | None = None,
        assembler: DSTAssembler | None = None,
        prompts_dir: str = "prompts/sections",
        output_dir: str = "output",
    ) -> None:
        self.source_extractor = source_extractor or DriveSourceExtractor()
        self.section_generator = section_generator or DSTSectionGenerator()
        self.assembler = assembler or DSTAssembler()
        self.prompts_dir = Path(prompts_dir)
        self.output_dir = Path(output_dir)

    def generate_from_drive_folder(
        self,
        dst_id: str,
        folder_id: str,
    ) -> Path:
        documents = self.source_extractor.extract_folder_document(folder_id)
        source_context = self._build_source_context(documents)

        section_output_dir = self.output_dir / dst_id / "sections"
        section_output_dir.mkdir(parents=True, exist_ok=True)

        sections = self._build_sections(section_output_dir)

        generated_section_paths = []

        for section in sections:
            section_markdown = self.section_generator.generate_section(
                dst_id=dst_id,
                source_context=source_context,
                prompt_path=section.prompt_path,
            )

            section.output_path.write_text(section_markdown, encoding="utf-8")
            generated_section_paths.append(section.output_path)

        final_output_path = self.output_dir / dst_id / f"{dst_id}.md"

        return self.assembler.assemble(
            section_paths=generated_section_paths,
            final_output_path=final_output_path,
        )

    def _build_sections(self, section_output_dir: Path) -> list[DSTSection]:
        sections = []

        for prompt_filename in self.DEFAULT_SECTION_PROMPTS:
            prompt_path = self.prompts_dir / prompt_filename

            if not prompt_path.exists():
                raise FileNotFoundError(f"Missing section prompt: {prompt_path}")

            output_path = section_output_dir / prompt_filename

            sections.append(
                DSTSection(
                    name=prompt_filename,
                    prompt_path=prompt_path,
                    output_path=output_path,
                )
            )

        return sections

    def _build_source_context(self, documents: list[SourceDocument]) -> str:
        sections = []

        for document in documents:
            sections.append(
                "\n".join(
                    [
                        f"# SOURCE: {document.source_file.name}",
                        f"FILE_ID: {document.source_file.id}",
                        f"MIME_TYPE: {document.source_file.mime_type}",
                        "",
                        document.text,
                    ]
                )
            )

        return "\n\n---\n\n".join(sections)