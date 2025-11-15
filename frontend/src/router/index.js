import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/views/HomeView.vue";
import NotFound from "@/views/NotFound.vue";
import CharacterIndexView from "@/views/Character/CharacterIndexView.vue";
import CharacterCreateView from "@/views/Character/CharacterCreateView.vue";
import CharacterDetailView from "@/views/Character/CharacterDetail/CharacterDetailView.vue";
import SkillCreateView from "@/views/Skills/SkillCreateView.vue";
import SkillDetailView from "@/views/Skills/SkillDetailView.vue";
import SkillIndexView from "@/views/Skills/SkillIndexView.vue";
import CharacterGenerateView from "@/views/Character/CharacterGenerateView.vue";
import CharacterPrintableView from "@/views/Character/CharacterPrintableView.vue";
import DocsIndexView from "@/views/Docs/DocsIndexView.vue";
import AdminView from "@/views/Admin/AdminView.vue";
import UsersView from "@/views/Admin/Users/UsersView.vue";
import UserView from "@/views/Admin/Users/UserView.vue";
import UserViewCreate from "@/views/Admin/Users/UserViewCreate.vue";
import AdminForbiddenView from "@/views/Admin/AdminForbiddenView.vue";
import {useUserStore} from "@/stores/user.js";

const routes = [
  {
    path: '/Admin',
    name: 'admin-dashboard',
    component: AdminView,
    meta: { requiresAdmin: true },
    children: [
      {
        path: 'users',
        name: 'admin-users',
        component: UsersView,
      },
      {
        path: 'user/:id(\\d+)',
        name: 'admin-user',
        component: UserView,
      },
      {
        path: 'user/',
        name: 'admin-user-add',
        component: UserViewCreate,
      }
    ]
  },
  {
    path: '/Admin/forbidden',
    name: 'admin-forbidden',
    component: AdminForbiddenView,
  },
  {
    path: '/character/print/:id(\\d+)',
    name: 'character-print',
    component: CharacterPrintableView,
  },
  {
    path: '/',
    name: 'home',
    component: HomeView,
    children: [
      {
        path: 'character',
        name: 'character-index',
        component: CharacterIndexView,
      },
      {
        path: '/character/:id(\\d+)',
        name: 'character-detail',
        component: CharacterDetailView,
      },
      {
        path: '/character/new',
        name: 'character-add',
        component: CharacterCreateView,
      },
      {
        path: '/character/generate',
        name: 'character-generate',
        component: CharacterGenerateView,
      },
      {
        path: 'skill',
        name: 'skill-index',
        component: SkillIndexView,
      },
      {
        path: 'skill/:id(\\d+)',
        name: 'skill-detail',
        component: SkillDetailView,
      },
      {
        path: 'skill/new/',
        name: 'skill-add',
        component: SkillCreateView,
      },
      {
        path: 'docs',
        name: 'docs-index',
        component: DocsIndexView,
      },
    ]
  },
  // catchAll powinien być na końcu
  {
    path: '/:catchAll(.*)',
    component: NotFound
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

router.beforeEach(async (to, from, next) => {
  const user = useUserStore();

  if (to.meta?.requiresAdmin) {
    // jeśli brak danych — pobierz; jeśli trwa już ładowanie, poczekaj
    if (user.data == null) {
      if (!user.loading) {
        try {
          await user.fetchUserData();
        } catch (e) {
          // traktuj jak brak uprawnień
        }
      } else {
        // poczekaj aż loading się zakończy
        while (user.loading) {
          await sleep(50);
        }
      }
    }

    // bezpieczny odczyt computed/ref
    const isAdmin = !!(user.isAdmin?.value ?? user.isAdmin);

    if (!isAdmin) {
      return next({ name: 'admin-forbidden' });
    }
  }

  next();
});

export default router
