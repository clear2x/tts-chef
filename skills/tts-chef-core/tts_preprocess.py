#!/usr/bin/env python3
"""
TTS 文案预处理脚本

在将文本送入 TTS 引擎之前进行预处理，提高朗读准确率。
支持中文、英文、日文，可自动检测语言。

主要处理：
1. 多音字替换 —— 将 TTS 容易读错的词替换为同音字
2. 环境变量/代码标识符 —— 下划线转空格、驼峰拆分
3. 数字和版本号 —— 转为目标语言的读法
4. 英文缩写 —— 逐字母展开（如 API → A P I）
5. 运算符和符号 —— 转为目标语言的表达
6. URL/邮箱/路径 —— 转为可读文本
7. 标点和格式清理 —— Markdown/HTML 标记去除

用法:
    python tts_preprocess.py input.txt
    python tts_preprocess.py input.txt --lang zh
    python tts_preprocess.py input.txt --lang en
    python tts_preprocess.py input.txt --lang ja
    python tts_preprocess.py -i input.txt -o output.txt
    echo "需要调试 ENV_VAR" | python tts_preprocess.py -
    python tts_preprocess.py input.txt --rules custom_rules.json
"""

import re
import sys
import json
import argparse
from pathlib import Path
from typing import Optional


# ============================================================
#  多音字替换表
#  原则：替换为同音字，让 TTS 读出正确发音
#  注意：不同 TTS 引擎表现不同，请根据实际效果增删
# ============================================================

