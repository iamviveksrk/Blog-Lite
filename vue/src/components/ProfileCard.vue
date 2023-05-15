<template>

<div class="container">
    <div class = "card card-profile">
        <div class="profile-edit-icon" v-if="$store.state.logged_in && $store.state.username == username">
            <router-link to="/avatar"><span class="material-symbols-outlined">edit</span></router-link>
        </div>
        <div class="horizontal-flex-container">
            <div class="vertical-flex-container">
                <div>
                    <span v-html="profile_image"></span><br>
                </div>
            </div>
            <div class="vertical-flex-container" style="width: 200px;">
                <div class="profile-title">
                    <router-link :to="user_link">
                        {{ username }}
                    </router-link>
                </div>
                <div class="card-info">
                    {{ bio }}
                </div>
                <div class="horizontal-flex-container" style="justify-content: center;" v-show="profile_page">
                    <div class="card-text">
                        <span>{{ post_count }}</span> <br>
                        <span class="card-text">Posts</span>
                    </div>
                    <div class="card-text" @click="$emit('view_followers')">
                        <span>{{ follower_count }}</span> <br>
                        <span class="card-text">Followers</span>
                    </div>
                    <div class="card-text" @click="$emit('view_following')">
                        <span>{{ following_count }}</span> <br>
                        <span>Following</span>
                    </div>
                </div>
            </div>
        </div>
        <br>
        <div align="center" v-if="$store.state.logged_in && $store.state.username != username">
            <button class="unfollow-button" @click="unfollowUser(username); $emit('unfollow')" v-if="isFollowing(username)">Unfollow</button>
            <button class="follow-button" @click="followUser(username); $emit('follow')" v-else>Follow</button>
        </div>
        <div align="center" v-if="$store.state.logged_in && $store.state.username == username">
            <router-link to="/post/manage"><span class="material-symbols-outlined">note_add</span></router-link>
            <div class="profile-export-icon" v-if="$store.state.logged_in && $store.state.username == username">
                <a href="#" @click="post_export"><span class="material-symbols-outlined"><span class="material-symbols-outlined">move_to_inbox</span></span></a>
            </div>
        </div>
    </div>
</div>

</template>

<script>

import { Avataaars } from '@/avataaars.js'
import { mapActions } from 'vuex'

export default {
    name : "ProfileCard",
    props : ['username', 'bio', 'avatar', 'profile_page', 'post_count', 'follower_count', 'following_count'],
    computed:{
        profile_image () {
            return Avataaars.create({ 
                width : 90,
                height : 90, 
                style : 'circle',
                background : '#404089',
                ...this.avatar
            })
        },
        user_link () {
            return '/profile/' + this.username
        }
    },
    methods : {
        isFollowing (username) {
            return this.$store.state.following.includes(username)
        },
        post_export () {
            this.$store.dispatch('postExport')
        },
        ...mapActions([
            'followUser',
            'unfollowUser',
        ])
    },
}

</script>