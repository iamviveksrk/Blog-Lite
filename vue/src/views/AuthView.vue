<template>
  <div class="container">
    <div class="card card-form">
      <div class="card-image">	
        <h2 class="card-heading card-heading-form" v-if="!auth_state">
          Welcome Back!
          <small>Please Log In</small>
        </h2>
        <h2 class="card-heading card-heading-form" v-else>
          No Account?
          <small>Create an Account</small>
        </h2>
      </div>
      <form class="card-form">
        <div class="input">
          <input type="text" class="input-field" value="test" v-model="username" required/>
          <label class="input-label">Username</label>
        </div>
        <div class="card-info-warning">{{ errors.username }}</div>
        <div class="input">
          <input type="password" class="input-field" value="qq" v-model="password" required/>
          <label class="input-label">Password</label>
        </div>
        <div class="card-info-warning">{{ pwError }}</div>
        <div class="input" v-show="auth_state">
          <input type="password" class="input-field" v-model="confirm" required/>
          <label class="input-label">Confirm Password</label>
        </div>
        <div class="card-info-warning" v-show="auth_state">{{ errors.confirm }}</div>
        <div class="input" v-show="auth_state">
          <input type="text" class="input-field" v-model="email" required/>
          <label class="input-label">Email Address</label>
        </div>
        <div class="card-info-warning" v-show="auth_state">{{ errors.email }}</div>
        <div class="action">
          <button href="#" type="button" class="action-button" v-touch="buttonClick">{{ !auth_state ? "Login" : "Register" }}</button>
        </div>
        <div class="card-info">
          <p v-if="auth_state">Have an account already? <a href="#" @click="switch_state()">Login</a></p>
          <p v-else>No account yet? <a href="#" @click="switch_state()">Register</a></p>
          <!-- <ul>
            <li v-for="error in errors">{{ error }}</li>
          </ul> -->
        </div>
      </form>
    </div>
  </div>
</template>

<script>

import axios from 'axios';

export default{
  data() {
    return {
      username: '',
      password: '',
      confirm: '',
      email: '',
      auth_state: 0,
      errors:{
        username : '',
        confirm : '',
        email : '',
      },
      username_exists : true,
      search_data: [],
    }
  },
  methods:{
    validator() {
      this.errors = [];
      const authData = {
        username:this.username,
        password:this.password,
      }
      if (this.auth_state) {
        if (!this.username_exists){
          if (this.password == this.confirm){
            if (this.isValidEmail){
              authData.email = this.email
              this.$store.dispatch("register", authData)
            }
            else {
              this.errors.email = "Bad Email Format!"
            }
          }
          else {
            this.errors.confirm = "Passwords don't match!"
          }
        }
        else {
          this.errors.username = "Username <" + this.username + "> already exists!"
        }
      }
      else {
        if (this.username_exists){
          this.$store.dispatch("login", authData)
        }
        else {
          this.errors.username = "Username <" + this.username + "> does not exist!"
        }
      }
    },
    buttonClick() {
      this.$store.state.login_err = ''
      if (this.username){
        axios.get('/search/' + this.username)
          .then(res => {
            this.search_data =  res.data.users;
            this.username_exists = false
            for (let i in this.search_data){
              if (this.search_data[i].username == this.username) {
                this.username_exists = true
              }
            }
            this.validator()
          })
      }
      else {
        this.errors.username = "Username field must not be empty!"
      }
    },
    switch_state () {
      this.auth_state = !this.auth_state
      this.$store.state.login_err = ''
    }
  },
  computed:{
    pwError(){
      return this.$store.state.login_err
    },
    isValidEmail() {
      return /^[^@]+@\w+(\.\w+)+\w$/.test(this.email)
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

.input-label {
  color: #8597a3;
  position: absolute;
  font-size: 0.7rem;
  top: 1.5rem;
  transition: 0.25s ease;
}

.input-field {
  border: 0;
  z-index: 1;
  background-color: transparent;
  border-bottom: 2px solid #eee;
  font: inherit;
  font-size: 0.7rem;
}
.input-field:focus, .input-field:valid {
  outline: 0;
  border-bottom-color: #6658d3;
}
.input-field:focus + .input-label, .input-field:valid + .input-label {
  color: #6658d3;
  transform: translateY(-1.1rem);
}


.action {
  margin-top: 2rem;
}

.action-button {
  font: inherit;
  font-size: 1rem;
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