/*
    OWL Imports etc...
 */
const { Component, mount, xml, useRef, onMounted, onRendered, onError, onWillStart, onPatched, useState, reactive, useEnv, whenReady } = owl;
function useStore() {
    const env = useEnv();
    return useState(env.store);
}




$(document).ready(function(){


});
