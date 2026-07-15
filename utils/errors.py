class AtlasTraderError(Exception):
    """Base AtlasTrader exception."""
    pass


class DataFeedError(AtlasTraderError):
    """Raised when market data cannot be downloaded."""
    pass


class InvalidSymbolError(AtlasTraderError):
    """Raised when an invalid symbol is requested."""
    pass


class MarketAnalysisError(AtlasTraderError):
    """Raised when market analysis fails."""
    pass