<template>
    <nav>
        <v-app-bar
                app
                color="primary"
                short
                collapse-on-scroll
        >

            <v-app-bar-nav-icon class="black--text" @click="isLeftDrawerOpened = !isLeftDrawerOpened"/>

            <v-toolbar-title class="text-uppercase black--text">
                <v-icon class="black--text" left>mdi-camera</v-icon>
                <span class="font-weight-bold">PARKER</span>
            </v-toolbar-title>

            <v-spacer></v-spacer>

<!--            <v-toolbar-items>-->
<!--                <v-btn @click="isRightDrawerOpened = !isRightDrawerOpened" color="primary" rounded depressed>-->
<!--                    <v-icon class="black&#45;&#45;text">settings</v-icon>-->
<!--                </v-btn>-->
<!--            </v-toolbar-items>-->

        </v-app-bar>

        <v-navigation-drawer
                v-model="isLeftDrawerOpened"
                app
                left
                color="primary"
        >
            <v-list
                    color="primary"

            >
                <v-list-item v-for="link in links" :key="link.route" router :to="link.route">
                    <v-list-item-action>
                        <v-icon class="black--text">{{ link.icon }}</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title class="font-weight-bold">{{ link.title }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>

        </v-navigation-drawer>

<!--        <v-navigation-drawer-->
<!--                v-model="isRightDrawerOpened"-->
<!--                app-->
<!--                right-->
<!--                class="pa-5"-->
<!--                color="primary"-->

<!--        >-->

<!--            <v-text-field-->
<!--                    v-model="timeToAccept"-->
<!--                    required-->
<!--                    color="black"-->
<!--                    class="black&#45;&#45;text"-->
<!--                    type="number"-->
<!--                    label="Seconds to accept">-->
<!--                <v-icon slot="prepend" color="black" left>alarm</v-icon>-->

<!--            </v-text-field>-->

<!--        </v-navigation-drawer>-->
    </nav>
</template>

<script>
    export default {
        name: "NavBar",

        data: () => {
            return {
                timeToAccept: 30,
                isLeftDrawerOpened: false,
                isRightDrawerOpened: false,
                links: [
                    {icon: 'dashboard', title: 'Dashboard', route: '/'}
                ]
            }
        }
    }
</script>

<style scoped>

</style>