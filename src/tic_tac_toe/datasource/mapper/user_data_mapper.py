from tic_tac_toe.domain.model.user import User as DomainUser
from tic_tac_toe.infrastructure.persistence.model.user_model import UserModel


def to_data(domain: DomainUser) -> UserModel:
    return UserModel(
        id=domain.id, 
        login=domain.login, 
        password_hash=domain.passwd_hash
    )


def to_domain(data: UserModel) -> DomainUser:
    return DomainUser(
        id=data.id,
        login=data.login,
        passwd_hash=data.password_hash
    )
