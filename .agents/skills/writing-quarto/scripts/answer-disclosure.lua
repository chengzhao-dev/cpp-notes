-- 将正文里的 .answer fenced div 渲染为默认收起的原生答案块。
local function answer_disclosure(div)
  if not div.classes:includes("answer") then
    return nil
  end

  local blocks = {
    pandoc.RawBlock("html", '<details class="answer-disclosure">'),
    pandoc.RawBlock("html", "<summary>查看答案</summary>"),
  }

  for _, block in ipairs(div.content) do
    blocks[#blocks + 1] = block
  end

  blocks[#blocks + 1] = pandoc.RawBlock("html", "</details>")
  return blocks
end

return {
  Div = answer_disclosure,
}
