/** @odoo-module **/
const { whenReady, Component, onMounted } = owl;
import { setupAndMount } from '@website_octoopus/js/owl'

whenReady(() => setupAndMount(FooterMain));


export class FooterMain extends Component {
    setup() {
        onMounted(() => {
            console.log("Footer mounted");
        });
    }
}
FooterMain.components = { };
FooterMain.template = 'website_octoopus.FooterMain';
