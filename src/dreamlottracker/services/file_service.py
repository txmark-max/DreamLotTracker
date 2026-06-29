import shutil
import subprocess
from pathlib import Path

from dreamlottracker.database.models import Document, Photo
from dreamlottracker.database.session import SessionLocal


PROJECT_ROOT = Path(__file__).resolve().parents[3]
FILES_ROOT = PROJECT_ROOT / "data" / "files"


class FileService:
    def add_photo(self, property_id: int, source_path: Path, caption: str = "", photo_type: str = "General") -> None:
        destination = self._copy_file(property_id, source_path, "photos")
        with SessionLocal() as session:
            session.add(Photo(property_id=property_id, file_path=str(destination), caption=caption, photo_type=photo_type))
            session.commit()

    def add_document(self, property_id: int, source_path: Path, document_type: str = "General", notes: str = "") -> None:
        destination = self._copy_file(property_id, source_path, "documents")
        with SessionLocal() as session:
            session.add(Document(property_id=property_id, file_path=str(destination), document_type=document_type, notes=notes))
            session.commit()

    def delete_photo(self, photo_id: int) -> None:
        with SessionLocal() as session:
            photo = session.query(Photo).get(photo_id)
            if photo:
                session.delete(photo)
                session.commit()

    def delete_document(self, document_id: int) -> None:
        with SessionLocal() as session:
            document = session.query(Document).get(document_id)
            if document:
                session.delete(document)
                session.commit()

    def open_file(self, file_path: str) -> None:
        path = Path(file_path)
        if path.exists():
            subprocess.run(["open", str(path)], check=False)

    def _copy_file(self, property_id: int, source_path: Path, category: str) -> Path:
        source_path = Path(source_path)
        destination_dir = FILES_ROOT / f"property_{property_id}" / category
        destination_dir.mkdir(parents=True, exist_ok=True)

        destination = destination_dir / source_path.name

        counter = 1
        while destination.exists():
            destination = destination_dir / f"{source_path.stem}_{counter}{source_path.suffix}"
            counter += 1

        shutil.copy2(source_path, destination)
        return destination
