from discord_webhook import DiscordWebhook, DiscordEmbed

with open('discord_webhook.txt', 'r') as f:
    URL = f.read()

def send_message(message: str) -> None:
    webhook = DiscordWebhook(url=URL, content=message)
    response = webhook.execute()


def send_embed_bank(team: str, message: str, description: str, color: str, field_name: str, bank_coins: int) -> None:
    webhook = DiscordWebhook(url=URL)
    embed = DiscordEmbed(
        title= f'{team} {message}',
        description= description,
        color=color
    )
    embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/Coins_1000.png?978c8')
    embed.add_embed_field(name=field_name, value=bank_coins)
    webhook.add_embed(embed)
    response = webhook.execute()