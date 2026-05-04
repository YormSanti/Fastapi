from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"
    USER = "user"


VIEW_ALL_ORDERS_ROLES = (UserRole.ADMIN, UserRole.MANAGER)
CREATE_ORDER_ROLES = (UserRole.ADMIN, UserRole.MANAGER, UserRole.STAFF, UserRole.USER)
UPDATE_ORDER_ROLES = (UserRole.ADMIN, UserRole.MANAGER, UserRole.STAFF)
DELETE_ORDER_ROLES = (UserRole.ADMIN,)
MANAGE_USERS_ROLES = (UserRole.ADMIN,)
ASSIGN_ROLES = (UserRole.ADMIN,)
CHANGE_ANY_PASSWORD_ROLES = (UserRole.ADMIN,)
CHANGE_OWN_PASSWORD_ROLES = (UserRole.ADMIN, UserRole.MANAGER, UserRole.STAFF, UserRole.USER)
VIEW_REPORTS_ROLES = (UserRole.ADMIN, UserRole.MANAGER)
