"""Run this script to launch the pipeline"""

from etl.master import run_etl

if __name__ == "__main__":
    run_etl("cake_data.csv")