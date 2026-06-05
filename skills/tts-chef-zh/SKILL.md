---
name: tts-chef-zh
description: Chinese TTS text preprocessing — polyphone replacement for ~200 commonly mispronounced words, number-to-Chinese conversion (years, decimals, percentages, versions), Chinese punctuation normalization, sentence breaking rules, and tech abbreviation expansion. Use when preprocessing Chinese text for TTS, fixing polyphone pronunciation, or converting numbers to Chinese reading form.
license: MIT
---

# TTS-Chef Chinese (中文)

## When to Use This Skill

Apply when preprocessing **Chinese text** for TTS synthesis. Use when the text contains Chinese characters and needs polyphone correction, number conversion, or punctuation cleanup for speech output.

**Prerequisite:** Run **tts-chef-core** pipeline steps first (URL/email/code cleanup), then apply this skill's rules.

## Polyphone Replacement

Chinese TTS engines frequently mispronounce polyphone characters. Replace these words with homophone substitutes that force the correct pronunciation.

**Rule:** Apply **longest match first** — match "重定向" before "重定" before "重".

### 调 tiáo (TTS often reads diào)

| Original | Replacement |
|----------|-------------|
| 调试 | 条试 |
| 调用 | 条用 |
| 调解 | 条解 |
| 调整 | 条整 |
| 调配 | 条配 |
| 调味 | 条味 |
| 调控 | 条控 |
| 调音 | 条音 |
| 调节 | 条节 |
| 调侃 | 条侃 |
| 协调 | 协条 |
| 空调 | 空条 |
| 单调 | 单条 |
| 色调 | 色条 |
| 强调 | 强条 |
| 步调 | 步条 |

### 处 chǔ (TTS often reads chù)

| Original | Replacement |
|----------|-------------|
| 处理 | 楚理 |
| 相处 | 相楚 |
| 处分 | 楚分 |
| 处方 | 楚方 |
| 处决 | 楚决 |
| 处事 | 楚事 |
| 共处 | 共楚 |
| 处置 | 楚置 |
| 惩处 | 惩楚 |
| 办事处 | 办事楚 |
| 妙处 | 妙楚 |
| 难处 | 难楚 |
| 用处 | 用楚 |
| 好处 | 好楚 |
| 害处 | 害楚 |

### 重 chóng (TTS often reads zhòng)

| Original | Replacement |
|----------|-------------|
| 重复 | 虫复 |
| 重写 | 虫写 |
| 重装 | 虫装 |
| 重启 | 虫启 |
| 重建 | 虫建 |
| 重叠 | 虫叠 |
| 重播 | 虫播 |
| 重组 | 虫组 |
| 重做 | 虫做 |
| 重试 | 虫试 |
| 重新 | 虫新 |
| 重逢 | 虫逢 |
| 重生 | 虫生 |
| 重合 | 虫合 |
| 重命名 | 虫命名 |
| 重定向 | 虫定向 |

### 长 zhǎng (TTS often reads cháng)

| Original | Replacement |
|----------|-------------|
| 长大 | 掌大 |
| 成长 | 成掌 |
| 长辈 | 掌辈 |
| 长官 | 掌官 |
| 首长 | 首掌 |
| 增长 | 增掌 |
| 班长 | 班掌 |
| 校长 | 校掌 |
| 行长 | 航掌 |
| 区长 | 区掌 |
| 州长 | 州掌 |
| 乡长 | 乡掌 |
| 厂长 | 厂掌 |
| 师长 | 师掌 |
| 科长 | 科掌 |
| 局长 | 局掌 |
| 队长 | 队掌 |
| 部长 | 部掌 |
| 市长 | 市掌 |
| 省长 | 省掌 |
| 县长 | 县掌 |
| 村长 | 村掌 |
| 家长 | 家掌 |
| 兄长 | 兄掌 |
| 长者 | 掌者 |

### 少 shǎo (TTS often reads shào)

| Original | Replacement |
|----------|-------------|
| 少数 | 炒数 |
| 减少 | 减炒 |
| 多少 | 多炒 |
| 至少 | 至炒 |
| 少量 | 炒量 |
| 少许 | 炒许 |
| 少了 | 炒了 |

### 为 wèi (TTS often reads wéi)

| Original | Replacement |
|----------|-------------|
| 因为 | 因未 |
| 为此 | 未此 |
| 为何 | 未何 |
| 为止 | 未止 |
| 为期 | 未期 |
| 为了 | 未了 |
| 为什么 | 为什莫 |

### 了 liǎo (TTS often reads le)

| Original | Replacement |
|----------|-------------|
| 了解 | 辽解 |
| 一目了然 | 一目辽然 |
| 了结 | 辽结 |
| 了却 | 辽却 |
| 没完没了 | 没完没辽 |
| 了如指掌 | 辽如指掌 |

