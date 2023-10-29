/** @odoo-module **/
const { whenReady, Component, onMounted } = owl;
import { setupAndMount } from '@website_octoopus/js/owl'

whenReady(() => setupAndMount(FlowbiteScript));


export class FlowbiteScript extends Component {
    setup() {
        onMounted(() => {
            console.log("FlowbiteScript mounted");
        });
    }
}
FlowbiteScript.components = { };
FlowbiteScript.template = 'website_octoopus.FlowbiteScript';
