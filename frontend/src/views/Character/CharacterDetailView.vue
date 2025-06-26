<script setup>
import {createResource, deleteResource, readResource, updateResource} from "@/assets/utils/axios/crud.js";
import {computed, onBeforeMount, ref, watch} from "vue";
import {useRoute} from 'vue-router'
import Input from "@/components/form/Input.vue";
import ConditionalLoader from "@/components/loader/ConditionalLoader.vue";
import {useToasterStore} from "@/stores/toaster.js";
import CharacterNotes from "@/components/character/detail/CharacterNotes.vue";
import CharacterAbilities from "@/components/character/detail/CharacterAbilities.vue";
import CharacterSkills from "@/components/character/detail/CharacterSkills.vue";
import CharacterRoles from "@/components/character/detail/CharacterRoles.vue";
import CharacterPsychHealth from "@/components/character/detail/CharacterPsychHealth.vue";
import {sheetModes} from "@/enums.js";
import router from "@/router/index.js";
import Tabs from "@/components/Tabs/Tabs.vue";
import Tab from "@/components/Tabs/Tab.vue";
import { io } from "socket.io-client";

const toasterStore = useToasterStore();

const tabs = ref([
    {
      title: 'Notatki',
      icon: 'icon-sticky-note',

    },
    {
      title: 'Cechy i umiejętności',
      icon: 'icon-calculator',
    }
]);
const activeTab = ref(tabs.value[1]);


const route = useRoute();
const socket = io();
const isLoading = ref(true);
const showNotes = ref(false);

const character = ref({});
const characterOriginal = ref({});
const characterNotes = ref('');

const orderedCharacterSkills = computed(() => {
  return character.value.character_skills.sort((a, b) => {
    return a.skill.name.localeCompare(b.skill.name);
  });
});

const orderedCharacterRoles = computed(() => {
  return character.value.character_roles.sort((a, b) => {
    return a.role.name.localeCompare(b.role.name);
  });
});

const ensureDeletingCharacter = ref('');
const characterAbilitiesCost = computed(() => {
  return character.value.int + character.value.ref
      + character.value.dex + character.value.tech
      + character.value.cool + character.value.will
      + character.value.luck + character.value.move
      + character.value.body + character.value.emp_base;
});

const skills = ref([]);
const skillsSerach = ref('')
const newSkillInitialLevel = ref(0);
const filteredSkills = computed(() => {
  const characterCurrentSkillsIds = character.value.character_skills.map(skill => skill.skill.id);
  return skills.value.filter(skill =>
      skill.name.toLowerCase().includes(
          skillsSerach.value.toLowerCase()
      )).filter(skill => {
    return !characterCurrentSkillsIds.includes(skill.id);
  }).sort((a, b) => {
    return a.name.localeCompare(b.name);
  });
});
const summarySkillsCost = computed(() => {
  return character.value.character_skills.reduce((acc, skill) => {
    return acc + (skill.level * skill.skill.cost_multiplier);
  }, 0);
});

const roles = ref([]);
const rolesSerach = ref('')
const filteredRoles = computed(() => {
  const characterCurrentRolesIds = character.value.character_roles.map(role => role.role.id);
  return roles.value.filter(role =>
      role.name.toLowerCase().includes(
          rolesSerach.value.toLowerCase()
      )).filter(role => {
    return !characterCurrentRolesIds.includes(role.id);
  }).sort((a, b) => {
    return a.name.localeCompare(b.name);
  });
})

const sheetMode = ref(sheetModes.play);

const isCharacterChanged = computed(() => {
  return JSON.stringify(character.value) !== JSON.stringify(characterOriginal.value)
})

const isNotesChanged = computed(() => {
  return characterNotes.value !== character.value.notes;
})

const updateNotes = () => {
  character.value.notes = characterNotes.value;
}

watch(character, async () => {
  if (isCharacterChanged.value) {
    await updateCharacter();
  }
}, {deep: true});

