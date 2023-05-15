<template>
        <div class="post-grid">
            <div v-for="post in posts" class = "card card-profile">
                <div class="profile-edit-icon" v-show="post.user.username == $store.state.username">
                    <a href="#" @click="editPost(post.data.post_id)"><span class="material-symbols-outlined">edit</span></a> <br>
                </div>
                <div class="profile-delete-icon" v-show="post.user.username == $store.state.username">
                    <a href="#" @click="deletePost(post.data.post_id)" ><span class="material-symbols-outlined">delete</span></a>
                </div>
                <div class="vertical-flex-container">
                    <div class="horizontal-flex-container" style="justify-content: left;">
                        <span v-html="profile_image(post.user.avatar)"></span>
                        <div class="vertical-flex-container profile-title" style="font-size: 15px;">
                            <router-link :to="user_link(post.user.username)">
                                {{ post.user.username }}
                            </router-link>
                        </div>
                    </div>
                    <hr>
                    <img style="height:275px;width:275px;object-fit:contain" :src="image_path(post.data.post_id)" :alt="image_path(post.data.post_id)"><br>
                    <div class="input-label" align="center"> {{ post.data.title }}</div>
                    <div class="card-info">{{ post.data.caption }}</div>
                </div>
            </div>
            <div v-show="!posts.length">
                No posts available to show!
            </div>
        </div>
</template>

<script>

import axios from 'axios'
import { Avataaars } from '@/avataaars'

export default {
    name : 'PostList',
    props : ['post_ids'],
    data() {
        return {
            posts : [], 
        }
    },
    mounted () {
        this.addPost()
    },
    watch : {
        'post_ids' : {
            handler(newValue){
                this.addPost()
            }
        }
    },
    methods : {
        async addPost () {
            this.post_list = []
            for (let post_id in this.post_ids){
                await axios.get('/post', {params:{post_id:this.post_ids[post_id]}, headers:{'Authorization' : this.$store.state.access_token_header}})
                            .then(post => {
                                let post_user = post.data.username
                                axios.get('/' + post_user + '/info', {headers:{'Authorization' : this.$store.state.access_token_header}})
                                    .then(res => {
                                        let post_user_avatar = res.data.avatar
                                        this.post_list.push({
                                            user : {
                                                username : post_user,
                                                avatar : post_user_avatar
                                            },
                                            data : post.data
                                        })
                                    })
                            })
            }
            this.posts = this.post_list
        },
        image_path (post_id) {
            return '/posts/' + post_id + '.png'
        },
        cleanDate(d) {
            let date_obj =  new Date(1000 * d)
            return date_obj.toLocaleString()
        }
        ,
        editPost (post_id) {
            this.$router.push('/post/manage/'+post_id)
        },
        deletePost (post_id) {
            this.$store.dispatch('deletePost', post_id)
        },
        profile_image (avatar) {
            return Avataaars.create({ 
                width : 50,
                height : 50, 
                style : 'circle',
                background : '#404089',
                ...avatar
            })
        },
        user_link (username) {
            return '/profile/' + username
        }
    },
}

</script>

<style>

</style>