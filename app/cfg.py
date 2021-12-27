from decouple import AutoConfig
from app.constants import SRC_ROOT


config = AutoConfig(search_path=SRC_ROOT)

DB_CONNSTR = config("DB_CONNSTR", None)