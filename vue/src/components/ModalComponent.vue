<template>
  <div class="modal-backdrop">
    <div class="modal">
      <header class="modal-header">
        {{ title }}
        <button
          type="button"
          class="btn-close"
          @click="$emit('close')"
        >
          x
        </button>
      </header>

      <section class="modal-body">
          <div v-for="user in user_list">
              <ProfileCard :username="user.username" :bio="user.bio" :avatar="user.avatar" @close_modal="$emit('close')" @unfollow="$emit('unfollow')" @follow="$emit('follow')"/>
          </div>
        </section>
    </div>
  </div>
</template>

<script>

import ProfileCard from '@/components/ProfileCard.vue'

export default {
  name : 'modal',
  props: ['title', 'user_list'],
  components : {
      ProfileCard,
  },
}

</script>

<style scoped>

</style><style>
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: #FFFFFF;
  /* box-shadow: 2px 2px 10px p; */
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  width: 500px;
  height: 600px;
  border-radius: 1%;
  z-index: 2;
}

.modal-header{
  padding: 15px;
  display: flex;
}

.modal-header {
  position: relative;
  border-bottom: 1px solid #eeeeee;
  color: #6658d3;
  justify-content: space-between;
}

.modal-body {
  position: relative;
  padding: 20px 10px;
  overflow-y: auto;
}

.btn-close {
  position: absolute;
  top: 0;
  right: 0;
  border: none;
  font-size: 20px;
  padding: 10px;
  cursor: pointer;
  font-weight: bold;
  color: #6658d3;
  background: transparent;
}

.btn-green {
  color: white;
  background: #6658d3;
  border: 1px solid #6658d3;
  border-radius: 2px;
}
</style>