# discordのbotに必要なライブラリをインポート
import discord
import datetime

# BOTのアクセストークン
TOKEN = "BOTのトークンはここ"

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 発言したチャンネルのカテゴリ内にチャンネルを作成する非同期関数
# @client.event
async def create_channel(message, permittion, channel_name):
    print("-----create_channel-----")
    category_id = message.channel.category_id
    category = message.guild.get_channel(category_id)

    # 第二引数が1の場合、プライベートチャンネルを作成
    try:
        if permittion == "1":
            overwrites = {
                message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                message.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            new_channel = await category.create_text_channel(name=channel_name, overwrites=overwrites)
        elif permittion =="0":
            new_channel = await category.create_text_channel(name=channel_name)
    except:
        import traceback
        traceback.print_exc()
        return
    return new_channel

async def create_scheduled_event(message, message_list):
    # スケジュールイベント作成
    name = message_list[4]
    tdatetime = datetime.datetime.strptime(message_list[3], '%Y%m%d-%H%M')
    start_time = tdatetime - datetime.timedelta(hours=9) 
    end_time = start_time + datetime.timedelta(days=1)
    # どのVCか判定
    location = message_list[2]

    privacy_level = discord.ScheduledEventPrivacyLevel.guild_only
    await discord.Guild.create_scheduled_event(self=message.guild , name=name, description="", start_time=start_time,end_time=end_time, location=location, privacy_level=privacy_level, reason=None)



@client.event
async def on_message(message):
    print("-----on_message-----")
    # "!作成 (0or1)　(イベントを実施するボイスチャンネル名) (日付:202204101900) 作成したいチャンネル名" になっていること
    message_list = list()
    message_list = message.content.split()
    error = ""
    # メッセージ送信者がBotだった場合は無視する
    if message.author == client.user:
        return
    if message_list[0].startswith('!ナマステ'):
        text = f'``` ナマステ～ ```'
        await message.channel.send(text)
        return
    if message_list[0].startswith('!help'):
        text = f'作成したいカテゴリー内のテキストチャンネルにて\n ``` !作成 (公開チャンネル: 0 or プライベートチャンネル: 1) (どのVCでやるか) (日付: <例>20220415-1900) 作成したいチャンネル名 \n !ナマステ : ナマステと返してくれる ```'
        await message.channel.send(text)
        return

    # !作成コマンド処理
    if message_list[0].startswith('!作成'):
        # コマンドのバリデーション判定
        if len(message_list) != 5:
            error = "!作成 (0or1) (どのVCでやるか:VC名) (日付:202204101900) 作成したいチャンネル名になっていない"    
        elif not message_list[1]=="0" and not message_list[1]=="1":
            error = "1つ目が0,1ではない"
        elif not message_list[2]=="ボイスチャンネル1":
            error = "正しいボイスチャンネルではない"

        if error:
            text = f'チャンネルの作成に失敗しました。エラー内容：{error}'
            await message.channel.send(text)
        try:
            # イベント作成
            await create_scheduled_event(message, message_list)

            # テキストチャンネル作成
            new_channel = await create_channel(message,message_list[1],message_list[4])

            # 全て作成完了後、メッセージを送る
            print("チャンネル作成完了")
            text = f'{new_channel.mention} を作成しました'
            await message.channel.send(text)
        except TypeError as e:
            text = f'作成失敗しました。エラー内容：{e}'
            await message.channel.send(text)
        except:
            import traceback
            traceback.print_exc()
            text = f'作成失敗しました。エラー内容：エラー'
            await message.channel.send(text)
            return
    return

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)