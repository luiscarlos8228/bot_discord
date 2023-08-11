import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from yt_dlp import YoutubeDL


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

commands_dict = {
    '!hello': 'Exibe uma saudação do bot.',
    '!ping': 'Responde com "Pong!" para testar a conexão.',
    '!play': 'Reproduz música do YouTube em um canal de voz.',
    # Adicionar mais comandos conforme necessário
}

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'verbose': True
}

@bot.event
async def on_ready():
    print(f'Bot está pronto como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Olá, eu sou um bot de exemplo!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def play(ctx, *, query):
    author_voice_state = ctx.author.voice

    if not author_voice_state or not author_voice_state.channel:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
        return

    voice_channel = author_voice_state.channel

    if not ctx.voice_client:
        await voice_channel.connect()

    voice_client: VoiceClient = ctx.voice_client

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            url = info['url']
            print(url)
            voice_client.stop()
            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn',
                'executable': f'C:\FFmpeg/bin/ffmpeg.exe',
            }
            voice_client.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
            await ctx.send(f"Reproduzindo: {info['title']}")

    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao reproduzir a música: {e}")

@bot.command(name='comandos')
async def bot_help(ctx):
    help_text = "Comandos disponíveis:\n"
    for command, description in commands_dict.items():
        help_text += f"{command}: {description}\n"

    await ctx.send(help_text)

bot.run('')
