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



    goToPage(pageNum){
        if (pageNum < 1){ pageNum = 1;}
        if (pageNum > this.page_max){ pageNum = this.page_max;}

        this.page_current = pageNum;
        this.active_composers = this.composers.slice(this.page_limit*(this.page_current-1), this.page_limit*this.page_current);
        this.results_min = 1 + (this.page_limit * (this.page_current-1));
        this.results_max = this.results_min + this.active_composers.length - 1;
    }
    nextPage() { this.goToPage(this.page_current+1); }
    prevPage() { this.goToPage(this.page_current-1); }


    async fetchComposerList(){
        let res = await callApi(
            '/api/composer/search',
            {
                "fields": ['id', 'slug_url', 'name', 'first_name', 'birth', 'display_date', 'portrait_url', 'work_qty', 'period_id'],
                "related_fields": {"period_id": ["color_material", "date_start"]},
            },
        );
        console.log(res);

        let page_ratio = res.result.data_count/this.page_limit;
        this.page_max += Number.isInteger(page_ratio) ? page_ratio : Math.floor(page_ratio)+1;
        this.composers = res.result.data.sorted('period_id.date_start');
        this.results_count = res.result.data_count;
        this.nextPage();
    }

}





class ComposerCard extends Component{
    static template = xml`
<li class="oo_composer_card_item" >
    <article t-attf-class="material-card {{props.composer.period_id.color_material}}">
        <a t-attf-href="/what/composer/{{props.composer.slug_url}}">
            <h2>
                <span><t t-esc="props.composer.name"/>, <t t-esc="props.composer.first_name"/></span>
                <strong>
    <!--                <i class="fa fa-fw fa-star"></i>-->
    <!--                The Spanish Guy-->
                    (<t t-esc="props.composer.display_date"/>)
                </strong>
            </h2>
        </a>
        <div class="mc-content">
            <div class="img-container" t-attf-style="background-image:url('{{props.composer.portrait_url}}');" />
            <div class="mc-description">
                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            </div>
        </div>
        <a class="mc-btn-action" t-on-click="toggleActive">
            <i class="fa fa-bars"></i>
        </a>
        <div class="mc-footer">
            <h4>
                Social
            </h4>
            <a class="fa fa-fw fa-facebook"></a>
            <a class="fa fa-fw fa-twitter"></a>
            <a class="fa fa-fw fa-linkedin"></a>
            <a class="fa fa-fw fa-google-plus"></a>
        </div>
    </article>
</li>
`;

    static props = ["composer"];
    setup(){
        this.store = useStore()
    }

    toggleActive(ev){
        let card = $(ev.target).parentsUntil(".oo_composer_card_item").last();
        let icon = card.find('i');
        let removedClass = '';
        let addedClass = '';
        icon.addClass('fa-spin-fast');

        if (card.hasClass('mc-active')) {
            removedClass = 'fa-arrow-left';
            addedClass = 'fa-bars';
        } else {
            addedClass = 'fa-arrow-left';
            removedClass = 'fa-bars';
        }
        card.toggleClass('mc-active');
        window.setTimeout(function() {
            icon.removeClass(removedClass).removeClass('fa-spin-fast').addClass(addedClass);
        }, 300);
    }
}



/**
 * Composers Grid
 */
class ComposerGrid extends Component {
    static template = xml`
<!--<div class="oo_what_composer_grid">-->
<ul class="oo_composer_cards_TMP">
    <t t-foreach="store.active_composers" t-as="composer" t-key="composer.id">
        <ComposerCard composer="composer" />
    </t>
</ul>
<!--</div>-->
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
    <h3>Filters</h3>

    <div class="mux form-group">
        <input type="text" class="form-control" id="name_search" />
        <label for="name_search">Name</label>
    </div>
    
    <div class="mux form-check">
        <input type="checkbox" class="form-check-input" id="is_popular" />
        <label class="form-check-label" for="is_popular" />
        <span>Popular</span>
    </div>
    
    <div class="mux form-check">
        <input type="checkbox" class="form-check-input" id="is_essential" />
        <label class="form-check-label" for="is_essential" />
        <span>Essential</span>
    </div>
    
        
    

    <fieldset>
        <legend>Dates</legend>
            <div class="label-input-double">
                <span>
                    <i class="material-icons prefix">child_care</i>
                    <label>Birth</label>
                </span>
                <div class="input-field inline small">
                    <input id="min_birth" type="text" class="validate" maxlength="4" size="1" />
                    <label for="min_birth">Min</label>
                </div>
                <div class="input-field inline small">
                    <input id="max_birth" type="text" class="validate" maxlength="4" size="1" />
                    <label for="max_birth">Max</label>
                </div>
            </div>

            <div class="label-input-double">
                <span>
                    <i class="material-icons prefix">elderly</i>
                    <label>Death</label>
                </span>
                <div class="input-field inline small">
                    <input id="min_death" type="text" class="validate" maxlength="4" size="1" />
                    <label for="min_death">Min</label>
                </div>
                <div class="input-field inline small">
                    <input id="max_death" type="text" class="validate" maxlength="4" size="1" />
                    <label for="max_death">Max</label>
                </div>
            </div>
    </fieldset>
    
    
</div>
`;
}


class ComposerOrderingTopBar extends Component{
    static template = xml`
<div class="row oo_what_composer_top_bar flex-gap">
    <div class="oo_what_composer_top_bar_results col-2">
        Results: 
        <span class="results_min_page"><t t-esc="store.results_min" /></span> -
        <span class="results_max_page"><t t-esc="store.results_max" /></span>/
        <span class="results_count"><t t-esc="store.results_count" /></span>
    </div>

    <nav aria-label="Page navigation example" class="oo_center_horizontal">
        <ul class="pagination">
            <li class="page-item">
                <a class="page-link" href="#" aria-label="Previous" t-on-click="() => this.store.prevPage()">
                    <i class="fa fa-angle-double-left" />
                </a>
            </li>
            
            <li t-foreach="Array.from({length: this.store.page_max}, (_, i) => i + 1)" t-as="i" t-key="i"
                t-attf-class="page-item {{ store.page_current == i ? 'active' : '' }}">
                <a class="page-link" href="#" t-on-click="() => this.store.goToPage(i)" ><t t-esc="i" /></a>
            </li>
            
            <li class="page-item">
              <a class="page-link" href="#" aria-label="Next" t-on-click="() => this.store.nextPage()">
                  <i class="fa fa-angle-double-right" />
              </a>
            </li>
        </ul>
    </nav>

    <div class="col-4">
        <div class="row gap1 oo_center_vertical oo_center_horizontal oo_what_composer_top_bar_order_by ">
            <div class="form-select mux">
                <label>Order By</label>
                <select name="order_by" id="order_by" placeholder="Sort by...">
                    <option value="name">Name</option>
                    <option value="works_quantity">Works quantity</option>
                    <option value="birth">Birth date</option>
                    <option value="death">Death date</option>
                </select>
            </div>

            <div class="mux form-check double-label">
                <span>Asc.</span>
                <input type="checkbox" class="form-check-input" id="order_direction" />
                <label class="form-check-label" for="order_direction" />
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





