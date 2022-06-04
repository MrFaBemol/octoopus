// Setup code
function workSearchPanelSetup() {
    const env = { store: createWorkStore() };
    mount(WorkSearchPanel, $('WorkSearchPanel')[0], { env: env });
}

whenReady(workSearchPanelSetup);


// -------------------------------------------------------------------------
// Store
// -------------------------------------------------------------------------
function createWorkStore() {
  return reactive(new WorkStore());
}


class WorkStore {
    mode = "";
    works = [];

    changeMode(ev){
        this.mode = ev.target.name;
        $('.oo_what_work_mode_buttons').children().removeClass("active_mode");
        $(ev.target).addClass("active_mode");
        ev.target.blur();

    }

    async searchWorksByName(search){
        let res = await callApi('/api/work/search',{"search": search, "related_fields": {"composer_id": ["full_name", "slug_url"]}});
        this.works = res.result.data.sorted("composer_id.full_name");
    }

}


class WorkSearchByName extends Component {
    static template = xml`
<div class="oo_what_work_search_by_name">
    <div><input placeholder="Enter your search" type="text" t-on-keyup="searchWorksByName" /></div>
    <div t-if="store.works.length > 0"><b>Total: <t t-esc="store.works.length"/> results</b></div>
    <table style="margin:10px" >
        <thead>
            <tr>
                <td>Composer</td>
                <td>Title</td>
            </tr>
        </thead>
        <tbody>
            <t t-foreach="store.works" t-as="work" t-key="work.id">
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

    setup(){
        this.store = useStore()
    }

    searchWorksByName(ev) {
        if (ev.keyCode === 13) {
            this.store.searchWorksByName(ev.target.value)
        }
    }

}




class WorkSearchPanel extends Component{
        static template = xml`
<div class="oo_what_work_search_panel">
    <div class="oo_row oo_center_horizontal oo_what_work_mode_buttons" >
        <button name="search_by_name" t-on-click="changeMode">Search by name</button>
        <button name="search_by_instruments" t-on-click="changeMode">Search by instruments</button>
    </div>
    
    
    <WorkSearchByName t-if="store.mode === 'search_by_name'" />
</div>
`;

    static components = { WorkSearchByName };
    setup(){
        this.store = useStore()
    }


    changeMode(ev){
        this.store.changeMode(ev);
    }

}