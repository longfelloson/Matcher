from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.users.rates.keyboards import rate_buttons_keyboard
from bot.users.guesses.schemas import Guess
from bot.users.guesses.states import GuessesState
from bot.users.guesses.utils import get_points_for_user_guess
from bot.users.models import User
from bot.users import crud as users_crud
from bot.users.rates.states import RateState
from bot.users.utils import get_user_from_redis
from bot.users.guesses import crud

router = Router(name="Guesses")


@router.message(GuessesState.user_age, F.text.isdigit())
async def age_guess_button_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    user_age_guess = int(message.text)
    user_for_view = await get_user_from_redis(state, session)

    points = get_points_for_user_guess(
        user_age_guess=user_age_guess, user_for_view=user_for_view
    )
    guess = Guess(
        guesser_user_id=user.id, guessed_user_id=user_for_view.id, points=points
    )

    await crud.add_guess(guess, session)
    await users_crud.increase_user_points(user.id, points, session)

    answer = "Теперь оцени анкету ⤴️"
    if points > 0:
        answer = f"(+{points} 🎈) {answer}"

    await state.set_state(RateState.user)
    await message.answer(answer, reply_markup=rate_buttons_keyboard())
