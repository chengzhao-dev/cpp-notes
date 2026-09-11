## 中文措辞审校路由
本文件只定义适用范围。项目常用替换词、冗余表达、过度承诺和中文技术文档的反例归知识库维护。

润色阶段运行 `python .agents/skills/agent-ops/scripts/run.py kb-search "中文技术文档 措辞替换" --domain quarto-docs`。

## 中文段落与句式路由
本文件只定义适用范围。中文段落的连接关系、长句拆分、术语节奏、代码块前后闭环和多文件复核属于项目知识库案例。

遇到段落跳跃、术语密集、命令解释不闭环或多页面重复时，运行 `python .agents/skills/agent-ops/scripts/run.py kb-search "中文段落衔接 代码块闭环" --domain quarto-docs`。

导语、过渡句或目录树邻接文字显得生硬时，先区分读者引导和作者维护说明，再检索自然句式案例；运行 `python .agents/skills/agent-ops/scripts/run.py kb-search "导语动作链 自然衔接 维护说明" --domain quarto-docs`。
