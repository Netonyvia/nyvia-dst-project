from pathlib import Path


class DSTAssembler:
    """Assembles generated DST sections into one Markdown document."""

    def assemble(
        self,
        section_paths: list[Path],
        final_output_path: Path,
    ) -> Path:
        parts = [
            section_path.read_text(encoding="utf-8").strip()
            for section_path in section_paths
        ]

        final_output_path.parent.mkdir(parents=True, exist_ok=True)
        final_output_path.write_text(
            "\n\n---\n\n".join(parts),
            encoding="utf-8",
        )

        return final_output_path