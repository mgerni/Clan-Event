from discord_webhook import DiscordWebhook, DiscordEmbed

with open('discord_webhook.txt', 'r') as f:
    URL = f.read()

def send_message(message: str) -> None:
    webhook = DiscordWebhook(url=URL, content=message)
    response = webhook.execute()


def send_embed_bank_passed(team: str, bank_coins: int) -> None:
    webhook = DiscordWebhook(url=URL)
    embed = DiscordEmbed(
        title= f'{team} passed bank tile!',
        description= "5 coins were deposited to the bank!",
        color='F2C105'
    )
    embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/Coins_1000.png?978c8')
    embed.add_embed_field(name='Bank Value', value=f'{bank_coins}')
    webhook.add_embed(embed)
    response = webhook.execute()