onBeforeMount(async () => {
  socket.emit('join_character', {character_id: route.params.id});
  socket.on('character_update', data => {
    character.value = data;
    characterOriginal.value = {...data};
    characterNotes.value = data.notes;
  });
  await getCharacter();
  await getSkills();
  await getRoles();
  document.title = character.value.name;
  characterNotes.value = character.value.notes;
  isLoading.value = false;
})

const getCharacter = async () => {
  await readResource(`/character/${route.params.id}/`, response => {
        character.value = response.data;
        characterOriginal.value = {...character.value}
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      });
}

const getSkills = async () => {
  await readResource(`/skill/`, response => {
        skills.value = response.data;
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      });
}

const getRoles = async () => {
  await readResource(`/role/`, response => {
        roles.value = response.data;
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      });
}

const updateCharacter = async () => {
  const data = {
    name: character.value.name,
    notes: character.value.notes,
    int: character.value.int,
    ref: character.value.ref,
    dex: character.value.dex,
    tech: character.value.tech,
    cool: character.value.cool,
    will: character.value.will,
    luck: character.value.luck,
    move: character.value.move,
    body: character.value.body,
    humanity: character.value.humanity,
    emp_base: character.value.emp_base,
    health: character.value.health,
  }
  await updateResource(
      `/character/${route.params.id}/`,
      data,
      response => {
        character.value = response.data;
        characterOriginal.value = {...character.value}
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
}

const deleteCharacter = async () => {
  if (ensureDeletingCharacter.value !== character.value.name) {
    toasterStore.addMessage('error', 'Proszę wpisać nazwę postaci aby potwierdzić usunięcie.');
  } else {
    await deleteResource(
        `/character/${route.params.id}/`,
        response => {
          router.push({name: 'character-index'});
          toasterStore.addMessage('success', `Postać ${character.value.name} została usunięta.`);
        },
        error => {
          toasterStore.bulkRegisterBackendErrors(error);
        }
    );
  }
}

const addCharacterSkill = async (row) => {
  const data = {
    character_id: route.params.id,
    skill_id: row.id,
    level: newSkillInitialLevel.value,
  }
  await createResource(
      `/character/${route.params.id}/skill/`,
      data,
      response => {
        character.value.character_skills.push(response.data);
        toasterStore.addMessage('success', `Umiejętność ${response.data.skill.name} (${response.data.level}) została dodana.`);
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
};

const updateCharacterSkill = async (skill, addValue) => {
  const data = {
    level: skill.level + addValue,
  }
  await updateResource(
      `/character/${route.params.id}/skill/${skill.id}/`,
      data,
      response => {
        character.value.character_skills[character.value.character_skills.indexOf(skill)] = response.data;
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
}

const deleteCharacterSkill = async (skill) => {
  await deleteResource(
      `/character/${route.params.id}/skill/${skill.id}/`,
      response => {
        character.value.character_skills.splice(character.value.character_skills.indexOf(skill), 1);
        toasterStore.addMessage('success', `Umiejętność ${skill.skill.name} została usunięta.`);
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
}

const addCharacterRole = async (row) => {
  const data = {
    character_id: route.params.id,
    role_id: row.id,
    level: 0,
  }
  await createResource(
      `/character/${route.params.id}/role/`,
      data,
      response => {
        character.value.character_roles.push(response.data);
        toasterStore.addMessage('success', `Rola ${response.data.role.name} została dodana.`);
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
};

const updateCharacterRole = async (role, addValue) => {
  const data = {
    level: role.level + addValue,
  }
  await updateResource(
      `/character/${route.params.id}/role/${role.id}/`,
      data,
      response => {
        character.value.character_roles[character.value.character_roles.indexOf(role)] = response.data;
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
}

const deleteCharacterRole = async (role) => {
  await deleteResource(
      `/character/${route.params.id}/role/${role.id}/`,
      response => {
        character.value.character_roles.splice(character.value.character_roles.indexOf(role), 1);
        toasterStore.addMessage('success', `Rola ${role.role.name} została usunięta.`);
      },
      error => {
        toasterStore.bulkRegisterBackendErrors(error);
      }
  );
}

</script>

<template>
  <ConditionalLoader :is-loading="isLoading">
  <div class="field is-grouped is-grouped-right">
      <div class="control">
        <div class="buttons has-addons is-centered">
          <button class="button"
                  v-if="route.params.id"
                  @click="sheetMode = sheetModes.play"
                  :class="{'is-primary': sheetMode === sheetModes.play}">
            <i class="icon-user mr-3"></i>Gra</button>
          <button class="button"
                  v-if="route.params.id"
                  @click="sheetMode = sheetModes.edit"
                  :class="{'is-warning': sheetMode === sheetModes.edit}">
            <i class="icon-edit mr-3"></i>Edycja</button>
          <button class="button"
                  v-if="route.params.id"
                  @click="sheetMode = sheetModes.deleting"
                  :class="{'is-danger': sheetMode === sheetModes.deleting}">
            <i class="icon-trash mr-3"></i>Usówanie</button>
          <RouterLink :to="{name: 'character-print', id: route.params.id}" class="button">
            <i class="icon-print mr-3"></i>Drukuj
          </RouterLink>
        </div>
      </div>
    </div>

    <Input v-if="sheetMode === sheetModes.edit" class="is-large mb-4" v-model="character.name"/>
    <h1 v-else class="title is-1">{{ character.name }}</h1>

    <div class="box" v-if="sheetMode === sheetModes.deleting">
      <div class="field has-addons">
        <div class="control">
          <input class="input"
             type="text"
             placeholder="Wpisz nazwę postaci"
             :class="{'is-danger': ensureDeletingCharacter === character.name}"
             @keyup.enter="deleteCharacter()"
             v-model="ensureDeletingCharacter"/>
        </div>
        <div class="control">
          <button class="button is-danger"
                  :disabled="ensureDeletingCharacter !== character.name"
                  @click="deleteCharacter">
            <i class="icon-trash mr-3"></i> Usuń postać
          </button>
        </div>
      </div>
    </div>

    <Tabs>
      <Tab v-for="tab in tabs"
           :key="tab.title"
           :title="tab.title"
           :icon="tab.icon"
           :isActive="activeTab === tab"
           @click.native="activeTab = tab"/>
    </Tabs>

    <CharacterNotes
      v-if="activeTab === tabs[0]"
      :notes="characterNotes"
      :isChanged="isNotesChanged"
      @update:notes="val => characterNotes.value = val"
      @save="updateNotes"
      @cancel="characterNotes.value = character.notes"
    />

    <div v-if="activeTab === tabs[1]">
      <CharacterAbilities
        :character="character"
        :sheetMode="sheetMode"
        :cost="characterAbilitiesCost"/>

      <div class="columns">
        <div class="column">
          <CharacterSkills
            :ordered-skills="orderedCharacterSkills"
            :filtered-skills="filteredSkills"
            :skills-search="skillsSerach"
            :new-skill-level="newSkillInitialLevel"
            :sheet-mode="sheetMode"
            :summary-cost="summarySkillsCost"
            @update:skillsSearch="val => skillsSerach.value = val"
            @update:newSkillLevel="val => newSkillInitialLevel.value = val"
            @addSkill="addCharacterSkill"
            @updateSkill="updateCharacterSkill"
            @deleteSkill="deleteCharacterSkill"
          />
        </div>
        <div class="column">
          <CharacterPsychHealth :character="character" :sheetMode="sheetMode" />

          <CharacterRoles
            :ordered-roles="orderedCharacterRoles"
            :filtered-roles="filteredRoles"
            :roles-search="rolesSerach"
            :sheet-mode="sheetMode"
            @update:rolesSearch="val => rolesSerach.value = val"
            @addRole="addCharacterRole"
            @updateRole="updateCharacterRole"
            @deleteRole="deleteCharacterRole"
          />
        </div>
      </div>
    </div>

  </ConditionalLoader>
</template>

<style scoped>

</style>