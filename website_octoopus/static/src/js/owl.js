/** @odoo-module **/
const { App, Component, mount, xml, useRef, onMounted, onRendered, onError, onWillStart, onPatched, useState, reactive, useEnv, whenReady } = owl;
import { templates } from '@web/core/assets';

const devMode = true;

function useStore() {
    const env = useEnv();
    return useState(env.store);
}



export function setupAndMount(component) {
    let promisesList = [];
    $(component.name).each((i, node) => {
        // Give access to props in template (<node props-test-example="foobar" /> will init component with props.testExample = "foobar";)
        let propsData = {nodeIndex: i};
        let propsList = node.getAttributeNames().filter(att => att.startsWith("props-"));
        propsList.forEach((e) => {
            let keyElements = e.replace('props-', '').split("-");
            let key = keyElements[0] + keyElements.slice(1).map((e) => e.charAt(0).toUpperCase() + e.slice(1)).join("");
            propsData[key] = node.getAttribute(e);
        });

        let app = new App(
            component,
            {
                env: {},
                props: propsData,
                templates: templates,
                dev: devMode,
                translateFn: Component.env._t,
                translatableAttributes: ["data-tooltip"],
            },
        );
        promisesList.push(app.mount(node));
    });
    return Promise.all(promisesList);
}


export function loadScript(src, onload) {
  let script = document.createElement('script');
  script.onload = onload ? onload : function(e) {
      console.log(e.target.src + ' is loaded.');
    };
  script.src = src;
  script.async = false;
  document.body.appendChild(script);
}



$(document).ready(function(){
    console.log("Document ready");
    // loadScript('/website_octoopus/static/lib/flowbite.min.js');

});