from typing import Any, Optional

ActionCodeSettings: Any
CertificateFetchError: Any
Client: Any
ConfigurationNotFoundError: Any
DELETE_ATTRIBUTE: Any
DeleteUsersResult: Any
EmailAlreadyExistsError: Any
ErrorInfo: Any
ExpiredIdTokenError: Any
ExpiredSessionCookieError: Any
ExportedUserRecord: Any
GetUsersResult: Any
ImportUserRecord: Any
InsufficientPermissionError: Any
InvalidDynamicLinkDomainError: Any
InvalidIdTokenError: Any
InvalidSessionCookieError: Any
ListProviderConfigsPage: Any
ListUsersPage: Any
OIDCProviderConfig: Any
PhoneNumberAlreadyExistsError: Any
ProviderConfig: Any
RevokedIdTokenError: Any
RevokedSessionCookieError: Any
SAMLProviderConfig: Any
TokenSignError: Any
UidAlreadyExistsError: Any
UnexpectedResponseError: Any
UserImportHash: Any
UserImportResult: Any
UserInfo: Any
UserMetadata: Any
UserNotFoundError: Any
UserProvider: Any
UserRecord: Any
UserIdentifier: Any
UidIdentifier: Any
EmailIdentifier: Any
PhoneIdentifier: Any
ProviderIdentifier: Any

def create_custom_token(uid: Any, developer_claims: Optional[Any] = ..., app: Optional[Any] = ...): ...
def verify_id_token(id_token: Any, app: Optional[Any] = ..., check_revoked: bool = ...): ...
def create_session_cookie(id_token: Any, expires_in: Any, app: Optional[Any] = ...): ...
def verify_session_cookie(session_cookie: Any, check_revoked: bool = ..., app: Optional[Any] = ...): ...
def revoke_refresh_tokens(uid: Any, app: Optional[Any] = ...) -> None: ...
def get_user(uid: Any, app: Optional[Any] = ...): ...
def get_user_by_email(email: Any, app: Optional[Any] = ...): ...
def get_user_by_phone_number(phone_number: Any, app: Optional[Any] = ...): ...
def get_users(identifiers: Any, app: Optional[Any] = ...): ...
def list_users(page_token: Optional[Any] = ..., max_results: Any = ..., app: Optional[Any] = ...): ...
def create_user(**kwargs: Any): ...
def update_user(uid: Any, **kwargs: Any): ...
def set_custom_user_claims(uid: Any, custom_claims: Any, app: Optional[Any] = ...) -> None: ...
def delete_user(uid: Any, app: Optional[Any] = ...) -> None: ...
def delete_users(uids: Any, app: Optional[Any] = ...): ...
def import_users(users: Any, hash_alg: Optional[Any] = ..., app: Optional[Any] = ...): ...
def generate_password_reset_link(email: Any, action_code_settings: Optional[Any] = ..., app: Optional[Any] = ...): ...
def generate_email_verification_link(email: Any, action_code_settings: Optional[Any] = ..., app: Optional[Any] = ...): ...
def generate_sign_in_with_email_link(email: Any, action_code_settings: Any, app: Optional[Any] = ...): ...
def get_oidc_provider_config(provider_id: Any, app: Optional[Any] = ...): ...
def create_oidc_provider_config(provider_id: Any, client_id: Any, issuer: Any, display_name: Optional[Any] = ..., enabled: Optional[Any] = ..., app: Optional[Any] = ...): ...
def update_oidc_provider_config(provider_id: Any, client_id: Optional[Any] = ..., issuer: Optional[Any] = ..., display_name: Optional[Any] = ..., enabled: Optional[Any] = ..., app: Optional[Any] = ...): ...
def delete_oidc_provider_config(provider_id: Any, app: Optional[Any] = ...) -> None: ...
def get_saml_provider_config(provider_id: Any, app: Optional[Any] = ...): ...
def create_saml_provider_config(provider_id: Any, idp_entity_id: Any, sso_url: Any, x509_certificates: Any, rp_entity_id: Any, callback_url: Any, display_name: Optional[Any] = ..., enabled: Optional[Any] = ..., app: Optional[Any] = ...): ...
def update_saml_provider_config(provider_id: Any, idp_entity_id: Optional[Any] = ..., sso_url: Optional[Any] = ..., x509_certificates: Optional[Any] = ..., rp_entity_id: Optional[Any] = ..., callback_url: Optional[Any] = ..., display_name: Optional[Any] = ..., enabled: Optional[Any] = ..., app: Optional[Any] = ...): ...
def delete_saml_provider_config(provider_id: Any, app: Optional[Any] = ...) -> None: ...
def list_saml_provider_configs(page_token: Optional[Any] = ..., max_results: Any = ..., app: Optional[Any] = ...): ...
