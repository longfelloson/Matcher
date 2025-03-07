from aiogram.types import Message
from  aiogram.types.input_media_photo import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users.registration.constants import REGISTRATION_WARNING_TEXT
from bot.files import upload_user_photo_to_s3
from bot.users import crud as users_crud
from bot.users.configs import crud as users_config_crud
from bot.users.configs.schemas import UserConfig
from bot.users.registration.schemas import UserRegistrationInfo
from bot.notifications.new_users.publisher import publish_new_user


async def complete_user_registration(
    user_config_schema: UserConfig,
    photo_telegram_file_id: str,
    user_registration_info: UserRegistrationInfo,
    session: AsyncSession,
) -> None:
    await upload_user_photo_to_s3(telegram_file_id=photo_telegram_file_id)
    await users_crud.create_user(user_registration_info, session)
    await users_config_crud.add_user_config(user_config_schema, session)
    await publish_new_user(user_registration_info)


async def send_warning_about_username(
    message_to_answer: Message
) -> list[Message]:
    media = [
        InputMediaPhoto(
            media="https://img2.teletype.in/files/"
            "96/00/96000296-54a5-4d53-a9ba-fcd29d2856c9.png",
            caption=REGISTRATION_WARNING_TEXT,
        ),
        InputMediaPhoto(
            media="https://img1.teletype.in/files/"
            "49/2d/492dfe1f-e519-4d0f-9bec-904a0d938459.png"
        ),
        InputMediaPhoto(
            media="https://img1.teletype.in/files/"
            "49/2d/492dfe1f-e519-4d0f-9bec-904a0d938459.png"
        ), 
    ]
    media_group = await message_to_answer.answer_media_group(media)
    return media_group
