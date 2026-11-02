from openpyxl import load_workbook
from main import create_app
from models import db,Parts
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_excel_data():

    app = create_app()

    excel_file_path = "data/royal_enfield_spare_parts_20.xlsx"

    with app.app_context():
        workbook = load_workbook(excel_file_path,data_only=True)

        try:
            sheet = workbook["20 Spare Parts"]

            existing_part = set(
                db.session.execute(
                    db.select(Parts.part_id)
                ).scalars().all()
            )
            seen_parts = set()


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
            logger.info("Excel import completed successfully.")

        except Exception as Error:
            db.session.rollback()
            logger.info("Error occurring during importing parts from Excel")
            raise

        finally:
            workbook.close()

if __name__ == "__main__":
    import_excel_data()