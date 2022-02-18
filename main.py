from PIL import Image, ImageFilter, ImageDraw, ImageEnhance, ImageOps
import numpy as np
from scipy import ndimage


def get_mask(src_img):
    img = np.array(src_img)
    # laplace
    
    # would deform the image more
    # A = np.full((9, 9), -1)
    # A[4, 4] = 80

    A = np.full((3, 3), -1)
    A[1, 1] = 8

    # get edges
    out = ndimage.convolve(img, A)

    # Convert back to PIL image
    out = Image.fromarray(np.uint8(out))
    mask = out.convert("RGB")
    seed = (0, 0)
    rep_value = (255, 0, 0)
    ImageDraw.floodfill(mask, seed, rep_value, thresh=0)
    n_mask = np.array(mask)
    reds = (n_mask[:, :, 0] == 255) & (n_mask[:, :, 1] == 0) & (n_mask[:, :, 2] == 0)
    img_mask = Image.fromarray((reds * 255).astype(np.uint8))

    # making mask smoother by blurring it and getting mask by threshold
    blur_factor = 10
    blurred_mask = img_mask.filter(ImageFilter.GaussianBlur(blur_factor))
    n_b_mask = np.array(blurred_mask.convert("RGB"))
    blacks = (n_b_mask[:, :, 0] > 120)
    img_b_mask = Image.fromarray((blacks * 255).astype(np.uint8))

    return img_b_mask


def white_to_transparent(src_img):
    # almost white, also takes slightly grey, because of the damaged images
    x = np.asarray(src_img.convert('RGBA')).copy()

    x[:, :, 3] = (255 * (x[:, :, :3] < 240).any(axis=2)).astype(np.uint8)

    return Image.fromarray(x)


def get_fingerprint_photo(fingerprint, skin, background, damage):
    # fingerprint
    pic = Image.open(fingerprint).convert('L')
    # skin
    skin = Image.open(skin)
    skin = skin.resize(pic.size)
    # background
    bg = Image.open(background)
    bg = bg.resize(pic.size)
    # damage
    dmg = Image.open(damage)
    dmg = dmg.resize(pic.size)
    # getting rid of blur edges after resize
    n_dmg = np.array(dmg.convert("RGB"))
    blacks = (n_dmg[:, :, 0] > 180)
    dmg = Image.fromarray((blacks * 255).astype(np.uint8))
    dmg = white_to_transparent(dmg)

    # editing skin to different shades
    factor = 0.95  # used between papillary lines
    ultra_dark_factor = 0.5  # used on edged
    skin_darker = ImageEnhance.Brightness(skin).enhance(factor)
    skin_ultra_darker = ImageEnhance.Brightness(skin).enhance(ultra_dark_factor)
    white_bg = Image.new("RGB", pic.size, color="white")
    papillar = white_bg.copy()
    darker_edges = white_bg.copy()
    damage_masked = white_bg.copy()
    skin_saturation = ImageEnhance.Color(skin_darker).enhance(1.05)

    # getting mask, inverted mask and blurred mask
    mask = get_mask(pic)
    blur_factor = 50
    blurred_mask = mask.filter(ImageFilter.GaussianBlur(blur_factor))

    invert_blurred_mask = ImageOps.invert(blurred_mask)
    inverted_mask = ImageOps.invert(mask)

    darker_edges.paste(invert_blurred_mask, (0, 0), inverted_mask)

    orig_pic = white_to_transparent(pic)  # basically a mask from fingerprint

    papillar.paste(skin, (0, 0), orig_pic)  # maps skin to papillary lines
    skin_darker.paste(pic, (0, 0), mask)  # cuts finger shape into skin
    damage_masked.paste(skin_saturation, (0, 0), dmg)  # cuts damage into skin
    damage_masked.paste(pic, (0, 0), mask)  # cuts damage to shape of finger

    # combines papillary lines and finger "background"
    orig_img = Image.blend(papillar.convert('RGBA'), skin_darker.convert('RGBA'), alpha=0.8)
    orig_img.paste(damage_masked, (0, 0), dmg)  # adds damage

    # makes edges darker
    final = Image.composite(orig_img, skin_ultra_darker, darker_edges.convert('L'))
    bg.paste(final, (0, 0), inverted_mask)
    return bg
