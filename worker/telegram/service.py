from telebot.async_telebot import AsyncTeleBot
from .config import *
from .exception import ErrorCode
from app.utils.helper import Helper

class BaseBot:
    def __init__(self, channel_id: str):
        self.bot = AsyncTeleBot(BOT_TOKEN)
        self.environment = ENVIRONMENT
        self.channel_id = channel_id

    async def send_message(self, message: str):
        # Only send when Environment is Dev
        if self.environment not in ["development"]:
            return

        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
        except Exception as e:
            # print(f"Error when sending telegram message: {e}")
            raise ErrorCode.SendBotFailed()


class SentryBot(BaseBot):
    async def send_telegram(self, data: dict):
        title = data.get("title")
        url = data.get("url")
        method = data.get("method")
        filename = data.get("filename")
        function_name = data.get("function")
        lineno = data.get("lineno")
        context_line = data.get("context_line")
        issues_link = data.get("issues_link")

        message = (
            f"<b>❌ SENTRY ERROR</b>\n\n"
            f"<b>Environment:</b> {self.environment}\n"
            f"<b>Title:</b> {title}\n"
            f"<b>URL:</b> {url}\n"
            f"<b>Method:</b> {method}\n"
            f"<b>Filename:</b> {filename}\n"
            f"<b>Function:</b> {function_name}\n"
            f"<b>Lineno:</b> {lineno}\n"
            f"<b>Context:</b><pre>{context_line}</pre>\n"
            f"<b>Issue link:</b> {issues_link}"
        )
        await self.send_message(message)


class InvoiceBot(BaseBot):
    async def send_telegram(self, data: dict):
        items_text = ""
        for idx, item in enumerate(data.get("items", []), start=1):
            items_text += (
                f"\n  {idx}. <b>{item.get('name')}</b>\n"
                f"ID: {item.get('product_id')}\n"
                f"Qty: {item.get('quantity')} | "
                f"Price: {item.get('price')} | "
                f"Total: {float(item.get('price', 0)) * int(item.get('quantity', 0))}"
            )

        message = (
            f"<b>🧾 NEW INVOICE</b>\n"
            f"<b>Invoice ID:</b> {data.get('_id', '-')}\n"
            f"<b>User ID:</b> {data.get('user_id')}\n"
            f"<b>Status:</b> {data.get('status', '-')}\n"
            f"<b>Type VAT:</b> {data.get('type_vat', '-')}\n"
            f"<b>Created At:</b> {Helper.timestamp_to_date(ts=data.get('created_at'), tz="Asia/Ho_Chi_Minh")}\n\n"
            f"<b>Items:</b>{items_text}\n\n"
            f"<b>Total Items:</b> {data.get('total_items', 0)}\n"
            f"<b>Total Price:</b> {data.get('total_price', 0.0)}\n"
            f"<b>Address:</b> {data.get('address', '-')}\n"
            f"<b>Note:</b> {data.get('note', '-')}"
        )

        await self.send_message(message)

class SepayBot(BaseBot):
    async def send_telegram(self, data: dict):
        sepay_id = data.get("sepay_id")
        gateway = data.get("gateway")
        transaction_date = data.get("transaction_date")
        account_number = data.get("account_number")
        code = data.get("code")
        content = data.get("content")
        transfer_type = data.get("transfer_type")
        transfer_amount = data.get("transfer_amount")
        accumulated = data.get("accumulated")
        sub_account = data.get("sub_account")
        reference_code = data.get("reference_code")
        description = data.get("description")

        message = (
            f"<b>💰 SEPAY TRANSACTION</b>\n\n"
            f"<b>Environment:</b> {self.environment}\n"
            f"<b>Sepay ID:</b> {sepay_id}\n"
            f"<b>Gateway:</b> {gateway}\n"
            f"<b>Transaction Date:</b> {transaction_date}\n"
            f"<b>Account Number:</b> {account_number}\n"
            f"<b>Code:</b> {code}\n"
            f"<b>Content:</b> {content}\n"
            f"<b>Transfer Type:</b> {transfer_type}\n"
            f"<b>Transfer Amount:</b> {transfer_amount:,}\n"
            f"<b>Accumulated:</b> {accumulated if accumulated is not None else '—'}\n"
            f"<b>Sub Account:</b> {sub_account}\n"
            f"<b>Reference Code:</b> {reference_code}\n"
            f"<b>Description:</b> {description or '—'}"
        )

        await self.send_message(message)


sentry_bot = SentryBot(CHANNEL_ID)
invoice_bot = InvoiceBot(CHANNEL_ID)
sepay_bot = SepayBot(CHANNEL_ID)