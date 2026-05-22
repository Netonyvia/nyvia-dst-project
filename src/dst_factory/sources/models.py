from dataclasses import dataclass

@dataclass(frozen=True)
class SourceFile:
    id: str
    name: str
    mime_type: str


@dataclass(frozen=True)
class SourceDocument:
    source_file: SourceFile
    text: str

