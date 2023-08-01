/** @odoo-module **/
const { Component, whenReady, onMounted, useRef, useState, onPatched, onWillUnmount, onWillDestroy,onWillRender, onRendered } = owl;
import { setupAndMount } from '@website_octoopus/js/owl'

whenReady(() => setupAndMount(DynamicPlaceholderInput));


export class DynamicPlaceholderInput extends Component {
    _id = "dpi";
    inputRef = useRef("input");

    setup() {

        this.state = useState({
            currentPlaceholderIndex: 0,
            currentCharIndex: 0,
            isDeleting: false,
        });

        onMounted(async () => {
            this.placeholders = await this.getPlaceholderValues();
            if (this.placeholders.length) {
                this._runTyping();
            }
        });

        onWillDestroy(() => {clearTimeout(this.timer)})
    }

    async getPlaceholderValues(){
        console.error(this.constructor.name + ".getPlaceholderValues() is not implemented!");
        return [];
    }
    getRandomDelay(min, max) {
        return Math.random() * (max - min) + min;
    }

    _runTyping() {
        let currentPlaceholder = this.placeholders[this.state.currentPlaceholderIndex];
        let typingSpeed = this.state.isDeleting ? this.getRandomDelay(5, 20) : this.getRandomDelay(10, 80);

        this.state.currentCharIndex += this.state.isDeleting ? -1 : 1;

        this.inputRef.el.placeholder = currentPlaceholder.slice(0, this.state.currentCharIndex);

        if (this.state.currentCharIndex === currentPlaceholder.length) {
            this.state.isDeleting = true;
            setTimeout(() => {this._runTyping()}, 2000);
        } else if (this.state.currentCharIndex === 0) {
            this.state.isDeleting = false;
            this.state.currentPlaceholderIndex = (this.state.currentPlaceholderIndex + 1) % this.placeholders.length;
            setTimeout(() => {this._runTyping()}, 1500);
        } else {
            setTimeout(() => {this._runTyping()}, typingSpeed);
        }
    }

}

DynamicPlaceholderInput.template = "website_octoopus.DynamicPlaceholderInput";


