import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ml_service:ml_pass@postgres:5432/ml_service_db"

# db = SQLAlchemy(app)
engine = create_engine('postgresql://ml_service:ml_pass@postgres:5432/ml_service_db', echo=True)
migrate = Migrate(app, engine)

fields = "description"


def drop_table(table_name):
   base = declarative_base()
   metadata = MetaData(engine, reflect=True)
   table = metadata.tables.get(table_name)
   if table is not None:
       base.metadata.drop_all(engine, [table], checkfirst=True)


def load_catalogue():
    catalogue = create_engine("postgresql://catalog_service_reader:readonly@77.234.215.138:18095/catalog_service_db")
    df = pd.read_sql(f"select id, {fields} from wine_position", catalogue)
    print(f'Loaded {df.shape[0]} records from catalogue')
    df.to_sql("wines", engine)


def load_all():
    df = pd.read_sql(f'SELECT * FROM wines', engine)
    df['description'] = ' '.join([df[field] for field in fields.split(', ')])
    return df


def load_by_ids(ids):
    indices = tuple(ids)
    alcohol = pd.read_sql(f'SELECT id, name, type, crop_year, manufacturer, brand, volume, country, region, color, grape, sugar FROM wines WHERE id IN {indices}', engine)
    return alcohol
