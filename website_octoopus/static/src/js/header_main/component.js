/** @odoo-module **/
const { whenReady, Component, onMounted } = owl;
import { setupAndMount, loadScript } from '@website_octoopus/js/owl';
// import { initFlowbite } from "flowbite";
import { Flowbite } from '@website_octoopus/lib/flowbite';
// import { Flowbite } from '@website_octoopus/lib/flowbite.min';



whenReady(() => setupAndMount(HeaderMain));


export class HeaderMain extends Component {
    setup() {
        onMounted(() => {
            console.log("Header mounted");
            console.log(Flowbite);
            // loadScript('/website_octoopus/static/lib/flowbite.min.js');
            // initFlowbite();
        });
    }
}

HeaderMain.components = { };
HeaderMain.template = 'website_octoopus.HeaderMain';
