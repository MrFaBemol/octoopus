// Setup code
function workSearchPanelSetup() {
    let node = $('WorkSearchPanel')[0];
    if (node){
        const env = { store: createWorkStore() };
        mount(WorkSearchPanel, node, { env: env });
    }
}

whenReady(workSearchPanelSetup);




// -------------------------------------------------------------------------
// Store
// -------------------------------------------------------------------------
function createWorkStore() {
  return reactive(new WorkStore());
}


/*********************************************
**                   STORE
**********************************************/

class WorkStore {
    // General (mode, autocomplete, ...)
    mode = "";
    instruments = [];
    composers = [];
    autocompleteFocus = -1;
    // Search by name
    name_search = "";
    name_search_works = [];
    // Search by instrument
    instrument_search_works = [];
    instrument_qty = 0;
    instrument_slots = [];

    changeMode(ev){ this.mode = typeof ev == "string" ? ev : ev.target.name; }
    focusNextSlot(){
        this.autocompleteFocus++;
        if (this.autocompleteFocus === this.instrument_slots.length){
            this.addInstrumentSlot();
        }
    }
    focusPreviousSlot(){
        if (this.autocompleteFocus === 0){
            this.autocompleteFocus = this.instrument_slots.length - 1;
        } else {
            this.autocompleteFocus--;
        }
    }

    // Initial fetching
    async fetchComposerList(){
        let res = await callApi(
            '/api/composer/search',
            {"fields": ['id', 'display_name']},
        );
        // console.log(res);
        this.composers = res.result.data;
    }
    async fetchInstrumentList(){
        let res = await callApi(
            '/api/instrument/search',
            {
                "fields": ['id', 'display_name', 'name', 'is_category', 'is_ensemble', 'is_accompaniment'],
            },
        );
        // console.log(res);
        this.instruments = res.result.data;
    }

    // Searches
    async searchWorksByName(search){
        let res = await callApi('/api/work/search',{"search": search, "related_fields": {"composer_id": ["full_name", "slug_url"]}});
        this.name_search = search;
        this.name_search_works = res.result.data.sorted("composer_id.full_name");
    }

    async searchWorksByInstrument(){
        disableNode("div.oo_what_work_search_panel");
        let res = await callApi('/api/workversion/search',{
            "instrument_slots": this.instrument_slots,
            "min_soloists_qty": this.instrument_slots.length,
            // "max_soloists_qty": this.instrument_slots.length,
        });
        enableNode("div.oo_what_work_search_panel");
    }

    // Getters
    getComposerIndexById(composer_id){
        composer_id = parseInt(composer_id);
        for (let i=0; i < this.composers.length; i++){
            if (this.composers[i].id === composer_id) return i;
        }
        return false;
    }
    getInstrumentById(instrument_id){
        instrument_id = parseInt(instrument_id);
        for (let i=0; i < this.instruments.length; i++){
            if (this.instruments[i].id === instrument_id) return this.instruments[i];
        }
        return {};
    }


    // Instrument slots management
    addInstrumentSlot(giveFocus = true){
        this.instrument_slots.push([]);
        if (giveFocus){this.autocompleteFocus = this.instrument_slots.length - 1;}
    }
    deleteInstrumentSlot(slotIndex){
        this.instrument_slots.splice(slotIndex, 1);
    }

    addInstrumentToSlot(slotIndex, instrument_id){
        if (!this.instrument_slots[slotIndex].includes(instrument_id)){
            this.instrument_slots[slotIndex].push(instrument_id);
        }
    }
    deleteInstrumentFromSlot(slotIndex, instrument_id){
        let instrumentIndex = this.instrument_slots[slotIndex].indexOf(instrument_id);
        if (instrumentIndex > -1){
            this.instrument_slots[slotIndex].splice(instrumentIndex, 1);
        }
    }



}


/*********************************************
**              SEARCH BY NAME
**********************************************/


class WorkSearchByName extends Component {
    static template = xml`
<div class="oo_what_work_search_by_name">
    <div><input placeholder="Enter your search" type="text" t-on-keyup="searchWorksByName" t-att-value="store.name_search" /></div>
    <div t-if="store.name_search_works.length > 0"><b>Total: <t t-esc="store.name_search_works.length"/> results</b></div>
    <table style="margin:10px" >
        <thead>
            <tr>
                <td>Composer</td>
                <td>Title</td>
            </tr>
        </thead>
        <tbody>
            <t t-foreach="store.name_search_works" t-as="work" t-key="work.id">
                <tr>
                    <td style="padding-right: 10px;">
                        <a t-attf-href="/what/composer/{{work.composer_id.slug_url}}"><t t-esc="work.composer_id.full_name"/></a>
                    </td>
                    <td style="padding-right: 5px;">
                        <t t-esc="work.title"/>
                    </td>
                </tr>
            </t>
        </tbody>
    </table>
</div>
`;

