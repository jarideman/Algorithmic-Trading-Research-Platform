from connection.mt5_connection import init_mt5, deinit_mt5
from pipeline.market_data_pipeline import run_market_data_pipeline

def main():
    if not init_mt5():
        return

    try:
        run_market_data_pipeline()

    finally:
        deinit_mt5()


if __name__ == "__main__":
    main()