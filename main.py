async def select_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.edit_message_reply_markup(
        reply_markup=None,
    )

    plan = query.data

    try:

        payment_url = create_checkout_session(
            plan,
            query.from_user.id,
        )

        if not payment_url:

            await query.message.reply_text(
                "❌ خطا در ایجاد لینک پرداخت."
            )
            return

        await query.answer(
            url=payment_url,
        )

    except Exception as e:

        print(e)

        await query.message.reply_text(
            "❌ خطا در ایجاد لینک پرداخت."
        )
