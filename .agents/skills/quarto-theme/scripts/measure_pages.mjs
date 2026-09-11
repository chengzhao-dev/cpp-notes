// measure_pages.mjs —— 从渲染产物里量出排版密度相关指标，交给 check_typography.py 断言。
//
// 为什么单独一个脚本：CSSOM 与 DOM 都只在浏览器里才有最终答案（grid 压缩、
// 同特异规则覆盖、CJK 折行点），源文件读得再细也测不出来。
//
// 三个口径决定断言是否可信，都在这里有唯一出处：
//   盒子   = 代码块 / 表格 / 提示框 / 引用块 / 图表容器，且只算最外层；
//   文字带 = 盒子之外的 p 与 li，即「纯文字落点带」，段/盒比用它做分子；
//   节     = 正文的直接子 section（一个 ## 一节），### 的盒子归父节，不重复计数。
//
// 用法：node measure_pages.mjs --book-dir _book --out out.json [--shots-dir DIR]
// 依赖：Playwright（NODE_PATH 指向自带 playwright 的 node_modules）与系统 Edge。
// 退出码：0 = 测量成功；2 = 运行时不可用或页面打不开（调用方据此判定 SKIP）。

import { mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const argv = process.argv.slice(2);
function flag(name, fallback) {
  const i = argv.indexOf(name);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : fallback;
}

const bookDir = resolve(flag("--book-dir", "_book"));
const outFile = flag("--out", "");
const shotsDir = flag("--shots-dir", "");
// 1280 是主目标视口，1100 是次目标（侧栏仍可见的最窄档）
const viewports = [1280, 1100];
const pages = [
  { id: "setup", file: "content/getting-started/setup-wsl2.html" },
  { id: "first-program", file: "content/getting-started/first-program.html" },
];

const PAGES = pages.map((p) => ({ ...p, path: resolve(bookDir, p.file) }));

async function collect(page) {
  return await page.evaluate(() => {
    const root = document.querySelector("#quarto-document-content");
    const px = (v) => parseFloat(v) || 0;
    const cs = (el) => getComputedStyle(el);

    const languageBlocks = [...root.querySelectorAll("div.sourceCode")].map((div) => {
      const pre = div.querySelector("pre");
      const code = div.querySelector("pre > code");
      const preStyle = pre ? cs(pre) : null;
      const codeStyle = code ? cs(code) : null;
      return {
        divBorderWidth: px(cs(div).borderTopWidth),
        preBorderWidth: preStyle ? px(preStyle.borderTopWidth) : null,
        codeWhiteSpace: codeStyle ? codeStyle.whiteSpace : null,
        text: (pre ? pre.textContent : div.textContent).replace(/\s+$/, ""),
      };
    });

    const barePres = [...root.querySelectorAll("pre")].filter(
      (pre) => !pre.closest("div.sourceCode") && !pre.classList.contains("mermaid-js"),
    ).map((pre) => ({
      preBorderWidth: px(cs(pre).borderTopWidth),
      codeWhiteSpace: pre.querySelector("code") ? cs(pre.querySelector("code")).whiteSpace : null,
      scrollWidth: pre.scrollWidth,
      clientWidth: pre.clientWidth,
      text: pre.textContent.replace(/\s+$/, ""),
    }));

    // 正文列宽：Quarto 把每个 ## 包进 <section>，直接子元素只有引言段，
    // 因此量全部段落（同一列，宽度一致），取最大值作为该页正文列宽。
    const paragraphs = [...root.querySelectorAll(":scope > p, :scope > section > p")];
    const paraWidths = paragraphs.map((p) => p.clientWidth);

    // 盒子：有外框的语言代码、表格、提示框、引用块和图表容器。目录树与
    // 独立 text 输出块不计入密度：它们表达结构或结果，没有语言块的外框层级。
    const boxSel = "div.sourceCode, table, .callout, blockquote, .cell";
    // 只保留最外层：代码块的 pre 与 div.sourceCode 同盒，.cell 内层还有 pre/div。
    // 注意不能用 el.closest(".cell")，closest 会把元素自己算进去。
    const matched = [...root.querySelectorAll(boxSel)];
    const candidate = new Set(matched);
    const boxes = matched.filter((el) => {
      for (let a = el.parentElement; a && a !== root; a = a.parentElement) {
        if (candidate.has(a)) return false;
      }
      return true;
    });
    const boxType = (el) => {
      if (el.matches(".cell")) return "chart";
      if (el.matches("div.sourceCode")) return "code";
      if (el.tagName === "TABLE") return "table";
      return el.classList.contains("callout") ? "callout" : "quote";
    };
    const boxSeq = boxes.map(boxType);

    // 盒子归属的顶层 ## 节：从盒子向上走到 root 的直接子节点
    const topSectionOf = (el) => {
      let node = el;
      while (node && node.parentElement && node.parentElement !== root) {
        node = node.parentElement;
      }
      return node && node.parentElement === root ? node : null;
    };
    const titleOf = (sec) => {
      if (!sec) return "(引言)";
      const h = sec.matches("section") ? sec.querySelector("h2, h3") : null;
      return (h ? h.textContent : "").trim() || "(引言)";
    };

    // 文字带：盒子之外的 p 与 li（列表项是可扫读的正文落点，不是盒子）
    const bands = [...root.querySelectorAll("p, li")].filter((el) => !el.closest(boxSel));

    // 段/盒比例按「同一节内的兄弟序列」统计，避免 section 嵌套重复计数
    let consecutive = 0;
    {
      const isBox = new Set(boxes);
      const isBand = new Set(bands);
      const groups = new Map();
      // 文档顺序遍历，盒子内部的所有文字（isBand 与 isBox 都不成立）直接跳过
      [...root.querySelectorAll(boxSel + ", p, li")].forEach((el) => {
        const kind = isBox.has(el) ? "box" : isBand.has(el) ? "band" : "";
        if (!kind) return;
        const key = titleOf(topSectionOf(el));
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key).push(kind);
      });
      for (const tags of groups.values()) {
        for (let i = 1; i < tags.length; i += 1) {
          if (tags[i] === "box" && tags[i - 1] === "box") consecutive += 1;
        }
      }
    }

    // 单个 ## 内盒子数（### 归父节）
    const sectionOrder = [...root.children].filter((el) => el.tagName === "SECTION");
    const boxesPerSection = sectionOrder.map((sec) => ({
      title: titleOf(sec),
      boxes: boxes.filter((el) => topSectionOf(el) === sec).length,
      bands: bands.filter((el) => topSectionOf(el) === sec).length,
      height: Math.round(sec.getBoundingClientRect().height),
    }));

    const tocItems = [...document.querySelectorAll('nav[role="doc-toc"] a.nav-link')].map((a) => ({
      text: a.textContent.trim(),
      height: Math.round(a.getBoundingClientRect().height),
    }));

    // 横向溢出：只扫正文与两个侧栏，页面根节点在窄栏下必然溢出（滚动条本身）
    const overflow = [];
    const scanRoots = [
      root,
      document.querySelector("#quarto-sidebar"),
      document.querySelector(".page-columns"),
    ];
    const seen = new Set();
    scanRoots.forEach((scope) => {
      if (!scope) return;
      scope.querySelectorAll("*").forEach((el) => {
        if (seen.has(el) || !el.clientWidth) return;
        seen.add(el);
        if (el.scrollWidth > el.clientWidth + 1) {
          const style = cs(el);
          const scrolls = style.overflowX === "auto" || style.overflowX === "scroll";
          overflow.push({
            tag: el.tagName.toLowerCase(),
            classes: typeof el.className === "string" ? el.className.trim().slice(0, 60) : "",
            scrollWidth: el.scrollWidth,
            clientWidth: el.clientWidth,
            scrolls,
            inPre: Boolean(el.closest("pre")),
          });
        }
      });
    });

    return {
      contentHeight: Math.round(root.getBoundingClientRect().height),
      paragraphWidth: paraWidths.length ? Math.max(...paraWidths) : 0,
      paragraphWidths: paraWidths.map((w) => Math.round(w)),
      paragraphCount: paragraphs.length,
      textBandCount: bands.length,
      boxCount: boxes.length,
      boxTypes: boxSeq,
      boxes: boxes.map((el) => {
        const pre = el.querySelector("pre");
        return {
          type: boxType(el),
          height: Math.round(el.getBoundingClientRect().height),
          lines: pre ? pre.textContent.replace(/\s+$/, "").split("\n").length : 0,
          section: titleOf(topSectionOf(el)),
        };
      }),
      consecutiveBoxes: consecutive,
      boxesPerSection,
      languageBlocks,
      barePres,
      tocItems,
      overflow,
      sidebarWidth: Math.round(
        (document.querySelector("#quarto-sidebar") || { getBoundingClientRect: () => ({ width: 0 }) })
          .getBoundingClientRect().width,
      ),
    };
  });
}

