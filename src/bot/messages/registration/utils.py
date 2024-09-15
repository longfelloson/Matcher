from sqlalchemy.ext.asyncio import AsyncSession

from bot.files import upload_user_photo_to_s3
from bot.messages.registration.schemas import UserRegistrationInfo
from bot.users import crud as users_crud
from bot.users.configs import crud as users_config_crud
from bot.users.configs.schemas import UserConfig
from bot.users.enums import UserStatus


async def complete_user_registration(
    user_config_schema: UserConfig,
    photo_telegram_file_id: str,
    user_registration_info: UserRegistrationInfo,
    session: AsyncSession,
) -> None:
    await upload_user_photo_to_s3(
        telegram_file_id=photo_telegram_file_id
    )
    await users_crud.update_user(
        user_config_schema.user_id, session, **user_registration_info.model_dump(), status=UserStatus.active
    )
    await users_config_crud.add_user_config(user_config_schema, session)
