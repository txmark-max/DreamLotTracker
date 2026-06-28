from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from dreamlottracker.services.property_service import PropertyService


class ExportService:
    def __init__(self):
        self.property_service = PropertyService()

    def export_properties_to_excel(self, output_path: Path) -> Path:
        properties = self.property_service.get_all_properties()

        output_path.parent.mkdir(parents=True, exist_ok=True)

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Properties"

        headers = [
            "Address",
            "City",
            "County",
            "State",
            "Price",
            "Acres",
            "Price Per Acre",
            "Status",
            "Dream Score",
            "Recommendation",
        ]

        header_fill = PatternFill("solid", fgColor="D9EAF7")

        for column, header in enumerate(headers, start=1):
            cell = sheet.cell(row=1, column=column, value=header)
            cell.font = Font(bold=True)
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")

        for row_number, property_ in enumerate(properties, start=2):
            listing = property_.listings[0] if property_.listings else None
            scores = property_.scores

            price = float(listing.asking_price) if listing else 0.0
            status = listing.status if listing else "Unknown"
            dream_score = (
                float(scores.dream_score)
                if scores and scores.dream_score is not None
                else 0.0
            )
            recommendation = (
                scores.recommendation
                if scores and scores.recommendation
                else ""
            )

            sheet.cell(row=row_number, column=1, value=property_.address)
            sheet.cell(row=row_number, column=2, value=property_.city)
            sheet.cell(row=row_number, column=3, value=property_.county)
            sheet.cell(row=row_number, column=4, value=property_.state)
            sheet.cell(row=row_number, column=5, value=price)
            sheet.cell(row=row_number, column=6, value=float(property_.acres or 0))
            sheet.cell(row=row_number, column=7, value=f"=IF(F{row_number}>0,E{row_number}/F{row_number},0)")
            sheet.cell(row=row_number, column=8, value=status)
            sheet.cell(row=row_number, column=9, value=dream_score)
            sheet.cell(row=row_number, column=10, value=recommendation)

        last_row = max(len(properties) + 1, 2)

        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = f"A1:J{last_row}"

        for row in range(2, last_row + 1):
            sheet.cell(row=row, column=5).number_format = "$#,##0"
            sheet.cell(row=row, column=6).number_format = "0.00"
            sheet.cell(row=row, column=7).number_format = "$#,##0"
            sheet.cell(row=row, column=9).number_format = "0.0"

        # Add a simple summary sheet instead of a formal Excel table object.
        summary = workbook.create_sheet("Summary")
        summary["A1"] = "Dream Lot Tracker Export"
        summary["A1"].font = Font(bold=True, size=16)

        summary["A3"] = "Total Properties"
        summary["B3"] = len(properties)

        summary["A4"] = "Average Dream Score"
        summary["B4"] = '=IFERROR(AVERAGE(Properties!I2:I1000),0)'
        summary["B4"].number_format = "0.0"

        summary["A5"] = "Average Price"
        summary["B5"] = '=IFERROR(AVERAGE(Properties!E2:E1000),0)'
        summary["B5"].number_format = "$#,##0"

        summary["A6"] = "Average Acres"
        summary["B6"] = '=IFERROR(AVERAGE(Properties!F2:F1000),0)'
        summary["B6"].number_format = "0.00"

        for column in range(1, len(headers) + 1):
            letter = get_column_letter(column)
            max_length = len(str(sheet.cell(row=1, column=column).value))

            for row in range(2, last_row + 1):
                value = sheet.cell(row=row, column=column).value
                if value is not None:
                    max_length = max(max_length, len(str(value)))

            sheet.column_dimensions[letter].width = min(max_length + 2, 45)

        summary.column_dimensions["A"].width = 24
        summary.column_dimensions["B"].width = 18

        workbook.save(output_path)
        return output_path
