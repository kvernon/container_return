from dependency_injector import containers, providers

from data_layers.db_assets import DbAssets
from data_layers.db_rentals import DbRental
from data_layers.db_users import DbUsers
from repositories.assets_repository import AssetsRepository
from repositories.rentals_repository import RentalsRepository
from repositories.users_repository import UsersRepository
from src.services.return_service import ReturnService


class Injector(containers.DeclarativeContainer):
    db_rentals = providers.Singleton(DbRental)
    db_users = providers.Singleton(DbUsers)
    db_assets = providers.Singleton(DbAssets)
    rental_repository = providers.Factory(RentalsRepository, rentals_query=db_rentals)
    users_repository = providers.Factory(UsersRepository, users_query=db_users)
    assets_repository = providers.Factory(AssetsRepository, query=db_assets)
    return_service = providers.Factory(ReturnService,
                                       user_repo=users_repository,
                                       assets_repo=assets_repository,
                                       rental_repo=rental_repository
                                       )