POLYPHONE_MAP: dict[str, str] = {
    # ---- 调 tiáo（TTS 易读成 diào）----
    "调试": "条试",
    "调用": "条用",
    "调解": "条解",
    "调整": "条整",
    "调配": "条配",
    "调味": "条味",
    "调控": "条控",
    "调音": "条音",
    "调节": "条节",
    "调侃": "条侃",
    "协调": "协条",
    "空调": "空条",
    "单调": "单条",
    "色调": "色条",
    "强调": "强条",
    "步调": "步条",

    # ---- 处 chǔ（TTS 易读成 chù）----
    "处理": "楚理",
    "相处": "相楚",
    "处分": "楚分",
    "处方": "楚方",
    "处决": "楚决",
    "处事": "楚事",
    "共处": "共楚",
    "处置": "楚置",
    "惩处": "惩楚",
    "妙处": "妙楚",
    "难处": "难楚",
    "用处": "用楚",
    "好处": "好楚",
    "害处": "害楚",
    "办事处": "办事楚",

    # ---- 重 chóng（TTS 易读成 zhòng）----
    "重复": "虫复",
    "重写": "虫写",
    "重装": "虫装",
    "重启": "虫启",
    "重建": "虫建",
    "重叠": "虫叠",
    "重播": "虫播",
    "重组": "虫组",
    "重做": "虫做",
    "重试": "虫试",
    "重新": "虫新",
    "重逢": "虫逢",
    "重生": "虫生",
    "重合": "虫合",
    "重命名": "虫命名",
    "重定向": "虫定向",

    # ---- 长 zhǎng（TTS 易读成 cháng）----
    "长大": "掌大",
    "成长": "成掌",
    "长辈": "掌辈",
    "长官": "掌官",
    "首长": "首掌",
    "增长": "增掌",
    "班长": "班掌",
    "校长": "校掌",
    "行长": "航掌",
    "区长": "区掌",
    "州长": "州掌",
    "乡长": "乡掌",
    "厂长": "厂掌",
    "师长": "师掌",
    "科长": "科掌",
    "局长": "局掌",
    "队长": "队掌",
    "部长": "部掌",
    "市长": "市掌",
    "省长": "省掌",
    "县长": "县掌",
    "村长": "村掌",
    "家长": "家掌",
    "兄长": "兄掌",
    "长者": "掌者",

    # ---- 少 shǎo（TTS 易读成 shào）----
    "少数": "炒数",
    "减少": "减炒",
    "多少": "多炒",
    "至少": "至炒",
    "少量": "炒量",
    "少许": "炒许",
    "少了": "炒了",

    # ---- 为 wèi（TTS 易读成 wéi）----
    "因为": "因未",
    "为此": "未此",
    "为何": "未何",
    "为止": "未止",
    "为期": "未期",
    "为了": "未了",
    "为什么": "为什莫",

    # ---- 了 liǎo（TTS 易读成 le）----
    "了解": "辽解",
    "一目了然": "一目辽然",
    "了结": "辽结",
    "了却": "辽却",
    "没完没了": "没完没辽",
    "了如指掌": "辽如指掌",

    # ---- 倒 dào（TTS 易读成 dǎo）----
    "倒是": "到是",
    "倒不如": "到不如",
    "倒过来": "到过来",
    "倒推": "到推",
    "倒序": "到序",
    "倒置": "到置",
    "倒数": "到数",
    "倒计时": "到计时",
    "倒排": "到排",
    "倒转": "到转",
    "反倒": "反到",
    "倾倒": "倾到",

    # ---- 降 jiàng（TTS 易读成 xiáng）----
    "降低": "匠低",
    "降温": "匠温",
    "下降": "下匠",
    "降水": "匠水",
    "降价": "匠价",
    "降级": "匠级",
    "降临": "匠临",
    "降落": "匠落",
    "降雨": "匠雨",
    "降低": "匠低",

    # ---- 弹 dàn（TTS 易读成 tán）----
    "子弹": "子旦",
    "弹幕": "旦幕",
    "弹药": "旦药",
    "导弹": "导旦",
    "炸弹": "炸旦",
    "弹药": "旦药",
    "弹药库": "旦药库",
    "核弹": "核旦",
    "炮弹": "炮旦",

    # ---- 觉 jué（TTS 易读成 jiào）----
    "觉得": "决得",
    "感觉": "感决",
    "自觉": "自决",
    "发觉": "发决",
    "察觉": "察决",
    "觉悟": "决悟",
    "觉醒": "决醒",
    "知觉": "知决",
    "幻觉": "幻决",
    "错觉": "错决",
    "听觉": "听决",
    "视觉": "视决",
    "嗅觉": "嗅决",
    "触觉": "触决",

    # ---- 行 háng（TTS 易读成 xíng）----
    "银行": "银航",
    "行列": "航列",
    "行数": "航数",
    "排行": "排航",
    "内行": "内航",
    "一行": "一航",
    "多行": "多航",
    "单行": "单航",
    "行距": "航距",
    "行业": "行业",  # 大多数 TTS 能读对
    "行情": "航情",
    "商行": "商航",
    "洋行": "洋航",

    # ---- 没 méi（TTS 易读成 mò）----
    "没有": "梅有",
    "没用": "梅用",
    "没关系": "梅关系",
    "没什么": "梅什么",
    "没准": "梅准",
    "没人": "梅人",
    "没想": "梅想",
    "没钱": "梅钱",
    "没事": "梅事",
    "没看": "梅看",
    "没听": "梅听",
    "没做": "梅做",
    "没说": "梅说",
    "没去": "梅去",
    "没来": "梅来",
    "没完": "梅完",
    "没找": "梅找",

    # ---- 率 lǜ（TTS 易读成 shuài/lù）----
    "概率": "概绿",
    "效率": "效绿",
    "频率": "频绿",
    "速率": "速绿",
    "比率": "比绿",
    "利率": "利绿",
    "功率": "功绿",
    "命中率": "命中绿",
    "成功率": "成功绿",
    "覆盖率": "覆盖绿",
    "使用率": "使用绿",
    "增长率": "增长绿",

    # ---- 藏 cáng（TTS 易读成 zàng）----
    "隐藏": "隐藏",  # 跳过，多数 TTS 能读对
    "收藏": "收苍",
    "藏身": "苍身",
    "藏匿": "苍匿",
    "储藏": "储苍",
    "冷藏": "冷苍",
    "矿藏": "矿苍",
    "珍藏": "珍苍",

    # ---- 朝 cháo（TTS 易读成 zhāo）----
    "朝阳": "潮阳",
    "朝代": "潮代",
    "朝廷": "潮廷",
    "朝向": "潮向",
    "朝圣": "潮圣",
    "朝拜": "潮拜",
    "朝政": "潮政",
    "南朝": "南潮",
    "北朝": "北潮",
    "隋朝": "隋潮",
    "唐朝": "唐潮",
    "宋朝": "宋潮",
    "明朝": "明潮",
    "清朝": "清潮",

    # ---- 似 shì（TTS 易读成 sì）----
    "似的": "是地",

    # ---- 给 jǐ（TTS 易读成 gěi）----
    "给予": "几予",
    "补给": "补几",
    "供给": "供几",
    "自给": "自几",
    "薪给": "薪几",
    "给养": "几养",

    # ---- 便 pián（TTS 易读成 biàn）----
    "便宜": "骈宜",
    "大腹便便": "大腹骈骈",

    # ---- 削 xuē（TTS 易读成 xiāo）----
    "削弱": "薛弱",
    "削减": "薛减",
    "剥削": "剥薛",
    "削价": "薛价",
    "瘦削": "瘦薛",

    # ---- 奇 jī（TTS 易读成 qí）----
    "奇数": "畸数",

    # ---- 壳 ké（TTS 易读成 qiào）----
    "外壳": "外柯",
    "蛋壳": "蛋柯",
    "贝壳": "贝柯",
    "卡壳": "卡柯",
    "弹壳": "旦柯",

    # ---- 帖 tiě/tiè（TTS 易读成 tiē）----
    "请帖": "请铁",
    "帖子": "铁子",
    "字帖": "字铁",
    "碑帖": "碑铁",

    # ---- 强 qiǎng（TTS 易读成 qiáng）----
    "勉强": "免抢",
    "强迫": "抢迫",
    "强求": "抢求",
    "倔强": "倔匠",
    "牵强": "牵抢",
    "强词夺理": "抢词夺理",

    # ---- 剥 bō（TTS 易读成 bāo）----
    "剥削": "波削",
    "剥夺": "波夺",
    "剥落": "波落",

    # ---- 露 lù（TTS 易读成 lòu）----
    "暴露": "暴路",
    "揭露": "揭路",
    "裸露": "裸路",
    "显露": "显路",
    "展露": "展路",
    "流露": "流路",
    "表露": "表路",
    "露骨": "路骨",
    "露天": "路天",
    "露营": "路营",
    "露台": "路台",

    # ---- 塞 sè（TTS 易读成 sāi）----
    "堵塞": "堵色",
    "闭塞": "闭色",
    "阻塞": "阻色",
    "语塞": "语色",

    # ---- 答 dá（TTS 易读成 dā）----
    "回答": "回答",  # 跳过，多数正确
    "答理": "达理",
    "答应": "达应",

    # ---- 冠 guàn（TTS 易读成 guān）----
    "冠军": "灌军",
    "夺冠": "夺灌",
    "冠名": "灌名",

    # ---- 载 zài（TTS 易读成 zǎi）----
    "下载": "下在",
    "上传": "上传",  # 跳过
    "加载": "加在",
    "承载": "承在",
    "满载": "满在",
    "记载": "记宰",
    "连载": "连宰",
    "刊载": "刊宰",
    "转载": "转宰",

    # ---- 差 chā/chāi/chà（TTS 易混淆）----
    "出差": "出拆",
    "差事": "拆事",
    "差遣": "拆遣",
    "差劲": "茬劲",
    "差点": "茬点",
    "偏差": "偏差",  # 跳过
    "误差": "误差",  # 跳过
    "温差": "温差",  # 跳过

    # ---- 发 fā/fà ----
    "头发": "头法",
    "理发": "理法",
    "结发": "结法",
    "令人发指": "令人法指",

    # ---- 创 chuàng（TTS 易读成 chuāng）----
    "创伤": "窗伤",
    "创口": "窗口",
    "创面": "窗面",
    "重创": "虫窗",

    # ---- 拗 ǎo/ào/niù ----
    "执拗": "执纽",
    "拗口": "袄口",

    # ---- 着 zhuó（TTS 易读成 zháo）----
    "着重": "浊重",
    "着落": "浊落",
    "着陆": "浊陆",
    "着手": "浊手",
    "着眼": "浊眼",
    "着想": "浊想",
    "著称": "浊称",
    "着装": "浊装",

    # ---- 参 cēn（TTS 易读成 cān）----
    "参差": "岑疵",

    # ---- 哄 hǒng/hòng ----
    "起哄": "起洪",
    "哄堂大笑": "洪堂大笑",
    "一哄而散": "一洪而散",
}

