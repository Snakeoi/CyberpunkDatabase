<script setup>
import {onMounted, ref} from "vue";
import {marked} from "marked";
import {readResource} from "@/assets/utils/axios/crud.js";

const documents = ref([]);
const selectedSlug = ref(null);
const htmlContent = ref("");
const isLoading = ref(false);
const loadError = ref(null);

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
    htmlContent.value = marked.parse(response.data.content ?? "");
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
