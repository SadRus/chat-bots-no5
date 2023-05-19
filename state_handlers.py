from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from elastic_handlers import (
    add_product_to_cart,
    create_cart,
    create_customer,
    get_cart_content,
    get_cart_products,
    get_customer_by_id,
    get_image_link,
    get_products,
    get_product_by_id,
    get_product_image,
    remove_item_from_cart,
)


def send_cart(update, context, elastic_token, cart_reference):
    query = update.callback_query
    cart_products = get_cart_products(elastic_token, cart_reference)
    if cart_products:
        text = ''
        keyboard = []
        for product in cart_products:
            name = product['name']
            description = product['description']
            quantity = product['quantity']
            unit_price = product['unit_price']['amount']
            text += f"{name}\n"
            text += f"{description}\n"
            text += f"{quantity}kg in cart for ${quantity*unit_price}\n\n"
            button = InlineKeyboardButton(
                f'Удалить {name}',
                callback_data=f'{product["id"]}'
            )
            keyboard.append(button)
        keyboard.append(
            [
                InlineKeyboardButton('В меню', callback_data='menu'),
                InlineKeyboardButton('Оплата', callback_data='payment'),
            ]
        )
        cart_content = get_cart_content(elastic_token, cart_reference)
        total_sum = cart_content['meta']['display_price']['with_tax']['amount']
        text += f'Total: ${total_sum}'
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
        )
        context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=query.message.message_id,
        )
    else:
        keyboard = [
            [InlineKeyboardButton('В меню', callback_data='menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='У вас нет товаров в корзине',
            reply_markup=reply_markup,
        )
        context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=query.message.message_id,
        )


def get_or_create_cart(update, context, elastic_token):
    chat_id = update.effective_chat.id
    cart_reference = context.user_data.get('cart_reference')
    if not cart_reference:
        cart_reference = create_cart(elastic_token, user_id=chat_id)['id']
        context.user_data['cart_reference'] = cart_reference
    return cart_reference


def start(update, context, elastic_token):
    products = get_products(elastic_token)
    keyboard = []
    for product in products:
        keyboard.append(
            [InlineKeyboardButton(f'{product["attributes"]["name"]}', callback_data=product['id'])]
        )
    keyboard.append([InlineKeyboardButton('Корзина', callback_data='cart')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Please choose:',
        reply_markup=reply_markup,
    )
    return 'HANDLE_MENU'


def button(update, context, elastic_token):
    query = update.callback_query
    query.answer()

    if query.data == 'cart':
        cart_reference = context.user_data.get('cart_reference')
        send_cart(update, context, elastic_token, cart_reference)
        return 'HANDLE_CART'

    keyboard = [
        [
            InlineKeyboardButton('1 kg', callback_data=1),
            InlineKeyboardButton('5 kg', callback_data=5),
            InlineKeyboardButton('10 kg', callback_data=10)
        ],
        [InlineKeyboardButton('Назад', callback_data='menu')],
        [InlineKeyboardButton('Корзина', callback_data='cart')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    product_id = query.data
    context.user_data['product_id'] = product_id
    product = get_product_by_id(elastic_token, product_id)['attributes']
    image_id = get_product_image(elastic_token, product_id)['id']
    image_link = get_image_link(elastic_token, image_id)

    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        caption=f"{product['name']}\n\n"
                f"{product['description']}\n"
                f"{product['slug']}\n",
        photo=f'{image_link}',
        reply_markup=reply_markup,
    )
    context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=query.message.message_id,
    )
    return 'HANDLE_DESCRIPTION'


def description_button(update, context, elastic_token):
    query = update.callback_query
    query.answer()
    if query.data == 'menu':
        start(update, context, elastic_token)
        context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=query.message.message_id,
        )
        return 'HANDLE_MENU'
    if query.data == 'cart':
        cart_reference = context.user_data.get('cart_reference')
        send_cart(update, context, elastic_token, cart_reference)
        return 'HANDLE_CART'
    else:
        cart_reference = get_or_create_cart(update, context, elastic_token)
        product_id = context.user_data['product_id']
        quantity = int(query.data)
        add_product_to_cart(
            token=elastic_token,
            cart_reference=cart_reference,
            product_id=product_id,
            quantity=quantity,
        )
        return 'HANDLE_DESCRIPTION'


def cart_button(update, context, elastic_token):
    query = update.callback_query
    query.answer()
    if query.data == 'menu':
        start(update, context, elastic_token)
        context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=query.message.message_id,
        )
        return 'HANDLE_MENU'
    elif query.data == 'payment':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Пожалуйста пришлите ваш email:',
        )
        return "WAITING_EMAIL"
    else:
        cart_reference = context.user_data['cart_reference']
        remove_item_from_cart(elastic_token, cart_reference, query.data)
        send_cart(update, context, elastic_token, cart_reference)
        return 'HANDLE_CART'


def handle_email(update, context, elastic_token):
    user_email = update.message.text
    user_id = str(update.effective_chat.id)

    customer_id = create_customer(elastic_token, user_id, user_email)['id']

    # Для проверки
    user_email = get_customer_by_id(elastic_token, customer_id)['email']

    keyboard = [
        [
            InlineKeyboardButton('В меню', callback_data='menu'),
            InlineKeyboardButton('Корзина', callback_data='cart'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=user_id,
        text=f'Вы указали почту:\n{user_email}',
        reply_markup=reply_markup,
    )
    return 'HANDLE_DESCRIPTION'