async function loadPlaywright() {
  // ESM 的 import() 不查 NODE_PATH，因此显式用 CJS 解析器找 playwright：
  // NODE_PATH（自带 runtime 的 node_modules）→ 脚本同级 node_modules。
  const { createRequire } = await import("node:module");
  const req = createRequire(import.meta.url);
  try {
    return req("playwright");
  } catch (err) {
    const { existsSync } = await import("node:fs");
    const { delimiter, join } = await import("node:path");
    for (const dir of (process.env.NODE_PATH || "").split(delimiter).filter(Boolean)) {
      const candidate = join(dir, "playwright", "index.js");
      if (existsSync(candidate)) return req(candidate);
    }
    throw err;
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  const { chromium } = await loadPlaywright();
  const browser = await chromium.launch({ channel: "msedge" });
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const result = { viewports: {} };
  await context.close();

  for (const width of viewports) {
    const ctx = await browser.newContext({ viewport: { width, height: 900 } });
    result.viewports[width] = {};
    for (const p of PAGES) {
      const page = await ctx.newPage();
      await page.goto(pathToFileURL(p.path).href, { waitUntil: "networkidle" });
      // 等 Mermaid 渲染完，避免把未替换的占位块算成空盒子
      await sleep(800);
      const data = await collect(page);
      result.viewports[width][p.id] = data;
      if (shotsDir) {
        await mkdir(shotsDir, { recursive: true });
        await page.screenshot({
          path: resolve(shotsDir, `${p.id}-${width}-1.png`),
          clip: { x: 0, y: 0, width, height: 900 },
        });
        const total = Math.min(
          (await page.evaluate(() => document.body.scrollHeight)) - 900,
          data.contentHeight,
        );
        for (let i = 1; i <= 3; i += 1) {
          await page.evaluate((y) => window.scrollTo(0, y), (total / 4) * i);
          await sleep(150);
          await page.screenshot({
            path: resolve(shotsDir, `${p.id}-${width}-${i + 1}.png`),
            clip: { x: 0, y: 0, width, height: 900 },
          });
        }
      }
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();

  const json = JSON.stringify(result);
  if (outFile) {
    await writeFile(resolve(outFile), json, "utf8");
    console.log(`OK measure wrote ${resolve(outFile)} (${json.length} bytes)`);
  } else {
    console.log(json);
  }
}

main().catch((err) => {
  console.error("MEASURE-FAILED " + (err && err.message ? err.message : String(err)));
  process.exit(2);
});
