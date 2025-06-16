<script setup>
import {createResource, deleteResource, readResource, updateResource} from "@/assets/utils/axios/crud.js";
import {computed, onBeforeMount, ref, watch} from "vue";
import {useRoute} from 'vue-router'
import Input from "@/components/form/Input.vue";
import ConditionalLoader from "@/components/loader/ConditionalLoader.vue";
import {useToasterStore} from "@/stores/toaster.js";
import Abilities from "@/components/character/Abilities.vue";
import Ability from "@/components/character/Ability.vue";
import DataTable from "@/components/common/data_table/DataTable.vue";
import SearchInput from "@/components/common/SearchInput.vue";
import {sheetModes} from "@/enums.js";
import router from "@/router/index.js";
import {QuillEditor} from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import Tabs from "@/components/Tabs/Tabs.vue";
import Tab from "@/components/Tabs/Tab.vue";

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


    <div class="content" v-if="activeTab === tabs[0]">
      <div>
        <div class="buttons has-addons is-right">
          <button :disabled="!isNotesChanged" class="button is-primary" @click="updateNotes">
            <i class="icon-save"></i> Zapisz notatki
          </button>
          <button class="button is-warning" :disabled="!isNotesChanged" @click="characterNotes = character.notes">
            <i class="icon-remove"></i> Anuluj zmiany
          </button>
        </div>

        <QuillEditor
             theme="snow"
             :content-type="'html'"
             :placeholder="'Opis postaci'"
             v-model:content="characterNotes"
        />
      </div>
    </div>

    <div v-if="activeTab === tabs[1]">
      <div class="box">
        <Abilities>
          <Ability v-model="character.int" :sheetMode=sheetMode heading="INT"/>
          <Ability v-model="character.ref" :sheetMode=sheetMode heading="REF"/>
          <Ability v-model="character.dex" :sheetMode=sheetMode heading="ZW"/>
          <Ability v-model="character.tech" :sheetMode=sheetMode heading="TECH"/>
          <Ability v-model="character.cool" :sheetMode=sheetMode heading="CHA"/>
          <Ability v-model="character.will" :sheetMode=sheetMode heading="SW"/>
          <Ability v-model="character.body" :sheetMode=sheetMode heading="BC"/>
          <Ability v-model="character.luck" :sheetMode=sheetMode heading="SZ"/>
          <Ability v-model="character.move" :sheetMode=sheetMode heading="RUCH"/>
        </Abilities>
        <p class="has-text-centered">Koszt zdolności: <b>{{ characterAbilitiesCost }}</b></p>
      </div>
      <div class="columns">
      <div class="column">
        <div class="box">
          <h2 class="title is-4">Umiejętności</h2>
          <p class="has-text-right">Koszt umiejętności: <b>{{ summarySkillsCost }}</b></p>
          <table class="table is-fullwidth">
            <thead>
            <tr>
              <th>Nazwa</th>
              <th>Dziedziczy</th>
              <th>Poziom</th>
              <th>Cecha</th>
              <th>Baza</th>
              <th v-if="[sheetModes.edit, sheetModes.deleting].includes(sheetMode)">Akcje</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="skill in orderedCharacterSkills">
              <td>
                {{ skill.skill.name }}
                <span v-if="skill.skill.cost_multiplier > 1" class="has-text-warning">
                  (x{{ skill.skill.cost_multiplier }})
                </span>
              </td>
              <td>{{ skill.skill.inherit.toUpperCase() }}</td>
              <td>{{ skill.level }}</td>
              <td>{{ skill.ability_level }}</td>
              <td><b>{{ skill.base }}</b></td>
              <td v-if="sheetMode === sheetModes.edit" class="has-text-primary">
                <i @click=updateCharacterSkill(skill,-1) class="icon-minus-square is-clickable pr-4"></i>
                <i @click=updateCharacterSkill(skill,1) class="icon-plus-square is-clickable"></i>
              </td>
              <td v-if="sheetMode === sheetModes.deleting" class="has-text-danger">
                <i @click=deleteCharacterSkill(skill) class="icon-trash is-clickable"></i>
              </td>
            </tr>
            </tbody>
          </table>

          <div class="field" v-if="sheetMode === sheetModes.edit">
            <label class="label">Dodaj umiejętność</label>
            <div class="my-3">
              <div class="field is-grouped">
                <div class="field">
                  <label class="label">Szukaj</label>
                  <SearchInput v-model="skillsSerach"/>
                </div>
                <div class="field">
                  <label class="label">Poziom początkowy</label>
                  <Input v-model="newSkillInitialLevel" type="number" min="0" max="10"/>
                </div>
              </div>
            </div>
            <DataTable
              :storageName="'skills'"
              :data="filteredSkills"
              :onRowClick="addCharacterSkill"
              :structure="[
                {
                  key: 'name',
                  title: 'Nazwa',
                  type: 'string',
                  isSortable: true
                },
                {
                  key: 'inherit',
                  title: 'Zdolność',
                  type: 'string',
                  isSortable: true
                },
                {
                  key: 'cost_multiplier',
                  title: 'Mnożnik kosztu',
                  type: 'string',
                  isSortable: true
                },
              ]"
          />
          </div>

        </div>
      </div>
      <div class="column">

        <div class="box">
          <h2 class="title is-4">Psychika</h2>
          <Abilities>
            <Ability v-model="character.humanity" :editableAt="['play', 'edit']" :sheetMode=sheetMode heading="Człowieczeństwo"/>
            <Ability v-model="character.emp_base" class="subtitle" :sheetMode=sheetMode heading="EMP baza"/>
            <Ability v-model="character.emp_debuff" class="subtitle" :class="{'has-text-danger': character.emp_debuff !== 0}" heading="EMP kara"/>
            <Ability v-model="character.emp" heading="EMP"/>
          </Abilities>
        </div>

        <div class="box">
          <h2 class="title is-4">Zdrowie</h2>
          <Abilities>
            <Ability v-model="character.health" :editableAt="['play', 'edit']" :sheetMode="sheetMode" heading="Zdrowie"/>
            <Ability v-model="character.health_base" heading="Max. zdrowie"/>
            <Ability v-model="character.serious_wounds" heading="Poważne rany"/>
            <Ability v-model="character.survivability" heading="Przeżywalność"/>
          </Abilities>
        </div>

        <div class="box">
          <h2 class="title is-4">Role</h2>
          <table class="table is-fullwidth">
            <thead>
            <tr>
              <th>Nazwa</th>
              <th>Zdolność specjalna</th>
              <th>Poziom</th>
              <th v-if="[sheetModes.edit, sheetModes.deleting].includes(sheetMode)">Akcje</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="role in orderedCharacterRoles">
              <td>{{ role.role.name }}</td>
              <td>{{ role.role.special_ability }}</td>
              <td><b>{{ role.level }}</b></td>
              <td v-if="sheetMode === sheetModes.edit" class="has-text-primary">
                <i @click=updateCharacterRole(role,-1) class="icon-minus-square is-clickable pr-4"></i>
                <i @click=updateCharacterRole(role,1) class="icon-plus-square is-clickable"></i>
              </td>
              <td v-if="sheetMode === sheetModes.deleting" class="has-text-danger">
                <i @click=deleteCharacterRole(role) class="icon-trash is-clickable"></i>
              </td>
            </tr>
            </tbody>
          </table>

          <div class="field" v-if="sheetMode === sheetModes.edit">
            <label class="label">Dodaj rolę</label>
            <div class="my-3">
              <SearchInput v-model="rolesSerach"/>
            </div>
            <DataTable
              :storageName="'skills'"
              :data="filteredRoles"
              :onRowClick="addCharacterRole"
              :structure="[
                {
                  key: 'name',
                  title: 'Nazwa',
                  type: 'string',
                  isSortable: true
                },
                {
                  key: 'special_ability',
                  title: 'Zdolność specjalna',
                  type: 'string',
                  isSortable: true
                },
              ]"
          />
          </div>

        </div>
      </div>
    </div>
    </div>

  </ConditionalLoader>
</template>

<style scoped>

</style>