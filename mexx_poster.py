import folder_paths
from comfy.cli_args import args

from html2image import Html2Image
from PIL import Image
from PIL.PngImagePlugin import PngInfo

import numpy as np
import json
import os
import shutil
import random


class ComfyUI_Mexx_Poster:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        styles = ["card","card_big"]
        return {
            "required":
                {"images": ("IMAGE",),
                 "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                 "fps": ("FLOAT", {"default": 6.0, "min": 0.01, "max": 1000.0, "step": 0.01}),
                 "compress_level": ("INT", {"default": 4, "min": 0, "max": 9}),
                 "style": (styles,),
                 },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()

    FUNCTION = "poster"

    OUTPUT_NODE = True

    CATEGORY = "ComfyUI_Mexx"

    def poster(self,
               images,
               fps,
               compress_level,
               filename_prefix="ComfyUI",
               style="card",
               prompt=None,
               extra_pnginfo=None):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        pil_images = []
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            pil_images.append(img)

        metadata = None
        if not args.disable_metadata:
            metadata = PngInfo()
            if prompt is not None:
                metadata.add(b"comf",
                             "prompt".encode("latin-1", "strict") + b"\0" + json.dumps(prompt).encode("latin-1",
                                                                                                      "strict"),
                             after_idat=True)
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add(b"comf",
                                 x.encode("latin-1", "strict") + b"\0" + json.dumps(extra_pnginfo[x]).encode("latin-1",
                                                                                                             "strict"),
                                 after_idat=True)

        file = f"{filename}_{counter:05}_.png"
        os_path_join_file = os.path.join(full_output_folder, file)
        pil_images[0].save(os_path_join_file, pnginfo=metadata, compress_level=compress_level,
                           save_all=True, duration=int(1000.0 / fps), append_images=pil_images[1:])
        print(f'[Mexx]生成图片地址:{file}')
        hti = Html2Image()
        current_directory = os.path.dirname(os.path.realpath(__file__))
        print(f'[Mexx]当前插件地址:{current_directory}')

        css_file = open(f"{current_directory}/{style}/poster.css", encoding='UTF-8')
        css_template = css_file.read()
        colors = ['#0094DF', '#FF6B20', '#D53B2A', '#FF6B20', '#8E1580', '#76368C', '#1DEAFF', '#FFA500',
                  '#960309', '#086AAA', '#22625E', '#F9A1D0', '#273268', '#547443']
        color1 = random.choice(colors)
        color2 = random.choice(colors)
        color3 = random.choice(colors)
        color4 = random.choice(colors)
        css = css_template.replace("{current_directory}", current_directory)
        css = css.replace("{color1}", color1)
        css = css.replace("{color2}", color2)
        css = css.replace("{color3}", color3)
        css = css.replace("{color4}", color4)
        html_file = open(f"{current_directory}/{style}/poster.html", encoding='UTF-8')
        html_template = html_file.read()
        clans = ['机娘', '女妖', '神秘', '巫师', '骑士', '战士', '兽族', '帝国',
                 '联盟', '部落', '五行', '高塔', '星灵']
        clan = random.choice(clans)
        nicknames = ['機械女', '弓腰女', '使者', '万法', '女帝', '垣法', '行走', '逍遥', ]
        nickname = random.choice(nicknames)
        names = ['富江', '春春', '富春', '希仔', '幺幺', '湾仔', '花花', '襄垣']
        name = random.choice(names)
        titles = ['雞湯', '心灵', '行舟', '侧畔', '春晓', '执着', '卷子', '慎独']
        title1 = random.choice(titles)
        descriptions = ['員工技，作為一名優秀的員工，当老闆給妳灌了一口雞湯，妳的血量-1。',
                        '主公技，作為一名優秀的老闆，当給員工灌了一口雞湯时，妳的金钱+2。']
        description1 = random.choice(descriptions)
        print(f'[Mexx]需要载入图片地址:{os_path_join_file}')

        html = html_template.replace("{os_path_join_file}", os_path_join_file)
        html = html.replace("{clan}", clan)
        html = html.replace("{nickname}", nickname)
        html = html.replace("{name}", name)
        html = html.replace("{title1}", title1)
        html = html.replace("{description1}", description1)
        poster = f"{filename}_{counter:05}_Poster.png"
        print(f'[Mexx]生成海报名称:{poster}')
        size = (768, 1040)
        if style == 'card':
            size = (425, 585)
        if style == 'card_big':
            size = (768, 1040)
        hti.screenshot(html_str=html, css_str=css, save_as=poster, size=size)
        shutil.move(poster, full_output_folder)
        print(f'[Mexx]移动海报到output目录:{full_output_folder}')
        results.append({
            "filename": poster,
            "subfolder": subfolder,
            "type": self.type
        })
        return {"ui": {"images": results, "animated": (False,)}}


NODE_CLASS_MAPPINGS = {
    "ComfyUI_Mexx_Poster": ComfyUI_Mexx_Poster
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_Mexx_Poster": "ComfyUI_Mexx_Poster"
}
