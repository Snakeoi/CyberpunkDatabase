<script setup>
import {onMounted, ref} from "vue";
import {marked} from "marked";
import {readResource} from "@/assets/utils/axios/crud.js";

const documents = ref([]);
const selectedSlug = ref(null);
const htmlContent = ref("");
const isLoading = ref(false);
const loadError = ref(null);
const tocItems = ref([]);
const isTocVisible = ref(true);

const renderMarkdownWithToc = (markdown) => {
  const renderer = new marked.Renderer();
  const slugger = new marked.Slugger();
  const headings = [];

  renderer.heading = (text, level, raw) => {
    const headingText = (raw ?? text ?? "").toString();
    const plainText = headingText.replace(/<[^>]*>/g, "").trim();
    const slug = slugger.slug(plainText);

    headings.push({
      id: slug,
      text: plainText,
      level,
    });

    return `<h${level} id="${slug}">${text}</h${level}>`;
  };

  const html = marked.parse(markdown, {renderer});
  tocItems.value = headings;
  return html;
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
    const markdown = response.data.content ?? "";
    htmlContent.value = renderMarkdownWithToc(markdown);
  } catch (error) {
    loadError.value = "Nie udało się pobrać treści dokumentu.";
    htmlContent.value = "";
    tocItems.value = [];
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadDocuments();
});
</script>

<template>
  <section class="docs-section">
    <div class="columns is-multiline">
      <div class="column is-12-tablet is-3-desktop">
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
      <div class="column is-12-tablet" :class="{'is-6-desktop': isTocVisible, 'is-9-desktop': !isTocVisible}">
        <div class="content-header">
          <button
              class="button is-small is-light"
              type="button"
              @click="isTocVisible = !isTocVisible"
          >
            {{ isTocVisible ? 'Ukryj spis treści' : 'Pokaż spis treści' }}
          </button>
        </div>
        <div v-if="loadError" class="notification is-danger">
          {{ loadError }}
        </div>
        <div v-else-if="isLoading" class="has-text-centered">
          Ładowanie...
        </div>
        <article v-else class="content" v-html="htmlContent" />
      </div>
      <div
          v-if="isTocVisible"
          class="column is-12-tablet is-3-desktop"
      >
        <div class="toc-container">
          <div class="toc-header">
            <h2 class="toc-title">Spis treści</h2>
          </div>
          <nav v-if="tocItems.length" class="toc-list">
            <a
                v-for="item in tocItems"
                :key="item.id"
                class="toc-link"
                :href="`#${item.id}`"
                :style="{paddingLeft: `${(item.level - 1) * 12}px`}"
            >
              {{ item.text }}
            </a>
          </nav>
          <p v-else class="toc-empty">Brak nagłówków w dokumencie.</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.docs-section {
  padding-bottom: 2rem;
}

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

.content-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.toc-container {
  position: sticky;
  top: 1rem;
  max-height: calc(100vh - 2rem);
  padding: 1rem;
  border: 1px solid #dbdbdb;
  border-radius: 8px;
  overflow-y: auto;
  background-color: white;
}

.toc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.toc-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.toc-link {
  color: #4a4a4a;
  text-decoration: none;
  padding: 0.25rem 0;
  border-radius: 4px;
  transition: background-color 0.15s ease-in-out;
}

.toc-link:hover {
  background-color: rgba(72, 95, 199, 0.1);
}

.toc-empty {
  font-size: 0.875rem;
  color: #7a7a7a;
  margin: 0;
}

@media screen and (max-width: 1023px) {
  .content-header {
    justify-content: flex-start;
  }

  .toc-container {
    position: relative;
    top: auto;
    max-height: none;
  }
}
</style>