# ============================================================
#  英文缩写 → TTS 友好展开
#  短缩写逐字母展开；有通用读法的保持读法
# ============================================================

ABBREVIATION_MAP: dict[str, str] = {
    # --- 网络协议 ---
    "HTTP": "H T T P",
    "HTTPS": "H T T P S",
    "FTP": "F T P",
    "SSH": "S S H",
    "SSL": "S S L",
    "TLS": "T L S",
    "TCP": "T C P",
    "UDP": "U D P",
    "DNS": "D N S",
    "CDN": "C D N",
    "VPN": "V P N",
    "WAN": "W A N",
    "LAN": "L A N",

    # --- 编程/技术 ---
    "API": "A P I",
    "SDK": "S D K",
    "IDE": "I D E",
    "CLI": "C L I",
    "GUI": "G U I",
    "URL": "U R L",
    "URI": "U R I",
    "JSON": "J S O N",
    "XML": "X M L",
    "YAML": "Y A M L",
    "TOML": "T O M L",
    "HTML": "H T M L",
    "CSS": "C S S",
    "SQL": "S Q L",
    "NoSQL": "No S Q L",
    "REST": "R E S T",
    "RPC": "R P C",
    "GraphQL": "Graph Q L",
    "gRPC": "g R P C",
    "AJAX": "A J A X",
    "WASM": "W A S M",
    "DOM": "D O M",
    "BOM": "B O M",
    "MVC": "M V C",
    "MVVM": "M V V M",
    "CRUD": "C R U D",
    "JWT": "J W T",
    "OAuth": "O Auth",
    "SaaS": "S a a S",
    "PaaS": "P a a S",
    "IaaS": "I a a S",
    "CI/CD": "C I C D",
    "PR": "P R",
    "MR": "M R",

    # --- AI/ML ---
    "AI": "A I",
    "ML": "M L",
    "LLM": "L L M",
    "GPT": "G P T",
    "RAG": "R A G",
    "NLP": "N L P",
    "CV": "C V",
    "CNN": "C N N",
    "RNN": "R N N",
    "GAN": "G A N",
    "RLHF": "R L H F",
    "SFT": "S F T",
    "IoT": "I o T",
    "AGI": "A G I",

    # --- 硬件/系统 ---
    "CPU": "C P U",
    "GPU": "G P U",
    "TPU": "T P U",
    "RAM": "R A M",
    "ROM": "R O M",
    "SSD": "S S D",
    "HDD": "H D D",
    "OS": "O S",
    "iOS": "i O S",
    "MAC": "M A C",
    "IP": "I P",

    # --- 开发工具 ---
    "npm": "n p m",
    "pip": "p i p",
    "git": "g i t",
    "GNU": "G N U",
    "BSD": "B S D",
    "MIT": "M I T",
    "W3C": "W three C",
    "RFC": "R F C",

    # --- 常见缩写 ---
    "EOF": "E O F",
    "NaN": "N a N",
    "UUID": "U U I D",
    "MD5": "M D five",
    "SHA": "S H A",
    "RSA": "R S A",
    "AES": "A E S",
    "K8s": "K eight S",
    "i18n": "i eighteen n",
    "l10n": "l ten n",
    "a11y": "a eleven y",
    "DIY": "D I Y",
    "FYI": "F Y I",
    "BTW": "B T W",
    "IMO": "I M O",
    "TLDR": "T L D R",
    "WTF": "W T F",
    "QA": "Q A",
    "PM": "P M",
    "UI": "U I",
    "UX": "U X",
    "BFF": "B F F",
    "SRE": "S R E",
    "SPA": "S P A",
    "SSR": "S S R",
    "CSR": "C S R",
    "PWA": "P W A",
    "AWS": "A W S",
    "GCP": "G C P",
}

# ============================================================
#  符号替换表（按语言）
# ============================================================

SYMBOL_MAP_ZH: dict[str, str] = {
    "%": "百分之",
    "℃": "摄氏度",
    "°C": "摄氏度",
    "°F": "华氏度",
    "¥": "元",
    "$": "美元",
    "€": "欧元",
    "£": "英镑",
    "≤": "小于等于",
    "≥": "大于等于",
    "≠": "不等于",
    "≈": "约等于",
    "±": "正负",
    "×": "乘以",
    "÷": "除以",
    "→": "变为",
    "←": "来自",
    "⇒": "推导出",
    "&": "和",
    "@": "艾特",
    "~": "约",
    "+": "加",
    "—": "，",
    "……": "，",
    "·": "，",
    "//": "注释",
}

