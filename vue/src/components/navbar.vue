<template>
<header class="header">
	<div class="header-content responsive-wrapper">
		<div class="header-logo">
			<router-link to="/">
				<div>
					<img src="https://assets.codepen.io/285131/untitled-ui-icon.svg" />
				</div>
			</router-link>
		</div>
		<div class="header-navigation">
			<nav class="header-navigation-links">
				<router-link to="/auth" v-if="!$store.state.logged_in"> Sign In </router-link>
				<router-link v-show="$store.state.logged_in" :to="user_link"> Profile </router-link> 
			</nav>
			<div class="header-navigation-actions">
				<a v-show="$store.state.logged_in" @click="$store.dispatch('logout')" href="#" class="button">
					<span>Logout</span>
				</a>
				<router-link to="/search" class="icon-button">
					<span class="link-icon">
					<!-- icon -->
					<svg xmlns="http://www.w3.org/2000/svg" width="192" height="192" fill="currentColor" viewBox="0 0 256 256">
						<rect width="256" height="256" fill="none"></rect>
						<circle cx="116" cy="116" r="84" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="16"></circle>
						<line x1="175.39356" y1="175.40039" x2="223.99414" y2="224.00098" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="16"></line>
					</svg>
					<!-- /icon -->
					</span>
				</router-link>
				<router-link :to="user_link" class="avatar" v-show="$store.state.logged_in">
					<span v-html="profile_image"></span><br>
				</router-link>
			</div>
		</div>
	</div>
</header>

</template>

<script>

import { Avataaars } from '@/avataaars.js'

export default {
    name: "CSSNavBar",
    computed: {
        user_link() {
            return "/profile/" + this.$store.state.username;
        },
		profile_image () {
            return Avataaars.create({ 
                width : 35,
                height : 35, 
                style : 'circle',
                background : '#404089',
                ...this.$store.state.avatar
            })
		}
    },
}

</script>

<style scoped>


@import url("https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");

img {
  display: block;
  max-width: 100%;
}


:focus {
  outline: 0;
}

.responsive-wrapper {
  width: 95%;
  max-width: 1280px;
  margin-left: 50px;
  margin-right: 50px;
}

@media (max-width:1200px) {
  .responsive-wrapper{
    margin-left: 5px;
    margin-right: 5px;
  }
}

.link-icon {
  width: 20px;
  height: 20px;
  display: block;
  flex-shrink: 0;
  left: 18px;
}
.link-icon svg {
  width: 20px;
  height: 20px;
}

.header {
  font-family: "DM Sans", sans-serif;
  display: flex;
  align-items: center;
  height: 60px;
  border-bottom: 1px solid #eff1f6;
  background-color: #ffffff;
  border-radius: 10px;
}

.header-content {
  display: flex;
  align-items: center;
}
.header-content > a {
  display: none;
}
@media (max-width: 1200px) {
  .header-content {
    justify-content: space-between;
  }
  .header-content > a {
    display: inline-flex;
  }
}

.header-logo {
  margin-right: 1.5rem;
}
.header-logo a {
  display: flex;
  align-items: center;
}
.header-logo a div {
  flex-shrink: 0;
  position: relative;
}
.header-logo a div:after {
  display: block;
  content: "";
  position: absolute;
  left: 0;
  top: auto;
  right: 0;
  bottom: 0;
  overflow: hidden;
  height: 50%;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  background-color: rgba(255, 255, 255, 0.2);
  -webkit-backdrop-filter: blur(4px);
          backdrop-filter: blur(4px);
}

.header-navigation {
  display: flex;
  flex-grow: 1;
  align-items: center;
  justify-content: space-between;
  font-size: 0.8rem;
}
/* @media (max-width: 1200px) {
  .header-navigation {
    display: none;
  }
} */

.header-navigation-links {
  display: flex;
  align-items: center;
}
.header-navigation-links a {
  text-decoration: none;
  color: #404089;
  font-weight: 500;
  transition: 0.15s ease;
}
.header-navigation-links a + * {
  margin-left: 1.5rem;
}
.header-navigation-links a:hover, .header-navigation-links {
  color: #434ce8;
}

.header-navigation-actions {
  display: flex;
  align-items: center;
}

.header-navigation-actions a {
  text-decoration: none;
  color: #404089;
  font-weight: 500;
  transition: 0.15s ease;
  font-size: 0.75rem;
}
.header-navigation-actions a + * {
  margin-left: 1.5rem;
}
.header-navigation-actions a:hover, .header-navigation-actions a:focus {
  color: #434ce8;
}
.header-navigation-actions > .avatar {
  margin-left: 0.75rem;
}
.header-navigation-actions > .icon-button + .icon-button {
  margin-left: 0.25rem;
}
.header-navigation-actions > .button + .icon-button {
  margin-left: 1rem;
}

.button {
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 1em;
  height: 40px;
  border-radius: 8px;
  line-height: 1;
  border: 2px solid #eff1f6;
  color: #404089;
  font-size: 0.875rem;
  transition: 0.15s ease;
  background-color: #ffffff;
}
.button i {
  margin-right: 0.5rem;
  font-size: 1.25em;
}
.button span {
  font-weight: 500;
}
.button:hover, .button:focus {
  border-color: #434ce8;
  color: #434ce8;
}

.icon-button {
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  color: #404089;
  transition: 0.15s ease;
}
.icon-button i {
  font-size: 1.25em;
}
.icon-button:focus, .icon-button:hover {
  background-color: #ecf3fe;
  color: #282a32;
}

</style>