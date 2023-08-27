from PIL import ImageOps

# ... (other imports and functions)

async def get_thumb(videoid, user_profile_picture_url, group_picture_url):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        # ... (existing code to fetch video details)

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(10))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.5)
        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 30)
        font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 30)

        # Fetch and resize the user's profile picture
        async with aiohttp.ClientSession() as session:
            async with session.get(user_profile_picture_url) as resp:
                if resp.status == 200:
                    user_profile_image = Image.open(await resp.read())
                    user_profile_image = ImageOps.fit(user_profile_image, (100, 100), method=0)

        # Fetch and resize the group picture
        async with aiohttp.ClientSession() as session:
            async with session.get(group_picture_url) as resp:
                if resp.status == 200:
                    group_image = Image.open(await resp.read())
                    group_image = ImageOps.fit(group_image, (100, 100), method=0)

        # Paste user's profile picture and group picture onto the thumbnail
        background.paste(user_profile_image, (10, 10))
        background.paste(group_image, (10, 120))

        # ... (existing code to add text, lines, and other elements)

        # ... (existing code to save and return the thumbnail)

    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
