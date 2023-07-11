import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomeViews.vue'
import Analysis1 from '../views/Analysis1Views.vue'
import Analysis2 from '../views/Analysis2Views.vue'
import Analysis3 from '../views/Analysis3Views.vue'
import Analysis4 from '../views/Analysis4Views.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: Home 
        }
        ,   
        {
            path: '/analysis1',
            component: Analysis1        
        }
        ,
        {
            path: '/analysis2',
            component: Analysis2      
        }
        ,
        {
            path: '/analysis3',
            component: Analysis3  
        }
        ,
        {
            path: '/analysis4',
            component: Analysis4 
        }
    ]
})

export default router