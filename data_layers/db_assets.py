from jojanga_queries import assets


class DbAssets:
    def __init__(self):
        pass

    def get_asset(self, asset_id: str) -> assets.Asset:
        return assets.get_asset(asset_id)
