"""
Rocco Ahching
25 August 2021
Embedded Programming
Low-level abstractions of Discord's Embed structure
"""


import discord
import json
from typing import Iterable, Optional, Union, Any




# Convert str to discord.Color
def str_to_discord_color(h: str) -> discord.Color:
    h = h[1:]
    return discord.Color.from_rgb(*(int(h[i:i+2], 16) for i in (0, 2, 4)))

# Convert discord.Embed object to request-ready json-serializable object.
def embeds_to_json(*embeds: Iterable[discord.Embed]) -> dict:
    assert type(embeds) == tuple, \
        f"This function requires an unpacked list of embeds. I.E. \"embeds_to_json(emb, emb1)\""

    # If you need an explanation on this, let me know -R
    results = map(lambda emb: json.loads(json.dumps(
        emb.to_dict()).replace('"None"', 'null')), embeds)

    # convert map object to generated list
    return list(results)


# Build entire embed object in one-line (personal preference here)
def build_embed(
    title = None,
    description = None,
    color = 000000,
    url = None,
    image_url = None,
    thumbnail_url = None,
    author_info = None,
    footer = None,
    fields = None
        # title: Optional[str] = None,
        # description: Optional[str] = None,
        # color: Optional[Union[discord.Color, int]] = 000000,
        # url: Optional[str] = None,
        # image_url: Optional[str] = None,
        # thumbnail_url: Optional[str] = None,
        # author_info: Optional[tuple[Optional[str],
        #                             Optional[str], Optional[str]]] = None,
        # footer: Optional[tuple[str, str]] = None,
        # fields: Optional[list[tuple[str, str, Optional[bool]]]] = None,
) -> discord.Embed:

    # create embed object from Discord
    emb: discord.Embed = discord.Embed(
        title=title, description=description, color=color, url=url)

    # set image / thumbnail urls (could type check but not needed)
    emb.set_image(url=image_url)
    emb.set_thumbnail(url=thumbnail_url)

    # type checking
    assert type(fields) in [list, tuple, type(None)], f"Embed fields must be a list of tuples, not {fields.__class__.__name__}"

    # convert single object to list for iteration
    if fields:
        if type(fields) == tuple:
            fields = [fields]

        for field in fields:
            # content checking
            assert 1 < len(field) < 4, f'Embed fields must be 2 or 3 items long.'
            emb.add_field(name=field[0], value=field[1], inline=field[2] if len(field) == 3 else True)

    # type checking
    assert type(author_info) in [tuple, type(None)], f"Author info must be a tuple, not {author_info.__class__.__name__}"

    if author_info:
        # content checking
        assert len(footer) < 4, f'Footer must be at most 3 elements long.'
        emb.set_author(name=author_info[0], icon_url=author_info[1], url=author_info[2])

    # type checking
    assert type(footer) in [tuple, type(None)], \
        f"Footer info must be a tuple, not {author_info.__class__.__name__}"

    if footer:
        # content checking
        assert len(footer) < 3, f'Footer must be at most 2 elements long.'
        emb.set_footer(text=footer[0], icon_url=footer[1])

    # return constructed embed
    return emb


if __name__ == "__main__":
    from pprint import pprint
    emb = build_embed("hi", fields=[("hi", "hi"), ("hi", "hi")])
    emb2 = build_embed("hi", fields=(("hi", "hi")))
    emb_json = embeds_to_json(emb, emb2)
    import requests
    result = requests.post('http://8.8.8.8', json={"embeds": emb_json})
    pprint(emb_json)
    pprint(result.request.body.decode("utf-8"))
