from sqlalchemy import Table, Column, Integer, ForeignKey

from ..db.db_sqlalchemy import BaseModel

# relationship many to many
orders_tables = Table(
    'orders_tables',
    BaseModel.metadata,
    Column('order_id', Integer, ForeignKey('orders.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('table_id', Integer, ForeignKey('tables.id', onupdate='CASCADE', ondelete='CASCADE'))
)
