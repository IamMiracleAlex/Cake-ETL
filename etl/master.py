from .extractor import Extractor
from .loader import Loader
from .transformer import Transformer
from .reports import Report


def run_etl(input_file: str):
    """
    Runs whole ETL pipeline

    Args:
        input_file: path to the source file
    """
    extractor = Extractor(input_file)
    transformer = Transformer(extractor.extract_data())
    loader = Loader(transformer.transform_data())

    loader.load_data()

    # create reports
    report = Report()
    report.create_report()
