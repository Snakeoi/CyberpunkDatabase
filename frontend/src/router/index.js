import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/views/HomeView.vue";
import NotFound from "@/views/NotFound.vue";
import CharacterIndexView from "@/views/Character/CharacterIndexView.vue";
import CharacterCreateView from "@/views/Character/CharacterCreateView.vue";
import CharacterDetailView from "@/views/Character/CharacterDetail/CharacterDetailView.vue";
import SkillCreateView from "@/views/Abilities/SkillCreateView.vue";
import SkillDetailView from "@/views/Abilities/SkillDetailView.vue";
import SkillIndexView from "@/views/Abilities/SkillIndexView.vue";
import CharacterGenerateView from "@/views/Character/CharacterGenerateView.vue";
import CharacterPrintableView from "@/views/Character/CharacterPrintableView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/:catchAll(.*)',
      component: NotFound
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
      ]
    },
  ]
})

export default router
