from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
TEST_DIR = ROOT_DIR / "tests"

SUPPORTED_FORMATS = (".txt", ".csv", ".tab", ".dat", ".json", ".arff", ".xml", ".xlsx")
PLAIN_FORMATS = (".txt", ".csv", ".tab", ".dat")
SIZE_UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB"]
SEPARATORS = ["\t", " ", ",", ";", "|"]
SEPARATOR_NAMES = ["tab", "space", "comma", "semi_colon", "pipe"]
BIG_FILE = 104_857_600  # 100MB

DATA_TYPE_CONVERSION = {
    "postgres": {
        # "int64": "INTEGER",
        "int64": "BIGINT",
        "float64": "DOUBLE PRECISION",
        "object": "VARCHAR({})",
        "bool": "BOOLEAN",
        "datetime64[ns]": "TIMESTAMP",
        "datetime64[ns, UTC]": "TIMESTAMP",
        "datetime64[ns, CET]": "TIMESTAMP",
        "datetime64[ns, CEST]": "TIMESTAMP",
    },
    "sqlite": {
        "int64": "INTEGER",
        "float64": "REAL",
        "object": "TEXT",
        "bool": "BOOLEAN",
        "datetime64[ns]": "TIMESTAMP",
        "datetime64[ns, UTC]": "TIMESTAMP",
        "datetime64[ns, CET]": "TIMESTAMP",
        "datetime64[ns, CEST]": "TIMESTAMP",
    },
}
