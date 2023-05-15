<template>
    <div class="container">
      <div class="card card-form">
        <span v-html="profile_image"></span>
        <form class="avatar-card-form">
            <div class="input">
                <label class="input-label">Bio</label>
                <input type="text" class="input-field" v-model="bio" required/>
            </div>
            <div class="input">
                <label>Skin Tone</label> <br>
                <div class="btn-container">
                    <div v-for="(hex, color) in options.colors.skin">
                        <span class="checkmark" :style="{backgroundColor:hex,color:hex}">
                            <input type="radio" v-model="skin" :value="color" :checked="color==skin">
                        </span>
                    </div>
                </div>
            </div>
            <hr>
            <div class="input">
                <label>Hair Style</label> <br>
                <select v-model="top">
                    <option v-for="option in options.paths.hair" :selected="option == top" :value="option">{{ titleCase(option) }}</option>
                </select> <br>
                <label>Hair Colour</label> <br>
                <div class="btn-container">
                    <div v-for="(hex, color) in options.colors.hair">
                        <span class="checkmark" :style="{backgroundColor:hex,color:hex}">
                            <input type="radio" v-model="hairColor" :value="color" :checked="color==hairColor">
                        </span>
                    </div>
                </div>
            </div>
            <hr>
            <div class="input">
                <label>Eyes</label> <br>
                <select v-model="eyes">
                    <option v-for="option in options.paths.eyes" :selected="option == eyes" :value="option">{{ titleCase(option) }}</option>
                </select> <br>
                <label>Eyebrows</label> <br>
                <select v-model="eyebrows">
                    <option v-for="option in options.paths.eyebrows" :selected="option == eyebrows" :value="option">{{ titleCase(option) }}</option>
                </select> <br>
            </div>
            <hr>
            <div class="input">
                <label>Mouth</label> <br>
                <select v-model="mouth">
                    <option v-for="option in options.paths.mouth" :selected="option == mouth" :value="option">{{ titleCase(option) }}</option>
                </select> <br>
                <label>Eyebrows</label> <br>
                <select v-model="facialHair">
                    <option v-for="option in options.paths.facialHair" :selected="option == facialHair" :value="option">{{ titleCase(option) }}</option>
                </select> <br>
                <label>Facial Hair Colour</label> <br>
                <div class="btn-container">
                    <div v-for="(hex, color) in options.colors.hair">
                        <span class="checkmark" :style="{backgroundColor:hex,color:hex}">
                            <input type="radio" v-model="facialHairColor" :value="color" :checked="color==facialHairColor">
                        </span>
                    </div>
                </div>
            </div>
            <hr>
            <div class="input">
                <label>Clothing</label> <br>
                <select v-model="clothing">
                    <option v-for="option in options.paths.clothing" :selected="option == clothing" :value="option">{{ titleCase(option) }}</option>
                </select> <br>
                <label>Clothing Colour</label> <br>
                <div class="btn-container">
                    <div v-for="(hex, color) in options.colors.palette">
                        <span class="checkmark" :style="{backgroundColor:hex,color:hex}">
                            <input type="radio" v-model="clothingColor" :value="color" :checked="color==clothingColor">
                        </span>
                    </div>
                </div>
            </div>
            <hr>
            <div class="input">
                <label>Glasses</label> <br>
                <select v-model="accessories">
                    <option v-for="option in options.paths.accessories" :selected="option == accessories" :value="option">{{ titleCase(option) }}</option>
                </select> <br>
                <label>Glasses Color</label> <br>
                <div class="btn-container">
                    <div v-for="(hex, color) in options.colors.palette">
                        <span class="checkmark" :style="{backgroundColor:hex,color:hex}">
                            <input type="radio" v-model="accessoriesColor" :value="color" :checked="color==accessoriesColor">
                        </span>
                    </div>
                </div>
            </div>
            <div class="action">
                <button href="#" type="button" class="action-button" v-touch="buttonClick">Update</button>
            </div>
        </form>
      </div>
    </div>
  </template>
  
<script>

import { Avataaars } from '@/avataaars.js'
import axios from 'axios';
import router from '@/router';

