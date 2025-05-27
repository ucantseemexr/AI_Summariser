// Navbar.vue
<template>
  <nav class="navbar">
    <div class="logo">AI Summariser</div>
    <ul class="nav-links">
      <li><a href="#">Home</a></li>
      <li><a href="#">Templates</a></li>
      <li><a href="#">API</a></li>
      <li><a href="#">About</a></li>
      <li><a href="#">Login/Signup</a></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'NavbarComponent'
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.75rem;
  margin-bottom: 1.5rem;
}

.logo {
  font-weight: bold;
  font-size: 1.25rem;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 1.25rem;
}

.nav-links a {
  text-decoration: none;
  color: #007bff;
}
</style>
