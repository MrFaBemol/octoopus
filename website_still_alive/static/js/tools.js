/*
    OWL Imports etc...
 */
const { Component, mount, xml, useRef, onMounted, onRendered, onError, onWillStart, onPatched, useState, reactive, useEnv, whenReady } = owl;
function useStore() {
    const env = useEnv();
    return useState(env.store);
}

/*
    Standard method to call the api
    No need to pass a token as the request comes from local server.
    Todo: Check when in prod! The request could come from BROWSER (rip)
 */
function callApi(url, data) {
    return $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
    });
}


// Misc
function enableNode(nodeName){$(nodeName).removeClass("disabled")}
function disableNode(nodeName){$(nodeName).addClass("disabled")}

// Array helpers
Array.prototype.sorted = function(key, reverse=false){
    let keys = key.split(".");
    if (keys.length > 0){
        let sortedArray = this.sort( (a, b) => {
            for (let i = 0; i < keys.length; i++){
                a = a[keys[i]];
                b = b[keys[i]];
            }
            let res = (a > b) ? 1 : ((b > a) ? -1 : 0);
            return reverse ? -1*res : res;
        });
        this.splice(0, sortedArray.length, ...sortedArray);
    }
    return this;
};