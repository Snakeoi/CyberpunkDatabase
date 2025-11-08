<script setup>
import {onMounted, ref} from "vue";
import {readResource} from "@/assets/utils/axios/crud.js";

const documents = ref([]);
const selectedSlug = ref(null);
const htmlContent = ref("");
const isLoading = ref(false);
const loadError = ref(null);

const convertMarkdownToHtml = (markdown = "") => {
  const escapeHtml = (value) =>
    value
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");

  const escapeAttribute = (value) => escapeHtml(value).replaceAll("`", "&#96;");

  const sanitizeUrl = (value) => {
    const trimmed = value.trim();
    if (!trimmed) {
      return "#";
    }
    const lower = trimmed.toLowerCase();
    if (lower.startsWith("javascript:") || lower.startsWith("data:")) {
      return "#";
    }
    return trimmed;
  };

  const applyInlineFormatting = (value, options = {}) => {
    const { allowLinks = true } = options;
    if (!value) {
      return "";
    }

    const codePlaceholders = [];
    const imagePlaceholders = [];
    const linkPlaceholders = [];

    let working = value.replace(/`([^`]+)`/g, (_, code) => {
      const placeholder = `__CODE_${codePlaceholders.length}__`;
      codePlaceholders.push(`<code>${escapeHtml(code)}</code>`);
      return placeholder;
    });

    working = working.replace(/!\[([^\]]*)]\(([^)]+)\)/g, (_, alt, url) => {
      const placeholder = `__IMAGE_${imagePlaceholders.length}__`;
      imagePlaceholders.push(
        `<img src="${escapeAttribute(sanitizeUrl(url))}" alt="${escapeAttribute(alt)}" />`
      );
      return placeholder;
    });

    if (allowLinks) {
      working = working.replace(/\[([^\]]+)]\(([^)]+)\)/g, (_, text, url) => {
        const placeholder = `__LINK_${linkPlaceholders.length}__`;
        linkPlaceholders.push(
          `<a href="${escapeAttribute(sanitizeUrl(url))}" target="_blank" rel="noopener">${applyInlineFormatting(text, { allowLinks: false })}</a>`
        );
        return placeholder;
      });
    }

    working = escapeHtml(working);

    working = working.replace(/~~(.+?)~~/g, "<del>$1</del>");
    working = working.replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>");
    working = working.replace(/___(.+?)___/g, "<strong><em>$1</em></strong>");
    working = working.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    working = working.replace(/__(.+?)__/g, "<strong>$1</strong>");
    working = working.replace(/\*(.+?)\*/g, "<em>$1</em>");
    working = working.replace(/_(.+?)_/g, "<em>$1</em>");

    codePlaceholders.forEach((html, index) => {
      working = working.replace(`__CODE_${index}__`, html);
    });
    imagePlaceholders.forEach((html, index) => {
      working = working.replace(`__IMAGE_${index}__`, html);
    });
    linkPlaceholders.forEach((html, index) => {
      working = working.replace(`__LINK_${index}__`, html);
    });

    return working;
  };

  const splitTableRow = (line) =>
    line
      .trim()
      .replace(/^\|/, "")
      .replace(/\|$/, "")
      .split("|")
      .map((cell) => applyInlineFormatting(cell.trim()));

  const parseTableAlignment = (line) =>
    line
      .trim()
      .replace(/^\|/, "")
      .replace(/\|$/, "")
      .split("|")
      .map((cell) => {
        const trimmed = cell.trim();
        const startsWithColon = trimmed.startsWith(":");
        const endsWithColon = trimmed.endsWith(":");
        if (startsWithColon && endsWithColon) {
          return "center";
        }
        if (startsWithColon) {
          return "left";
        }
        if (endsWithColon) {
          return "right";
        }
        return null;
      });

  const isTableDivider = (line) => {
    const trimmed = line.trim();
    if (!trimmed) {
      return false;
    }
    const normalized = trimmed
      .replace(/^\|/, "")
      .replace(/\|$/, "")
      .split("|");
    return (
      normalized.length > 0 &&
      normalized.every((cell) => /^\s*:?-{3,}:?\s*$/.test(cell))
    );
  };

  const isTableRow = (line) => {
    const trimmed = line.trim();
    if (!trimmed.includes("|")) {
      return false;
    }
    const stripped = trimmed.replace(/^\|/, "").replace(/\|$/, "");
    return stripped.split("|").length > 1;
  };

  const tryParseTable = (lines, startIndex) => {
    if (startIndex + 1 >= lines.length) {
      return null;
    }
    const headerLine = lines[startIndex];
    const dividerLine = lines[startIndex + 1];
    if (!isTableRow(headerLine) || !isTableDivider(dividerLine)) {
      return null;
    }

    const headerCells = splitTableRow(headerLine);
    const alignments = parseTableAlignment(dividerLine);
    const bodyRows = [];
    let currentIndex = startIndex + 2;

    while (currentIndex < lines.length && isTableRow(lines[currentIndex])) {
      bodyRows.push(splitTableRow(lines[currentIndex]));
      currentIndex += 1;
    }

    const buildRow = (cells, cellTag) =>
      cells
        .map((cell, index) => {
          const alignment = alignments[index] ?? null;
          const alignmentAttribute = alignment ? ` style="text-align: ${alignment};"` : "";
          return `<${cellTag}${alignmentAttribute}>${cell}</${cellTag}>`;
        })
        .join("");

    const headerHtml = `<thead><tr>${buildRow(headerCells, "th")}</tr></thead>`;
    const bodyHtml = bodyRows
      .map((row) => `<tr>${buildRow(row, "td")}</tr>`)
      .join("");

    return {
      html: `<table>${headerHtml}<tbody>${bodyHtml}</tbody></table>`,
      endIndex: currentIndex - 1,
    };
  };

  const lines = markdown.replace(/\r\n?/g, "\n").split("\n");
  const htmlLines = [];
  let inUnorderedList = false;
  let inOrderedList = false;
  let inBlockquote = false;
  let inCodeBlock = false;
  let codeBlockLanguage = "";
  let codeBlockBuffer = [];

  const closeLists = () => {
    if (inUnorderedList) {
      htmlLines.push("</ul>");
      inUnorderedList = false;
    }
    if (inOrderedList) {
      htmlLines.push("</ol>");
      inOrderedList = false;
    }
  };

  const closeBlockquote = () => {
    if (inBlockquote) {
      htmlLines.push("</blockquote>");
      inBlockquote = false;
    }
  };

  const flushCodeBlock = () => {
    if (!inCodeBlock) {
      return;
    }
    const languageClass = codeBlockLanguage
      ? ` class="language-${escapeAttribute(codeBlockLanguage)}"`
      : "";
    const content = escapeHtml(codeBlockBuffer.join("\n"));
    htmlLines.push(`<pre><code${languageClass}>${content}</code></pre>`);
    inCodeBlock = false;
    codeBlockLanguage = "";
    codeBlockBuffer = [];
  };

  for (let index = 0; index < lines.length; index += 1) {
    const rawLine = lines[index];
    const trimmed = rawLine.trim();

    if (/^```/.test(trimmed)) {
      if (inCodeBlock) {
        flushCodeBlock();
      } else {
        closeLists();
        closeBlockquote();
        inCodeBlock = true;
        codeBlockLanguage = trimmed.replace(/^```/, "").trim();
        codeBlockBuffer = [];
      }
      continue;
    }

    if (inCodeBlock) {
      codeBlockBuffer.push(rawLine);
      continue;
    }

    if (!trimmed) {
      flushCodeBlock();
      closeLists();
      closeBlockquote();
      continue;
    }

    if (/^(-{3,}|\*{3,}|_{3,})$/.test(trimmed.replace(/\s+/g, ""))) {
      closeLists();
      closeBlockquote();
      htmlLines.push("<hr />");
      continue;
    }

    if (trimmed.startsWith(">")) {
      closeLists();
      if (!inBlockquote) {
        htmlLines.push("<blockquote>");
        inBlockquote = true;
      }
      const content = trimmed.replace(/^>\s?/, "");
      htmlLines.push(`<p>${applyInlineFormatting(content)}</p>`);
      continue;
    }

    closeBlockquote();

    const table = tryParseTable(lines, index);
    if (table) {
      closeLists();
      htmlLines.push(table.html);
      index = table.endIndex;
      continue;
    }

    if (trimmed.startsWith("### ")) {
      closeLists();
      htmlLines.push(`<h3>${applyInlineFormatting(trimmed.slice(4))}</h3>`);
      continue;
    }

    if (trimmed.startsWith("## ")) {
      closeLists();
      htmlLines.push(`<h2>${applyInlineFormatting(trimmed.slice(3))}</h2>`);
      continue;
    }

    if (trimmed.startsWith("# ")) {
      closeLists();
      htmlLines.push(`<h1>${applyInlineFormatting(trimmed.slice(2))}</h1>`);
      continue;
    }

    if (/^(\*|\+|-)\s+/.test(trimmed)) {
      if (!inUnorderedList) {
        closeLists();
        htmlLines.push("<ul>");
        inUnorderedList = true;
      }
      const content = trimmed.replace(/^(\*|\+|-)\s+/, "");
      htmlLines.push(`<li>${applyInlineFormatting(content)}</li>`);
      continue;
    }

    if (/^\d+\.\s+/.test(trimmed)) {
      if (!inOrderedList) {
        closeLists();
        htmlLines.push("<ol>");
        inOrderedList = true;
      }
      const content = trimmed.replace(/^\d+\.\s+/, "");
      htmlLines.push(`<li>${applyInlineFormatting(content)}</li>`);
      continue;
    }

    closeLists();
    htmlLines.push(`<p>${applyInlineFormatting(trimmed)}</p>`);
  }

  flushCodeBlock();
  closeLists();
  closeBlockquote();

  return htmlLines.join("\n");
};

const loadDocuments = async () => {
  loadError.value = null;
  try {
    const response = await readResource("/docs/");
    documents.value = response.data;
    if (documents.value.length > 0 && !selectedSlug.value) {
      await loadDocument(documents.value[0].slug);
    }
  } catch (error) {
    loadError.value = "Nie udało się pobrać listy dokumentów.";
  }
};

const loadDocument = async (slug) => {
  loadError.value = null;
  isLoading.value = true;
  try {
    selectedSlug.value = slug;
    const response = await readResource(`/docs/${slug}`);
    htmlContent.value = convertMarkdownToHtml(response.data.content ?? "");
  } catch (error) {
    loadError.value = "Nie udało się pobrać treści dokumentu.";
    htmlContent.value = "";
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadDocuments();
});
</script>

<template>
  <section>
    <div class="columns is-multiline">
      <div class="column is-3-desktop is-12-tablet">
        <aside class="menu">
          <p class="menu-label">
            Dokumenty
          </p>
          <ul class="menu-list">
            <li v-for="document in documents" :key="document.slug">
              <a
                  :class="{'is-active': selectedSlug === document.slug}"
                  @click.prevent="loadDocument(document.slug)"
                  href="#"
              >
                {{ document.title }}
              </a>
            </li>
          </ul>
        </aside>
      </div>
      <div class="column is-9-desktop is-12-tablet">
        <div v-if="loadError" class="notification is-danger">
          {{ loadError }}
        </div>
        <div v-else-if="isLoading" class="has-text-centered">
          Ładowanie...
        </div>
        <article v-else class="content" v-html="htmlContent" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.menu-list a.is-active {
  background-color: #485fc7;
  color: white;
}

.menu-list a {
  display: block;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  transition: background-color 0.15s ease-in-out;
}

.menu-list a:hover {
  background-color: rgba(72, 95, 199, 0.15);
}
</style>