### 倒 dào (TTS often reads dǎo)

| Original | Replacement |
|----------|-------------|
| 倒是 | 到是 |
| 倒不如 | 到不如 |
| 倒过来 | 到过来 |
| 倒推 | 到推 |
| 倒序 | 到序 |
| 倒置 | 到置 |
| 倒数 | 到数 |
| 倒计时 | 到计时 |
| 倒排 | 到排 |
| 倒转 | 到转 |
| 反倒 | 反到 |
| 倾倒 | 倾到 |

### 降 jiàng (TTS often reads xiáng)

| Original | Replacement |
|----------|-------------|
| 降低 | 匠低 |
| 降温 | 匠温 |
| 下降 | 下匠 |
| 降水 | 匠水 |
| 降价 | 匠价 |
| 降级 | 匠级 |
| 降临 | 匠临 |
| 降落 | 匠落 |
| 降雨 | 匠雨 |

### 弹 dàn (TTS often reads tán)

| Original | Replacement |
|----------|-------------|
| 子弹 | 子旦 |
| 弹幕 | 旦幕 |
| 弹药 | 旦药 |
| 导弹 | 导旦 |
| 炸弹 | 炸旦 |
| 弹药库 | 旦药库 |
| 核弹 | 核旦 |
| 炮弹 | 炮旦 |

### 觉 jué (TTS often reads jiào)

| Original | Replacement |
|----------|-------------|
| 觉得 | 决得 |
| 感觉 | 感决 |
| 自觉 | 自决 |
| 发觉 | 发决 |
| 察觉 | 察决 |
| 觉悟 | 决悟 |
| 觉醒 | 决醒 |
| 知觉 | 知决 |
| 幻觉 | 幻决 |
| 错觉 | 错决 |
| 听觉 | 听决 |
| 视觉 | 视决 |
| 嗅觉 | 嗅决 |
| 触觉 | 触决 |

### 行 háng (TTS often reads xíng)

| Original | Replacement |
|----------|-------------|
| 银行 | 银航 |
| 行列 | 航列 |
| 行数 | 航数 |
| 排行 | 排航 |
| 内行 | 内航 |
| 一行 | 一航 |
| 多行 | 多航 |
| 单行 | 单航 |
| 行距 | 航距 |
| 行情 | 航情 |
| 商行 | 商航 |
| 洋行 | 洋航 |

### 没 méi (TTS often reads mò)

| Original | Replacement |
|----------|-------------|
| 没有 | 梅有 |
| 没用 | 梅用 |
| 没关系 | 梅关系 |
| 没什么 | 梅什么 |
| 没准 | 梅准 |
| 没人 | 梅人 |
| 没想 | 梅想 |
| 没钱 | 梅钱 |
| 没事 | 梅事 |
| 没看 | 梅看 |
| 没听 | 梅听 |
| 没做 | 梅做 |
| 没说 | 梅说 |
| 没去 | 梅去 |
| 没来 | 梅来 |
| 没完 | 梅完 |
| 没找 | 梅找 |

### 率 lǜ (TTS often reads shuài/lù)

| Original | Replacement |
|----------|-------------|
| 概率 | 概绿 |
| 效率 | 效绿 |
| 频率 | 频绿 |
| 速率 | 速绿 |
| 比率 | 比绿 |
| 利率 | 利绿 |
| 功率 | 功绿 |
| 命中率 | 命中绿 |
| 成功率 | 成功绿 |
| 覆盖率 | 覆盖绿 |
| 使用率 | 使用绿 |
| 增长率 | 增长绿 |

### 朝 cháo (TTS often reads zhāo)

| Original | Replacement |
|----------|-------------|
| 朝阳 | 潮阳 |
| 朝代 | 潮代 |
| 朝廷 | 潮廷 |
| 朝向 | 潮向 |
| 朝圣 | 潮圣 |
| 朝拜 | 潮拜 |
| 朝政 | 潮政 |
| 南朝 | 南潮 |
| 北朝 | 北潮 |
| 隋朝 | 隋潮 |
| 唐朝 | 唐潮 |
| 宋朝 | 宋潮 |
| 明朝 | 明潮 |
| 清朝 | 清潮 |

### 其他常见多音字

