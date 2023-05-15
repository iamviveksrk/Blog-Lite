<template>

    <div>
        <ProfileCard v-if="!self"
            :username="username" 
            :bio="bio" 
            :avatar="avatar" 
            profile_page=true 
            :post_count="post_ids.length" 
            :follower_count="follower_count" 
            :following_count="following_count" 
            @unfollow="follower_count -= 1" 
            @follow="follower_count += 1" 
            @view_followers=" view_modal('followers')"
            @view_following="view_modal('following')"
        />
        <ProfileCard v-else
            :username="$store.state.username" 
            :bio="$store.state.bio" 
            :avatar="$store.state.avatar" 
            profile_page=true 
            :post_count="post_ids.length" 
            :follower_count="follower_count" 
            :following_count="following_count" 
            @unfollow="following_count -= 1" 
            @follow="following_count += 1" 
            @view_followers=" view_modal('followers')"
            @view_following="view_modal('following')"
        />

        <PostList :post_ids="post_ids"></PostList>

        <ModalComponent v-if="view_modal_flag && self"  :title="modal_title" :user_list="user_list" @close=" userinfo()" />
        <ModalComponent v-else-if="view_modal_flag && !self"  :title="modal_title" :user_list="user_list" @close=" userinfo()" />

    </div>

</template>

<script>

import axios from 'axios'
import ProfileCard from '@/components/ProfileCard.vue'
import ModalComponent from '@/components/ModalComponent.vue'
import PostList from '@/components/PostList.vue'

export default {
    name : 'profile', 
    data() {
        return {
            username : this.$route.params.username,
            post_ids : [],
            follower_count : 0,
            following_count : 0,
            avatar: {},
            bio : '',
            posts : [],
            user_list : [],
            view_modal_flag : false,
            modal_title : ''
        }
    },
    beforeCreate() {
        if (this.$store.state.logged_in){
            this.$store.dispatch('refreshUserState')
        }
        const getPostIds = async (username) => {
            await axios.get('/' + username + '/info', {headers:{'Authorization' : this.$store.state.access_token_header}})
                        .then(res => {

                            this.post_ids = res.data.post_ids
                            this.avatar = res.data.avatar
                            this.bio = res.data.bio
                        })
        }
        getPostIds(this.$route.params.username)
    },
    mounted(){
        axios.get('/' + this.username + '/followers')
                .then(res => this.follower_count = res.data.follower_count);
        axios.get('/' + this.username + '/following')
            .then(res => this.following_count = res.data.following_count);
    },
    computed : {
        self () {
            return this.$store.state.username == this.username
        },
    },
    watch: {
        '$route.params' : {
            handler(newValue){
                this.username = newValue.username
                this.userinfo()
            }
        }
    },
    methods:{
        userinfo () {
            this.post_ids = []
            this.follower_count = 0
            this.following_count = 0
            this.avatar = null
            this.bio = ''
            this.posts = []
            this.user_list = []
            
            this.modal_title = ''
            this.view_modal_flag = false;
            axios.get('/' + this.username + '/info', {headers:{'Authorization' : this.$store.state.access_token_header}})
                .then(res => {

                    this.post_ids = res.data.post_ids
                    this.avatar = res.data.avatar
                    this.bio = res.data.bio
                    
                    this.posts.sort((a, b) => a.timestamp-b.timestamp)
                })

            axios.get('/' + this.username + '/followers')
                .then(res => this.follower_count = res.data.follower_count);
            axios.get('/' + this.username + '/following')
                .then(res => this.following_count = res.data.following_count);
        },
        isFollowing (username) {
            return this.$store.state.following.includes(username)
        },
        view_modal (type) {
            if (type == 'followers') {
                axios.get('/' + this.username + '/followers/list')
                    .then(res => {
                        this.user_list = res.data.followers
                        this.modal_title = 'Followers'
                        this.view_modal_flag = true
                    });
            }
            else {
                axios.get('/' + this.username + '/following/list')
                    .then(res => {
                        this.user_list = res.data.following
                        this.modal_title = 'Following'
                        this.view_modal_flag = true
                    });
            }
        }
    },
    components : {
        ProfileCard,
        ModalComponent,
        PostList
    }
}

</script>