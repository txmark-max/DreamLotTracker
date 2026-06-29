from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from dreamlottracker.services.property_service import PropertyService


class PDFReportService:
    def __init__(self):
        self.property_service = PropertyService()

    def export_property_report(self, property_id: int, output_path: Path) -> Path:
        property_ = self.property_service.get_property(property_id)

        if not property_:
            raise ValueError("Property not found")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        listing = property_.listings[0] if property_.listings else None
        scores = property_.scores
        note = property_.notes[0] if property_.notes else None

        price = listing.asking_price if listing else 0
        status = listing.status if listing else "Unknown"
        score = scores.dream_score if scores and scores.dream_score is not None else 0
        recommendation = scores.recommendation if scores and scores.recommendation else ""

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Dream Lot Tracker Property Report", styles["Title"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(property_.address, styles["Heading1"]))
        story.append(Paragraph(f"{property_.city}, {property_.state}", styles["Normal"]))
        story.append(Spacer(1, 12))

        overview_data = [
            ["Metric", "Value"],
            ["Price", f"${price:,.0f}"],
            ["Acres", f"{property_.acres:.2f}"],
            ["Price / Acre", f"${price / property_.acres:,.0f}" if property_.acres else ""],
            ["Status", status],
            ["Dream Score", f"{score:.1f}"],
            ["Recommendation", recommendation],
            ["County", property_.county or ""],
            ["Parcel", property_.parcel_number or ""],
            ["GPS", self._gps_text(property_)],
        ]

        story.append(self._table(overview_data))
        story.append(Spacer(1, 16))

        story.append(Paragraph("Notes", styles["Heading2"]))
        notes_data = [
            ["Pros", note.pros if note and note.pros else ""],
            ["Cons", note.cons if note and note.cons else ""],
            ["Questions", note.questions if note and note.questions else ""],
            ["Builder Notes", note.builder_notes if note and note.builder_notes else ""],
            ["Final Recommendation", note.final_recommendation if note and note.final_recommendation else ""],
        ]

        story.append(self._table(notes_data, col_widths=[130, 360]))

        doc.build(story)
        return output_path

    def _gps_text(self, property_) -> str:
        if property_.latitude is None or property_.longitude is None:
            return ""
        return f"{property_.latitude:.6f}, {property_.longitude:.6f}"

    def _table(self, data, col_widths=None):
        table = Table(data, colWidths=col_widths)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return table