    setup(){this.store = useStore();}

    searchWorksByName(ev) {
        if (ev.keyCode === 13) {
            this.store.searchWorksByName(ev.target.value)
        }
    }

}

/*********************************************
**            SEARCH BY INSTRUMENT
**********************************************/



class InstrumentSlot extends Component {
    setup(){
        this.store = useStore();
        $(document).on('click', (ev) => {
            const html = $("html")[0];
            if ($(ev.target).parentsUntil("span.autocomplete").last()[0] == html){
                this.closeAllAutocompleteList();
            }
        })
    }
    static props = ["slot", "index"];
    autocompleteSuggestions = useState([]);
    state = useState({open: true, currentIndex: -1});

    static template = xml`
<div class="oo_instrument_slot" t-att-id="props.index">
    <span style="padding:5px;"><i class="fa fa-trash" t-on-click="() => store.deleteInstrumentSlot(props.index)" /></span>
    <span># <t t-esc="props.index + 1" /></span>
    <span class="autocomplete">
        <input id="searchInstrumentInput" type="text" placeholder="Start typing..."
            t-attf-class="{{state.open ? 'open' : 'closed'}}"
            t-on-input="searchInstrument"
            t-on-focus="openAutocompleteList"
            t-on-keydown="onKeyDown" />
        <div id="autocomplete-list" t-attf-class="autocomplete-items {{!state.open ? 'invisible' : ''}} ">

            <div t-foreach="autocompleteSuggestions" t-as="suggestion" t-key="suggestion.id"
                 t-attf-class="oo_autocomplete_suggestion {{suggestion_index == state.currentIndex ? 'autocomplete-active' : ''}}"
                 t-att-id="suggestion.id"
                 t-on-click="selectInstrument" >
                    <t t-esc="suggestion.display_name" /><t t-if="suggestion.is_category">*</t>
            </div>

        </div>
    </span>
    
    <span class="oo_slot_instruments">
        <span t-foreach="props.slot" t-as="instrument_id" t-key="instrument_id"
            class="mdl-chip mdl-chip--contact mdl-chip--deletable"
            t-att-id="instrument_id" >
                <t t-set="instrument" t-value="store.getInstrumentById(instrument_id)" />
                <img class="mdl-chip__contact" src="/website_still_alive/static/img/icons/confused.png" />
                <span class="mdl-chip__text" t-att-title="instrument.display_name"><t t-esc="instrument.name"/><t t-if="instrument.is_category">*</t></span>
                <a class="mdl-chip__action" t-on-click="deleteInstrument" ><i class="fa fa-trash" /></a>
        </span>
    </span>
</div>
`;


    onKeyDown(ev){
        if (ev.keyCode === 40) {                                                                // Down
            if (this.state.currentIndex >= this.autocompleteSuggestions.length-1){
                this.state.currentIndex = 0;
            } else{
                this.state.currentIndex++;
            }
        } else if (ev.keyCode === 38) {                                                         // Up
            if (this.state.currentIndex <= 0){
                this.state.currentIndex = this.autocompleteSuggestions.length - 1;
            } else{
                this.state.currentIndex--;
            }
        } else if (ev.keyCode === 13 && this.state.currentIndex > -1) {                         // Enter
            ev.preventDefault();
            this.getAutocompleteListNode(ev).find("div")[this.state.currentIndex].click();
        } else if (ev.keyCode === 27){                                                          // Escape
            this.closeSuggestions();
        } else if (ev.keyCode === 9){                                                           // Tab
            ev.preventDefault();
            if (ev.shiftKey){
                this.store.focusPreviousSlot();
            } else {
                this.store.focusNextSlot();
            }
        }
    }


    //Getter
    getInputNode(ev){return $(ev.target).parentsUntil("div.oo_instrument_slot").find("input#searchInstrumentInput");}
    getAutocompleteListNode(ev){return $(ev.target).parentsUntil("div.oo_instrument_slot").find("div#autocomplete-list");}
    getSlotNode(index){return $(".oo_what_work_search_panel").find("div.oo_instrument_slot#" + index.toString());}
    getStoreSlot(){return this.store.instrument_slots[this.props.index];}

