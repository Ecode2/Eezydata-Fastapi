"""Base settings class contains only important fields."""
# mypy: ignore-errors
import ast, os, secrets
from typing import Annotated, List, Union, Dict, Optional, Any
from pydantic import BaseModel, AnyHttpUrl, validator, PostgresDsn, MongoDsn, field_validator
from pydantic_settings import BaseSettings
from ..utils.logging import StandardFormatter, ColorFormatter
from dotenv import load_dotenv

load_dotenv()

class LoggingConfig(BaseModel):
    version: int
    disable_existing_loggers: bool = False
    formatters: Dict
    handlers: Dict
    loggers: Dict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'EezyDataApi'
    PROJECT_SLUG: str = 'eezydataapi'

    DEBUG: Annotated[bool, True] = True
    API_STR: str = "/api/v1"

    # ##################### Access Token Configuration #########################
    # TODO: Please note that, the secret key will be different for each running
    # instance or each time restart the service, if you prefer a stable one,
    # please use an environment variable.
    SECRET_KEY: str = os.getenv("SECRET_KEY") #secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7
    # 60 minutes * 24 hours * 30 * 6  months = 6 months
    ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN: int = 30
    JWT_ENCODE_ALGORITHM: str = "HS256"

    # ########################### CORS Configuration ###########################
    """CORS_ORIGINS is a JSON-formatted list of origins
    e.g: ["http://localhost", "http://localhost:4200", "http://localhost:3000",
    "http://localhost:8080"]"""
    CORS_ORIGINS: Union[List[AnyHttpUrl], str] = []
    """A regex string to match against origins that should be permitted to make
    cross-origin requests.
    For example, your domain is example, then the regex should be something like
        ```r"https:\/\/.*\.example\.?"```
    """
    CORS_ORIGIN_REGEX: str | None = None
    """A list of HTTP methods that should be allowed for cross-origin requests.
    Defaults to ['*']. You can use ['GET'] to allow standard GET method."""
    CORS_METHODS: List[str] = ['GET', "POST", "PUT", "DELETE"]
    """A list of HTTP request headers that should be supported for cross-origin
    requests. Defaults to ['*'] to allow all headers. """
    CORS_HEADERS: List[str] = []
    """ Indicate that cookies should be supported for cross-origin requests.
    Defaults to True."""
    CORS_CREDENTIALS: bool = True

    # noinspection PyMethodParameters
    @field_validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Validate the value of BACKEND_CORS_ORIGINS.

        Args:
            v (Union[str, List[str]): the value of BACKEND_CORS_ORIGINS.

        Returns:
            A list of urls, if v is a list of str in string format.
            The given value v, if v is a list or string.

        Raises
            ValueError, if v is in other format.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("[") and v.endswith("]"):
            return ast.literal_eval(v)
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # ########################### DB Configuration #############################
    POSTGRES_SERVER: Optional[str | None] = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: Optional[str | None] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str | None] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: Optional[str | None]= os.getenv("POSTGRES_DB")
    # set the default value to None, such that the assemble_db_connection can
    # build the URI for us and do checks.
    SQLALCHEMY_DATABASE_URI: Optional[str | None] = None  #Optional[PostgresDsn] = None

    # noinspection PyMethodParameters
    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Assemble the postgres DB URI with the provided POSTGRES_SERVER,
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB.

        Args:
            v (Optional[str]): the value of defined SQLALCHEMY_DATABASE_URI.
            values (Dict[str, Any]): a dictionary contains the requisite values.

        Returns:
            str: the postgres DB URI.
        """
        
        if isinstance(v, str):
            return v
        
        """ return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        ) """
        """ return "mysql+pymysql://{}:{}@{}/{}".format(values.get("POSTGRES_USER"), values.get("POSTGRES_PASSWORD"), values.get("POSTGRES_SERVER"), values.get('POSTGRES_DB')) """
        return "sqlite:///billsql.db"

    # ######################## Logging Configuration ###########################
    # logging configuration for the project logger, uvicorn loggers
    LOGGING_CONFIG: LoggingConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            'colorFormatter': {'()': ColorFormatter},
            'standardFormatter': {'()': StandardFormatter},
        },
        "handlers": {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': "DEBUG",
                'formatter': 'standardFormatter',
                'stream': 'ext://sys.stdout',
            },
        },
        "loggers": {
            "eezydataapi": {
                'handlers': ['consoleHandler'],
                'level': "DEBUG",
            },
            "uvicorn": {
                'handlers': ['consoleHandler']
            },
            "uvicorn.access": {
                # Use the project logger to replace uvicorn.access logger
                'handlers': []
            }
        }
    }

    class Config:
        case_sensitive = True
