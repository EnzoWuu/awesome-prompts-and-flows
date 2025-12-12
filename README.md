# Awesome Prompts and Flows 🌟  
[English Version](README_EN.md)

一个跨平台的 **真实 AI 示例集合**，覆盖：

**LLM · NanoBanana · ComfyUI · Dify · Coze · LibLib**

本仓库中的每个示例包含：

- `input.xxx`（示例输入）  
- `output.xxx`（模型真实输出）  
- `prompt.txt` 或 `flow.json` 或 `code.py`（核心逻辑）  
- `readme.md`（说明文档）  

全部内容皆可复现，真实有效，无套路。

---

## 📁 仓库结构（平台 → 示例）

```
awesome-prompts-and-flows/
│
├── gpt/
├── qwen/
├── nano-banana/
├── comfyui/
├── dify/
├── coze/
└── tools/
```

---

## 🗂️ 示例总览（自动生成）

下列内容由 `scripts/update_readme.py` 自动维护，请勿手动修改。

<!-- AUTO-GENERATED:START -->
| 模型（平台） | 说明 | 输入 | 输出 | Prompt | 文件夹 |
| --- | --- | --- | --- | --- | --- |
| Nano Banana<br><strong>照片 → 角色手办展示场景</strong> | 将真实人物照片转换为“角色手办 + 包装盒 + Blender”完整展示场景。 | 示例输入图（`input.png`）<br>![示例输入图](nano-banana/figure_creation_scene/input.png) | 生成效果（`output.jpg`）<br>![生成效果](nano-banana/figure_creation_scene/output.jpg) | [prompt.txt](nano-banana/figure_creation_scene/prompt.txt) | [文件夹](nano-banana/figure_creation_scene)<br>[README](nano-banana/figure_creation_scene/README.md) |
<!-- AUTO-GENERATED:END -->

---

## 🔍 示例目录标准（必须包含 4 项）

```
example-name/
  ├── input.xxx
  ├── output.xxx
  ├── prompt.txt   或 flow.json 或 code.py
  └── readme.md
```

---

## 📝 示例 readme.md 模板

```
# 示例名称

## 🧩 作用
一句话说明该示例能做什么。

---

## 📝 Prompt / Flow / Code
- Prompt 示例：`prompt.txt`
- 工作流示例：`flow.json`
- Python Agent 示例：`code.py`

---

## 📥 输入（input.xxx）
```
（粘贴示例输入内容）
```

---

## 📤 输出（output.xxx）
```
（粘贴示例输出）
```

---

## 💡 使用说明
- 推荐模型 / 工具  
- 使用方式  
- 注意事项  

---

## 📂 文件说明
- input.xxx：示例输入  
- output.xxx：模型真实输出  
- prompt.txt / flow.json / code.py：核心逻辑  
- readme.md：说明文档
```

---

## 🧾 metadata.json（可选但推荐）

若需在首页示例总览中展示多输入/输出、视频或自定义图片说明，可在示例目录中添加 `metadata.json`：

```json
{
  "title": "示例名称（可覆盖 README）",
  "description": "一句话说明",
  "inputs": [
    { "file": "input.png", "label": "示例输入图", "type": "image" },
    { "file": "input.mp4", "label": "输入视频", "type": "video" }
  ],
  "outputs": [
    { "file": "output.jpg", "label": "生成结果", "type": "image" }
  ],
  "core": ["prompt.txt", "flow.json"]
}
```

字段说明：
- `title` / `description`：覆盖自动提取的标题与说明。
- `inputs` / `outputs`：数组元素可指定 `file`、`label`、`type=image|video|file`。
- `core`：核心 prompt/flow/code 文件数组，将在 README 中生成链接。

脚本优先读取 metadata，缺失字段会自动扫描文件名（input*/output*/prompt* 等）。

---

## 🤝 如何贡献

欢迎提交各种平台的真实示例：

- GPT / Qwen / Llama  
- ComfyUI JSON  
- Dify Flow  
- Coze Bot Flow  
- NanoBanana 示例  

**贡献规则：**

1. 顶层按平台分类  
2. 每个示例必须独立文件夹  
3. 必须包含 input / output / readme + prompt/flow/code  
4. 文件命名用小写 + 中横线  
5. 大文件放外链  

---

## 📅 Roadmap
- 每周新增示例  
- 支持更多平台（Sora / Claude / Runway / Grok）  
- 增加 Example Viewer  
- 增加搜索功能  
- 完整双语文档  

---

## 📄 License  
MIT License
