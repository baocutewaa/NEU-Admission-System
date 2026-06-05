import os
import urllib
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "NEU Admission System"
    API_V1_STR: str = "/api/v1"
    
    # Database Settings
    DB_SERVER: str = os.getenv("DB_SERVER", r"(localdb)\MSSQLLocalDB")
    DB_NAME: str = os.getenv("DB_NAME", "neu_tuyensinh")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Construct the connection string using pyodbc
        if self.DB_USER and self.DB_PASSWORD:
            conn_str = (
                f"DRIVER={{{self.DB_DRIVER}}};"
                f"SERVER={self.DB_SERVER};"
                f"DATABASE={self.DB_NAME};"
                f"UID={self.DB_USER};PWD={self.DB_PASSWORD};"
                "TrustServerCertificate=yes;"
            )
        else:
            conn_str = (
                f"DRIVER={{{self.DB_DRIVER}}};"
                f"SERVER={self.DB_SERVER};"
                f"DATABASE={self.DB_NAME};"
                "Trusted_Connection=yes;"
                "TrustServerCertificate=yes;"
            )
        quoted_conn_str = urllib.parse.quote_plus(conn_str)
        return f"mssql+pyodbc:///?odbc_connect={quoted_conn_str}"

settings = Settings()
