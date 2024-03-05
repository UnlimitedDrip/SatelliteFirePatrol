import {createRouter, createWebHistory} from "vue-router"
import HomeView from "../views/HomeView.vue"
import AboutView from "../views/AboutView.vue"
import AccountView from "../views/AccountView.vue"
import ReferencesView from "../views/ReferencesView.vue"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "home",
            component: HomeView
        },
        {
            path:"/about",
            name: "about",
            component: AboutView
        },
        {
            path:"/account",
            name: "account",
            component: AccountView
        },
        {
            path:"/references",
            name: "references",
            component: ReferencesView
        }
    ]
})

export default router