SYMBOL_MAP_EN: dict[str, str] = {
    "%": "percent",
    "℃": "degrees celsius",
    "°C": "degrees celsius",
    "°F": "degrees fahrenheit",
    "¥": "yen",
    "$": "dollars",
    "€": "euros",
    "£": "pounds",
    "≤": "less than or equal",
    "≥": "greater than or equal",
    "≠": "not equal",
    "≈": "approximately equal",
    "±": "plus or minus",
    "×": "times",
    "÷": "divided by",
    "→": "becomes",
    "←": "from",
    "⇒": "implies",
    "&": "and",
    "@": "at",
    "~": "approximately",
    "+": "plus",
    "//": "comment",
}

SYMBOL_MAP_JA: dict[str, str] = {
    "%": "パーセント",
    "℃": "度",
    "°C": "度",
    "°F": "華氏",
    "¥": "円",
    "$": "ドル",
    "€": "ユーロ",
    "£": "ポンド",
    "≤": "以下",
    "≥": "以上",
    "≠": "ノットイコール",
    "≈": "ほぼ等しい",
    "±": "プラスマイナス",
    "×": "かける",
    "÷": "わる",
    "→": "なる",
    "←": "から",
    "⇒": "導く",
    "&": "および",
    "@": "アット",
    "~": "約",
    "+": "プラス",
    "//": "コメント",
}


# ============================================================
#  英文数字转换工具
# ============================================================

