import gpt4docs.logger_config  # noqa: F401
from dotenv import load_dotenv
from gpt4docs import MainApplication

load_dotenv()


if __name__ == "__main__":
    args = MainApplication.parse_args()
    app = MainApplication(args)
    app()