    // Helpful methods
    openSuggestions(){this.state.open = this.autocompleteSuggestions.length > 0;}
    closeSuggestions(){this.state.open = false;}
    cleanSuggestions(){this.autocompleteSuggestions.splice(0, this.autocompleteSuggestions.length);}

    resetCurrentIndex(){this.state.currentIndex = this.autocompleteSuggestions ? 0 : -1;}
    cleanInput(ev){this.getInputNode(ev).val("");}


    closeAllAutocompleteList(){
        // To rerender the current list if needed
        this.closeSuggestions()
        // Close all autocomplete lists, so we have to use $(document)
        $(document).find(".autocomplete-items").addClass("invisible");
    }

    // Open items for only selected input (on focus)
    openAutocompleteList(){
        // Todo: change currentFocus
        this.closeAllAutocompleteList();
        this.resetCurrentIndex();
        this.openSuggestions();
    }

    // Filter store.instruments and save results in suggestions
    searchInstrument(ev){
        let val = ev.target.value;
        if (!val || val.length < 3){
            this.cleanSuggestions();
            return false;
        }

        // Filter by name + exclude already chosen instruments in slot
        const re = new RegExp(val, 'i');
        let currentSlot = this.getStoreSlot();
        let suggestions = this.store.instruments.filter(i => re.test(i.name)).filter(i => !currentSlot.includes(i.id.toString()));

        // Show real instruments first
        suggestions.sorted("is_accompaniment");
        suggestions.sorted("is_category");

        this.autocompleteSuggestions.splice(0, this.autocompleteSuggestions.length, ...suggestions);
        this.resetCurrentIndex();
        this.openSuggestions();
    }

    selectInstrument(ev){
        this.store.addInstrumentToSlot(this.props.index, $(ev.target).attr('id'));
        this.cleanInput(ev);
        this.cleanSuggestions();
        this.getInputNode(ev).focus();
        this.openAutocompleteList(ev);
    }

    deleteInstrument(ev){
        let instrument_id = $(ev.target).parentsUntil(".mdl-chip").parent().attr('id');
        this.store.deleteInstrumentFromSlot(this.props.index, instrument_id);
    }


}



class WorkSearchByInstrument extends Component {
    setup(){
        this.store = useStore();
        onMounted( (e) => {
            if (this.store.instrument_slots.length === 0){this.store.addInstrumentSlot();}
        });
        onPatched( (e) => {
            let node = $(`div.oo_instrument_slot#${this.store.autocompleteFocus}`).find("input#searchInstrumentInput");
            node.focus();
        });
    }
    static components = { InstrumentSlot };

    static template = xml`
<div class="oo_what_work_search_by_instrument">
    <button t-on-click="() => this.store.addInstrumentSlot()">Add slot</button>
    <button t-on-click="() => this.store.searchWorksByInstrument()">Show slots</button>
    <div class="oo_instrument_slots">
        <InstrumentSlot t-foreach="store.instrument_slots" t-as="slot" t-key="slot_index" slot="slot" index="slot_index" />
    </div>
    
</div>
`;

}




class WorkSearchPanel extends Component{
        static template = xml`
<div class="oo_what_work_search_panel disabled">
    <div class="oo_row oo_center_horizontal oo_what_work_mode_buttons" >
        <button name="name_search" t-attf-class="{{store.mode === 'name_search' ? 'active_mode': ''}}" t-on-click="(ev) => this.store.changeMode(ev)">
            Search by name
        </button>
        <button name="instrument_search" t-attf-class="{{store.mode === 'instrument_search' ? 'active_mode': ''}}" t-on-click="(ev) => this.store.changeMode(ev)">
            Search by instruments
        </button>
    </div>
    
    
    <WorkSearchByName t-if="store.mode === 'name_search'" />
    <WorkSearchByInstrument t-if="store.mode === 'instrument_search'" />
</div>
`;

    static components = { WorkSearchByName, WorkSearchByInstrument };
    setup(){
        this.store = useStore();
        onMounted( async (e) => {
            await this.store.fetchComposerList();
            await this.store.fetchInstrumentList();
            enableNode("div.oo_what_work_search_panel");
            this.store.changeMode("instrument_search");
        });
    }


}

// WorkSearchPanel.template = 'website_still_alive.WorkSearchPanel';