export default{
    data() {
        return {
            options: {
                colors: Avataaars.colors,
                paths: {
                    hair: Object.keys(Avataaars.paths.top).filter(function(v){
                        // Excluding hats
                        return !/^(eyepatch|turban|hijab|hat|winterHat01|winterHat02|winterHat03|winterHat04)$/.test(v);
                    }),
                    eyebrows: Object.keys(Avataaars.paths.eyebrows),
                    eyes: Object.keys(Avataaars.paths.eyes),
                    mouth: Object.keys(Avataaars.paths.mouth),
                    facialHair: Object.keys(Avataaars.paths.facialHair),
                    accessories: Object.keys(Avataaars.paths.accessories),
                    clothing: Object.keys(Avataaars.paths.clothing).filter(function(v){
                        // Excluding graphic shirt
                        return !/^(graphicShirt)$/.test(v);
                    }),
                },
            },
            bio : this.$store.state.bio,
            skin : this.$store.state.avatar['skin'],
            top : this.$store.state.avatar['top'],
            hairColor : this.$store.state.avatar['hairColor'],
            eyes : this.$store.state.avatar['eyes'],
            eyebrows : this.$store.state.avatar['eyebrows'],
            mouth : this.$store.state.avatar['mouth'],
            facialHair : this.$store.state.avatar['facialHair'],
            facialHairColor : this.$store.state.avatar['facialHairColor'],
            clothing : this.$store.state.avatar['clothing'],
            clothingColor : this.$store.state.avatar['clothingColor'],
            accessories : this.$store.state.avatar['accessories'],
            accessoriesColor : this.$store.state.avatar['accessoriesColor'],
        }
    },
    methods:{
        // Case converter
        titleCase: function(text) {
            const result = text.replace(/([A-Z])/g, " $1").replace(/([0-9]+)/g, " $1");
            return result.charAt(0).toUpperCase() + result.slice(1);
        },
        buttonClick () {
            this.$store.state.bio = this.bio
            this.$store.state.avatar['skin'] = this.skin
            this.$store.state.avatar['top'] = this.top
            this.$store.state.avatar['hairColor'] = this.hairColor
            this.$store.state.avatar['eyes'] = this.eyes
            this.$store.state.avatar['eyebrows'] = this.eyebrows
            this.$store.state.avatar['mouth'] = this.mouth
            this.$store.state.avatar['facialHair'] = this.facialHair
            this.$store.state.avatar['facialHairColor'] = this.facialHairColor
            this.$store.state.avatar['clothing'] = this.clothing
            this.$store.state.avatar['clothingColor'] = this.clothingColor
            this.$store.state.avatar['accessories'] = this.accessories
            this.$store.state.avatar['accessoriesColor'] = this.accessoriesColor

            axios.put('/' + this.$store.state.username + '/info', 
            {
                bio : this.bio,
                avatar : {
                    skin : this.skin,
                    top : this.top,
                    hairColor : this.hairColor,
                    eyes : this.eyes,
                    eyebrows : this.eyebrows,
                    mouth : this.mouth,
                    facialHair : this.facialHair,
                    facialHairColor : this.facialHairColor,
                    clothing : this.clothing,
                    clothingColor : this.clothingColor,
                    accessories : this.accessories,
                    accessoriesColor : this.accessoriesColor,
                }
            }).then(
                router.push('/profile/' + this.$store.state.username)
            )
        }
    },
    computed:{
        profile_image () {
            return Avataaars.create({ 
                width : 150,
                height : 150, 
                style : 'circle',
                background : '#404089',
                skin : this.skin,
                top : this.top,
                hairColor : this.hairColor,
                eyes : this.eyes,
                eyebrows : this.eyebrows,
                mouth : this.mouth,
                facialHair : this.facialHair,
                facialHairColor : this.facialHairColor,
                clothing : this.clothing,
                clothingColor : this.clothingColor,
                accessories : this.accessories,
                accessoriesColor : this.accessoriesColor,
            })
        }
    }
}

</script>

<style scoped>
::-webkit-scrollbar {
    display: none;
}
</style>