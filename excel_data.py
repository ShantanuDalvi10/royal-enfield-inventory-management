from openpyxl import load_workbook
from main import create_app
from models import db,Parts

app = create_app()

excel_file_path = "royal_enfield_spare_parts_20.xlsx"

with app.app_context():
    workbook = load_workbook(excel_file_path,data_only=True)
    sheet = workbook["20 Spare Parts"]

    existing_part = set(
        db.session.execute(
            db.select(Parts.part_id)
        ).scalars().all()
    )
    seen_parts = set()

    try:
        for part_id,part_name,price in sheet.iter_rows(
            min_row=2,
            max_col=3,
            values_only=True,
        ):
            if not part_id or not part_name or price is None:
                continue
            else:
                part_id = str(part_id).strip()
                part_name = str(part_name).strip()

            if part_id in seen_parts:
                continue
            else:
                seen_parts.add(part_id)

            if part_id in existing_part:
                continue

            else:
                new_part = Parts(
                    part_id=part_id,
                    part_name=part_name,
                    price = price,
                    stock=0
                )
                db.session.add(new_part)

                existing_part.add(part_id)

        db.session.commit()

    except Exception as Error:
        db.session.rollback()

    finally:
        workbook.close()

