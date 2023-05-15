<template>
    <div class="vertical-flex-container">
            <div class="search">
                <input type="text" placeholder="Search" v-model="query" @keyup="searchUser(query)"/>
                <button class="material-symbols-outlined">search</button>
            </div>
            <div v-for="user in users" v-if="user.username != $store.state.username">
                <ProfileCard :username="user.username" :bio="user.bio" :avatar="user.avatar" />
            </div>
    </div>
</template>

<script>

import axios from 'axios'
import { mapActions } from 'vuex'
import ProfileCard from '@/components/ProfileCard.vue'

export default {
    data () {
        return {
            query : '',
            users : [],
        }
    },
    methods : {
        searchUser () {
            if (this.query){
                axios.get('/search/' + this.query)
                    .then(res => this.users = res.data.users)
            }
        },
        user_link (username) {
            return '/profile/' + username
        },
        isFollowing (username) {
            return this.$store.state.following.includes(username)
        },
    },
    components : {
        ProfileCard,
    }
}

</script>

<style scoped>

.search {
  position: relative;
  display: flex;
  align-items: center;
  width: 80%;
  align-self: center;
  padding-top: 2rem;
}
.search input {
  font: inherit;
  color: inherit;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 1em 0 36px;
  height: 40px;
  border-radius: 8px;
  border: 2px solid #eff1f6;
  color: #404089;
  font-size: 0.875rem;
  transition: 0.15s ease;
  width: 100%;
  line-height: 1;
}
.search input::-moz-placeholder {
  color: #404089;
}
.search input:-ms-input-placeholder {
  color: #404089;
}
.search input::placeholder {
  color: #404089;
}
.search input:focus, .search input:hover {
  border-color: #434ce8;
}
.search button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 0;
  background-color: transparent;
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-12.5%);
  font-size: 1.25em;
  color: #404089;
  padding: 0;
  height: 40px;
}
</style>