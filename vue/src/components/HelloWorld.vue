<template>
  <div class="hello">
    <h2 id="description">Description</h2>
    <p>A simple social media application that offers a real-time multi-user environment for users to document and share their daily-life happenings with their friends. Each user can post pictures with a title and caption, and can follow other users to get a personalized feed.</p>
    <h2 id="technologies-used">Technologies Used</h2>
    <ul>
    <li>HTML, CSS, Javascript, Vue CLI - Front-end presentation logic and scaffolding (View)</li>
    <li>Python, Flask - Back-end API declarations for database interactions (Controller)</li>
    <li>Flask SQLAlchemy - Database Management Module (Model)</li>
    <li>Flask JWT - Token-based Authentication</li>
    <li>Celery - Asynchronous workers to offload resource-heavy and timed jobs</li>
    <li>Redis - NoSQL backend used for Celery event management and caching</li>
    <li>Flask-mail, Jinja2, Weasyprint, Pandas - Jobs requiring user exports, bulk-emails, and time-scheduled actions</li>
    </ul>
    <h2 id="db-schema-design">DB Schema Design</h2>
    <img src="@/assets/dbschema.png" width="600px" alt="db_schema">
    <p>Every post has a unique user associated as its creator, A user can follow many other users, and vice versa. The schema also stores data regarding the users’ avatar (display picture) in the userinfo relation. To serve and realise the described context, the above schema has been idealised and implemented.</p>
    <h2 id="api-design">API Design</h2>
    <img src="@/assets/api_declaration.png" width="600px" alt="api_declaration">
    <h2 id="architecture-and-features">Architecture and Features</h2>
    <p>The project has a high-level split into the folders ”flask” and ”vue”, which house the front-end and back-end of the application respectively.</p>
    <h3 id="flask-back-end">Flask back-end</h3>
    <p>Running the app.py file is enough to fire-up the backend. It aggregates various features such as API declarations, database models, mail clients, cache, celery workers, etc. API classes are declared in different and appropriately named scripts, as designed in the previous section. In a similar fashion, other aforementioned features are also initialized in different files, which are then collectively packed and served on localhost by the main script. The posts folder houses the image files for posts uploaded to the app, and the templates folder consists of jinja2 templates for email generation.</p>
    <h3 id="vue-front-end">Vue front-end</h3>
    <p>The default project folder scaffolding provided by the Vue CLI setup is used. Components and Views are stored in the src/components and src/views folder respectively. The public folder consists of the backbone index.html where the entire app is served, and src/App.vue aggregates all views, components and front-end logic into the div with id app.</p>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
a {
  color: #42b983;
}
</style>
