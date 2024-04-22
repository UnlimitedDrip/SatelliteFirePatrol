<script setup>
import { defineProps } from 'vue';

    defineProps({
        alertArr: Array
    });

    let boundingBox = "Bounding Box"

</script>

<template>

    <table>
        <thead>
            <th>Alert</th>
            <th>Temperature Threshold</th>
            <th>Bounding Box</th>
        </thead>
        <tbody>
            <tr v-for="(alert, i) in alertArr" :key="alert.id">
                <td>
                    {{ i + 1 }}
                </td>
                <td>
                    {{ alert["Temperature Threshold"] }}
                </td>
                <td v-for="value in alert[boundingBox]" :key="value.id">
                    {{ value + " " }}
                </td>
                <td>
                    <button @click="$emit('removeAlert', alert)">Delete</button>
                </td>
            </tr>
        </tbody>
    </table>

</template>

<script>
export default {
  data() {
    return {
        
    };
  },
    methods: {
  }
}

</script>