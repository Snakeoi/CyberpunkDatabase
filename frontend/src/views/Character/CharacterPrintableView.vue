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
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';

const toasterStore = useToasterStore();

const route = useRoute();
const isLoading = ref(true);

const character = ref({});
const characterOriginal = ref({})
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
const showNotes = ref(false);
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

const isChanged = computed(() => {
  return JSON.stringify(character.value) !== JSON.stringify(characterOriginal.value)
})

watch(character, async () => {
  if (isChanged.value) {
    await updateCharacter();
  }
}, { deep: true });

onBeforeMount(async () => {
  await getCharacter();
  await getSkills();
  await getRoles();
  document.title = character.value.name;
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

    <h1 class="title is-3">{{ character.name }}</h1>
    <p class="has-text-right">
      Koszt umiejętności: <b>{{ summarySkillsCost }}</b>,
      Koszt zdolności: <b>{{ characterAbilitiesCost }}</b>
    </p>
    <div>
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
      <p class="has-text-centered"></p>
    </div>

    <div class="columns">
      <div class="column is-9 is-size-7">
        <div>
          <table class="table is-fullwidth">
            <thead>
            <tr>
              <th>Nazwa umiejętności</th>
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
            </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="column is-size-7">

        <div>
          <div>
          <table class="table is-fullwidth">
            <thead>
            <tr>
              <th>Nazwa Roli</th>
              <th>Zdolność specjalna</th>
              <th>Poziom</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="role in orderedCharacterRoles">
              <td>{{ role.role.name }}</td>
              <td>{{ role.role.special_ability }}</td>
              <td><b>{{ role.level }}</b></td>
            </tr>
            </tbody>
          </table>
        </div>
          <table class="table is-fullwidth">
            <tbody>
              <tr>
                <th colspan="2">Psychika</th>
              </tr>
              <tr>
                <td>Czło.</td><td>{{ character.humanity }}</td>
              </tr>
              <tr>
                <td>EMP baza</td><td>{{ character.emp_base }}</td>
              </tr>
              <tr>
                <td>EMP kara</td><td>{{ character.emp_debuff }}</td>
              </tr>
              <tr>
                <td>EMP</td><td>{{ character.emp }}</td>
              </tr>
              <tr>
                <th colspan="2">Zdrowie</th>
              </tr>
              <tr>
                <td>Zdrowie</td><td>{{ character.health }}</td>
              </tr>
              <tr>
                <td>Max. zdrowie</td><td>{{ character.health_base }}</td>
              </tr>
              <tr>
                <td>Poważne rany</td><td>{{ character.serious_wounds }}</td>
              </tr>
              <tr>
                <td>Przeżywalność</td><td>{{ character.survivability }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>


    <div class="content" v-html="character.notes"></div>


  </ConditionalLoader>
</template>

<style scoped>

</style>