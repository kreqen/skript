from dataclasses import dataclass, field


@dataclass(slots=True)
class DocumentContent:
    file_path: str
    file_name: str
    file_type: str
    extracted_text: str
    page_count: int | None = None
    sheet_names: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)