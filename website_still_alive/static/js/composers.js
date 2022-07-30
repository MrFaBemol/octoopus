// Setup code
function composerPanelSetup() {
    let node = $('ComposerPanel')[0];
    if (node){
        const env = { store: createComposerStore() };
        mount(ComposerPanel, node, { env: env });
    }
}

whenReady(composerPanelSetup);


// -------------------------------------------------------------------------
// Store
// -------------------------------------------------------------------------
function createComposerStore() {
  return reactive(new ComposerList());
}


class ComposerList {
    composers = [];
    active_composers = [];

    results_count = 0;
    results_min = 0;
    results_max = 0;

    page_limit = 30;
    page_current = 0;
    page_max = 0;

    changePage(delta){
        this.page_current = Math.max(Math.min(this.page_current+delta, this.page_max), 1);
        this.active_composers = this.composers.slice(this.page_limit*(this.page_current-1), this.page_limit*this.page_current);
        this.results_min = 1 + (this.page_limit * (this.page_current-1));
        this.results_max = this.results_min + this.active_composers.length - 1;
    }
    nextPage() { this.changePage(1); }
    prevPage() { this.changePage(-1); }

    async fetchComposerList(){
        let res = await callApi(
            '/api/composer/search',
            {"fields": ['id', 'slug_url', 'name', 'first_name', 'birth', 'death', 'portrait_url', 'work_qty']},
        );
        let page_ratio = res.result.data_count/this.page_limit;
        this.page_max += Number.isInteger(page_ratio) ? page_ratio : Math.floor(page_ratio)+1;
        this.composers = res.result.data;
        this.results_count = res.result.data_count;
        this.nextPage();
    }

}





class ComposerCard extends Component{
    static template = xml`
<div class="oo_composer_card" t-attf-style="background-image:url('{{props.composer.portrait_url}}');">
    <a t-attf-href="/what/composer/{{props.composer.slug_url}}"><span class="oo_composer_card_link" /></a>
    <div class="oo_composer_card_infos">
        <div class="name" >
            <a t-attf-href="/what/composer/{{props.composer.slug_url}}" class="oo_composer_card_link">
                <t t-esc="props.composer.name"/>, <t t-esc="props.composer.first_name"/>
            </a>
        </div>
        <div class="infos">#<t t-esc="props.composer.id"/> - <t t-esc="props.composer.work_count"/> works</div>
    </div>
</div>
`;

    static props = ["composer"];
    setup(){
        this.store = useStore()
    }
}



/**
 * Composers Grid
 */
class ComposerGrid extends Component {
    static template = xml`
<div class="oo_what_composer_grid">
    <t t-foreach="store.active_composers" t-as="composer" t-key="composer.id">
        <ComposerCard composer="composer" />
    </t>
</div>
`;

    static components = { ComposerCard };


    setup(){
        this.store = useStore()

        onMounted((e) => {
            this.store.fetchComposerList()
        });
    }


}





class ComposerFilter extends Component{
    static template = xml`
<div class="col-md-auto oo_what_composers_filters">
    <div class="form-group mux">
        <input type="text" class="form-control" id="name_search" />
        <label for="name_search">Name</label>
    </div>
    
</div>
`;
}


class ComposerOrderingTopBar extends Component{
    static template = xml`
<div class="row oo_what_composer_top_bar flex-gap">
    <div class="oo_what_composer_top_bar_results col-2">
        Results: 
        <span class="results_min_page"><t t-esc="store.results_min" /></span> -
        <span class="results_max_page"><t t-esc="store.results_max" /></span> /
        <span class="results_count"><t t-esc="store.results_count" /></span>
    </div>

    <div class="col oo_center_horizontal oo_what_composer_top_bar_pagination">
        <a href="#" class="prev_page" t-on-click="() => this.store.prevPage()">&lt;</a>
        Page: <span class="current_page"><t t-esc="store.page_current" /></span> / <span class="total_page"><t t-esc="store.page_max" /></span>
        <a href="#" class="next_page" t-on-click="() => this.store.nextPage()">&gt;</a>
    </div>

    <div class="col-4">
        <div class="row gap1 oo_center_vertical oo_center_horizontal oo_what_composer_top_bar_order_by ">
            <div class="col input-field">
                <select name="order_by" id="order_by" placeholder="Sort by...">
                    <option value="default">Default (popular first)</option>
                    <option value="name">Name</option>
                    <option value="works_quantity">Works quantity</option>
                    <option value="birth">Birth date</option>
                    <option value="death">Death date</option>
                </select>
                <label>Order By</label>
            </div>

            <div class="mux form-check double-label">
                <span>Asc.</span>
                <input type="checkbox" class="form-check-input" id="exampleCheck2" />
                <label class="form-check-label" for="exampleCheck2" />
                <span>Desc.</span>
            </div>
            
        </div>
    </div>
</div>
`;
    setup(){
        this.store = useStore()
    }
}
class ComposerOrderingBottomBar extends Component{
    static template = xml`
<div class="row oo_what_composer_bottom_bar flex-gap">
    <div class="col-2 oo_what_composer_top_bar_results">
        Results: <span class="results_min_page">0</span> - <span class="results_max_page">0</span> / <span class="results_count">0</span>
    </div>

    <div class="col oo_center_horizontal oo_what_composer_top_bar_pagination">
        <a href="#" class="prev_page">&lt;</a>
        Page: <span class="current_page">-</span> / <span class="total_page">-</span>
        <a href="#" class="next_page">&gt;</a>
    </div>

    <div class="col-4"> </div>
</div>
`;
}



class ComposerPanel extends Component{
    static template = xml`
<div class="oo_row">
    <ComposerFilter />
    <div class="col">
        <ComposerOrderingTopBar />
        <ComposerGrid />
        <ComposerOrderingBottomBar />
    </div>
</div>
`;

    static components = { ComposerFilter, ComposerOrderingTopBar, ComposerOrderingBottomBar, ComposerGrid };
}





