import discord
import json
from typing import Optional, Union, Any


def str_to_discord_color(h: str) -> discord.Color:
    h = h[1:]
    return discord.Color.from_rgb(
        *(int(h[i:i+2], 16) for i in (0, 2, 4))
    )


def embeds_to_json(embeds: Union[list[discord.Embed], discord.Embed]) -> dict:

    def test(embed: discord.Embed):
        emb_dict = embed.to_dict()

        # def recursive(key: Any, value: Any):
        #     nonlocal emb_dict
        #     if type(value) != dict:
        #         if value == 'None':
        #             emb_dict[key] = None
        #     else:
        #         for subkey, subvalue in value.items():
        #             if subvalue == 'None':
        #                 emb_dict[key][subkey] = None

        # for key, value in emb_dict.items():
        #     recursive(key, value)

        test = json.dumps(emb_dict).replace('"None"', "null")
        return json.loads(test)

    assert type(embeds) in [Union[list[discord.Embed]], discord.Embed]
    if type(embeds) == discord.Embed:
        embeds = [embeds]
    results = map(test, embeds)
    return list(results)


def build_embed(
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[Union[discord.Color, int]] = 000000,
        url: Optional[str] = None,
        image_url: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        author_info: Optional[tuple[Optional[str],
                                    Optional[str], Optional[str]]] = None,
        fields: Optional[list[tuple[str, str, Optional[bool]]]] = None,
        footer: Optional[tuple[str, str]] = None,
) -> discord.Embed:

    emb: discord.Embed = discord.Embed(
        title=title, description=description, color=color, url=url)
    emb.set_image(url=image_url)
    emb.set_thumbnail(url=thumbnail_url)

    assert type(fields) in [list[tuple], tuple, type(
        None)], f"Embed fields must be a list of tuples, each tuple containing a name, value, and possible inlining."
    if fields:
        if type(fields) == type((str, str, Optional[bool])):
            fields = [fields]
        for field in fields:
            emb.add_field(name=field[0], value=field[1],
                          inline=field[2] if len(field) == 3 else True)

    assert type(author_info) in [tuple, type(None)]
    if author_info:
        emb.set_author(
            name=author_info[0], icon_url=author_info[1], url=author_info[2])

    assert type(footer) in [(str, str), type(None)]
    if footer:
        emb.set_footer(text=footer[0], icon_url=footer[1])
    return emb



if __name__ == "__main__":
    emb = build_embed("hi", fields=(("hi", None)))
    emb_json = embeds_to_json(emb)
    print(emb_json)