_EN_ONES = [
    "", "one", "two", "three", "four", "five",
    "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]
_EN_TENS = [
    "", "", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety",
]
_EN_ORDINALS_IRREGULAR = {
    1: "first", 2: "second", 3: "third",
    5: "fifth", 8: "eighth", 9: "ninth",
    12: "twelfth",
}


def _en_number_to_words(n: int) -> str:
    """将整数转为英文单词（支持 0-999999）"""
    if n == 0:
        return "zero"
    if n < 0:
        return "minus " + _en_number_to_words(-n)
    parts = []
    if n >= 1000:
        parts.append(_en_number_under_1000(n // 1000) + " thousand")
        n %= 1000
    if n > 0:
        parts.append(_en_number_under_1000(n))
    return " ".join(parts)


def _en_number_under_1000(n: int) -> str:
    if n >= 100:
        remainder = n % 100
        if remainder:
            return f"{_EN_ONES[n // 100]} hundred {_en_number_under_100(remainder)}"
        return f"{_EN_ONES[n // 100]} hundred"
    return _en_number_under_100(n)


def _en_number_under_100(n: int) -> str:
    if n < 20:
        return _EN_ONES[n]
    tens = n // 10
    ones = n % 10
    if ones:
        return f"{_EN_TENS[tens]}-{_EN_ONES[ones]}"
    return _EN_TENS[tens]


def _en_ordinal(n: int) -> str:
    """将整数转为英文序数词"""
    if n in _EN_ORDINALS_IRREGULAR:
        return _EN_ORDINALS_IRREGULAR[n]
    if n < 20:
        return _EN_ONES[n] + "th"
    if n % 100 < 20 and n % 100 >= 10:
        return _en_number_to_words(n) + "th"
    last_digit = n % 10
    suffix = {1: "st", 2: "nd", 3: "rd"}.get(last_digit, "th")
    return _en_number_to_words(n) + suffix


# ============================================================
#  日文数字转换工具
# ============================================================

_JA_DIGITS = "零一二三四五六七八九"


def _ja_digit(d: int) -> str:
    return _JA_DIGITS[d]


def _ja_number(n: int) -> str:
    """将数字转为日文读法（支持 0-9999）"""
    if n == 0:
        return "ゼロ"
    parts = []
    if n >= 1000:
        s = n // 1000
        if s > 1:
            parts.append(_ja_digit(s))
        parts.append("千")
        n %= 1000
    if n >= 100:
        s = n // 100
        if s > 1:
            parts.append(_ja_digit(s))
        parts.append("百")
        n %= 100
    if n >= 10:
        s = n // 10
        if s > 1:
            parts.append(_ja_digit(s))
        parts.append("十")
        n %= 10
    if n > 0:
        parts.append(_ja_digit(n))
    return "".join(parts)


# ============================================================
#  语言检测
# ============================================================

def detect_language(text: str) -> str:
    """
    检测文本的主要语言。返回 "zh", "en", "ja" 之一。
    混合语言时返回占比最大的语言。
    """
    cjk_count = 0
    hiragana_count = 0
    katakana_count = 0
    latin_count = 0

    for ch in text:
        cp = ord(ch)
        if 0x4E00 <= cp <= 0x9FFF:
            cjk_count += 1
        elif 0x3040 <= cp <= 0x309F:
            hiragana_count += 1
        elif 0x30A0 <= cp <= 0x30FF:
            katakana_count += 1
        elif 0x41 <= cp <= 0x5A or 0x61 <= cp <= 0x7A:
            latin_count += 1

    total_cjk = cjk_count + hiragana_count + katakana_count
    total = total_cjk + latin_count

    if total == 0:
        return "en"  # 无文字内容，默认英文

    if total_cjk / total > 0.6:
        kana_total = hiragana_count + katakana_count
        if total_cjk > 0 and kana_total / total_cjk > 0.3:
            return "ja"
        return "zh"
    elif latin_count / total > 0.6:
        return "en"
    else:
        # 混合语言：看哪边更多
        if total_cjk > latin_count:
            kana_total = hiragana_count + katakana_count
            if total_cjk > 0 and kana_total / total_cjk > 0.3:
                return "ja"
            return "zh"
        return "en"


class TTSPreprocessor:
    """TTS 文案预处理器（支持中文/英文/日文）"""

    def __init__(self, lang: str = "auto", custom_rules_file: Optional[str] = None):
        """
        Args:
            lang: "zh", "en", "ja", or "auto" (auto-detect per text)
            custom_rules_file: 自定义规则 JSON 文件路径
        """
        self.lang = lang
        self.polyphone_map = dict(POLYPHONE_MAP)
        self.abbreviation_map = dict(ABBREVIATION_MAP)
        self.custom_replacements: dict[str, str] = {}

        # 预编译正则（只编译一次，提高性能）
        self._compile_patterns()

        if custom_rules_file:
            self._load_custom_rules(custom_rules_file)

    # 中文是 Unicode word char，Python 3 的 \b 在中文和英文/数字之间不生效
    # 用负向前瞻/后瞻替代 \b
    _WB_L = r'(?<![a-zA-Z0-9_])'   # 左侧不是英文/数字/下划线
    _WB_R = r'(?![a-zA-Z0-9_])'    # 右侧不是英文/数字/下划线

    def _compile_patterns(self):
        """预编译正则表达式"""
        # 环境变量：${VAR}, $VAR, %VAR%
        self._re_env_dollar_brace = re.compile(r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}')
        self._re_env_dollar = re.compile(r'\$([A-Z][A-Z0-9_]*)')
        self._re_env_percent = re.compile(r'%([A-Z][A-Z0-9_]*)%')

        # SCREAMING_SNAKE_CASE（至少一个下划线）
        self._re_screaming_snake = re.compile(
            self._WB_L + r'([A-Z][A-Z0-9]*_(?:[A-Z0-9]+_*)+[A-Z0-9]*)' + self._WB_R
        )

        # camelCase / PascalCase
        self._re_camel = re.compile(
            self._WB_L + r'([a-z][a-z0-9]*[A-Z][a-zA-Z0-9]*)' + self._WB_R
        )
        self._re_pascal = re.compile(
            self._WB_L + r'([A-Z][a-z]+(?:[A-Z][a-zA-Z0-9]*)+)' + self._WB_R
        )

        # URL
        self._re_url = re.compile(r'https?://[^\s<>\"\'）】」』\)]+')

        # 邮箱
        self._re_email = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')

        # 文件路径（包含扩展名的路径）
        self._re_filepath = re.compile(r'(?:/?[\w.-]+/)+[\w.-]+\.\w{1,6}')

        # 版本号：v1.0.3
        self._re_version = re.compile(
            self._WB_L + r'v\d+(?:\.\d+)+' + self._WB_R, re.IGNORECASE
        )

        # 年份：2024年
        self._re_year = re.compile(r'(\d{4})年')

        # 小数：3.14（用 (?<![.\d]) 避免匹配 IP 地址）
        self._re_decimal = re.compile(r'(?<![.\d])(\d+)\.(\d+)(?![.\d])')

        # 转义字符：\n \t \r
        self._re_escape = re.compile(r'\\([ntrvfab\\])')

        # HTML 标签
        self._re_html_tag = re.compile(r'<[^>]+>')

        # Markdown 加粗/斜体
        self._re_md_bold_italic = re.compile(r'\*{1,3}([^*]+)\*{1,3}')
        self._re_md_underline = re.compile(r'_{1,2}([^_]+)_{1,2}')

        # Markdown 标题
        self._re_md_header = re.compile(r'^#{1,6}\s+', re.MULTILINE)

        # Markdown 列表标记
        self._re_md_list = re.compile(r'^\s*[-*+]\s+', re.MULTILINE)
        self._re_md_num_list = re.compile(r'^\s*\d+\.\s+', re.MULTILINE)

        # Markdown 代码块
        self._re_md_codeblock = re.compile(r'```[\s\S]*?```')

        # Markdown 行内代码
        self._re_md_inline_code = re.compile(r'`([^`]+)`')

        # 多个连续标点
        self._re_multi_period = re.compile(r'[。]{2,}')
        self._re_multi_comma = re.compile(r'[，]{2,}')
        self._re_multi_pause = re.compile(r'[、]{2,}')

        # 英文序数词：1st, 2nd, 3rd, 4th, etc.
        self._re_ordinal = re.compile(r'\b(\d+)(st|nd|rd|th)\b', re.IGNORECASE)

        # Markdown 链接：[text](url)
        self._re_md_link = re.compile(r'\[([^\]]+)\]\([^)]+\)')

    def _load_custom_rules(self, filepath: str):
        """加载自定义规则 JSON 文件"""
        path = Path(filepath)
        if not path.exists():
            print(f"警告: 自定义规则文件 {filepath} 不存在，跳过", file=sys.stderr)
            return

        with open(path, "r", encoding="utf-8") as f:
            custom = json.load(f)

        if "polyphone" in custom:
            self.polyphone_map.update(custom["polyphone"])
        if "abbreviation" in custom:
            self.abbreviation_map.update(custom["abbreviation"])
        if "symbol" in custom:
            # 兼容旧的 symbol 字段
            pass
        if "custom_replacements" in custom:
            self.custom_replacements.update(custom["custom_replacements"])

    def _resolve_lang(self, text: str) -> str:
        """确定实际使用的语言"""
        if self.lang == "auto":
            return detect_language(text)
        return self.lang

    def process(self, text: str) -> str:
        """执行全部预处理流程（顺序重要）"""
        lang = self._resolve_lang(text)

        text = self._replace_custom(text)
        text = self._replace_escape_chars(text, lang)
        text = self._replace_codeblocks(text)
        text = self._replace_inline_code(text)
        text = self._replace_urls(text, lang)
        text = self._replace_emails(text, lang)
        text = self._replace_file_paths(text)
        text = self._replace_env_vars(text)
        text = self._replace_code_identifiers(text)
        text = self._replace_version_numbers(text, lang)
        text = self._replace_operators(text, lang)
        text = self._replace_numbers(text, lang)
        text = self._replace_symbols(text, lang)
        text = self._replace_abbreviations(text)
        if lang == "zh":
            text = self._replace_polyphones(text)
        if lang == "en":
            text = self._replace_ordinals(text)
        text = self._clean_markdown(text)
        text = self._clean_punctuation(text, lang)
        text = self._clean_whitespace(text)
        return text

    # ----------------------------------------------------------
    #  各规则实现
    # ----------------------------------------------------------

    def _replace_custom(self, text: str) -> str:
        """应用自定义直接替换"""
        for old, new in self.custom_replacements.items():
            text = text.replace(old, new)
        return text

    def _replace_escape_chars(self, text: str, lang: str) -> str:
        """替换转义字符"""
        if lang == "zh":
            escape_map = {
                "n": "换行", "t": "制表符", "r": "回车",
                "v": "垂直制表符", "f": "换页", "a": "警报",
                "b": "退格", "\\": "反斜杠",
            }
        elif lang == "ja":
            escape_map = {
                "n": "改行", "t": "タブ", "r": "キャリッジリターン",
                "v": "垂直タブ", "f": "フォームフィード", "a": "アラート",
                "b": "バックスペース", "\\": "バックスラッシュ",
            }
        else:  # en
            escape_map = {
                "n": "newline", "t": "tab", "r": "carriage return",
                "v": "vertical tab", "f": "form feed", "a": "alert",
                "b": "backspace", "\\": "backslash",
            }

        def replacer(match):
            ch = match.group(1)
            return escape_map.get(ch, match.group(0))

        return self._re_escape.sub(replacer, text)

    def _replace_codeblocks(self, text: str) -> str:
        """处理 Markdown 代码块：保留内容，去掉围栏标记"""
        def replacer(match):
            content = match.group(0)
            # 去掉 ``` 围栏
            lines = content.split('\n')
            # 去掉首尾的 ``` 行
            if lines and lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            return '\n'.join(lines)

        return self._re_md_codeblock.sub(replacer, text)

    def _replace_inline_code(self, text: str) -> str:
        """处理 Markdown 行内代码"""
        return self._re_md_inline_code.sub(r'\1', text)

    def _replace_urls(self, text: str, lang: str) -> str:
        """将 URL 转为可读描述"""
        prefix = "链接" if lang == "zh" else ("リンク" if lang == "ja" else "link")

        def replacer(match):
            url = match.group(0)
            domain_match = re.search(r'://([^/]+)', url)
            if domain_match:
                domain = domain_match.group(1)
                return f"{prefix} {domain}"
            return url
        return self._re_url.sub(replacer, text)

    def _replace_emails(self, text: str, lang: str) -> str:
        """将邮箱转为可读文本"""
        at_word = "艾特" if lang == "zh" else ("アット" if lang == "ja" else "at")

        def replacer(match):
            email = match.group(0)
            parts = email.split("@")
            if len(parts) == 2:
                return f"{parts[0]} {at_word} {parts[1]}"
            return email
        return self._re_email.sub(replacer, text)

    def _replace_file_paths(self, text: str) -> str:
        """处理文件路径"""
        def replacer(match):
            path = match.group(0)
            clean = re.sub(r'^(?:\.\.?/)+', '', path)
            clean = clean.lstrip('/')
            clean = clean.replace('/', ' ')
            return clean
        return self._re_filepath.sub(replacer, text)

    def _replace_env_vars(self, text: str) -> str:
        """处理环境变量"""
        def to_readable(var_name: str) -> str:
            return var_name.lower().replace("_", " ")

        text = self._re_env_dollar_brace.sub(lambda m: to_readable(m.group(1)), text)
        text = self._re_env_dollar.sub(lambda m: to_readable(m.group(1)), text)
        text = self._re_env_percent.sub(lambda m: to_readable(m.group(1)), text)
        return text

    def _replace_code_identifiers(self, text: str) -> str:
        """处理代码标识符（仅处理 SCREAMING_SNAKE_CASE，驼峰命名不拆分）"""
        # SCREAMING_SNAKE_CASE: ENV_VAR_NAME → env var name
        text = self._re_screaming_snake.sub(
            lambda m: m.group(0).lower().replace("_", " "), text
        )
        return text

    def _replace_version_numbers(self, text: str, lang: str) -> str:
        """处理版本号"""
        def replacer_zh(match):
            ver = match.group(0).lstrip('vV')
            parts = ver.split('.')
            result = "版本"
            for i, p in enumerate(parts):
                if i > 0:
                    result += "点"
                for c in str(int(p)):
                    result += "零一二三四五六七八九"[int(c)]
            return result

        def replacer_en(match):
            ver = match.group(0).lstrip('vV')
            parts = ver.split('.')
            result = "version"
            for i, p in enumerate(parts):
                if i > 0:
                    result += " point"
                result += " " + _en_number_to_words(int(p))
            return result

        def replacer_ja(match):
            ver = match.group(0).lstrip('vV')
            parts = ver.split('.')
            result = "バージョン"
            for i, p in enumerate(parts):
                if i > 0:
                    result += "てん"
                for c in str(int(p)):
                    result += _ja_digit(int(c))
            return result

        replacer = {"zh": replacer_zh, "en": replacer_en, "ja": replacer_ja}[lang]
        return self._re_version.sub(replacer, text)

    def _replace_operators(self, text: str, lang: str) -> str:
        """处理代码运算符（按长度降序匹配，避免部分匹配）"""
        ops_zh = [
            ("!==", "不全等于"), ("===", "全等于"), ("!=", "不等于"),
            ("==", "等于等于"), (">=", "大于等于"), ("<=", "小于等于"),
            ("=>", "箭头"), ("->", "箭头"),
            ("++", "自增"), ("--", "自减"),
            ("+=", "加等于"), ("-=", "减等于"), ("*=", "乘等于"), ("/=", "除等于"),
            ("&&", "并且"), ("||", "或者"),
        ]
        ops_en = [
            ("!==", "not strictly equal"), ("===", "strictly equal"), ("!=", "not equal"),
            ("==", "equal equal"), (">=", "greater than or equal"), ("<=", "less than or equal"),
            ("=>", "arrow"), ("->", "arrow"),
            ("++", "increment"), ("--", "decrement"),
            ("+=", "plus equals"), ("-=", "minus equals"), ("*=", "times equals"), ("/=", "divide equals"),
            ("&&", "and"), ("||", "or"),
        ]
        ops_ja = [
            ("!==", "厳密不等"), ("===", "厳密等価"), ("!=", "不等"),
            ("==", "等価"), (">=", "以上"), ("<=", "以下"),
            ("=>", "アロー"), ("->", "アロー"),
            ("++", "インクリメント"), ("--", "デクリメント"),
            ("+=", "足す代入"), ("-=", "引く代入"), ("*=", "掛ける代入"), ("/=", "割る代入"),
            ("&&", "かつ"), ("||", "または"),
        ]
        ops = {"zh": ops_zh, "en": ops_en, "ja": ops_ja}[lang]
        for op, replacement in ops:
            text = text.replace(op, replacement)
        return text

    def _replace_numbers(self, text: str, lang: str) -> str:
        """处理数字"""
        if lang == "zh":
            return self._replace_numbers_zh(text)
        elif lang == "en":
            return self._replace_numbers_en(text)
        else:
            return self._replace_numbers_ja(text)

    def _replace_numbers_zh(self, text: str) -> str:
        """中文数字处理"""
        # 年份：2024年 → 二零二四年
        def year_replacer(match):
            year = match.group(1)
            return "".join("零一二三四五六七八九"[int(c)] for c in year) + "年"
        text = self._re_year.sub(year_replacer, text)

        # 百分比：15% → 十五百分之
        def percent_replacer(match):
            num_str = match.group(1)
            if '.' in num_str:
                integer, decimal = num_str.split('.')
                result = ""
                for c in integer:
                    result += "零一二三四五六七八九"[int(c)]
                result += "点"
                for c in decimal:
                    result += "零一二三四五六七八九"[int(c)]
            else:
                result = self._number_to_chinese(int(num_str))
            return result + "百分之"

        text = re.sub(r'(\d+(?:\.\d+)?)%', percent_replacer, text)

        # 小数：3.14 → 三点一四
        def decimal_replacer(match):
            integer = match.group(1)
            decimal = match.group(2)
            result = ""
            for c in integer:
                result += "零一二三四五六七八九"[int(c)]
            result += "点"
            for c in decimal:
                result += "零一二三四五六七八九"[int(c)]
            return result
        text = self._re_decimal.sub(decimal_replacer, text)

        return text

    def _replace_numbers_en(self, text: str) -> str:
        """英文数字处理"""
        # 百分比：15% → fifteen percent
        def percent_replacer(match):
            num_str = match.group(1)
            if '.' in num_str:
                integer, decimal = num_str.split('.')
                result = _en_number_to_words(int(integer)) + " point"
                for c in decimal:
                    result += " " + _EN_ONES[int(c)]
            else:
                result = _en_number_to_words(int(num_str))
            return result + " percent"

        text = re.sub(r'(\d+(?:\.\d+)?)%', percent_replacer, text)

        # 小数：3.14 → three point one four
        def decimal_replacer(match):
            integer = match.group(1)
            decimal = match.group(2)
            result = _en_number_to_words(int(integer)) + " point"
            for c in decimal:
                result += " " + _EN_ONES[int(c)]
            return result
        text = self._re_decimal.sub(decimal_replacer, text)

        return text

    def _replace_numbers_ja(self, text: str) -> str:
        """日文数字处理"""
        # 年份：2024年 → にせんにじゅうよねん（用汉字表示）
        def year_replacer(match):
            year = int(match.group(1))
            return _ja_number(year) + "年"
        text = self._re_year.sub(year_replacer, text)

        # 百分比：15% → じゅうごパーセント
        def percent_replacer(match):
            num_str = match.group(1)
            if '.' in num_str:
                integer, decimal = num_str.split('.')
                result = _ja_number(int(integer)) + "てん"
                for c in decimal:
                    result += _ja_digit(int(c))
            else:
                result = _ja_number(int(num_str))
            return result + "パーセント"

        text = re.sub(r'(\d+(?:\.\d+)?)%', percent_replacer, text)

        # 小数：3.14 → さんてんいちよん
        def decimal_replacer(match):
            integer = match.group(1)
            decimal = match.group(2)
            result = _ja_number(int(integer)) + "てん"
            for c in decimal:
                result += _ja_digit(int(c))
            return result
        text = self._re_decimal.sub(decimal_replacer, text)

        return text

    def _replace_ordinals(self, text: str) -> str:
        """替换英文序数词：1st → first, 2nd → second"""
        def replacer(match):
            n = int(match.group(1))
            return _en_ordinal(n)
        return self._re_ordinal.sub(replacer, text)

    def _replace_symbols(self, text: str, lang: str) -> str:
        """替换特殊符号"""
        symbol_map = {"zh": SYMBOL_MAP_ZH, "en": SYMBOL_MAP_EN, "ja": SYMBOL_MAP_JA}[lang]
        for symbol, replacement in symbol_map.items():
            text = text.replace(symbol, replacement)
        return text

    def _replace_abbreviations(self, text: str) -> str:
        """替换英文缩写"""
        # 按长度降序匹配
        sorted_abbrs = sorted(
            self.abbreviation_map.items(), key=lambda x: len(x[0]), reverse=True
        )
        for abbr, expansion in sorted_abbrs:
            pattern = self._WB_L + re.escape(abbr) + self._WB_R
            text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)
        return text

    def _replace_polyphones(self, text: str) -> str:
        """替换多音字词（按词组长度降序匹配）"""
        sorted_words = sorted(
            self.polyphone_map.items(), key=lambda x: len(x[0]), reverse=True
        )
        for word, replacement in sorted_words:
            text = text.replace(word, replacement)
        return text

    def _clean_markdown(self, text: str) -> str:
        """清理 Markdown 格式标记"""
        text = self._re_md_header.sub('', text)
        text = self._re_md_list.sub('', text)
        text = self._re_md_num_list.sub('', text)
        text = self._re_md_bold_italic.sub(r'\1', text)
        text = self._re_md_underline.sub(r'\1', text)
        text = self._re_md_link.sub(r'\1', text)
        return text

    def _clean_punctuation(self, text: str, lang: str) -> str:
        """清理标点"""
        text = self._re_html_tag.sub('', text)

        if lang == "zh":
            text = self._clean_punctuation_zh(text)
        elif lang == "ja":
            text = self._clean_punctuation_ja(text)
        # en: 不做标点转换

        return text

    def _clean_punctuation_zh(self, text: str) -> str:
        """中文标点清理"""
        text = self._re_multi_period.sub('。', text)
        text = self._re_multi_comma.sub('，', text)
        text = self._re_multi_pause.sub('、', text)

        # 英文标点转中文
        text = text.replace(',', '，')
        text = text.replace('?', '？')
        text = text.replace('!', '！')
        text = text.replace(';', '；')
        text = re.sub(r'(?<![/\w]):(?![/\d])', '：', text)
        return text

    def _clean_punctuation_ja(self, text: str) -> str:
        """日文标点清理：半角→全角"""
        text = text.replace(',', '、')
        text = text.replace('.', '。')
        text = text.replace('?', '？')
        text = text.replace('!', '！')
        text = text.replace(':', '：')
        text = text.replace(';', '；')
        text = text.replace('(', '（')
        text = text.replace(')', '）')
        text = text.replace('[', '「')
        text = text.replace(']', '」')
        return text

    def _clean_whitespace(self, text: str) -> str:
        """清理空白"""
        text = re.sub(r' {2,}', ' ', text)
        text = '\n'.join(line.strip() for line in text.split('\n'))
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    # ----------------------------------------------------------
    #  工具方法
    # ----------------------------------------------------------

    @staticmethod
    def _number_to_chinese(n: int) -> str:
        """数字转中文（简易版，处理 0-99）"""
        digits = "零一二三四五六七八九"
        if n < 10:
            return digits[n]
        if n < 20:
            return "十" if n == 10 else "十" + digits[n % 10]
        if n < 100:
            tens = n // 10
            ones = n % 10
            return digits[tens] + "十" + (digits[ones] if ones else "")
        return str(n)


def main():
    parser = argparse.ArgumentParser(
        description="TTS 文案预处理工具（支持中文/英文/日文，自动检测语言）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python tts_preprocess.py input.txt                     # 自动检测语言
  python tts_preprocess.py input.txt --lang zh           # 指定中文
  python tts_preprocess.py input.txt --lang en           # 指定英文
  python tts_preprocess.py input.txt --lang ja           # 指定日文
  python tts_preprocess.py -i in.txt -o out.txt          # 指定输入输出
  echo "调试代码" | python tts_preprocess.py -            # 管道输入
  python tts_preprocess.py in.txt --rules rules.json     # 使用自定义规则
  python tts_preprocess.py in.txt --dry-run              # 查看前后对比

支持的语言: zh (中文), en (English), ja (日本語), auto (自动检测, 默认)
        """,
    )
    parser.add_argument("input", nargs="?", help="输入文件（- 表示 stdin）")
    parser.add_argument("-i", "--input-file", help="输入文件路径")
    parser.add_argument("-o", "--output-file", help="输出文件路径")
    parser.add_argument("-r", "--rules", help="自定义规则 JSON 文件")
    parser.add_argument(
        "--lang", choices=["zh", "en", "ja", "auto"], default="auto",
        help="目标语言 (默认: auto 自动检测)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="显示处理前后的对比",
    )

    args = parser.parse_args()

    # 读取输入
    input_path = args.input_file or args.input
    if input_path and input_path != "-":
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    # 处理
    processor = TTSPreprocessor(lang=args.lang, custom_rules_file=args.rules)
    result = processor.process(text)

    # 输出
    if args.dry_run:
        detected = processor._resolve_lang(text)
        print(f"=== 检测语言: {detected} ===")
        print("=== 原文 ===")
        print(text)
        print("\n=== 处理后 ===")
        print(result)
        print("\n=== 变更摘要 ===")
        if text == result:
            print("（无变化）")
        else:
            # 简单的行级 diff
            orig_lines = text.splitlines()
            new_lines = result.splitlines()
            for i, (o, n) in enumerate(zip(orig_lines, new_lines)):
                if o != n:
                    print(f"第{i+1}行:")
                    print(f"  - {o}")
                    print(f"  + {n}")
    elif args.output_file:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"已写入: {args.output_file}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
