<template>
    <v-app id="inspire">
        <v-navigation-drawer
                v-model="drawer"
                app
                clipped
        >
            <v-list dense>
                <v-list-item to="/" link>
                    <v-list-item-action>
                        <v-icon>mdi-view-dashboard</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Dashboard</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>

                <v-list-item to="Camera" link>
                    <v-list-item-action>
                        <v-icon>mdi-camera</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Camera</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>

                <v-list-item to="settings" link>
                    <v-list-item-action>
                        <v-icon>mdi-settings</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Settings</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar
                app
                clipped-left
        >
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
            <v-toolbar-title>Parker</v-toolbar-title>
        </v-app-bar>

        <v-content>
            <v-container
                    fluid
            >

                <transition name="slide">
                    <router-view/>
                </transition>
            </v-container>
        </v-content>

    </v-app>
</template>

<script>
    export default {
        props: {
            source: String,
        },

        data: () => ({
            drawer: null,
        }),

        created() {
            this.$vuetify.theme.dark = true
        },
    }
</script>