| Original | Replacement | Pronunciation |
|----------|-------------|---------------|
| 似的 | 是地 | shì de |
| 给予 | 几予 | jǐ yǔ |
| 便宜 | 骈宜 | pián yi |
| 削弱 | 薛弱 | xuē ruò |
| 削减 | 薛减 | xuē jiǎn |
| 剥削 | 剥薛 | bō xuē |
| 奇数 | 畸数 | jī shù |
| 外壳 | 外柯 | ké |
| 蛋壳 | 蛋柯 | ké |
| 贝壳 | 贝柯 | ké |
| 帖子 | 铁子 | tiě zi |
| 请帖 | 请铁 | tiě |
| 勉强 | 免抢 | miǎn qiǎng |
| 强迫 | 抢迫 | qiǎng pò |
| 暴露 | 暴路 | bào lù |
| 揭露 | 揭路 | jiē lù |
| 堵塞 | 堵色 | dǔ sè |
| 闭塞 | 闭色 | bì sè |
| 冠军 | 灌军 | guàn jūn |
| 下载 | 下在 | xià zài |
| 加载 | 加在 | jiā zài |
| 承载 | 承在 | chéng zài |
| 满载 | 满在 | mǎn zài |
| 出差 | 出拆 | chū chāi |
| 头发 | 头法 | tóu fà |
| 理发 | 理法 | lǐ fà |
| 创伤 | 窗伤 | chuāng shāng |
| 着重 | 浊重 | zhuó zhòng |
| 着手 | 浊手 | zhuó shǒu |
| 着眼 | 浊眼 | zhuó yǎn |
| 参差 | 岑疵 | cēn cī |
| 起哄 | 起洪 | qǐ hòng |

## Number Conversion

### Years

Digit-by-digit reading, not as a full number.

```
2024年 → 二零二四年
1999年 → 一九九九年
```

### Percentages

Read the number, then "百分之".

```
15% → 十五百分之
98.5% → 九八点五百分之
100% → 一百百分之
```

### Decimals

Read integer part digit-by-digit (or as full number if <100), "点", then decimal part digit-by-digit.

```
3.14 → 三点一四
0.618 → 零点六一八
100.5 → 一百点五
```

### Version Numbers

"版本" prefix, each number segment read digit-by-digit, joined by "点".

```
v2.0.1 → 版本二点零点一
v10.3.5 → 版本一零点三点五
```

## Punctuation Normalization

### English → Chinese Punctuation

For Chinese-dominant text, convert English punctuation to Chinese:

| English | Chinese |
|---------|---------|
| `,` | `，` |
| `?` | `？` |
| `!` | `！` |
| `;` | `；` |

Note: Don't convert colons that appear in URLs, time (12:30), or code (`::`).

### Collapse Repeated Punctuation

```
。。。 → 。
，，， → ，
、、、 → 、
```

### Strip HTML Tags

Remove any `<tag>` markup. Keep the text content.

## Sentence Breaking

Break long text into sentences for TTS engines that have length limits.

**Break on:**
- `。` `！` `？` followed by non-punctuation content
- `；` when the resulting segments are still too long

**Don't break on:**
- Quoted content mid-sentence: 「...」or "..." 内部不断
- Number ranges: 1-10, 2024-2025
- Abbreviations with dots: U.S.A., v.s.

**Target sentence length:** 30-60 characters per segment for optimal TTS quality.

## Tech Abbreviation Expansion

Expand English tech abbreviations by spelling out each letter with spaces. Match case-insensitively, longest first.

| Abbreviation | Expansion |
|-------------|-----------|
| HTTP | H T T P |
| HTTPS | H T T P S |
| API | A P I |
| SDK | S D K |
| JSON | J S O N |
| HTML | H T M L |
| CSS | C S S |
| SQL | S Q L |
| LLM | L L M |
| GPU | G P U |
| CPU | C P U |
| AI | A I |
| ML | M L |
| URL | U R L |
| SSH | S S H |
| VPN | V P N |
| DNS | D N S |
| CDN | C D N |
| JWT | J W T |
| REST | R E S T |
| gRPC | g R P C |
| GraphQL | Graph Q L |
| NoSQL | No S Q L |
| CI/CD | C I C D |
| K8s | K eight S |
| i18n | i eighteen n |
| OAuth | O Auth |
| SaaS | S a a S |

Full list contains ~100 abbreviations. See `tts_preprocess.py` (in tts-chef-core skill directory) for the complete `ABBREVIATION_MAP`.

## Agent Guidelines

- **MUST invoke `tts_preprocess.py`** (from tts-chef-core skill directory) to perform preprocessing. Do NOT apply these rules manually — the script implements them all.
- Run **tts-chef-core** pipeline first, then apply this skill
- Apply polyphone replacement **after** all other text transformations
- For mixed Chinese/English text, apply Chinese rules to Chinese segments only
- Different TTS engines may need different polyphone tables — the user can provide a custom rules JSON file

## Do Not

- ❌ Convert English words to Chinese phonetic equivalents (e.g. GitHub→吉特哈布, Python→派森). Always leave English words as-is — the TTS engine is responsible for pronouncing them.
