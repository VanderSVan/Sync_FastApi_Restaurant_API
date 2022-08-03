# !!! Inserting data into an empty database only !!!

from src.db.db_sqlalchemy import SessionLocal
from src.models.user import UserModel
from src.models.table import TableModel
from src.models.schedule import ScheduleModel
from src.models.order import OrderModel
from src.utils.populating_db.data_preparation import prepare_data_for_insertion
from src.utils.logger.main import logger


def insert_data_to_db(users_json: list,
                      tables_json: list,
                      schedules_json: list,
                      orders_json: list) -> None:
    """Inserts prepared data into an empty database only!"""
    db = SessionLocal()
    try:
        if (
                db.query(UserModel).count() == 0
                and
                db.query(TableModel).count() == 0
                and
                db.query(ScheduleModel).count() == 0
                and
                db.query(OrderModel).count() == 0
        ):
            prepared_data: dict = prepare_data_for_insertion(users_json,
                                                             tables_json,
                                                             schedules_json,
                                                             orders_json)

            db.add_all(prepared_data['users'])
            db.add_all(prepared_data['tables'])
            db.add_all(prepared_data['schedules'])
            db.add_all(prepared_data['orders'])

            db.commit()
            logger.success("Data has been added to db")

        else:
            logger.info("Data cannot be inserted into the database because the database is not empty")
    finally:
        db.close()
