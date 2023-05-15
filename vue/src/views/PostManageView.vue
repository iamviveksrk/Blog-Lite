<template>
    <div class="container">
        <div class="card card-form">
        <form class="card-form">
            <div class="input">
                <input type="text" class="input-field" value="test" v-model="title" required/>
                <label class="input-label">Title</label>
            </div>
            <div class="input">
                <input type="text" class="input-field" value="qq" v-model="caption" required/>
                <label class="input-label">Caption</label>
            </div>
            <br>
            <div class="file-upload" v-if="!post_id">
                <label style="color: #6658d3;">Image</label>
                <input type="file" name="file" id="file">
            </div>
            <div class="input">
                <input type="checkbox" class="input-field" v-model="private"/>
                <label style="color: #6658d3;">Archive?</label>
            </div>
            <div class="card-info-warning">{{ file_required_error }}</div>
            <div class="action">
                <button v-if="!post_id" href="#" type="button" class="action-button" v-touch="postForm">Post!</button>
                <button v-else href="#" type="button" class="action-button" v-touch="putForm">Post!</button>
            </div>
        </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            title : '',
            caption : '',
            post_id : this.$route.params.post_id,
            file_required_error : '',
            private : false,
        }
    },
    mounted (){
        if (this.post_id){
          axios.get('/post', {params:{post_id:this.post_id}})
            .then(post => {
                this.title = post.data.title
                this.caption = post.data.caption
                this.private = post.data.private == 1
            })
        }
    },
    methods : {
        postForm() {
            let postData = new FormData()
            let image = document.querySelector('#file')

            if (image.files.length == 0){
              this.file_required_error = 'Image required.'
            }
            else {
              postData.append('title', this.title)
              postData.append('caption', this.caption)
              postData.append('image', image.files[0])
              postData.append('timestamp', Date.now())
              postData.append('private', this.private ? 1 : 0)
            

              this.$store.dispatch("createPost", postData)
            }

        },
        putForm() {

            let postData = new FormData()

            postData.append('post_id', this.post_id)
            postData.append('title', this.title)
            postData.append('caption', this.caption) 
            postData.append('timestamp', Date.now())
            postData.append('private', this.private ? 1 : 0)

            this.$store.dispatch("updatePost", postData)

          }
    }
}

</script>


<style scoped>

img {
  max-width: 100%;
  display: block;
}

.card-heading-form {
  position: absolute;
  font-weight: 700;
  color: #735400;
}

.card-heading small {
  display: block;
  font-size: 0.75em;
  font-weight: 400;
  margin-top: 0.25em;
}


.input {
  display: flex;
  flex-direction: column-reverse;
  position: relative;
  padding-top: 1.5rem;
}
.input + .input {
  margin-top: 1.5rem;
}

.input-label {
  color: #8597a3;
  position: absolute;
  top: 1.5rem;
  transition: 0.25s ease;
}

.input-field {
  border: 0;
  z-index: 1;
  background-color: transparent;
  border-bottom: 2px solid #eee;
  font: inherit;
  font-size: 1.125rem;
  padding: 0.25rem 0;
}
.input-field:focus, .input-field:valid {
  outline: 0;
  border-bottom-color: #6658d3;
}
.input-field:focus + .input-label, .input-field:valid + .input-label {
  color: #6658d3;
  transform: translateY(-1.5rem);
}


.action {
  margin-top: 2rem;
}

.action-button {
  font: inherit;
  font-size: 1.25rem;
  padding: 1em;
  width: 100%;
  font-weight: 500;
  background-color: #6658d3;
  border-radius: 6px;
  color: #fff;
  border: 0;
  cursor:pointer;
}


.action-button:focus {
  outline: 0;
}
</style>