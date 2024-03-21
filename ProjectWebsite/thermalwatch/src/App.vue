<script setup>
import {RouterView} from "vue-router"
</script>

<template>
  <main>
    <div class="nav-container">
      <h1><a href="/" style="color: #FF208D">ThermalWatch</a></h1>
      <ul class="nav">
        <li class="item"><a href="/">Home</a></li>
        <li class="item"><a href="/about">About</a></li>
        <li class="item"><a href="/references">References</a></li>
        <li class="item"><a href="/account">Account</a></li>
      </ul>
    </div>
    <RouterView/>
  </main>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Balsamiq+Sans:ital,wght@0,400;0,700;1,400;1,700&display=swap');

a {
  text-decoration: none;
  color: #FF53A7;
  transition: 400ms cubic-bezier(0.7, -0.6, 0.3, 1.2) letter-spacing;
  font-family: 'Balsamiq Sans', sans-serif;
}
h1 {
  color: #FF208D;
  margin: 0%;
  font-family: 'Balsamiq Sans', sans-serif;
}

.container {
  width: 100vw;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: linear-gradient(160deg, #0093e9 0%, #80d0c7 100%);
}

.nav-container {
  display: flex;
  padding: 16px 0px 16px 16px;
  justify-content: space-between;
}

.nav {
  list-style: none;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color:white;
  margin: 0;
  width: 50%;
}

.item a {
  position: relative;
  user-select: none;
  font-size: 20px;
  text-transform: uppercase;
  cursor: pointer;
  margin: 0 20px;
}

.item a:before {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 0px;
  width: 100%;
  height: 2px;
  background: #FF53A7;
  transform: scaleX(0);
  transition: 400ms cubic-bezier(0.7, -0.6, 0.3, 1.2) transform;
}

.item a:hover {
  letter-spacing: 2px;
}

.item a:hover:before {
  transform: scaleX(1);
}
</style>