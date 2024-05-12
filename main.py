import discord
from discord.ext import commands
from binance.client import Client as bnc
import io
import matplotlib.pyplot as plt
import requests

# Configurações do bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True
binance_api_key = "Sua api da binance"
binance_secret = "sua binance secret key"
Bot = commands.Bot(command_prefix=".", intents=intents)

# Configurações da API da Binance
client_binance = bnc(api_key=binance_api_key, api_secret=binance_secret)


# Comando para verificar informações sobre uma moeda na Binance
@Bot.command()
async def moeda(ctx, moeda: str):
    try:
        # Adiciona "USDT" ao símbolo inserido pelo usuário
        symbol = f"{moeda.upper()}USDT"
        # Obtem informações sobre a moeda binance
        ticker = client_binance.get_ticker(symbol=symbol)

        # Verifica se o ticker retornou dados
        if ticker:
            # Formatar os preços com duas casas decimais
            circulating_supply = ticker.get("circulatingSupply", "Não disponível")
            market_cap = ticker.get("marketCap", "Não disponível")

            # Exibir informações no Discord
            embed = discord.Embed(
                title=f"Informações sobre {moeda.upper()}",
                description=(
                    f"**Variação 24h:** {ticker['priceChangePercent']}%\n"
                    f"**Volume 24h:** {ticker['volume']} {moeda.upper()}\n"
                    f"**Máxima 24h:** {ticker['highPrice']} USDT\n"
                    f"**Mínima 24h:** {ticker['lowPrice']} USDT\n"
                    f"**Preço Atual:** {ticker['lastPrice']} USDT\n"
                    f"**Fornecimento Circulante:** {circulating_supply} {moeda.upper()}\n"
                    f"**Capitalização de Mercado:** {market_cap} USDT\n"
                    f"🚀 Dados em tempo real! 🚀"
                ),
                color=0x00FF00,  # Cor do embed (verde)
            )

            # Adicionar um rodapé
            embed.set_footer(text="Dados em tempo real!")

            # Exibir o embed no Discord
            await ctx.send(embed=embed)
        else:
            await ctx.send("Moeda não encontrada na Binance.")

    except Exception as e:
        await ctx.send(f"Erro ao obter informações da Binance: {e}")


def get_historical_data(symbol, interval, limit):
    url = f"https://api.binance.com/api/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Erro ao obter dados históricos:", response.text)
        return None


@Bot.command()
async def grafico(ctx, moeda: str):
    try:
        # Obter dados históricos da Binance
        symbol = f"{moeda.upper()}USDT"
        interval = "1h"
        limit = 100
        historical_data = get_historical_data(symbol, interval, limit)
        if not historical_data:
            await ctx.send("Não foi possível obter os dados históricos.")
            return

        # Extrair timestamps e preços de fechamento
        timestamps = [item[0] for item in historical_data]
        close_prices = [float(item[4]) for item in historical_data]

        # Gerar o gráfico usando Matplotlib
        plt.plot(timestamps, close_prices)

        # Configurar o gráfico
        plt.title(f"Gráfico de preços para {moeda.upper()}")
        plt.xlabel("Tempo")
        plt.ylabel("Preço")

        # Salvar o gráfico em um buffer de memória
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Enviar o gráfico para o Discord
        file = discord.File(buf, filename="grafico.png")
        await ctx.send(file=file)

    except Exception as e:
        await ctx.send(f"Erro ao gerar o gráfico: {e}")


# Função para obter os pares de moedas suportados
def get_supported_pairs():
    supported_pairs = [
        "BRLBTC",
        "BRLUSDT",
        "BTCUSDT",
        "ETHBTC",
        "ETHUSDT",
        "LTCBTC",
        "LTCUSDT",
        "XRPBTC",
        "XRPUSDT",
    ]
    return supported_pairs


# Função para formatar os pares de moedas suportados
def format_supported_pairs():
    pairs = get_supported_pairs()
    formatted_pairs = "\n".join([pair[:3] + " para " + pair[3:] for pair in pairs])
    return formatted_pairs


def convert_currency(amount, from_currency, to_currency):
    client = bnc(binance_api_key, binance_secret)
    symbol = f"{from_currency.upper()}{to_currency.upper()}"
    ticker = client.get_symbol_ticker(symbol=symbol)
    rate = float(ticker["price"])
    converted_amount = amount * rate
    return converted_amount


@Bot.command()
async def convert(
    ctx, amount: float = None, from_currency: str = None, to_currency: str = None
):
    # Se não houver argumentos fornecidos, exibir a lista de pares de negociação suportados
    if amount is None or from_currency is None or to_currency is None:
        supported_pairs_message = f"Os pares de negociação suportados são:\n{format_supported_pairs()}\n\nPor favor, digite o comando na forma .convert <quantidade> <moeda de origem> <moeda de destino>."
        await ctx.send(supported_pairs_message)
        return

    # Caso contrário, realizar a conversão de moeda
    try:
        converted_amount = convert_currency(amount, from_currency, to_currency)
        await ctx.send(
            f"{amount} {from_currency.upper()} = {converted_amount} {to_currency.upper()}"
        )
    except Exception as e:
        await ctx.send(f"Erro ao converter moeda: {e}")


# Limpar Chat maximo 100 mensagens
@Bot.command()
async def limpar(ctx, quantidade: int):
    if quantidade > 100:
        await ctx.send("Você só pode limpar até 100 mensagens de uma vez.")
        return

    messages = []
    async for message in ctx.channel.history(limit=quantidade + 1):
        messages.append(message)

    await ctx.channel.delete_messages(messages)

    # Mensagem de confirmação
    await ctx.send(f"{quantidade} mensagens foram excluídas.")


# Inicia o bot
Bot.run("seu token")
