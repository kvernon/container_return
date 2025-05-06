from data_layers.db_assets import DbAssets
from jojanga_queries.assets import Asset


class AssetsRepository:
    def __init__(self, query: DbAssets):
        self.query = query

    def get_asset_by_id(self, asset_id: str) -> Asset | None:
        try:
            asset = self.query.get_asset(asset_id)
            if asset is None:
                return None
            return asset
        except Exception:
            print("get_asset_by_id failed")
            return None
