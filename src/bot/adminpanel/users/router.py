from aiogram import Router

from bot.adminpanel.users.routers.callback import router as callback_users_router

router = Router()
router.include_router(callback_users_router)
