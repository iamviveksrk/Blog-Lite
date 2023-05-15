import Vue from "vue";
import Vuex from "vuex";
import axios from 'axios'
import router from '@/router'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);
Vue.config.devtools = true

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    access_token_header : null,
    refresh_token_header : null,
    logged_in : false,
    username : null,
    following : [],
    login_err : null,
    avatar : null,
    bio : null,
    feed : [],

  },
  getters: {},
  mutations: {
    authUser (state, userData) {
      state.access_token_header = 'Bearer ' + userData.access_token
      state.refresh_token_header = 'Bearer ' + userData.refresh_token
      state.logged_in = true
      state.username = userData.username
      state.avatar = userData.avatar
      state.bio = userData.bio
    },
    feedFollow (state, userData) {
      state.feed = userData.feed
      state.following = userData.following
    },
    logoutUser (state) {
      state.access_token_header = null;
      state.refresh_token_header = null;
      state.logged_in = false;
      state.username = null;
      state.following = [];
    },
    errors (state, errorData){
      state.login_err = errorData
    }
  },
  actions: {
    register ({commit, dispatch}, authData) {
      
      axios.post('/register', authData)
        .then(res => {
          commit('authUser', {
            access_token : res.data.access_token,
            refresh_token : res.data.refresh_token,
            username : res.data.username,
            avatar : res.data.avatar,
            bio : res.data.bio,
          })
          dispatch('refreshUserState')
          router.push('/profile/' + this.state.username)
        })
        .catch(err => console.log(err))
    },
    login ({commit, dispatch}, authData) {
      
      axios.post('/login', authData)
        .then(res => {
          commit('authUser', {
            access_token : res.data.access_token,
            refresh_token : res.data.refresh_token,
            username : res.data.username,
            avatar : res.data.avatar,
            bio : res.data.bio,
          })
          dispatch('refreshUserState')
          router.push('/profile/' + this.state.username)
        })
        .catch(err => {commit('errors', err.response.data.message)})
    },
    logout ({commit}) {
      commit('logoutUser')
      router.push('/').catch(err => {})
    },
    refreshUserState ({commit}) {
      let userData = {feed : [], following : []}
      axios.get('/feed', {headers:{'Authorization' : this.state.access_token_header}})
        .then(res => {
          userData.feed=res.data.post_ids
          axios.get('/' + this.state.username + '/following/list')
            .then(ress => {
              for (let i in ress.data.following){
                userData.following.push(ress.data.following[i].username)
              }
              commit('feedFollow', userData)
            })
        })
    },
    createPost ({commit}, postData) {

      axios.post('/post', postData, {
        headers:{
          'Authorization' : this.state.access_token_header,
          'Content-Type': 'multipart/form-data',
        }
      })
        .then(res => router.push('/profile/' + this.state.username))

    },
    updatePost ({commit}, postData) {

      axios.put('/post', postData, {
        headers:{
          'Authorization' : this.state.access_token_header,
          'Content-Type': 'multipart/form-data',
        }
      })
        .then(res => router.push('/profile/' + this.state.username))

    },
    deletePost({commit}, post_id){
      axios.delete('/post', {
        params:{
          post_id:post_id
        },
        headers:{
          'Authorization' : this.state.access_token_header,
        }
      })
        .then(res => router.push('/'))
    },
    followUser ({commit}, username){
      axios.post('/follow', {'username' : username}, {headers:{'Authorization' : this.state.access_token_header}})
        .then(res => {
            this.state.following.push(username)
            axios.get('/feed', {headers:{'Authorization' : this.state.access_token_header}})
              .then(res=>this.state.feed=res.data.post_ids)
        })
    },
    unfollowUser ({commit}, username){
        axios.post('/unfollow', {'username' : username}, {headers:{'Authorization' : this.state.access_token_header}})
          .then(res => {
              this.state.following.splice(this.state.following.indexOf(username), 1)
              axios.get('/feed', {headers:{'Authorization' : this.state.access_token_header}})
                .then(res=>this.state.feed=res.data.post_ids)
          })
    },
    postExport({commit}) {
      axios.get('/user/export', {headers:{'Authorization' : this.state.access_token_header}})
    }
  },
  modules: {},
});
