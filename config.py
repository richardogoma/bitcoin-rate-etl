"""ETL Pipeline configurations."""


class Config:
    """
    Configuration class for the program.
    """

    DATABASE_URI = "./data/processed/bitcoin_rate_tracker.db"
    API_URI = "https://api.coindesk.com/v1/bpi/currentprice.json"

    def get_config_value(self, key):
        """
        Get the value of a configuration option.

        Args:
            key (str): The configuration option key.

        Returns:
            Any: The value of the configuration option.
        """
        return getattr(self, key)

    def set_config_value(self, key, value):
        """
        Set the value of a configuration option.

        Args:
            key (str): The configuration option key.
            value (Any): The value to be set for the configuration option.
        """
        setattr(self, key, value)
